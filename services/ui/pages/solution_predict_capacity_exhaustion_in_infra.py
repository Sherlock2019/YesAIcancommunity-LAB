import streamlit as st

st.set_page_config(
    page_title="AI Solution — Predict Capacity Exhaustion in Infra",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("AI Solution — Predict Capacity Exhaustion in Infra")
st.caption("Neural capacity oracle for proactive infra planning.")

st.markdown(
    """
### 0. Challenge Snapshot
- **Submitter:** Santiago Rivera — Data Center Engineering (LATAM)  
- **Need:** Predict storage/CPU exhaustion before thresholds breach so workloads can be rebalanced.

---

### 1. Problem in One Line
“Forecast capacity burn per cluster and alert weeks before exhaustion, including recommended mitigations.”

---

### 2. Proposed AI Approach
- Multivariate time-series models (Prophet/TFT) per cluster.
- Feature engineering for seasonality, workload mix, planned maintenance.
- LLM summarizer to explain forecast + actions.

---

### 3. Data & Signals
- Telemetry metrics (CPU, memory, disk, IOPS) at hourly granularity.
- Workload placements, reservations, growth factors.
- Incident and maintenance history.

---

### 4. Solution Architecture
1. **Data Lake:** Centralize metrics + metadata (Delta tables or TSDB extracts).
2. **Forecast Service:** Train + serve forecasts with sliding windows and anomaly detection.
3. **Insight Layer:** Streamlit dashboards with sparkline forecasts, exhaustion date, confidence intervals.
4. **Action Recommender:** Rule engine that suggests rebalance, procurement, cleanup tasks.

---

### 5. Delivery Plan
- **Phase 1:** Batch forecast for top 10 clusters, manual CSV ingestion.
- **Phase 2:** Automated pipeline + alerting integration (Slack/Teams, ticketing).
- **Phase 3:** API + automation hooks to trigger mitigation workflows.

---

### 6. Risks & Guardrails
- Data gaps → highlight “low confidence / missing telemetry” states.
- Over-alerting → enable per-cluster threshold tuning.
- Security → scrub tenant-identifying info; enforce RBAC for dashboards.

---

### 7. Success Metrics
- % of exhaustion events predicted ≥14 days prior.
- Reduction in emergency migrations.
- Planner/NOC satisfaction and adoption.
"""
)
