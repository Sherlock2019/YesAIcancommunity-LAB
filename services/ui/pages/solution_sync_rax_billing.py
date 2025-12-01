import streamlit as st

st.set_page_config(
    page_title="AI Solution — Sync Rax Billing with Customer Billing Format",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("AI Solution — Sync Rax Billing with Customer Billing Format")
st.caption("Baseline AI solution card that pairs with the Sync Rax Billing challenge.")

st.markdown(
    """
### 0. Challenge Snapshot
- **Challenge:** Sync Rax billing with customer billing format  
- **Submitter:** Jon — Billing Ops / APAC  
- **Category:** Finance  
- **Difficulty:** Easy → Medium  
- **Impact:** Removes monthly swivel-chair reconciliation work.

---

### 1. Problem in One Line
“Transform any Rackspace billing export into each customer’s bespoke invoice template with audit-grade accuracy.”

---

### 2. Proposed AI Approach
- Detect schemas for both Rackspace exports and customer templates.
- Use fuzzy matching + LLM hints to propose `source → target` mappings with confidence.
- Apply deterministic transforms (math, date formats, grouping) via a reusable pipeline.
- Validate totals and log every transformation for audit trail.

---

### 3. Data & Signals
- Rackspace billing CSV/XLSX per month.
- Customer invoice template, constraints, and contractual rules.
- Optional history of previously approved mappings for reinforcement.
- Signals: column name similarity, value patterns, reconciliation deltas.

---

### 4. Solution Architecture
1. **Ingest + Profile** sources and target templates into normalized dataframes.
2. **Schema Mapper** combines heuristics + LLM prompt to draft mapping spec (JSON).
3. **Transform Engine** executes renames, derived fields, aggregation policies.
4. **Validation Layer** compares totals, row counts, taxes, currency.
5. **Export + Profile Store** saves mapping + logs for subsequent months.

---

### 5. Delivery Plan
- **Phase 1:** Manual mapping UI with saved profiles and deterministic transforms.
- **Phase 2:** AI-assisted mapping suggestions + discrepancy dashboard.
- **Phase 3:** Scheduled runs, approvals, and deep audit logging.

---

### 6. Risks & Guardrails
- Mis-mapped financial fields → require human approval + diff viewer.
- Silent row drops → block run if variance > threshold and surface exception files.
- Data residency → keep all processing in approved Rackspace infra; no external LLM.

---

### 7. Success Metrics
- % of monthly billing files produced without manual edits.
- Reduction in customer invoice correction tickets.
- Analyst time saved per billing cycle.
"""
)
