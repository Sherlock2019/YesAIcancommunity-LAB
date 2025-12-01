import streamlit as st

st.set_page_config(
    page_title="Challenge Spec — OpenStack Deployment Readiness Validator",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Challenge Spec — OpenStack Deployment Readiness Validator")

st.markdown(
    """
## 1. Business Problem

Engineering teams roll new OpenStack releases into customer environments with limited automated validation.
Logs, config drifts, and dependency mismatches are manually inspected, delaying change windows.
Critical blockers are often discovered late, triggering rollbacks.

---

## 2. Desired Outcome

Deliver a **readiness validator** that ingests deployment artifacts (logs, configs, topology), runs rule/ML checks,
and produces a go/no-go dashboard with remediation actions.

---

## 3. Users & Personas

- **Primary:** Cloud Infra engineers preparing deployments.
- **Secondary:** Change managers and on-call SREs.
- **System:** Pre-change validation portal + CLI output.

---

## 4. Inputs & Data Sources

- Deployment logs, config bundles, inventory files.
- Known blocker catalog, historical incidents.
- Telemetry snapshots (capacity, alarms).

---

## 5. Outputs & UX Surfaces

- Readiness score per component.
- Remediation checklist grouped by severity.
- DAG visualization of dependencies with highlighted failures.

---

## 6. Constraints & Non-Goals

- Must run offline/air-gapped if needed; no external dependencies.
- Not intended to manage deployments, only validate readiness.
- False positives should be explainable with log snippets.

---

## 7. Implementation Hints

- Parse logs with regex + anomaly detection (e.g., Prophet/IsolationForest for metric trends).
- Encode rules as YAML for maintainability.
- Build Streamlit UI with expandable sections per subsystem.

---

## 8. Test / Acceptance Criteria

- Validator catches known blockers in historical incidents.
- Engineers can upload a bundle and receive score in <5 minutes.
- Exportable PDF/JSON report for change records.

> Codex: Treat this as the master spec for the readiness validator agent.
"""
)
