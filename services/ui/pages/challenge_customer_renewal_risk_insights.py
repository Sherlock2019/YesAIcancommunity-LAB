import streamlit as st

st.set_page_config(
    page_title="Challenge Spec — Customer Renewal Risk Insights",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Challenge Spec — Customer Renewal Risk Insights")

st.markdown(
    """
## 1. Business Problem

Sales Ops teams lack a unified signal on renewal risk.
Notes live in CRM free text, QBR decks, and call summaries, making it hard to prioritize save motions.
Renewal surprises lead to revenue leakage.

---

## 2. Desired Outcome

Provide an **AI-powered renewal risk console** that ingests CRM data, call transcripts, usage metrics,
and surfaces churn scores, sentiment drivers, and recommended actions per account.

---

## 3. Users & Personas

- **Primary:** Sales strategists / Customer Success managers.
- **Secondary:** Renewal desk, leadership dashboards.
- **System:** Weekly planning workspace with alerts for high-risk accounts.

---

## 4. Inputs & Data Sources

- CRM opportunities + renewal dates.
- Call summaries, Gong/Zoom transcripts, email threads.
- Product usage / telemetry, support ticket trends.

---

## 5. Outputs & UX Surfaces

- Risk tier (Low/Med/High) with explanation bullets.
- Timeline of signals (sentiment dips, usage drops, escalations).
- Suggested next best action + owners.

---

## 6. Constraints & Non-Goals

- Respect customer data privacy; redact PII where necessary.
- Not a forecasting replacement; augment existing renewal pipeline.
- Provide confidence scores to avoid over-automation.

---

## 7. Implementation Hints

- Blend structured features (usage deltas) with LLM-extracted sentiment from notes.
- Use vector search to surface similar churn stories.
- Streamlit UI with filters by region, ARR, segment.

---

## 8. Test / Acceptance Criteria

- Pilot cohort shows lift in early intervention (e.g., >20% more save plans initiated).
- Users can trace every risk driver back to source text/data.
- Alerts configurable to avoid noise.

> Codex: Use this as the blueprint for the renewal risk insight agent.
"""
)
