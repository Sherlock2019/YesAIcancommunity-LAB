from __future__ import annotations

import os
from typing import Any, Dict, List

import requests
import streamlit as st


API_BASE_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://localhost:8090"))
PAGE_TITLE = "Challenge Hub — YES AI CAN"
UPLOAD_SESSION_KEY = "challenge_hub_refresh"


def api_endpoint(path: str) -> str:
    return f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def fetch_challenges() -> List[Dict[str, Any]]:
    try:
        response = requests.get(api_endpoint("/challenges"), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Unable to load challenges: {exc}")
        return []


def submit_challenge(form_data: Dict[str, Any], uploaded_file) -> Dict[str, Any] | None:
    try:
        response = requests.post(api_endpoint("/challenges"), json=form_data, timeout=10)
        response.raise_for_status()
        payload = response.json()
        if uploaded_file is not None:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type or "application/octet-stream")}
            upload_resp = requests.post(
                api_endpoint(f"/challenges/{payload['id']}/upload"),
                files=files,
                timeout=20,
            )
            upload_resp.raise_for_status()
            payload = upload_resp.json()
        return payload
    except requests.RequestException as exc:
        st.error(f"Failed to submit challenge: {exc}")
        return None


def go_to_solution(challenge_id: int) -> None:
    st.session_state["solution_target_challenge"] = challenge_id
    try:
        st.switch_page("pages/solution_submit.py")
    except Exception:
        st.query_params = {"challenge_id": challenge_id}


def render_challenge_card(challenge: Dict[str, Any]) -> None:
    tags = challenge.get("tags") or []
    cols = st.columns([3, 1])
    with cols[0]:
        st.markdown(f"#### 🧩 {challenge.get('title')}")
        st.caption(f"{challenge.get('submitter_name')} — {challenge.get('department')} • {challenge.get('region')}")
        st.write(challenge.get("description"))
        st.markdown(
            f"**Signals:** ⚡ {challenge.get('urgency', 0):.1f} • 🎯 {challenge.get('impact', 0):.1f}"
        )
        if tags:
            st.write("**Tags:** " + ", ".join(tags))
        if challenge.get("attachment_path"):
            st.write(f"📎 Attachment stored at `{challenge.get('attachment_path')}`")
    with cols[1]:
        st.markdown(f"**Category:** {challenge.get('category')}")
        st.markdown(f"**Difficulty:** {challenge.get('difficulty')}")
        if st.button("Submit Solution", key=f"submit_solution_{challenge['id']}", use_container_width=True):
            go_to_solution(challenge["id"])
        st.write(f"{len(challenge.get('solutions', []))} solutions submitted")


def render_submission_form() -> Dict[str, Any] | None:
    st.subheader("Submit a Challenge")
    with st.form("challenge_form"):
        submitter_name = st.text_input("Name *")
        department = st.text_input("Department *")
        region = st.text_input("Region *")
        role = st.text_input("Role *")
        title = st.text_input("Challenge Title *")
        description = st.text_area("Description *", height=150)
        task_type = st.text_input("Task Type *")
        category = st.text_input("Business Category *")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        impact = st.slider("Expected Impact (1-10)", 1.0, 10.0, 7.0)
        urgency = st.slider("Urgency (1-10)", 1.0, 10.0, 7.0)
        tags_input = st.text_input("Tags (comma separated) *")
        confidentiality = st.selectbox("Confidentiality", ["Public", "Internal", "Confidential"])
        team_size = st.number_input("Team Size", min_value=1, value=2)
        attachment = st.file_uploader("File Upload", type=["csv", "pdf", "jpg", "jpeg", "png", "json"])
        submitted = st.form_submit_button("Submit Challenge", use_container_width=True)

        if submitted:
            tags_list = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
            if not all([submitter_name, department, region, role, title, description, category, difficulty, task_type, tags_list]):
                st.error("Please fill in all required fields.")
            else:
                form_data = {
                    "submitter_name": submitter_name,
                    "department": department,
                    "region": region,
                    "role": role,
                    "title": title,
                    "description": description,
                    "task_type": task_type,
                    "category": category,
                    "difficulty": difficulty,
                    "impact": impact,
                    "urgency": urgency,
                    "tags": tags_list,
                    "confidentiality": confidentiality,
                    "team_size": team_size,
                }
                created = submit_challenge(form_data, attachment)
                if created:
                    st.success("Challenge submitted successfully!")
                    st.session_state[UPLOAD_SESSION_KEY] = st.session_state.get(UPLOAD_SESSION_KEY, 0) + 1
                    st.rerun()
    return None


def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, layout="wide")
    st.title("Challenge Hub")
    st.caption("Submit challenges and track AI solution progress across Rackers.")
    render_submission_form()
    st.divider()
    st.subheader("Live Challenges")
    challenges = fetch_challenges()
    if not challenges:
        st.info("No challenges yet. Be the first to submit!")
        return
    for challenge in challenges:
        with st.container():
            render_challenge_card(challenge)
            st.markdown("---")


if __name__ == "__main__":
    main()
