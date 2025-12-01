import streamlit as st

st.set_page_config(
    page_title="AI Solution — Onboarding Ticket Auto-Categorizer",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("AI Solution — Onboarding Ticket Auto-Categorizer")
st.caption("Vision/LLM hybrid to triage onboarding tickets + attachments.")

st.markdown(
    """
### 0. Challenge Snapshot
- **Submitter:** Rachel Gomez — HR Ops  
- **Pain:** Manual routing of onboarding tickets with attachments slows SLAs.

---

### 1. Problem in One Line
“Auto-classify onboarding requests and extract key entities from attachments so the right team acts immediately.”

---

### 2. Proposed AI Approach
- Multimodal LLM to process text + document scans.
- Few-shot classifier for categories (policy, hardware, payroll, security, manager action).
- Entity extraction of start dates, equipment, approvals; push to workflow routing.

---

### 3. Data & Signals
- Ticket text (forms, chat transcripts, emails).
- Attachments: offer letters, IDs, policy forms.
- Metadata: location, role type, urgency.

---

### 4. Solution Architecture
1. **Ingest & OCR:** Convert attachments to text; store embeddings.
2. **Classifier:** Prompt-tuned LLM / fine-tuned model predicts category + confidence.
3. **Entity Extractor:** Grab structured fields for downstream systems.
4. **Routing Layer:** ServiceNow/Jira integration + Streamlit supervisory UI for reassign.

---

### 5. Delivery Plan
- **Sprint 1:** Manual override UI + baseline classifier with human feedback capture.
- **Sprint 2-3:** Attachment OCR + entity extraction, SLA dashboard.
- **Sprint 4+:** Continuous learning loop + HRIS integration.

---

### 6. Risks & Guardrails
- Sensitive PII → encrypt attachments, mask outputs, follow retention rules.
- Misclassification → send low-confidence items to human queue; allow one-click correction feeding re-train set.
- Multilingual docs → add language detection + translation fallback.

---

### 7. Success Metrics
- % tickets auto-routed correctly.
- SLA improvements (time-to-first-touch, time-to-close).
- Reduction in backlog + HR Ops satisfaction.
"""
)
