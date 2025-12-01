import streamlit as st

st.set_page_config(
    page_title="AI Solution — Auto-Extract Partner Contract Data",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("AI Solution — Auto-Extract Partner Contract Data")
st.caption("The Feynman Extractor blueprint for Legal Ops.")

st.markdown(
    """
### 0. Challenge Snapshot
- **Submitter:** Oliver Grant — Legal Ops (EMEA)  
- **Need:** Faster extraction of renewal windows, SLAs, pricing riders from lengthy partner contracts.

---

### 1. Problem in One Line
“Upload a contract and receive structured clause data with evidence so partner packages can be assembled in hours, not days.”

---

### 2. Proposed AI Approach
- OCR + text normalization for scanned documents.
- Clause taxonomy driven by retrieval + LLM question answering.
- Provide explanation snippet + confidence for every extracted field.

---

### 3. Data & Signals
- Contract PDFs/DOCX, amendments, annexes.
- Clause definitions + prior annotated samples.
- Signals: key phrases ("Termination", "Renewal"), monetary amounts, durations, parties.

---

### 4. Solution Architecture
1. **Document Pipeline:** OCR (Tesseract/Azure) → text cleanup → chunking.
2. **Retrieval Layer:** Vector search over chunks keyed by clause taxonomy.
3. **Extraction Engine:** LLM prompts per clause returning value + rationale + location.
4. **Review UI:** Streamlit table with editable values, highlight viewer, export to CSV/API.

---

### 5. Delivery Plan
- **Phase 1:** Manual upload + deterministic regex/keyword extraction for top clauses.
- **Phase 2:** RAG-powered extraction + reviewer workflow with accept/reject.
- **Phase 3:** Integrations (CRM/CLM), analytics on clause trends, multi-language support.

---

### 6. Risks & Guardrails
- OCR errors → show confidence + original snippet side-by-side.
- Confidentiality → keep docs encrypted, enforce retention policies.
- Hallucinated clauses → require citation + highlight within document.

---

### 7. Success Metrics
- Time to assemble partner package.
- Reviewer correction rate per clause.
- % of contracts auto-processed end-to-end.
"""
)
