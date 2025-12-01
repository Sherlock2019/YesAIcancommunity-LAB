import streamlit as st

st.set_page_config(
    page_title="Challenge Spec — Auto-Extract Partner Contract Data",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Challenge Spec — Auto-Extract Partner Contract Data")

st.markdown(
    """
## 1. Business Problem

Legal Ops teams sift through lengthy partner contracts to pull clauses, renewal terms, SLAs, and pricing riders.
Manual review slows packaging deals for partners and increases risk of missing obligations.

---

## 2. Desired Outcome

Deliver an **explainable contract extraction assistant** that ingests PDFs, detects key clauses, and outputs structured data with reasoning snippets.
Focus on transparency so reviewers can trace every extraction back to source text.

---

## 3. Users & Personas

- **Primary:** Legal managers and contract analysts.
- **Secondary:** Partner operations, finance approvers.
- **System:** Streamlit UI for uploads + API for downstream CRM.

---

## 4. Inputs & Data Sources

- Partner agreements (PDF, DOCX, scanned images).
- Clause taxonomies and definitions.
- Historical annotated contracts for training/validation.

---

## 5. Outputs & UX Surfaces

- Structured JSON/CSV with clause fields (renewal window, exclusivity, payment terms, liabilities).
- Evidence viewer showing highlighted text spans and commentary.
- Alerts for missing/ambiguous clauses.

---

## 6. Constraints & Non-Goals

- Must handle multi-language clauses and scanned docs via OCR.
- Not a contract authoring tool; focused on extraction + review.
- Data must remain within secure legal environment.

---

## 7. Implementation Hints

- Combine OCR (e.g., Tesseract) with LLM QA prompts anchored by retrieval (RAG).
- Maintain clause schema in config for easy expansion.
- Provide reviewer workflow: accept/reject/edit extractions.

---

## 8. Test / Acceptance Criteria

- Extraction precision/recall targets per clause (e.g., >85%).
- Review cycle time reduced by 50% for pilot team.
- Every structured output links to underlying contract text.

> Codex: Use this spec when implementing The Feynman Extractor agent.
"""
)
