import streamlit as st

st.set_page_config(
    page_title="AI Solution — Predict Ticket Escalations for Managed Cloud",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("AI Solution — Predict Ticket Escalations for Managed Cloud")
st.caption("Escalation-risk playbook for Managed Cloud support queues.")

st.markdown(
    """
### 0. Challenge Snapshot
- **Submitter:** Sasha Ortiz — Support Lead (EMEA)  
- **Issue:** L3 escalations surprise teams; sentiment + workflow signals ignored.

---

### 1. Problem in One Line
“Score every active ticket for escalation risk using conversational and operational context so leads can intervene.”

---

### 2. Proposed AI Approach
- Stream chat/email transcripts through an LLM sentiment trajectory model.
- Fuse structured metrics (response latency, reopen count, severity) into a gradient-boosted classifier.
- Surface risk with explanations + recommended playbooks.

---

### 3. Data & Signals
- Ticket metadata (queues, severities, SLAs, assignees).
- Conversation text, customer sentiment, mention of blockers.
- Historical resolution paths + escalation labels.

---

### 4. Solution Architecture
1. **Feature Store:** Build rolling aggregates per ticket every N minutes.
2. **Model Layer:** Train classifier/sequence model to output P(escalate) + top drivers.
3. **Inference API:** Real-time scoring endpoint triggered by ticket updates.
4. **Ops Console:** Streamlit board sorted by risk with drill-down, timeline, and recommended step (assign SME, proactive update, etc.).

---

### 5. Delivery Plan
- **MVP:** Batch scoring + dashboard refresh every hour.
- **Phase 2:** Streaming inference hook into ServiceNow/Zendesk webhooks.
- **Phase 3:** Integrate automated routing + closed-loop feedback on actual escalations.

---

### 6. Risks & Guardrails
- Model bias toward noisy customers → include customer health normalization and human override workflow.
- Sensitive chat data → mask PII before storing features.
- False alarms → tune thresholds per tier; include confidence + similar-case references.

---

### 7. Success Metrics
- Recall on escalated tickets (target >70%).
- Reduction in mean time to resolution for high-risk queue.
- Adoption by support leads (daily active users).
"""
)
