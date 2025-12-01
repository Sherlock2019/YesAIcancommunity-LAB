import streamlit as st

st.set_page_config(
    page_title="Challenge Spec — Predict Ticket Escalations for Managed Cloud",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Challenge Spec — Predict Ticket Escalations for Managed Cloud")

st.markdown(
    """
## 1. Business Problem

Managed Cloud support teams battle noisy queues where tickets unexpectedly escalate to L3.
Signals are buried in chat logs, sentiment shifts, and historical resolution paths.
Without predictive tooling, managers react late, causing SLA misses and customer frustration.

---

## 2. Desired Outcome

Create a **sentiment + workflow trajectory model** that forecasts which tickets are likely to escalate.
Surface early warnings, recommended playbooks, and staffing signals so leads can intervene proactively.

---

## 3. Users & Personas

- **Primary:** Support leads / queue managers.
- **Secondary:** L2/L3 engineers, Customer Success for critical accounts.
- **System:** Live dashboard embedded in support runbooks + API for routing automation.

---

## 4. Inputs & Data Sources

- Historical ticket data with escalation labels.
- Chat transcripts / email threads (structured + unstructured text).
- Metadata: product, severity, customer health scores, agent notes.

---

## 5. Outputs & UX Surfaces

- Ranked list of active tickets with escalation probability.
- Explainability snippets: sentiment trend, similar past incidents, drivers.
- API/webhook to trigger automation or notify on-call leads.

---

## 6. Constraints & Non-Goals

- Model transparency required; avoid black-box predictions.
- Respect customer privacy; redact sensitive text when storing features.
- Not a full ticketing system—augment existing ServiceNow/Jira workflows.

---

## 7. Implementation Hints

- Combine LLM-based sentiment trajectory with gradient-boosted classifier on structured features.
- Use feature store for rolling aggregates (response time, reopen count).
- Deploy as Streamlit monitor + REST endpoint.

---

## 8. Test / Acceptance Criteria

- Precision/recall targets agreed with Support (e.g., >70% recall on escalations).
- Pilot reduces surprise escalations by measurable percentage.
- Users can provide feedback to retrain or adjust thresholds.

> Codex: Use this spec to drive backlog for the escalation predictor agent.
"""
)
