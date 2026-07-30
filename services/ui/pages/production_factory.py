"""🚀 Production Factory — Powered by CloudJumper.

Move validated agents, AI PoCs and application enhancements into governed FLEX,
OpenCenter and Palantir production.

This page is a summarised orchestration view. It deliberately does not show
UAT, canary or production status: CloudJumper does not observe deployment, so
those tiles would display data that nothing sets.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from integrations.cloudjumper import identity, is_enabled, package as pkg, readiness  # noqa: E402

st.set_page_config(page_title="Production Factory", page_icon="🚀", layout="wide")

if not is_enabled():
    st.warning("Production Factory is disabled (CLOUDJUMPER_PRODUCTION_FACTORY_ENABLED=0).")
    st.stop()

st.title("🚀 Production Factory — Powered by CloudJumper")
st.caption(
    "Move validated agents, AI PoCs, and application enhancements into governed "
    "FLEX, OpenCenter, and Palantir production."
)

st.info(
    "**YES AI CAN** finds the problem, builds the agent, validates the value and prepares the "
    "evidence. **CloudJumper** designs, deploys, validates and transitions the solution into "
    "governed production.",
    icon="🧭",
)

# ---------------------------------------------------------------- demo records
# Clearly labelled. Real candidates come from the Production Factory API.
DEMOS = [
    {
        "global_ai_project_id": "AIPROJ-2026-000101",
        "title": "Internal Knowledge Assistant",
        "adoption_mode": "GREENFIELD",
        "source_type": "YES_AI_CAN",
        "business_owner": "coo@acme.com", "technical_owner": "eng@acme.com",
        "data_owner": "dpo@acme.com", "production_owner": "ops@acme.com",
        "business_problem": "Staff cannot find internal documentation.",
        "target_kpi": "50% fewer support tickets", "agent_version": "0.9.0",
        "source_repository": "https://github.com/acme/kb-assistant",
        "model_name": "llama3.1", "model_version": "8b", "model_license": "Llama 3.1 Community",
        "health_endpoint": "/health", "data_sensitivity": "MEDIUM", "data_location": "eu-west",
        "pii_reviewed": True, "external_transfer_allowed": False, "human_approval_required": False,
        "rollback_behaviour": "Disable the assistant; search falls back to the wiki.",
        "target_environment": "FLEX + OpenCenter",
    },
    {
        "global_ai_project_id": "AIPROJ-2026-000102",
        "title": "Credit Appraisal Accelerator",
        "adoption_mode": "GREENFIELD", "source_type": "LAUNCHPAD",
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
        "global_ai_project_id": "AIPROJ-2026-000103",
        "title": "Claims Assistant PoC",
        "adoption_mode": "EXISTING_POC", "source_type": "GITHUB",
        "business_owner": "claims@acme.com", "technical_owner": "eng@acme.com",
        "business_problem": "Claims triage is manual.",
        "agent_version": "0.2.0", "source_repository": "https://github.com/acme/claims-poc",
        "model_name": "mistral", "health_endpoint": "/health",
        "data_sensitivity": "HIGH",
        # Deliberately incomplete: shows the gate refusing a handoff.
    },
]

EV = {"EVALUATION_REPORT": True}
assessed = [(d, readiness.assess(d, EV if d["global_ai_project_id"] != "AIPROJ-2026-000103" else {})) for d in DEMOS]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Production candidates", len(assessed))
c2.metric("Ready for CloudJumper", sum(1 for _, r in assessed if r["can_generate_package"]))
c3.metric("Blocked", sum(1 for _, r in assessed if r["verdict"] == "BLOCKED"))
c4.metric("Palantir required", sum(1 for d, _ in assessed if d.get("palantir_required")))

st.warning("The rows below are **DEMO** records, not live customer projects.", icon="⚠️")

mode_filter = st.multiselect("Adoption mode", list(identity.ADOPTION_MODES), default=list(identity.ADOPTION_MODES))

st.subheader("Production candidates")
for cand, result in assessed:
    if cand["adoption_mode"] not in mode_filter:
        continue
    verdict = result["verdict"]
    icon = {"READY": "✅", "READY_WITH_CHANGES": "🟡", "BLOCKED": "⛔", "MANUAL_REVIEW": "🔍"}.get(verdict, "•")

    with st.expander(f"{icon} **DEMO** · {cand['title']} · `{cand['global_ai_project_id']}` · {verdict}"):
        a, b = st.columns([2, 1])
        with a:
            st.write(f"**Adoption mode:** {cand['adoption_mode']} — **Source:** {cand['source_type']}")
            st.write(f"**Business problem:** {cand.get('business_problem') or '—'}")
            st.write(f"**Data:** {cand.get('data_sensitivity') or 'unclassified'} · {cand.get('data_location') or 'location unknown'}")
            st.write(f"**Target:** {cand.get('target_environment') or '—'}")
        with b:
            st.metric("Readiness", f"{result['score']}%")
            st.caption(
                f"{result['passed']} passed · {result['failed']} failed · "
                f"{result['not_checked']} not checked · confidence {result['confidence']}%"
            )

        if result["blockers"]:
            st.error("**Blocked — resolve before handoff**")
            for blocker in result["blockers"]:
                st.write(f"- **{blocker['title']}** → {blocker['remediation']}")

        # The formula is shown, never hidden.
        st.caption(f"How this is scored: {result['formula']}")

        if result["can_generate_package"]:
            if st.button("Generate Production Handoff", key=f"gen-{cand['global_ai_project_id']}"):
                try:
                    built = pkg.build_package(cand, {"score": 0.9, "summary": "Demo evaluation."})
                    st.success(f"Bundle built — {built['size']} bytes, checksum `{built['checksum'][:16]}…`")
                    st.write("**Files:** " + ", ".join(built["files"]))
                    if built["gaps"]:
                        st.warning("**Recorded gaps** (not stubbed):")
                        for g in built["gaps"]:
                            st.write(f"- **{g['severity']}** {g['title']} → {g['remediation']}")
                    st.download_button(
                        "⬇ Download handoff bundle",
                        data=built["bytes"],
                        file_name=built["filename"],
                        mime="application/zip",
                        key=f"dl-{cand['global_ai_project_id']}",
                    )
                    st.info("Import this bundle in CloudJumper Stage 9 using the **Upload** source.", icon="📦")
                except pkg.PackageError as exc:
                    st.error(f"Package refused: {exc}")
        else:
            st.button("Generate Production Handoff", key=f"gen-{cand['global_ai_project_id']}", disabled=True)
            st.caption("The readiness gate blocks handoff generation until the blockers above are resolved.")

st.divider()
st.caption(
    "Live CloudJumper status sync and webhooks are not enabled: CloudJumper currently has no "
    "service-to-service credential and emits no events. Handoff is by bundle — see "
    "docs/cloudjumper-integration-implementation-plan.md."
)
