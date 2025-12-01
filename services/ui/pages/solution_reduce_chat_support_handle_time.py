import streamlit as st

st.set_page_config(
    page_title="AI Solution — Reduce Chat Support Handle Time",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("AI Solution — Reduce Chat Support Handle Time")
st.caption("FastTrack Support Tutor blueprint for Tier-1 chat ops.")

st.markdown(
    """
### 0. Challenge Snapshot
- **Submitter:** Andrew Ng — Chat Ops Lead  
- **Pain:** Agents juggle multiple chats without contextual macro suggestions, causing long handle time.

---

### 1. Problem in One Line
“Detect intent live, recommend the best macro/KB snippet, and guide the agent to closure faster.”

---

### 2. Proposed AI Approach
- Streaming intent detection (embedding similarity + lightweight classifier).
- LLM synthesizes tailored macro drafts referencing KB articles + prior cases.
- Copilot sidebar showing suggested replies, next steps, and quality checklist.

---

### 3. Data & Signals
- Real-time chat transcript, metadata (queue, product, severity), historical transcripts w/ outcomes, macro usage stats, CSAT scores.

---

### 4. Solution Architecture
1. **Listener:** Hook into chat platform events to stream transcripts.
2. **Intent + Context Builder:** Maintain conversation state, detect intents, fetch KB snippets via vector search.
3. **Recommendation Engine:** Score macros, render suggestions with rationale + confidence.
4. **Coach UI:** Streamlit/embedded panel for accept/edit/send + capture feedback for learning.

---

### 5. Delivery Plan
- **Pilot:** Offline replays + agent feedback to tune similarity + macros.
- **MVP:** Real-time panel for limited queue; collect adoption metrics.
- **Scale:** Rollout to more queues, add automation for wrap-up notes.

---

### 6. Risks & Guardrails
- Bad suggestions degrade trust → include quality rating + quick decline reason.
- Sensitive data leaving chat platform → keep inference within secure enclave.
- Policy compliance → embed guardrails checklist (tone, disclaimers) per macro.

---

### 7. Success Metrics
- Average handle time reduction.
- Macro adoption / acceptance rate.
- CSAT uplift for assisted chats.
"""
)
