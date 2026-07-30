"""Tests for the CloudJumper Production Factory integration."""

import io
import json
import sys
import zipfile
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from integrations.cloudjumper import identity, package as pkg, passport, readiness  # noqa: E402


# ------------------------------------------------------------------ identity


def test_id_format_and_sequence():
    first = identity.next_global_ai_project_id([], year=2026)
    assert first == "AIPROJ-2026-000001"
    assert identity.is_valid(first)
    assert identity.next_global_ai_project_id([first], year=2026) == "AIPROJ-2026-000002"


def test_id_sequence_ignores_other_years_and_junk():
    existing = ["AIPROJ-2025-000900", "not-an-id", "", None, "AIPROJ-2026-000007"]
    assert identity.next_global_ai_project_id(existing, year=2026) == "AIPROJ-2026-000008"


def test_id_rejects_bad_shapes():
    for bad in ["AIPROJ-26-000001", "AIPROJ-2026-1", "PROJ-2026-000001", ""]:
        assert not identity.is_valid(bad)


def test_status_machine_is_forward_only():
    identity.validate_transition("DRAFT", "READY")
    identity.validate_transition("PACKAGED", "SUBMITTED")
    # A packaged candidate cannot silently return to DRAFT: its checksums would
    # no longer describe it.
    with pytest.raises(ValueError):
        identity.validate_transition("PACKAGED", "DRAFT")
    with pytest.raises(ValueError):
        identity.validate_transition("ACCEPTED", "SUBMITTED")
    with pytest.raises(ValueError):
        identity.validate_transition("ARCHIVED", "DRAFT")


def test_adoption_mode_matches_cloudjumper_enum():
    assert set(identity.ADOPTION_MODES) == {"GREENFIELD", "BROWNFIELD", "EXISTING_POC"}
    assert identity.validate_adoption_mode("greenfield") == "GREENFIELD"
    with pytest.raises(ValueError):
        identity.validate_adoption_mode("SIDEWAYS")


# ------------------------------------------------------------------ fixtures


@pytest.fixture
def complete():
    return {
        "global_ai_project_id": "AIPROJ-2026-000001",
        "title": "Credit Appraisal Agent",
        "adoption_mode": "BROWNFIELD",
        "source_type": "YES_AI_CAN",
        "business_owner": "cfo@acme.com",
        "technical_owner": "eng@acme.com",
        "data_owner": "dpo@acme.com",
        "production_owner": "ops@acme.com",
        "business_problem": "Manual appraisal takes 3 days.",
        "target_kpi": "4h median",
        "agent_version": "1.4.0",
        "source_repository": "https://github.com/acme/credit-agent",
        "model_name": "llama3.1",
        "model_version": "8b",
        "model_license": "Llama 3.1 Community",
        "health_endpoint": "/health",
        "data_sensitivity": "MEDIUM",
        "data_location": "eu-west",
        "pii_reviewed": True,
        "external_transfer_allowed": False,
        "human_approval_required": True,
        "rollback_behaviour": "Disable agent, manual queue resumes.",
    }


EV = {"EVALUATION_REPORT": True}


# ------------------------------------------------------------------ readiness


def test_complete_candidate_passes(complete):
    r = readiness.assess(complete, EV)
    assert r["verdict"] == "READY"
    assert r["can_generate_package"] is True
    assert r["failed"] == 0


@pytest.mark.parametrize("field", [
    "business_owner", "technical_owner", "data_owner", "production_owner",
    "model_license", "model_version", "health_endpoint", "data_sensitivity", "target_kpi",
])
def test_each_required_field_blocks(complete, field):
    broken = dict(complete)
    broken.pop(field)
    r = readiness.assess(broken, EV)
    assert r["verdict"] == "BLOCKED", field
    assert r["can_generate_package"] is False, field
    assert r["blockers"], field


def test_missing_evaluation_blocks(complete):
    r = readiness.assess(complete, {})
    assert r["verdict"] == "BLOCKED"
    assert any("valuation" in b["title"] for b in r["blockers"])


def test_unreviewed_pii_is_not_checked_not_pass(complete):
    """"Nobody looked" must not read like "we checked and found none"."""
    c = dict(complete)
    c["data_sensitivity"] = "LOW"
    c.pop("pii_reviewed")
    r = readiness.assess(c, EV)
    pii = [x for cat in r["categories"].values() for x in cat["controls"] if x["control_key"] == "pii_reviewed"][0]
    assert pii["status"] == "NOT_CHECKED"


def test_regulated_data_raises_the_bar(complete):
    c = dict(complete)
    c["data_sensitivity"] = "REGULATED"
    c.pop("pii_reviewed")
    r = readiness.assess(c, EV)
    # Unreviewed PII is merely unchecked at LOW, but blocking at REGULATED.
    assert r["verdict"] == "BLOCKED"
    assert any(b["control_key"] == "pii_reviewed" for b in r["blockers"])


def test_not_checked_never_counts_as_pass(complete):
    c = dict(complete)
    for optional in ("baseline_kpi", "estimated_value", "target_environment"):
        c.pop(optional, None)
    r = readiness.assess(c, EV)
    assert r["not_checked"] > 0
    assert r["confidence"] < 100
    assert "NOT_CHECKED is excluded" in r["formula"]


# ------------------------------------------------------------------ passport


def test_passport_never_invents_values():
    sparse = {"global_ai_project_id": "AIPROJ-2026-000002", "title": "X",
              "adoption_mode": "GREENFIELD", "model_license": "   "}
    p = passport.build(sparse)
    assert p["model"]["license"] is None          # whitespace is not a licence
    assert p["owners"]["business"] is None
    assert p["permissions"]["prohibited_actions"] == []
    assert "model.license" in passport.missing_fields(p)


def test_passport_checksum_is_reproducible(complete):
    """Same agent facts -> same digest, so it can serve as an idempotency key.

    Regression: the checksum used to include generated_at, so packaging the
    same agent twice produced two different digests.
    """
    import time

    a = passport.build(complete)
    time.sleep(0.01)
    b = passport.build(dict(reversed(list(complete.items()))))
    assert a["generated_at"] != b["generated_at"]     # genuinely different builds
    assert passport.checksum(a) == passport.checksum(b)


def test_passport_checksum_changes_when_the_agent_changes(complete):
    a = passport.build(complete)
    b = passport.build(dict(complete, model_version="9b"))
    assert passport.checksum(a) != passport.checksum(b)


# ------------------------------------------------------------------ package


def test_manifest_has_every_section_cloudjumper_requires(complete):
    m = pkg.build_manifest(complete)
    for section in ("schema_version", "project", "agent", "model", "data", "deployment"):
        assert section in m, section
    assert m["schema_version"] == "1.0"
    assert m["project"]["owner"] == complete["business_owner"]
    assert m["agent"]["health_endpoint"] == "/health"
    assert m["model"]["license"]
    assert m["data"]["sensitivity"] == "MEDIUM"


def test_missing_assets_become_gaps_not_placeholders(complete):
    built = pkg.build_package(complete)
    titles = [g["title"] for g in built["gaps"]]
    assert any("Dockerfile" in t for t in titles)
    assert any("Kubernetes" in t or "Helm" in t for t in titles)
    with zipfile.ZipFile(io.BytesIO(built["bytes"])) as zf:
        names = zf.namelist()
    # The gap is recorded; no stub Dockerfile is invented.
    assert not any(n.endswith("Dockerfile") for n in names)
    assert m_in(names, "production-gaps.json")


def m_in(names, suffix):
    return any(n.endswith(suffix) for n in names)


def test_package_layout_matches_cloudjumper_importer(complete):
    built = pkg.build_package(complete, {"score": 0.9})
    with zipfile.ZipFile(io.BytesIO(built["bytes"])) as zf:
        names = zf.namelist()
        # Single root dir, which CloudJumper descends into.
        assert all(n.startswith("production-handoff/") for n in names)
        assert m_in(names, "cloudjumper-handoff.yaml")
        assert m_in(names, "agent-passport.json")
        assert m_in(names, "checksums.sha256")
        manifest = yaml.safe_load(zf.read("production-handoff/cloudjumper-handoff.yaml"))
    assert manifest["schema_version"] == "1.0"


def test_only_one_manifest_is_written(complete):
    """Two manifests describing one project would drift; there is exactly one."""
    built = pkg.build_package(complete)
    with zipfile.ZipFile(io.BytesIO(built["bytes"])) as zf:
        manifests = [n for n in zf.namelist() if n.endswith(("manifest.yaml", "cloudjumper-handoff.yaml"))]
    assert manifests == ["production-handoff/cloudjumper-handoff.yaml"]


def test_checksums_cover_every_file(complete):
    built = pkg.build_package(complete)
    with zipfile.ZipFile(io.BytesIO(built["bytes"])) as zf:
        listed = {n.split("/", 1)[1] for n in zf.namelist()} - {"checksums.sha256"}
        lines = zf.read("production-handoff/checksums.sha256").decode().strip().splitlines()
    recorded = {ln.split("  ", 1)[1] for ln in lines}
    assert recorded == listed


def test_package_checksum_changes_with_content(complete):
    a = pkg.build_package(complete)
    other = dict(complete, title="Different Agent")
    assert a["checksum"] != pkg.build_package(other)["checksum"]


@pytest.mark.parametrize("payload", [
    "AKIA" + "B" * 16,
    "ghp_" + "c" * 30,
    "api_key = 'sk-" + "d" * 30 + "'",
    "-----BEGIN RSA PRIVATE KEY-----",
])
def test_secrets_block_package_generation(complete, payload):
    with pytest.raises(pkg.PackageError):
        pkg.build_package(complete, extra_files={"notes.txt": payload})


@pytest.mark.parametrize("name,expected", [
    ("../../etc/passwd", "passwd"),
    ("/abs/path/x.txt", "x.txt"),
    ("..\\..\\win.ini", "win.ini"),
    (".hidden", "hidden"),
    ("", "file"),
])
def test_filenames_are_sanitized(name, expected):
    assert pkg.sanitize_filename(name) == expected


def test_extra_file_cannot_escape_the_bundle(complete):
    built = pkg.build_package(complete, extra_files={"../../evil.txt": "harmless"})
    with zipfile.ZipFile(io.BytesIO(built["bytes"])) as zf:
        names = zf.namelist()
    assert all(n.startswith("production-handoff/") for n in names)
    assert not any(".." in n for n in names)
