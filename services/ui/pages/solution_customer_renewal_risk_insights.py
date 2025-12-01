import streamlit as st

st.set_page_config(
    page_title="AI Solution — Customer Renewal Risk Insights",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("AI Solution — Customer Renewal Risk Insights")
st.caption("Churn-signal workbench for Sales Ops / Customer Success.")

st.markdown(
    """
### 0. Challenge Snapshot
- **Submitter:** Laura Chen — Sales Ops (AMER)  
- **Problem:** Renewal signals are scattered (CRM notes, call summaries, tickets) leading to surprise churn.

---

### 1. Problem in One Line
“Fuse qualitative and quantitative signals to rank renewal risk and recommend save actions per account.”

---

### 2. Proposed AI Approach
- RAG pipeline over CRM notes, Gong/Zoom transcripts, support tickets.
- Combine sentiment trajectory + product usage deltas + deal context.
- LLM summarization that outputs risk drivers + next best action.

---

### 3. Data & Signals
- CRM opportunities, ARR, renewal dates, stage history.
- Call transcripts, meeting notes, QBR decks.
- Usage telemetry, ticket volumes, NPS survey data.

---

### 4. Solution Architecture
1. **Data Fabric:** Consolidate structured metrics + embeddings for unstructured text.
2. **Risk Model:** Gradient boosting / logistic regression with engineered features; LLM extractor contributes textual features.
3. **Insights Canvas:** Streamlit interface filtering by segment/region with account cards, driver bullets, recommended playbooks.
4. **Alerting:** Slack/Teams notifications when risk crosses threshold.

---

### 5. Delivery Plan
- **Phase 1:** Manual data upload + risk scoring workbook.
- **Phase 2:** Automated connectors + daily refresh, integrate usage telemetry.
- **Phase 3:** Action-tracking + workflow integration into CRM.

---

### 6. Risks & Guardrails
- Data privacy → enforce least privilege and redact sensitive meeting content.
- False alarms → show confidence + allow AE override & feedback loop.
- Explainability → tie each driver to exact sentence/data row.

---

### 7. Success Metrics
- Reduction in “surprise” churn cases.
- # of proactive save plans triggered from insights.
- CS/CX team satisfaction (survey) with tooling.
"""
)
