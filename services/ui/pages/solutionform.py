from __future__ import annotations

import textwrap
from datetime import datetime
from pathlib import Path
from typing import List

import streamlit as st

from services.ui.human_stack import HumanStack
from services.ui.utils.meta_store import load_json, save_json

SUBMISSIONS_FILE = "how_ai_help_submissions.json"
SOLUTIONS_FILE = "how_ai_help_solutions.json"
HUMAN_STACK_PATH = Path(__file__).resolve().parents[2] / "data" / "human_stack.json"
HUMAN_STACK = HumanStack(str(HUMAN_STACK_PATH))


def rerun_app() -> None:
    """Emit whichever Streamlit rerun hook is available."""
    rerun_fn = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
    if callable(rerun_fn):
        rerun_fn()


def load_submissions() -> List[dict]:
    return load_json(SUBMISSIONS_FILE, [])


def load_solutions() -> List[dict]:
    return load_json(SOLUTIONS_FILE, [])


def save_solutions(records: List[dict]) -> None:
    save_json(SOLUTIONS_FILE, records)


def ensure_submission_id(submission: dict) -> str:
    if submission.get("id"):
        return str(submission["id"])
    unique = f"{submission.get('title','')}_{submission.get('submitter',{}).get('name','')}"
    submission["id"] = unique
    return unique


def ensure_solution_id(solution: dict) -> str:
    if solution.get("id"):
        return str(solution["id"])
    solution["id"] = f"solution_{len(solution)}_{datetime.utcnow().timestamp()}"
    return solution["id"]


def generate_feature_tags(features: str) -> List[str]:
    tokens = []
    for token in features.replace("\n", " ").split():
        cleaned = token.strip(",.;()")
        if cleaned and cleaned[0].isupper():
            tokens.append(cleaned)
        if token.startswith("[") and token.endswith("]"):
            tokens.append(token.strip("[]"))
    return list(dict.fromkeys(tokens))[:8]


def ensure_session_state_keys() -> None:
    st.session_state.setdefault("howcanaihelp_selected_challenge_id", None)
    st.session_state.setdefault("howcanaihelp_components", [])
    st.session_state.setdefault("howcanaihelp_skill_matches", [])


def human_profile_for(name: str) -> dict | None:
    for entry in HUMAN_STACK.load():
        if entry.get("name", "").lower() == name.lower():
            return entry
    return None


def render_query_table(submissions: List[dict]) -> None:
    st.subheader("Table 1 — Challenge Feed")
    if not submissions:
        st.info("No challenges yet.")
        return
    table_rows = []
    for challenge in submissions:
        table_rows.append(
            {
                "Title": challenge.get("title", "Untitled"),
                "Submitter": challenge.get("submitter", {}).get("name", "Unknown"),
                "Dept / Region": f"{challenge.get('submitter', {}).get('department', '—')} / {challenge.get('submitter', {}).get('region', '—')}",
                "Impact": challenge.get("impact_score", 0),
                "Urgency": challenge.get("urgency", 0),
                "Category": challenge.get("category", "General"),
            }
        )
    st.table(table_rows)
    for challenge in submissions:
        if st.button(_button_label(challenge), key=f"aicanhelp_{ensure_submission_id(challenge)}"):
            st.session_state["howcanaihelp_selected_challenge_id"] = challenge["id"]
            rerun_app()


def _button_label(challenge: dict) -> str:
    return f"👉 Open {challenge.get('title', 'challenge')} in AI Help"


def render_challenge_preview(challenge: dict) -> None:
    st.markdown("#### 🔶 Section 1 — Select Challenge")
    st.info(
        f"📝 **{challenge.get('title','Untitled')}**\n\n"
        f"🧍 {challenge.get('submitter', {}).get('name','Unknown')} • "
        f"{challenge.get('submitter', {}).get('department','')} / {challenge.get('submitter', {}).get('region','')}\n\n"
        f"📎 Attachments: {', '.join(a.get('name', '—') for a in challenge.get('attachments', [])) or 'None'}\n\n"
        f"🎯 Impact Score: {challenge.get('impact_score', 0):.1f} • ⚡ Urgency: {challenge.get('urgency', 0):.1f}\n\n"
        f"🔁 Similar Agents: {', '.join(challenge.get('similar_agents', []) or ['None'])}"
    )


def render_profile_section(profile: dict | None) -> dict:
    st.markdown("#### 🔶 Section 2 — Your Profile")
    default_name = profile.get("name") if profile else "dzoan nguyen tran"
    default_team = profile.get("department") if profile else "YESAICAN Innovation Ops / AI Ambassadors"
    name = st.text_input("Name", value=default_name, key="solution_profile_name")
    team_role = st.text_input("Team / Role", value=default_team, key="solution_profile_team")
    skills = profile.get("skills", []) if profile else ["Analytics", "Streamlit", "Problem Framing"]
    st.write(f"Skill Tags from Human Stack: {', '.join(skills)}")
    return {"name": name, "team_role": team_role, "skills": skills}


def render_features_section() -> tuple[str, List[str]]:
    st.markdown("#### 🔶 Section 3 — The WHAT (Features of the Proposed Solution)")
    features = st.text_area("List the high-level features your AI solution will deliver.", height=140, key="solution_features")
    tags = generate_feature_tags(features)
    if tags:
        st.markdown("Feature Tags Auto-Generated: " + " ".join(f"`[{tag}]`" for tag in tags))
    return features, tags


def render_tools_section() -> List[str]:
    st.markdown("#### 🔶 Section 4 — AI Tools / Technologies Used")
    tools = st.multiselect(
        "Select relevant tools/technologies",
        [
            "LLM (Gemma, GPT, Mistral)",
            "OCR (EasyOCR, Tesseract, AWS Textract)",
            "RAG / Vector DB (FAISS, Chroma, LanceDB)",
            "Automation (LangChain, Airflow, Temporal)",
            "Streamlit or Dash UI",
            "FastAPI Backend",
            "PDF/Image Parsers",
            "Data validation (Pydantic)",
        ],
        default=["LLM (Gemma, GPT, Mistral)"],
        key="solution_tools_used",
    )
    return tools


def render_so_what_section() -> dict:
    st.markdown("#### 🔶 Section 5 — The SO WHAT (Business Benefits & Impact)")
    efficiency = st.text_area("1️⃣ Efficiency Gains", key="so_what_efficiency")
    cost = st.text_area("2️⃣ Cost Savings", key="so_what_cost")
    risk = st.text_area("3️⃣ Risk Reduction", key="so_what_risk")
    ux = st.text_area("4️⃣ User Experience Improvement", key="so_what_ux")
    return {"efficiency": efficiency, "cost": cost, "risk": risk, "ux": ux}


def render_components_section() -> List[dict]:
    st.markdown("#### 🔶 Section 6 — The HOW (Architecture / Components)")
    default_components = st.session_state["howcanaihelp_components"] or [
        {"Component": "Ingestion", "Type": "Service", "Description": "Pull customer billing formats", "Example": "S3 / PDF upload"},
        {"Component": "Parser", "Type": "AI", "Description": "Convert files → structured table", "Example": "LLM + Regex"},
        {"Component": "Mapping Engine", "Type": "Logic", "Description": "Align schema", "Example": "Python rules"},
        {"Component": "Dashboard", "Type": "UI", "Description": "Show reconciliation output", "Example": "Streamlit app"},
    ]
    editor = (
        st.data_editor(default_components, num_rows="dynamic", key="solution_components_editor")
        if hasattr(st, "data_editor")
        else st.experimental_data_editor(default_components, num_rows="dynamic", key="solution_components_editor")
    )
    components = editor.to_dict(orient="records") if hasattr(editor, "to_dict") else editor
    st.session_state["howcanaihelp_components"] = components
    return components


def render_skills_comparison(profile_skills: List[str]) -> tuple[List[dict], List[str]]:
    st.markdown("#### 🔶 Section 7 — Skills Needed VS My Skills VS Help Needed")
    required = ["Python", "Streamlit", "NLP", "Data Engineering", "ML Model Training", "UI/UX"]
    rows = []
    help_needed = []
    for skill in required:
        has_skill = skill in profile_skills
        gap = "No" if has_skill else "Yes"
        action = "—" if has_skill else "Find Partner"
        rows.append({"Required Skill": skill, "My Skill Level": "⭐⭐⭐⭐" if has_skill else "⭐⭐", "Gap?": gap, "Action": action})
        if not has_skill:
            help_needed.append(skill)
    st.table(rows)
    return rows, help_needed


def render_partner_button(missing_skills: List[str]) -> None:
    st.markdown("#### 🔶 Section 8 — “Search Skills Partner”")
    if not missing_skills:
        st.info("You have the core skills for this challenge. No partner needed.")
        return
    if st.button("🔍 Find People Who Can Help", key="solution_find_partners"):
        matches = HUMAN_STACK.search_people(" ".join(missing_skills))
        st.session_state["howcanaihelp_skill_matches"] = matches
        if matches:
            st.success("Found potential collaborators.")
        else:
            st.warning("No matches yet. Expand your network.")
    if st.session_state["howcanaihelp_skill_matches"]:
        st.table(
            [
                {
                    "Name": match.get("name"),
                    "Department": match.get("department"),
                    "Specialty": ", ".join(match.get("skills", [])),
                    "How They Can Help": ", ".join(match.get("superpowers", [])[:3]),
                    "Contact": match.get("email", "Slack"),
                }
                for match in st.session_state["howcanaihelp_skill_matches"]
            ]
        )


def render_difficulty_section() -> str:
    st.markdown("#### 🔶 Section 9 — Solution Difficulty")
    return st.selectbox(
        "How hard is the proposed solution?",
        ["Easy", "Medium", "Hard", "Requires Multi-Team Collaboration"],
        key="solution_difficulty",
    )


def render_summary_section(
    challenge: dict,
    profile: dict,
    features: str,
    tools: List[str],
    so_what: dict,
    components: List[dict],
    tags: List[str],
    difficulty: str,
) -> tuple[str, str]:
    st.markdown("#### 🔶 Section 10 — Final Solution Description (Codex-Generated Optional)")
    summary = textwrap.dedent(
        f"""
        Title: {challenge.get('title')}
        Challenge Chosen: {challenge.get('title')}
        Proposed Solution (WHAT): {features}
        AI Tools / Technologies: {', '.join(tools)}
        Business Benefits: Efficiency={so_what['efficiency']}, Cost={so_what['cost']}, Risk={so_what['risk']}, UX={so_what['ux']}
        Architecture Summary: {', '.join(sorted({comp.get('Component') for comp in components if comp.get('Component')}))}
        Skill Partners Needed: {', '.join(set(tags))}
        Timeline: 4-6 weeks
        Risks & Mitigations: TBD
        Difficulty: {difficulty}
        """
    ).strip()
    final_desc = st.text_area("Final Solution Summary", value=summary, key="solution_final_summary", height=200)
    return final_desc, summary


def build_solution_entry(
    challenge: dict,
    profile: dict,
    features: str,
    tools: List[str],
    so_what: dict,
    components: List[dict],
    tags: List[str],
    summary: str,
    difficulty: str,
) -> dict:
    token = f"{int(datetime.utcnow().timestamp())}"
    return {
        "id": f"solution_{token}",
        "challenge": challenge.get("title"),
        "challenge_id": challenge.get("id"),
        "author": profile.get("name"),
        "approach": summary,
        "difficulty": difficulty,
        "what_features": features,
        "ai_tools_used": tools,
        "so_what": so_what,
        "components": components,
        "tags": tags,
        "status": "Draft",
        "created_at": datetime.utcnow().isoformat(),
    }


def render_solution_form(submissions: List[dict], solutions: List[dict]) -> None:
    if not submissions:
        st.warning("Create challenges in Table 1 first.")
        return
    ensure_session_state_keys()
    selected_id = st.session_state.get("howcanaihelp_selected_challenge_id")
    selected_challenge = next((s for s in submissions if s["id"] == selected_id), submissions[0])
    st.session_state["howcanaihelp_selected_challenge_id"] = selected_challenge["id"]
    render_challenge_preview(selected_challenge)
    profile = human_profile_for("dzoan nguyen tran")
    profile_data = render_profile_section(profile or {})
    features, tags = render_features_section()
    tools = render_tools_section()
    so_what = render_so_what_section()
    components = render_components_section()
    _, missing = render_skills_comparison(profile_data["skills"])
    render_partner_button(missing)
    difficulty = render_difficulty_section()
    final_desc, summary = render_summary_section(
        selected_challenge, profile_data, features, tools, so_what, components, tags, difficulty
    )

    if st.button("🚀 Save Proposed Solution", key="solution_save"):
        if not (profile_data["name"] and features.strip()):
            st.error("Please fill at least your name and the WHAT section.")
            return
        entry = build_solution_entry(
            selected_challenge,
            profile_data,
            features,
            tools,
            so_what,
            components,
            tags,
            final_desc,
            difficulty,
        )
        solutions.insert(0, entry)
        save_solutions(solutions)
        st.success("Solution saved — Table 2 updated.")
        rerun_app()

    st.subheader("🧩 TABLE 2 — Proposed Cures and Solutions")
    if solutions:
        st.table(
            [
                {
                    "Challenge": idea.get("challenge"),
                    "Author": idea.get("author"),
                    "Difficulty": idea.get("difficulty"),
                    "Status": idea.get("status"),
                    "Summary": (idea.get("approach") or "")[:160],
                    "Created": idea.get("created_at", "")[:19],
                }
                for idea in solutions
            ]
        )
    else:
        st.info("No solution ideas yet.")


def main() -> None:
    st.set_page_config(page_title="AI Help — Teamwork Form", page_icon="🤝", layout="wide")
    st.title("✅ Improved Add a Proposed Solution Form (Teamwork-Ready)")
    st.write(
        "Select a challenge from Table 1, review the auto-filled preview, and craft a proposal that automatically populates Table 2."
    )
    submissions = load_submissions()
    solutions = load_solutions()
    render_query_table(submissions)
    st.divider()
    render_solution_form(submissions, solutions)


if __name__ == "__main__":
    main()
