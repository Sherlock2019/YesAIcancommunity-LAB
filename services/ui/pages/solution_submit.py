from __future__ import annotations

import os
from typing import Any, Dict, List

import requests
import streamlit as st


API_BASE_URL = st.secrets.get("API_URL", os.getenv("API_URL", "http://localhost:8090"))
PAGE_TITLE = "Solution Submit — YES AI CAN"


def api_endpoint(path: str) -> str:
    return f"{API_BASE_URL.rstrip('/')}/{path.lstrip('/')}"


def fetch_challenges() -> List[Dict[str, Any]]:
    try:
        response = requests.get(api_endpoint("/challenges"), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Unable to fetch challenges: {exc}")
        return []


def submit_solution(challenge_id: int, payload: Dict[str, Any]) -> Dict[str, Any] | None:
    try:
        response = requests.post(api_endpoint(f"/solutions/{challenge_id}"), json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Failed to submit solution: {exc}")
        return None


def fetch_solutions(challenge_id: int) -> List[Dict[str, Any]]:
    try:
        response = requests.get(api_endpoint(f"/solutions/{challenge_id}"), timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Unable to load solutions: {exc}")
        return []


def main() -> None:
    st.set_page_config(page_title=PAGE_TITLE, layout="wide")
    st.title("Submit an AI Solution")
    challenges = fetch_challenges()
    if not challenges:
        st.info("No challenges available. Visit the Challenge Hub to submit one.")
        return

    challenge_lookup = {challenge["id"]: challenge for challenge in challenges}
    preselect_id = st.session_state.pop("solution_target_challenge", None)
    query_params = st.query_params
    if "challenge_id" in query_params:
        try:
            preselect_id = int(query_params["challenge_id"])
        except ValueError:
            pass

    option_ids = list(challenge_lookup.keys())
    default_index = 0
    if preselect_id in option_ids:
        default_index = option_ids.index(preselect_id)

    selected_id = st.selectbox(
        "Choose a challenge",
        options=option_ids,
        index=default_index,
        format_func=lambda value: f"{challenge_lookup[value]['title']} — {challenge_lookup[value]['submitter_name']}",
    )
    selected_challenge = challenge_lookup[selected_id]

    st.write(f"**Description:** {selected_challenge.get('description')}")
    st.write(f"**Signals:** ⚡ {selected_challenge.get('urgency', 0):.1f} • 🎯 {selected_challenge.get('impact', 0):.1f}")

    with st.form("solution_form"):
        helper_name = st.text_input("Helper Name *")
        approach = st.text_area("Proposed AI Approach *", height=160)
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        status = st.selectbox("Status", ["Draft", "Prototype", "MVP Ready"])
        submitted = st.form_submit_button("Submit Solution", use_container_width=True)
        if submitted:
            if not helper_name or not approach:
                st.error("Helper Name and Proposed AI Approach are required.")
            else:
                payload = {
                    "helper_name": helper_name,
                    "approach": approach,
                    "difficulty": difficulty,
                    "status": status,
                }
                result = submit_solution(selected_challenge["id"], payload)
                if result:
                    st.success("Solution submitted!")
                    st.rerun()

    st.subheader("Solutions")
    solutions = fetch_solutions(selected_challenge["id"])
    if not solutions:
        st.info("No solutions yet — be the first to contribute!")
        return
    for solution in solutions:
        st.markdown(
            f"""
            **{solution['helper_name']}** — {solution['status']}  
            {solution['approach']}  
            _Difficulty: {solution['difficulty']}_
            """
        )
        st.markdown("---")


if __name__ == "__main__":
    main()
