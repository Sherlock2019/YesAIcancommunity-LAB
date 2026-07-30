"""🚀 Deployment in Production — YES AI CAN.

Sends a validated agent to CloudJumper for governed FLEX / OpenCenter /
Palantir production. The stage itself lives in integrations.cloudjumper.
deploy_stage so AI 4 the People renders exactly the same screen.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from integrations.cloudjumper import deploy_stage, is_enabled  # noqa: E402

st.set_page_config(page_title="Deployment in Production", page_icon="🚀", layout="wide")

if not is_enabled():
    st.warning("Disabled (CLOUDJUMPER_PRODUCTION_FACTORY_ENABLED=0).")
    st.stop()

CANDIDATES = [
    {
        "global_ai_project_id": "AIPROJ-2026-000101",
        "title": "Internal Knowledge Assistant",
        "adoption_mode": "GREENFIELD", "source_type": "YES_AI_CAN",
        "business_owner": "coo@acme.com", "technical_owner": "eng@acme.com",
        "data_owner": "dpo@acme.com", "production_owner": "ops@acme.com",
        "business_problem": "Staff cannot find internal documentation.",
        "target_kpi": "50% fewer support tickets", "agent_version": "0.9.0",
        "source_repository": "https://github.com/acme/kb-assistant",
        "model_name": "llama3.1", "model_version": "8b", "model_license": "Llama 3.1 Community",
        "health_endpoint": "/health", "data_sensitivity": "MEDIUM", "data_location": "eu-west",
        "pii_reviewed": True, "external_transfer_allowed": False, "human_approval_required": False,
        "rollback_behaviour": "Disable the assistant; wiki search resumes.",
        "target_environment": "FLEX + OpenCenter",
    },
    {
        "global_ai_project_id": "AIPROJ-2026-000102",
        "title": "Credit Appraisal Accelerator",
        "adoption_mode": "BROWNFIELD", "source_type": "LAUNCHPAD",
        "business_owner": "cfo@acme.com", "technical_owner": "eng@acme.com",
        "data_owner": "dpo@acme.com", "production_owner": "ops@acme.com",
        "business_problem": "Manual credit appraisal takes three days.",
        "target_kpi": "4h median decision", "agent_version": "1.4.0",
        "source_repository": "https://github.com/acme/credit-agent",
        "model_name": "llama3.1", "model_version": "8b", "model_license": "Llama 3.1 Community",
        "health_endpoint": "/health", "data_sensitivity": "REGULATED", "data_location": "eu-west",
        "pii_reviewed": True, "external_transfer_allowed": False, "human_approval_required": True,
        "rollback_behaviour": "Disable the agent; the manual queue resumes.",
        "target_environment": "FLEX + OpenCenter + Palantir", "palantir_required": True,
    },
    {
        # Deliberately incomplete: shows the gate refusing a deployment.
        "global_ai_project_id": "AIPROJ-2026-000103",
        "title": "Claims Assistant PoC",
        "adoption_mode": "EXISTING_POC", "source_type": "GITHUB",
        "business_owner": "claims@acme.com", "technical_owner": "eng@acme.com",
        "business_problem": "Claims triage is manual.", "agent_version": "0.2.0",
        "source_repository": "https://github.com/acme/claims-poc",
        "model_name": "mistral", "health_endpoint": "/health", "data_sensitivity": "HIGH",
    },
]


def evidence_for(candidate):
    # The incomplete PoC has no evaluation report, which is itself a blocker.
    return {} if candidate["global_ai_project_id"].endswith("103") else {"EVALUATION_REPORT": True}


deploy_stage.render(st, CANDIDATES, platform="YES AI CAN", evidence_for=evidence_for)
