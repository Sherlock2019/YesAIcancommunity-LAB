import streamlit as st

st.set_page_config(
    page_title="Challenge Spec — Auto-Generate Security Incident Reports",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Challenge Spec — Auto-Generate Security Incident Reports")

st.markdown(
    """
## 1. Business Problem

SOC teams summarize incidents manually from SIEM events, chat threads, and emails.
Different stakeholders require different formats (executive summary, compliance annex, customer-ready brief).
Manual compilation delays response reviews.

---

## 2. Desired Outcome

Create a **bias-aware incident reporting assistant** that ingests security events, distills timelines,
and generates structured reports tailored for compliance, leadership, and customers with traceable evidence.

---

## 3. Users & Personas

- **Primary:** SOC leads and incident commanders.
- **Secondary:** Compliance, Legal, Customer Success.
- **System:** Streamlit app embedded in post-incident workflow.

---

## 4. Inputs & Data Sources

- SIEM event streams, EDR alerts, chat transcripts, ticket notes.
- Playbooks + classification tags (severity, MITRE ATT&CK mapping).
- Existing report templates.

---

## 5. Outputs & UX Surfaces

- Multi-section report (executive summary, timeline, impact, remediation).
- Automatically populated appendices (IOCs, affected assets, contacts).
- Downloadable PDF/Docx plus copy-to-email mode.

---

## 6. Constraints & Non-Goals

- Maintain factual accuracy; highlight confidence and data source for each statement.
- Keep data within secure boundary; no external API calls without approval.
- Not replacing incident response tooling; supplements documentation.

---

## 7. Implementation Hints

- Use LLM templating with guardrails (structured prompts, citation enforcement).
- Provide redaction tooling for sensitive fields.
- Version control every generated report for audit trail.

---

## 8. Test / Acceptance Criteria

- Report generation time drops from hours to minutes.
- SMEs rate accuracy/explainability >90% in pilot.
- Generated docs pass compliance review without major edits.

> Codex: Use this spec for the FairSecure Reporter agent build.
"""
)
