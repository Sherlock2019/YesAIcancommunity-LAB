import streamlit as st

st.set_page_config(
    page_title="Challenge Spec — Automate Monthly Billing Reconciliation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Challenge Spec — Automate Monthly Billing Reconciliation")

st.markdown(
    """
## 1. Business Problem

Finance Ops teams reconcile twelve regional billing exports against ERP ledgers using **manual spreadsheets**.
Disparate currencies, adjustments, and exception codes make the job slow and inconsistent.
Escalations occur when mismatches slip through or documentation is missing.

---

## 2. Desired Outcome

Deliver an **AI + deterministic reconciliation assistant** that ingests ERP data and billing exports,
flags mismatches, proposes journal entries, and produces an auditable summary pack each month.
Goals: reduce manual touch time by 70%, shrink reconciliation cycles, and centralize evidence.

---

## 3. Users & Personas

- **Primary:** Regional Billing Analysts.
- **Secondary:** Controllers, Accounting leads, external auditors.
- **System:** Monthly close workflow plus ad-hoc reruns when corrections come in.

---

## 4. Inputs & Data Sources

- ERP ledger exports (CSV/XLSX or API pull).
- Billing system exports by region.
- Adjustment journals, FX tables, historical reconciliation comments.

---

## 5. Outputs & UX Surfaces

- Auto-generated reconciliation workbook with matched/unmatched lines.
- Suggested journal entries with reasoning trail.
- Dashboard summarizing open items, value at risk, top exception types.

---

## 6. Constraints & Non-Goals

- Must be auditable and SOX-compliant; no silent AI decisions.
- Not replacing ERP; only orchestrating reconciliation tasks.
- Sensitive financial data must stay inside approved environments.

---

## 7. Implementation Hints

- Combine rule-based matching (exact + fuzzy) with embedding similarity for narratives.
- Keep deterministic audit log per line item.
- Provide CSV exports + Streamlit UI for review/approval loops.

---

## 8. Test / Acceptance Criteria

- Sample month reconciles automatically with <5% manual touch.
- Exceptions list is reproducible when rerun.
- Users can approve/reject AI suggestions and changes persist.

> Codex: Use this as the detailed brief for the reconciliation copilot.
"""
)
