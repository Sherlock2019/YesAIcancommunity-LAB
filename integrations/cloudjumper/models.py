"""Production Factory tables.

Two tables, not the specification's six. `CloudJumperLink`, `ReadinessItem`,
`CloudJumperEvent` and `ProductionMetric` all serve live API sync and webhooks,
which cannot work until CloudJumper grows service-to-service auth and an event
emitter; adding empty tables now would just be schema nobody writes to.

Style follows services/api/models.py (SQLAlchemy 2.0 Mapped/mapped_column), and
the tables are created by the existing init_db() -> Base.metadata.create_all().
No existing table or column is touched.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from services.api.database import Base


class ProductionCandidate(Base):
    """A project promoted toward governed production."""

    __tablename__ = "production_candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # The identity that follows the project into CloudJumper, FLEX and Palantir.
    # Unique index is what actually guarantees no collision under concurrency.
    global_ai_project_id: Mapped[str] = mapped_column(String(32), unique=True, index=True, nullable=False)

    challenge_id: Mapped[int | None] = mapped_column(ForeignKey("challenges.id"), nullable=True)
    solution_id: Mapped[int | None] = mapped_column(ForeignKey("solutions.id"), nullable=True)

    agent_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    agent_version: Mapped[str | None] = mapped_column(String(60), nullable=True)

    adoption_mode: Mapped[str] = mapped_column(String(20), nullable=False)
    source_type: Mapped[str] = mapped_column(String(40), nullable=False, default="YES_AI_CAN")

    customer_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    business_system_id: Mapped[str | None] = mapped_column(String(120), nullable=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    business_owner: Mapped[str | None] = mapped_column(String(200), nullable=True)
    technical_owner: Mapped[str | None] = mapped_column(String(200), nullable=True)
    data_owner: Mapped[str | None] = mapped_column(String(200), nullable=True)
    production_owner: Mapped[str | None] = mapped_column(String(200), nullable=True)

    business_problem: Mapped[str | None] = mapped_column(Text, nullable=True)
    baseline_kpi: Mapped[str | None] = mapped_column(String(200), nullable=True)
    target_kpi: Mapped[str | None] = mapped_column(String(200), nullable=True)
    estimated_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(8), default="USD")

    data_sensitivity: Mapped[str | None] = mapped_column(String(20), nullable=True)
    data_location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    pii_present: Mapped[bool] = mapped_column(Boolean, default=False)
    external_transfer_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    human_approval_required: Mapped[bool] = mapped_column(Boolean, default=False)

    # Model facts. CloudJumper warns when the licence is absent, so it is a
    # first-class column rather than something buried in a JSON blob.
    model_runtime: Mapped[str | None] = mapped_column(String(120), nullable=True)
    model_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(60), nullable=True)
    model_license: Mapped[str | None] = mapped_column(String(120), nullable=True)
    gpu_required: Mapped[bool] = mapped_column(Boolean, default=False)
    minimum_ram_gb: Mapped[int] = mapped_column(Integer, default=0)
    minimum_vram_gb: Mapped[int] = mapped_column(Integer, default=0)

    health_endpoint: Mapped[str | None] = mapped_column(String(200), nullable=True)
    readiness_endpoint: Mapped[str | None] = mapped_column(String(200), nullable=True)
    source_repository: Mapped[str | None] = mapped_column(String(400), nullable=True)
    source_commit: Mapped[str | None] = mapped_column(String(80), nullable=True)

    target_environment: Mapped[str | None] = mapped_column(String(120), nullable=True)
    palantir_required: Mapped[bool] = mapped_column(Boolean, default=False)

    readiness_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    readiness_verdict: Mapped[str | None] = mapped_column(String(30), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="DRAFT", nullable=False)

    # Where the generated bundle landed, and what it hashed to. The checksum is
    # the idempotency key for a later CloudJumper submission.
    package_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    package_checksum: Mapped[str | None] = mapped_column(String(80), nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Demo rows must be visibly demo, everywhere they appear.
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    evidence: Mapped[list["ProductionEvidence"]] = relationship(
        "ProductionEvidence",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )


class ProductionEvidence(Base):
    """A generated artifact backing a production claim."""

    __tablename__ = "production_evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    candidate_id: Mapped[int] = mapped_column(ForeignKey("production_candidates.id"), nullable=False)
    global_ai_project_id: Mapped[str] = mapped_column(String(32), index=True, nullable=False)

    evidence_type: Mapped[str] = mapped_column(String(60), nullable=False)
    source_system: Mapped[str] = mapped_column(String(60), default="YES_AI_CAN")
    version: Mapped[str | None] = mapped_column(String(60), nullable=True)
    checksum: Mapped[str | None] = mapped_column(String(80), nullable=True)
    storage_reference: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="PRESENT")
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)

    candidate: Mapped[ProductionCandidate] = relationship("ProductionCandidate", back_populates="evidence")


EVIDENCE_TYPES = (
    "BUSINESS_CASE",
    "AGENT_PASSPORT",
    "DATA_CLASSIFICATION",
    "EVALUATION_REPORT",
    "CLOUDJUMPER_HANDOFF",
    "OPENAPI",
    "SBOM",
    "DEPLOYMENT_PACKAGE",
)
