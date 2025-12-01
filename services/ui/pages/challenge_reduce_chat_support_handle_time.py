import streamlit as st

st.set_page_config(
    page_title="Challenge Spec — Reduce Chat Support Handle Time",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("Challenge Spec — Reduce Chat Support Handle Time")

st.markdown(
    """
## 1. Business Problem

Tier-1 chat agents juggle dozens of simultaneous conversations without intelligent assistance.
Knowledge articles are scattered; macro suggestions are generic, leading to long handle times and inconsistent quality.

---

## 2. Desired Outcome

Launch a **chat copilot** that detects intent in real time, proposes personalized macros, and nudges agents toward next best actions.
It should shorten average handle time while improving CSAT.

---

## 3. Users & Personas

- **Primary:** Chat Ops leads and Tier-1 agents.
- **Secondary:** Knowledge managers monitoring macro performance.
- **System:** Side-panel assistant inside the existing chat console.

---

## 4. Inputs & Data Sources

- Live chat transcript stream.
- Knowledge base articles, macro library, troubleshooting trees.
- Historical conversation metadata (topic, resolution, CSAT).

---

## 5. Outputs & UX Surfaces

- Ranked macro suggestions with confidence and rationale.
- Auto-generated follow-up notes or closure summaries.
- Team dashboard measuring AHT, adoption, macro effectiveness.

---

## 6. Constraints & Non-Goals

- Must keep human in the loop; no fully automated replies.
- Respect data containment (no sending chat logs externally without approval).
- Not a replacement for the chat platform.

---

## 7. Implementation Hints

- Lightweight intent detection (embedding similarity + classifier) plus prompt-engineered LLM for macro drafts.
- Cache knowledge embeddings for low latency.
- Provide feedback controls (accept/modify/flag) to continuously improve.

---

## 8. Test / Acceptance Criteria

- Pilot shows measurable AHT reduction (target 15%).
- Agents report improved confidence and adoption >70%.
- Quality reviewers confirm copilot recommendations align with policy.

> Codex: Reference this spec when delivering the FastTrack Support Tutor agent.
"""
)
