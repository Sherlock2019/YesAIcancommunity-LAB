"""Production Factory API.

Six endpoints, not the specification's nineteen: the thirteen removed ones
proxy CloudJumper operations that require live API access, which this phase does
not have. They belong with Part 4.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session

from integrations.cloudjumper import client as cj_client
from integrations.cloudjumper import identity, package as package_mod, readiness as readiness_mod
from integrations.cloudjumper import is_enabled
from integrations.cloudjumper.models import ProductionCandidate, ProductionEvidence
from services.api.database import get_db

router = APIRouter(prefix="/api/v1/production-factory", tags=["production-factory"])

PACKAGE_DIR = Path(__file__).resolve().parents[1] / "production_packages"


def _guard() -> None:
    if not is_enabled():
        raise HTTPException(status_code=503, detail="Production Factory is disabled")


class CandidateIn(BaseModel):
    # model_name / model_version / model_license are CloudJumper's field names,
    # so they stay. Pydantic reserves the "model_" prefix, hence the opt-out.
    model_config = {"protected_namespaces": ()}

    title: str = Field(min_length=1, max_length=200)
    adoption_mode: str
    description: Optional[str] = None
    source_type: str = "YES_AI_CAN"
    challenge_id: Optional[int] = None
    solution_id: Optional[int] = None
    agent_id: Optional[str] = None
    agent_version: Optional[str] = None
    customer_id: Optional[str] = None
    business_system_id: Optional[str] = None
    business_owner: Optional[str] = None
    technical_owner: Optional[str] = None
    data_owner: Optional[str] = None
    production_owner: Optional[str] = None
    business_problem: Optional[str] = None
    baseline_kpi: Optional[str] = None
    target_kpi: Optional[str] = None
    estimated_value: Optional[float] = None
    data_sensitivity: Optional[str] = None
    data_location: Optional[str] = None
    pii_present: bool = False
    external_transfer_allowed: bool = False
    human_approval_required: bool = False
    model_runtime: Optional[str] = None
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    model_license: Optional[str] = None
    gpu_required: bool = False
    minimum_ram_gb: int = 0
    minimum_vram_gb: int = 0
    health_endpoint: Optional[str] = None
    readiness_endpoint: Optional[str] = None
    source_repository: Optional[str] = None
    source_commit: Optional[str] = None
    target_environment: Optional[str] = None
    palantir_required: bool = False
    is_demo: bool = False

    @field_validator("adoption_mode")
    @classmethod
    def _mode(cls, v: str) -> str:
        try:
            return identity.validate_adoption_mode(v)
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

    @field_validator("data_sensitivity")
    @classmethod
    def _sens(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        try:
            return identity.validate_sensitivity(v) or None
        except ValueError as exc:
            raise ValueError(str(exc)) from exc

    @field_validator("source_type")
    @classmethod
    def _src(cls, v: str) -> str:
        s = str(v or "").strip().upper()
        if s not in identity.SOURCE_TYPES:
            raise ValueError(f"source_type must be one of {list(identity.SOURCE_TYPES)}")
        return s


class CandidatePatch(BaseModel):
    model_config = {"extra": "forbid", "protected_namespaces": ()}

    title: Optional[str] = None
    description: Optional[str] = None
    business_owner: Optional[str] = None
    technical_owner: Optional[str] = None
    data_owner: Optional[str] = None
    production_owner: Optional[str] = None
    business_problem: Optional[str] = None
    baseline_kpi: Optional[str] = None
    target_kpi: Optional[str] = None
    estimated_value: Optional[float] = None
    data_sensitivity: Optional[str] = None
    data_location: Optional[str] = None
    pii_present: Optional[bool] = None
    external_transfer_allowed: Optional[bool] = None
    human_approval_required: Optional[bool] = None
    model_runtime: Optional[str] = None
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    model_license: Optional[str] = None
    gpu_required: Optional[bool] = None
    minimum_ram_gb: Optional[int] = None
    minimum_vram_gb: Optional[int] = None
    health_endpoint: Optional[str] = None
    readiness_endpoint: Optional[str] = None
    source_repository: Optional[str] = None
    source_commit: Optional[str] = None
    target_environment: Optional[str] = None
    palantir_required: Optional[bool] = None
    agent_version: Optional[str] = None
    status: Optional[str] = None


def _as_dict(c: ProductionCandidate) -> Dict[str, Any]:
    return {
        col.name: getattr(c, col.name)
        for col in ProductionCandidate.__table__.columns
    }


def _evidence_map(db: Session, candidate_id: int) -> Dict[str, bool]:
    rows = db.execute(
        select(ProductionEvidence.evidence_type).where(ProductionEvidence.candidate_id == candidate_id)
    ).scalars().all()
    return {t: True for t in rows}


@router.get("/candidates")
def list_candidates(db: Session = Depends(get_db)) -> Dict[str, Any]:
    _guard()
    rows = db.execute(select(ProductionCandidate).order_by(ProductionCandidate.id.desc())).scalars().all()
    return {"ok": True, "candidates": [_as_dict(r) for r in rows]}


@router.post("/candidates", status_code=201)
def create_candidate(payload: CandidateIn, db: Session = Depends(get_db)) -> Dict[str, Any]:
    _guard()
    # Read existing ids and insert in the same transaction so two concurrent
    # creates cannot mint the same number; the unique index is the backstop.
    existing = db.execute(select(ProductionCandidate.global_ai_project_id)).scalars().all()
    gid = identity.next_global_ai_project_id(list(existing))

    data = payload.model_dump()
    candidate = ProductionCandidate(global_ai_project_id=gid, status="DRAFT", **data)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return {"ok": True, "candidate": _as_dict(candidate)}


@router.get("/candidates/{candidate_id}")
def get_candidate(candidate_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    _guard()
    c = db.get(ProductionCandidate, candidate_id)
    if not c:
        raise HTTPException(status_code=404, detail="candidate not found")
    return {"ok": True, "candidate": _as_dict(c), "evidence": list(_evidence_map(db, c.id))}


@router.patch("/candidates/{candidate_id}")
def patch_candidate(candidate_id: int, payload: CandidatePatch, db: Session = Depends(get_db)) -> Dict[str, Any]:
    _guard()
    c = db.get(ProductionCandidate, candidate_id)
    if not c:
        raise HTTPException(status_code=404, detail="candidate not found")

    updates = payload.model_dump(exclude_unset=True)
    if "status" in updates and updates["status"] is not None:
        try:
            identity.validate_transition(c.status, updates["status"])
        except ValueError as exc:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
    if updates.get("data_sensitivity"):
        try:
            updates["data_sensitivity"] = identity.validate_sensitivity(updates["data_sensitivity"])
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc)) from exc

    for key, value in updates.items():
        if value is not None:
            setattr(c, key, value)
    db.commit()
    db.refresh(c)
    return {"ok": True, "candidate": _as_dict(c)}


@router.get("/candidates/{candidate_id}/readiness")
def get_readiness(candidate_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    _guard()
    c = db.get(ProductionCandidate, candidate_id)
    if not c:
        raise HTTPException(status_code=404, detail="candidate not found")

    result = readiness_mod.assess(_as_dict(c), _evidence_map(db, c.id))
    c.readiness_score = result["score"]
    c.readiness_verdict = result["verdict"]
    # Only the gate may move DRAFT to READY; a client cannot assert readiness.
    if result["can_generate_package"] and c.status == "DRAFT":
        c.status = "READY"
    db.commit()
    return {"ok": True, "readiness": result}


@router.post("/candidates/{candidate_id}/handoff")
def generate_handoff(candidate_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    _guard()
    c = db.get(ProductionCandidate, candidate_id)
    if not c:
        raise HTTPException(status_code=404, detail="candidate not found")

    evidence = _evidence_map(db, c.id)
    result = readiness_mod.assess(_as_dict(c), evidence)
    if not result["can_generate_package"]:
        # Refuse rather than emit a bundle that CloudJumper will reject.
        raise HTTPException(
            status_code=422,
            detail={
                "error": "readiness gate not passed",
                "verdict": result["verdict"],
                "blockers": result["blockers"],
            },
        )

    payload = _as_dict(c)
    payload["_has_evaluation"] = bool(evidence.get("EVALUATION_REPORT"))
    payload["_has_openapi"] = bool(evidence.get("OPENAPI"))
    payload["_has_sbom"] = bool(evidence.get("SBOM"))

    try:
        built = package_mod.build_package(payload)
    except package_mod.PackageError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    path = package_mod.write_package(built, PACKAGE_DIR)
    c.package_path = str(path)
    c.package_checksum = built["checksum"]
    if c.status in ("DRAFT", "READY"):
        c.status = "PACKAGED"

    db.add(
        ProductionEvidence(
            candidate_id=c.id,
            global_ai_project_id=c.global_ai_project_id,
            evidence_type="CLOUDJUMPER_HANDOFF",
            version=c.agent_version,
            checksum=built["checksum"],
            storage_reference=str(path),
            metadata_json=json.dumps({"files": built["files"], "size": built["size"]}),
        )
    )
    db.commit()

    return {
        "ok": True,
        "checksum": built["checksum"],
        "size": built["size"],
        "filename": built["filename"],
        "files": built["files"],
        "gaps": built["gaps"],
        "manifest": built["manifest"],
        "download_url": f"/api/v1/production-factory/candidates/{c.id}/handoff",
        "next_step": "Import this bundle in CloudJumper Stage 9 using the Upload source.",
    }


@router.get("/cloudjumper/health")
def cloudjumper_health() -> Dict[str, Any]:
    """Is CloudJumper reachable, and is our service key accepted?"""
    _guard()
    return {"ok": True, "config": cj_client.config_summary(), "health": cj_client.health_check()}


@router.post("/candidates/{candidate_id}/submit")
def submit_to_cloudjumper(candidate_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Send the handoff bundle to CloudJumper for deployment assessment.

    Requires a generated package: submitting means "deploy this exact artifact",
    and the checksum recorded here is what makes a retry idempotent rather than
    a second project.
    """
    _guard()
    c = db.get(ProductionCandidate, candidate_id)
    if not c:
        raise HTTPException(status_code=404, detail="candidate not found")
    if not c.package_path or not Path(c.package_path).is_file():
        raise HTTPException(status_code=409, detail="generate the handoff package first")
    if not cj_client.is_configured():
        raise HTTPException(
            status_code=503,
            detail={
                "error": "CloudJumper is not configured",
                "needed": ["CLOUDJUMPER_API_BASE_URL", "the variable named by CLOUDJUMPER_API_KEY_REFERENCE"],
                "config": cj_client.config_summary(),
            },
        )

    try:
        result = cj_client.submit_bundle(
            c.package_path,
            name=c.title,
            adoption_mode=c.adoption_mode,
            global_ai_project_id=c.global_ai_project_id,
            business_owner=c.business_owner or "",
            technical_owner=c.technical_owner or "",
            data_owner=c.data_owner or "",
            production_owner=c.production_owner or "",
            business_goal=c.business_problem or "",
            data_sensitivity=c.data_sensitivity or "",
            palantir_required=bool(c.palantir_required),
            customer_id=c.customer_id or "",
        )
    except cj_client.CloudJumperError as exc:
        # Say plainly what failed, whether anything was saved, and if retry is safe.
        raise HTTPException(
            status_code=502,
            detail={
                "error": str(exc),
                "saved": False,
                "retry_safe": exc.retry_safe,
                "correlation_id": exc.correlation_id,
                "next_action": "Retry" if exc.retry_safe else "Fix the configuration or bundle, then resubmit",
            },
        ) from exc

    # CloudJumper is the source of truth for what happens next; we record only
    # that it accepted the bundle.
    identity.validate_transition(c.status, "SUBMITTED")
    c.status = "SUBMITTED"
    c.submitted_at = datetime.utcnow()
    db.add(
        ProductionEvidence(
            candidate_id=c.id,
            global_ai_project_id=c.global_ai_project_id,
            evidence_type="DEPLOYMENT_PACKAGE",
            source_system="CLOUDJUMPER",
            checksum=c.package_checksum,
            storage_reference=result.get("cloudjumper_url"),
            metadata_json=json.dumps({
                "cloudjumper_project_id": result.get("project_id"),
                "readiness_score": result.get("readiness_score"),
                "verdict": result.get("verdict"),
                "duplicate": result.get("duplicate"),
            }),
        )
    )
    db.commit()
    return {"ok": True, "submitted": True, "cloudjumper": result}


@router.get("/candidates/{candidate_id}/handoff")
def download_handoff(candidate_id: int, db: Session = Depends(get_db)) -> Response:
    _guard()
    c = db.get(ProductionCandidate, candidate_id)
    if not c:
        raise HTTPException(status_code=404, detail="candidate not found")
    if not c.package_path or not Path(c.package_path).is_file():
        raise HTTPException(status_code=404, detail="no package generated yet")

    blob = Path(c.package_path).read_bytes()
    name = package_mod.sanitize_filename(Path(c.package_path).name)
    return Response(
        content=blob,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{name}"'},
    )
