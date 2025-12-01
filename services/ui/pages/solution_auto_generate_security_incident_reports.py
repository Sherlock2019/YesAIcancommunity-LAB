import streamlit as st

st.set_page_config(
    page_title="AI Solution — Auto-Generate Security Incident Reports",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("AI Solution — Auto-Generate Security Incident Reports")
st.caption("Bias-aware SOC documentation copilot.")

st.markdown(
    """
### 0. Challenge Snapshot
- **Submitter:** Karim Haddad — Security Ops  
- **Pain:** Manual compilation of multi-format incident reports delays approvals and is inconsistent.

---

### 1. Problem in One Line
“Given SIEM/EDR events + chat/ticket context, produce stakeholder-specific reports with citations and compliance sections.”

---

### 2. Proposed AI Approach
- Normalize events/timelines, then prompt an LLM with structured context blocks.
- Auto-generate executive summary, technical appendix, MITRE mapping, and customer-facing narrative.
- Provide inline citations referencing exact evidence.

---

### 3. Data & Signals
- SIEM alerts, EDR telemetry, chat transcripts, timeline annotations, ticket updates.
- Severity, MITRE techniques, impacted assets, remediation notes.

---

### 4. Solution Architecture
1. **Evidence Collector:** Connectors to SIEM/SOAR exports; allow manual uploads.
2. **Timeline Builder:** Order events + annotate with metadata.
3. **Report Generator:** Structured templates + LLM completions with guardrails/citations.
4. **Reviewer UI:** Streamlit editor to tweak sections, approve, and export PDF/Docx.

---

### 5. Delivery Plan
- **Phase 1:** Manual uploads + deterministic templating; store generated markdown.
- **Phase 2:** LLM augmentations with automated citation injection; multi-template support.
- **Phase 3:** Workflow integration (ticketing, e-sign) + knowledge base publishing.

---

### 6. Risks & Guardrails
- Hallucinations → enforce retrieval-augmented prompting with cite-every-claim policy.
- Data sensitivity → run models in secure environment; auto-redact high-risk fields.
- Compliance accuracy → keep version history + reviewer sign-off.

---

### 7. Success Metrics
- Report preparation time savings.
- Reviewer correction rate per section.
- Compliance/audit acceptance without rework.
"""
)
