import streamlit as st

st.set_page_config(
    page_title="Challenge Spec — Predict Capacity Exhaustion in Infra",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Challenge Spec — Predict Capacity Exhaustion in Infra")

st.markdown(
    """
## 1. Business Problem

Data center engineering teams discover storage or CPU exhaustion only when alerts fire.
Reactive scaling causes emergency migrations and costly downtime.
Telemetry is abundant but lacks predictive context.

---

## 2. Desired Outcome

Introduce a **time-series forecasting copilot** that predicts exhaustion windows,
flags clusters needing rebalance, and recommends mitigation options weeks in advance.

---

## 3. Users & Personas

- **Primary:** Infra reliability leads / capacity planners.
- **Secondary:** NOC/SRE teams and finance for CapEx planning.
- **System:** Streaming dashboard + weekly email digest.

---

## 4. Inputs & Data Sources

- Metrics from monitoring stack (CPU, memory, disk, network per cluster).
- Workload placement metadata, maintenance schedules.
- Incident history for context.

---

## 5. Outputs & UX Surfaces

- Forecast curves with predicted exhaustion date + confidence band.
- Recommended actions (rebalance, procure, clean-up) with impact estimate.
- API to trigger automation or ticket creation.

---

## 6. Constraints & Non-Goals

- Forecasts must highlight assumption windows and confidence.
- Not a full CMDB replacement; relies on existing inventory.
- Needs to operate across regions with varying telemetry quality.

---

## 7. Implementation Hints

- Use Prophet/Temporal Fusion Transformer or similar for multivariate series.
- Feature engineer leading indicators (growth rate, burstiness, seasonality).
- Provide backtesting module to prove accuracy to stakeholders.

---

## 8. Test / Acceptance Criteria

- Pilot predicts 80% of exhaustion events at least 2 weeks ahead.
- Users can drill down to raw metrics when questioning a forecast.
- Action recommendations tie to measurable risk reduction.

> Codex: Apply this spec when implementing the capacity oracle agent.
"""
)
