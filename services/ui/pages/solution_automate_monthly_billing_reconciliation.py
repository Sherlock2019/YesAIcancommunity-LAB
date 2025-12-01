import streamlit as st

st.set_page_config(
    page_title="AI Solution — Automate Monthly Billing Reconciliation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("AI Solution — Automate Monthly Billing Reconciliation")
st.caption("Baseline AI blueprint for the global billing reconciliation challenge.")

st.markdown(
    """
### 0. Challenge Snapshot
- **Submitter:** Finance Ops (Jordan Lee)  
- **Scope:** 12+ regions, ERP vs. billing vs. payments  
- **Pain:** Manual spreadsheets, delayed closes, poor auditability.

---

### 1. Problem in One Line
“Automatically reconcile invoices, payments, credits, and adjustments across systems, surfacing mismatches with explanations.”

---

### 2. Proposed AI Approach
- Normalize feeds from billing, ERP, payments, and credits into a canonical ledger.
- Use rule-based + ML-assisted matching to classify each line item (matched, missing, over/under, duplicate).
- Generate human-friendly narratives for each exception leveraging LLM templating.

---

### 3. Data & Signals
- Billing exports per period, ERP ledger snapshots, payment gateway data, credit memos, FX tables.
- Signals: invoice/account IDs, amount deltas, date proximity, text notes, historical exception labels.

---

### 4. Solution Architecture
1. **Ingest Layer:** Upload/API connectors drop files into a staging area (Parquet/Delta or Pandas cache).
2. **Standardization:** Apply schema harmonization + currency normalization.
3. **Matching Engine:** Cascading logic (exact match → fuzzy → ML classifier) that emits status + score.
4. **Narrative Generator:** LLM-based explanation referencing source rows.
5. **Review UI:** Streamlit board to filter by status, approve, and export reconciled package.

---

### 5. Delivery Plan
- **Sprint 1-2:** Deterministic matching + reconciliation summary exports.
- **Sprint 3-4:** ML-assisted exception scoring + natural-language explanations.
- **Sprint 5+:** Workflow integration (tickets, approvals) and scheduling.

---

### 6. Risks & Guardrails
- False positives causing rework → include threshold tuning + manual override.
- Regulatory data controls → ensure encryption at rest and role-based access.
- Traceability → keep immutable logs per reconciliation run.

---

### 7. Success Metrics
- Time to close vs. baseline.
- % of invoices auto-matched vs. manual.
- Auditor satisfaction / number of findings.
"""
)
