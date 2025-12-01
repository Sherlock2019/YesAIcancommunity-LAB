import streamlit as st

st.set_page_config(
    page_title="Challenge Spec — Onboarding Ticket Auto-Categorizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Challenge Spec — Onboarding Ticket Auto-Categorizer")

st.markdown(
    """
## 1. Business Problem

HR Ops receives hundreds of onboarding requests spanning hardware, policy, security, payroll.
Routing is manual, leading to delays and inconsistent SLA tracking.
Attachment-heavy tickets slow down triage.

---

## 2. Desired Outcome

Deploy an **AI triage assistant** that classifies tickets into actionable categories,
extracts key entities from attachments, and routes/assigns automatically.

---

## 3. Users & Personas

- **Primary:** People Ops triage desk.
- **Secondary:** IT fulfillment, hiring managers, security reviewers.
- **System:** Embedded into existing ticketing portals or as a Streamlit front-end.

---

## 4. Inputs & Data Sources

- Ticket text (email, form submissions, chat transcripts).
- Attachments (PDF offers, ID docs, policy acknowledgments).
- HR workflow metadata (location, role type, urgency).

---

## 5. Outputs & UX Surfaces

- Category + confidence + recommended team.
- Extracted summary (e.g., start date, hardware requested).
- SLA dashboard showing queue health.

---

## 6. Constraints & Non-Goals

- Must comply with privacy and data retention guidelines.
- Not a replacement for HRIS; only orchestrates intake.
- System should gracefully handle low-confidence predictions (fallback to manual).

---

## 7. Implementation Hints

- Fine-tune or prompt LLM with few-shot examples per category.
- Use lightweight OCR for attachments and embed results.
- Maintain taxonomy in JSON for easy updates.

---

## 8. Test / Acceptance Criteria

- 90%+ accuracy on primary routing categories during pilot.
- Time-to-triage reduced by >40%.
- Analysts can re-train / re-label via feedback UI.

> Codex: Reference this spec when building the onboarding categorizer agent.
"""
)
