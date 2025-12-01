from __future__ import annotations

import json
import hashlib
import html
from datetime import datetime
from pathlib import Path
from typing import List

import streamlit as st

# Backward-compat: ensure experimental_rerun exists even on Streamlit versions where it was removed.
if not getattr(st, "experimental_rerun", None):
    st.experimental_rerun = getattr(st, "rerun", lambda: None)

from services.ui.utils.meta_store import load_json, save_json
from services.ui.human_stack import HumanStack

SUBMISSIONS_FILE = "how_ai_help_submissions.json"
SOLUTIONS_FILE = "how_ai_help_solutions.json"
PROJECTS_FILE = "projects.json"
ASSET_DIR = Path(__file__).resolve().parents[2] / ".sandbox_meta" / "how_ai_help_assets"
ASSET_DIR.mkdir(parents=True, exist_ok=True)

HUMAN_STACK_PATH = Path(__file__).resolve().parents[2] / "data" / "human_stack.json"
HUMAN_STACK = HumanStack(str(HUMAN_STACK_PATH))

def rerun_app() -> None:
    """Use whichever rerun API Streamlit exposes in this version."""
    try:
        # Streamlit ≥ 1.30
        st.rerun()
    except AttributeError:
        try:
            # Fallback for older versions that still provide experimental_rerun
            st.rerun()
        except Exception:
            pass  # Silent fallback to avoid crashes

DEFAULT_SUBMISSIONS: List[dict] = []
DEFAULT_SOLUTIONS: List[dict] = []


def ensure_submission_id(submission: dict) -> str:
    if submission.get("id"):
        return str(submission["id"])
    submitter = submission.get("submitter", {})
    raw = (
        f"{submission.get('title', '')}|"
        f"{submitter.get('name', '')}|"
        f"{submitter.get('department', '')}|"
        f"{(submission.get('description') or '')[:80]}"
    )
    digest = hashlib.sha1(raw.encode("utf-8", "ignore")).hexdigest()[:10]
    anchor = f"challenge_{digest}"
    submission["id"] = anchor
    return anchor


def ensure_solution_id(solution: dict) -> str:
    if solution.get("id"):
        return str(solution["id"])
    raw = (
        f"{solution.get('challenge', '')}|"
        f"{solution.get('author', '')}|"
        f"{(solution.get('approach') or '')[:80]}"
    )
    digest = hashlib.sha1(raw.encode("utf-8", "ignore")).hexdigest()[:10]
    anchor = f"solution_{digest}"
    solution["id"] = anchor
    return anchor


def build_skill_query(submission: dict) -> str:
    if not submission:
        return ""
    skills = submission.get("skills_needed")
    if isinstance(skills, str):
        skills = [skills]
    if not skills:
        tags = submission.get("tags")
        if isinstance(tags, str):
            return tags
        if isinstance(tags, list):
            skills = tags
    fallback = []
    for field in ("category", "difficulty", "task_type", "description"):
        val = submission.get(field)
        if isinstance(val, list):
            fallback.extend(val)
        elif isinstance(val, str):
            fallback.append(val)
    if not skills and fallback:
        skills = fallback
    normalized = [str(item).strip() for item in (skills or []) if str(item).strip()]
    return " ".join(normalized)


def badge_html(label: str) -> str:
    style = (
        "display:inline-flex;padding:0.15rem 0.65rem;margin:0.1rem 0.25rem;"
        "border-radius:999px;background:rgba(59,130,246,0.13);color:#0f172a;"
        "font-size:0.78rem;font-weight:600;"
    )
    return f"<span style=\"{style}\">{html.escape(label)}</span>"


def display_human_stack_matches(matches: list[dict]) -> None:
    if not matches:
        st.info("No Rackers found for the requested skills yet.")
        return
    st.markdown("#### 👥 Rackers Who Can Help")
    col_count = min(len(matches), 3) or 1
    cols = st.columns(col_count)
    for idx, profile in enumerate(matches):
        with cols[idx % col_count]:
            skills = profile.get("skills", [])
            superpowers = profile.get("superpowers", [])
            project_summary = profile.get("projects_built", [])
            st.markdown(
                f"""
                <div style="border:1px solid rgba(15,23,42,0.1);border-radius:14px;padding:1rem;background:rgba(15,23,42,0.03);min-height:220px;">
                    <h4 style="margin-bottom:0.3rem;">{html.escape(profile.get('name','–'))}</h4>
                    <p style="margin:0.2rem 0;"><strong>Dept:</strong> {html.escape(profile.get('department','–'))}</p>
                    <p style="margin:0.2rem 0;"><strong>Region:</strong> {html.escape(profile.get('region','–'))}</p>
                    <div style="margin:0.35rem 0;">
                        {''.join(badge_html(skill) for skill in skills)}
                    </div>
                    <div style="margin:0.35rem 0;">
                        {''.join(badge_html(power) for power in superpowers)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if project_summary:
                st.caption(f"Projects built: {len(project_summary)}")


def find_submission_by_identifier(submissions: List[dict], identifier: str | None, fallback_title: str | None = None) -> dict | None:
    target = (identifier or "").strip()
    fallback = (fallback_title or "").strip().lower() if fallback_title else ""
    for submission in submissions:
        submission_id = ensure_submission_id(submission)
        if target and submission_id == target:
            return submission
        if fallback and submission.get("title", "").strip().lower() == fallback:
            return submission
    return None


def find_solution_by_identifier(solutions: List[dict], identifier: str | None, fallback_challenge: str | None = None) -> dict | None:
    target = (identifier or "").strip()
    fallback = (fallback_challenge or "").strip().lower() if fallback_challenge else ""
    for idea in solutions:
        solution_id = ensure_solution_id(idea)
        if target and solution_id == target:
            return idea
        if fallback and idea.get("challenge", "").strip().lower() == fallback:
            return idea
    return None


def _get_query_params() -> dict[str, list[str]]:
    raw = st.query_params
    params: dict[str, list[str]] = {}
    try:
        items = raw.items()
    except AttributeError:
        items = raw.to_dict().items()
    for key, value in items:
        if isinstance(value, (list, tuple)):
            params[key] = list(value)
        else:
            params[key] = [value]
    return params


def _set_query_params(params: dict[str, list[str] | str]) -> None:
    st.query_params = params


def clear_query_params(*keys: str) -> None:
    params = _get_query_params()
    mutated = False
    for key in keys:
        if key in params:
            params.pop(key, None)
            mutated = True
    if mutated:
        _set_query_params(params)


def render_leaderboard_and_blueprint(submissions: list[dict]) -> None:
    total = len(submissions)
    top = sorted(submissions, key=lambda x: x.get("upvotes", 0), reverse=True)[:3]
    highlights = "".join(
        f"<li><strong>{html.escape(item.get('title','—'))}</strong> — 👍 {item.get('upvotes',0)} | ⚡ {item.get('urgency',0):.1f} | 🎯 {item.get('impact_score',0):.1f}</li>"
        for item in top
    )
    st.markdown(
        f"""
        <div class="neon-table" style="margin-top:1rem;">
            <div class="neon-table-title">🏆 Kaggle-Style Leaderboard Signals</div>
            <ul style="color:rgba(15,23,42,0.85);line-height:1.6;margin-bottom:1rem;">
                {highlights}
            </ul>
            <p style="color:rgba(15,23,42,0.8);">
                Total challenges: <strong>{total}</strong> • Auto-computed ranking blends upvotes, urgency, impact, and discussion velocity.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="neon-table" style="margin-top:1rem;">
            <div class="neon-table-title">🤖 AI Auto-Blueprint</div>
            <p>Each submission triggers an AI baseline that drafts the A→F agent workflow, required datasets, risk notes, suggested UI/API surface, and a timeline estimate.</p>
            <ul>
                <li>🔍 Auto-detect similar agents & reusable patterns.</li>
                <li>🪄 Generate “Convert to Project” payload with owners + version 0.1.</li>
                <li>👥 Tag suggested Ambassadors & SMEs directly from the Human Stack.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_solution_detail_card(idea: dict) -> None:
    st.markdown(
        f"""
        <div class="neon-table" style="margin:1rem 0;">
            <div class="neon-table-title">🧩 {idea.get('challenge', 'Challenge')}</div>
            <p><strong>Author:</strong> {idea.get('author', 'Unknown')}</p>
            <p><strong>Approach:</strong> {idea.get('approach', '')}</p>
            <p><strong>Difficulty:</strong> {idea.get('difficulty', 'Medium')} • ⭐ {idea.get('upvotes', 0)} • 💬 {idea.get('comments', 0)}</p>
            <p><strong>Status:</strong> {idea.get('status', 'Draft')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _load_records(name: str, default: List[dict]) -> List[dict]:
    data = load_json(name, default)
    if isinstance(data, dict):
        for key in ("items", "records", "data"):
            if key in data and isinstance(data[key], list):
                return data[key]
        return [data]
    return data or []


def load_submissions() -> List[dict]:
    return _load_records(SUBMISSIONS_FILE, DEFAULT_SUBMISSIONS)


def save_submissions(records: List[dict]) -> None:
    save_json(SUBMISSIONS_FILE, records)


def load_solutions() -> List[dict]:
    return _load_records(SOLUTIONS_FILE, DEFAULT_SOLUTIONS)


def save_solutions(records: List[dict]) -> None:
    save_json(SOLUTIONS_FILE, records)


def save_projects(records: List[dict]) -> None:
    save_json(PROJECTS_FILE, records)


def load_projects() -> List[dict]:
    data = load_json(PROJECTS_FILE, [])
    return data or []


def store_attachments(files, token: str) -> List[dict]:
    stored = []
    for uploaded in files or []:
        suffix = Path(uploaded.name).suffix or ""
        dest = ASSET_DIR / f"{token}_{uploaded.name}"
        with open(dest, "wb") as handle:
            handle.write(uploaded.getbuffer())
        stored.append({"name": uploaded.name, "path": str(dest), "type": suffix.lstrip(".")})
    return stored


def comma_tags(raw: str) -> List[str]:
    if not raw:
        return []
    return [part.strip() for part in raw.split(",") if part.strip()]


def generate_ai_baseline(title: str, description: str, category: str, difficulty: str) -> dict:
    lower_desc = description.lower()
    data_needs = []
    if "invoice" in lower_desc or "billing" in lower_desc:
        data_needs.extend(["ERP exports", "Invoice CSV", "Ledger snapshots"])
    if "ticket" in lower_desc or "support" in lower_desc:
        data_needs.append("ServiceNow / Zendesk logs")
    if not data_needs:
        data_needs.append("Team-provided sample data")
    workflow = [
        "Intake & classify problem statement",
        "Assess available data + access controls",
        "Draft automation / agent blueprint",
        "Human validation and policy checks",
        "Deploy pilot, monitor telemetry",
    ]
    complexity = "High" if difficulty.lower() in {"hard", "critical"} else "Medium"
    timeline = "3-4 weeks" if difficulty.lower() == "medium" else "6-8 weeks"
    return {
        "summary": f"Baseline AI plan for {title}",
        "category": category,
        "workflow": workflow,
        "required_data": data_needs,
        "risks": ["Data quality", "Access controls", "Change management"],
        "similar_agents": ["Credit Appraisal Agent", "IT Troubleshooter"],
        "complexity": complexity,
        "timeline": timeline,
        "why_ai": "AI can eliminate repetitive toil and surface insights faster than manual processes.",
    }


def add_comment(submission: dict, author: str, note: str) -> None:
    submission.setdefault("comments_thread", []).append(
        {
            "author": author or "Anonymous",
            "note": note,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )


def convert_to_project(submission: dict) -> None:
    projects = load_projects()
    submission_id = submission.get("id")
    for proj in projects:
        if proj.get("source_submission_id") == submission_id:
            st.info("Project already exists for this challenge.")
            return
    project_entry = {
        "title": submission.get("title"),
        "authors": [submission.get("submitter", {}).get("name", "Unknown")],
        "business_area": submission.get("category", "General"),
        "summary": submission.get("description", ""),
        "status": "Incubation",
        "created_at": datetime.utcnow().isoformat(),
        "upvotes": submission.get("upvotes", 0),
        "comments": submission.get("comments", 0),
        "source_submission_id": submission_id,
        "ai_baseline": submission.get("ai_baseline"),
    }
    projects.append(project_entry)
    save_projects(projects)
    st.success("Project created in Project Hub metadata.")


def render_connection_panel() -> None:
    st.markdown(
        """
        ### 🤝 Connection Teams & Slack Channels
        - `#yesaican-lab` — Core coordination hub
        - `#ai-ambassadors` — Ambassador cohort + office hours
        - `#rex-integrations` — Feed ideas into REX 2.0 crew
        - Teams Chat: **YESAICAN Innovation Ops**
        - Teams Chat: **Customer Zero Project Leads**
        """
    )


def upvote_submission(submission: dict, submissions: List[dict]) -> None:
    submission["upvotes"] = submission.get("upvotes", 0) + 1
    submission["comments"] = submission.get("comments", 0)
    submission["urgency"] = submission.get("urgency", 6.0) + 0.1
    save_submissions(submissions)
    st.toast("Upvote recorded!", icon="👍")


def render_submission_card(
    submission: dict,
    submissions: List[dict],
    solutions: List[dict],
    active_target: str | None,
):
    submitter = submission.get("submitter", {})
    is_editing = st.session_state.get("editing_submission_id") == submission.get("id")
    st.markdown(
        f"""
        <div class="neon-table" style="margin-top:1rem;">
            <div class="neon-table-title">📝 {submission.get('title','Untitled')}</div>
            <p>{submission.get('description','')}</p>
            {f"<p><strong>Product Features:</strong> {submission.get('product_features','')}</p>" if submission.get('product_features') else ""}
            <p><strong>Submitter:</strong> {submitter.get('name','Unknown')} — {submitter.get('department','')} / {submitter.get('region','')}</p>
            <p><strong>Signals:</strong> 👍 {submission.get('upvotes',0)} • 💬 {submission.get('comments',0)} • ⚡ {submission.get('urgency',0):.1f} • 🎯 {submission.get('impact_score',0):.1f}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(5)
    if cols[0].button("👍 Upvote", key=f"upvote_{submission['id']}"):
        upvote_submission(submission, submissions)
        rerun_app()
    if cols[1].button("🚀 Convert to Project", key=f"convert_{submission['id']}"):
        convert_to_project(submission)
    if cols[2].button("➕ Add Solution", key=f"solution_{submission['id']}"):
        st.session_state["active_solution_target"] = submission["title"]
        rerun_app()
    if cols[3].button("✏️ Edit", key=f"edit_{submission['id']}"):
        st.session_state["editing_submission_id"] = submission["id"]
        rerun_app()
    if cols[4].button("🗑️ Delete", key=f"delete_{submission['id']}"):
        submissions[:] = [s for s in submissions if ensure_submission_id(s) != submission["id"]]
        save_submissions(submissions)
        st.success("Challenge deleted.")
        rerun_app()

    if is_editing:
        with st.expander("✏️ Change problem description", expanded=True):
            with st.form(f"edit_submission_form_{submission['id']}"):
                title = st.text_input("Challenge Title", value=submission.get("title", ""))
                description = st.text_area("Problem / Goal Description", value=submission.get("description", ""))
                product_features = st.text_area("Product Features", value=submission.get("product_features", ""))
                c1, c2, c3 = st.columns(3)
                category = c1.text_input("Department / Category", value=submission.get("category", ""))
                difficulty = c2.selectbox(
                    "Difficulty",
                    ["Easy", "Medium", "Hard", "Critical"],
                    index=["Easy", "Medium", "Hard", "Critical"].index(submission.get("difficulty", "Medium")) if submission.get("difficulty") in ["Easy", "Medium", "Hard", "Critical"] else 1,
                )
                impact_level = c3.selectbox(
                    "Impact",
                    ["Low", "Medium", "High", "Critical"],
                    index=["Low", "Medium", "High", "Critical"].index(submission.get("impact_level", "Medium")) if submission.get("impact_level") in ["Low", "Medium", "High", "Critical"] else 1,
                )
                task_type = st.multiselect(
                    "Task Type",
                    ["Repetitive", "Document-heavy", "Data-heavy", "Customer-facing", "Workflow", "Governance"],
                    default=submission.get("task_type", []),
                )
                tags = st.text_input("Tags (comma separated)", value=", ".join(submission.get("tags", [])))
                col_save, col_cancel = st.columns(2)
                save_edit = col_save.form_submit_button("Save changes", use_container_width=True)
                cancel_edit = col_cancel.form_submit_button("Cancel", use_container_width=True)
                if save_edit:
                    submission["title"] = title
                    submission["description"] = description
                    submission["product_features"] = product_features
                    submission["category"] = category
                    submission["difficulty"] = difficulty
                    submission["impact_level"] = impact_level
                    submission["task_type"] = task_type
                    submission["tags"] = comma_tags(tags)
                    save_submissions(submissions)
                    st.session_state.pop("editing_submission_id", None)
                    st.success("Challenge updated.")
                    rerun_app()
                if cancel_edit:
                    st.session_state.pop("editing_submission_id", None)
                    rerun_app()

    skill_query = build_skill_query(submission)
    if skill_query:
        if st.button("Find Rackers Who Can Help", key=f"find_rackers_{submission['id']}"):
            matches = HUMAN_STACK.search_people(skill_query)
            st.session_state["human_stack_matches_id"] = submission.get("id")
            st.session_state["human_stack_matches"] = matches
            rerun_app()

    with st.expander("🤖 AI Baseline"):
        baseline = submission.get("ai_baseline", {})
        st.json(baseline)

    with st.expander("💬 Discussion"):
        comments_thread = submission.get("comments_thread", [])
        if comments_thread:
            for comment in comments_thread:
                st.markdown(f"*{comment.get('author')}* — {comment.get('timestamp')}\n\n{comment.get('note')}")
        else:
            st.info("No comments yet.")
        author = st.text_input("Your name", key=f"comment_author_{submission['id']}")
        note = st.text_area("Add a comment", key=f"comment_note_{submission['id']}")
        if st.button("Submit Comment", key=f"submit_comment_{submission['id']}"):
            if note.strip():
                add_comment(submission, author, note)
                save_submissions(submissions)
                st.success("Comment added")
                rerun_app()
            else:
                st.warning("Please enter a comment before submitting.")

    # Inline add-solution form when this card is the active target
    if active_target and submission.get("title") and submission.get("title").strip().lower() == active_target.strip().lower():
        st.markdown("#### ➕ Add a Proposed Solution")
        sol_col1, sol_col2 = st.columns(2)
        author = sol_col1.text_input("Your Name", key=f"solution_author_{submission['id']}")
        difficulty = sol_col2.selectbox("Solution Difficulty", ["Easy", "Medium", "Hard", "Critical"], key=f"solution_diff_{submission['id']}")
        what_features = st.text_area("What (features)", key=f"solution_what_{submission['id']}")
        how_components = st.text_area("How (components / workflow)", key=f"solution_how_{submission['id']}")
        ai_tools_used = st.text_area("AI tools used", key=f"solution_tools_{submission['id']}")
        so_what_benefits = st.text_area("So what (benefits / impact)", key=f"solution_benefits_{submission['id']}")
        if st.button("Submit Solution", key=f"submit_solution_{submission['id']}", use_container_width=True):
            if not (author.strip() and what_features.strip()):
                st.error("Please add your name and at least the 'What (features)' section.")
            else:
                token = f"{int(datetime.utcnow().timestamp())}"
                approach_parts = [
                    f"• What: {what_features.strip()}",
                    f"• How: {how_components.strip()}" if how_components.strip() else "",
                    f"• AI tools: {ai_tools_used.strip()}" if ai_tools_used.strip() else "",
                    f"• So what: {so_what_benefits.strip()}" if so_what_benefits.strip() else "",
                ]
                approach = "\n".join(part for part in approach_parts if part)
                solutions.insert(
                    0,
                    {
                        "id": f"solution_{token}",
                        "challenge": submission.get("title"),
                        "author": author,
                        "approach": approach or what_features,
                        "difficulty": difficulty,
                        "what_features": what_features,
                        "how_components": how_components,
                        "ai_tools_used": ai_tools_used,
                        "so_what_benefits": so_what_benefits,
                        "upvotes": 0,
                        "comments": 0,
                        "status": "Draft",
                        "created_at": datetime.utcnow().isoformat(),
                    },
                )
                save_solutions(solutions)
                st.session_state["active_solution_target"] = None
                st.success("Solution submitted! 🧩")
                rerun_app()

    current_matches_id = st.session_state.get("human_stack_matches_id")
    current_matches = st.session_state.get("human_stack_matches", [])
    if current_matches_id == submission.get("id"):
        display_human_stack_matches(current_matches)


st.set_page_config(page_title="How Can AI Help? — YESAICAN LAB", page_icon="🔥", layout="wide")
st.markdown(
    """
    <div class="hero-title">🏠 YES AI CAN</div>
    <div class="hero-subtitle">the Place where Great peole help People become Happier , Greater, more Creative to help Other</div>
    <p class="hero-body-text">
        This is Rackspace’s internal, human-centered AI innovation ecosystem — a place where Rackers submit real problems,
        discover teammates, build solutions, and turn ideas into production-ready AI. Here, everyone can participate:
        technical or not. Every challenge becomes an opportunity. Every Racker becomes a creator.
    </p>
    """,
    unsafe_allow_html=True,
)
st.title("🔥 How Can AI Help? — Kaggle-Style Challenge Hub")
st.write("Crowdsource real-world problems, propose AI cures, and convert them into production projects.")

render_connection_panel()

submissions = load_submissions()
solutions = load_solutions()

# Submit a new challenge (moved to the top)
st.markdown("### 🧾 Submit a New Challenge")
with st.expander("Open challenge form", expanded=True):
    with st.form("challenge_form"):
        c1, c2, c3, c4 = st.columns(4)
        name = c1.text_input("Name")
        department = c2.text_input("Department / BU")
        region = c3.text_input("Region")
        role = c4.text_input("Role")
        title = st.text_input("Challenge Title")
        description = st.text_area("Problem / Goal Description (Markdown supported)")
        product_features = st.text_area("Product Features (Markdown supported)")
        attachments = st.file_uploader("Attachments", type=["csv", "pdf", "png", "jpg", "jpeg", "txt", "json"], accept_multiple_files=True)
        c5, c6, c7 = st.columns(3)
        category = c5.selectbox("Department", ["Executive Board", "Finance", "Customer Support", "Operations","Engineering","Sales", "Delivery", "Billing","HR", "Legal", "Marketing","Other"])
        difficulty = c6.selectbox("Difficulty", ["Easy", "Medium", "Hard", "Critical"])
        impact = c7.selectbox("Expected Impact", ["Low", "Medium", "High", "Critical"])
        task_type = st.multiselect("Task Type", ["Repetitive", "Document-heavy", "Data-heavy", "Customer-facing", "Workflow", "Governance"])
        tags = st.text_input("Tags (comma separated)")
        confidentiality = st.selectbox("Confidentiality", ["Public", "Internal", "Private-to-Team"])
        team_size = st.number_input("Team Size Needed", min_value=1, max_value=500, value=3)
        submitted = st.form_submit_button("Submit Challenge", use_container_width=True)
        if submitted:
            if not (name.strip() and title.strip() and description.strip()):
                st.error("Name, Title, and Description are required.")
            else:
                token = f"{int(datetime.utcnow().timestamp())}"
                stored_files = store_attachments(attachments, token)
                tag_list = comma_tags(tags)
                skills_needed = tag_list or [category, difficulty]
                similar_rackers = [
                    profile.get("name")
                    for profile in HUMAN_STACK.search_people(" ".join(skills_needed))
                ]
                similar_projects = [
                    project.get("title")
                    for project in HUMAN_STACK.search_projects(" ".join(skills_needed))
                ]
                new_entry = {
                    "id": f"challenge_{token}",
                    "title": title,
                    "description": description,
                    "product_features": product_features,
                    "submitter": {
                        "name": name,
                        "department": department,
                        "region": region,
                        "role": role,
                    },
                    "attachments": stored_files,
                    "category": category,
                    "difficulty": difficulty,
                    "impact_level": impact,
                    "task_type": task_type,
                    "tags": tag_list,
                    "skills_needed": skills_needed,
                    "confidentiality": confidentiality,
                    "team_size": team_size,
                    "upvotes": 0,
                    "comments": 0,
                    "urgency": 6.0,
                    "impact_score": 6.5,
                    "similar_agents": [],
                    "similar_rackers": similar_rackers,
                    "similar_projects": similar_projects,
                    "created_at": datetime.utcnow().isoformat(),
                }
                new_entry["ai_baseline"] = generate_ai_baseline(title, description, category, difficulty)
                submissions.insert(0, new_entry)
                save_submissions(submissions)
                st.success("Challenge submitted! 🎉")
                rerun_app()

query_params = _get_query_params()
challenge_param = query_params.get("challenge_id", [None])[-1]
challenge_title_param = query_params.get("challenge_title", [None])[-1]
solution_param = query_params.get("solution_id", [None])[-1]
solution_challenge_param = query_params.get("solution_challenge", [None])[-1]

st.subheader("➕ Add a Proposed Solution")
if not submissions:
    st.info("Add a challenge first, then propose a solution.")
else:
    challenge_titles = [sub.get("title", "Untitled") for sub in submissions]
    default_challenge = None
    # Prefer explicit solution_challenge param, fallback to challenge title param
    if solution_challenge_param and solution_challenge_param in challenge_titles:
        default_challenge = solution_challenge_param
    elif challenge_title_param and challenge_title_param in challenge_titles:
        default_challenge = challenge_title_param
    default_index = challenge_titles.index(default_challenge) if default_challenge in challenge_titles else 0

    with st.form("solution_proposal_form"):
        chosen_challenge = st.selectbox("Select a challenge to solve", challenge_titles, index=default_index)
        sol_col1, sol_col2 = st.columns(2)
        author = sol_col1.text_input("Your Name")
        difficulty = sol_col2.selectbox("Solution Difficulty", ["Easy", "Medium", "Hard", "Critical"])
        what_features = st.text_area("What (features)")
        how_components = st.text_area("How (components / workflow)")
        ai_tools_used = st.text_area("AI tools used")
        so_what_benefits = st.text_area("So what (benefits / impact)")
        submitted_solution = st.form_submit_button("Submit Solution Proposal", use_container_width=True)
        if submitted_solution:
            if not (author.strip() and what_features.strip() and chosen_challenge):
                st.error("Please provide your name, select a challenge, and describe the features.")
            else:
                token = f"{int(datetime.utcnow().timestamp())}"
                approach_parts = [
                    f"• What: {what_features.strip()}",
                    f"• How: {how_components.strip()}" if how_components.strip() else "",
                    f"• AI tools: {ai_tools_used.strip()}" if ai_tools_used.strip() else "",
                    f"• So what: {so_what_benefits.strip()}" if so_what_benefits.strip() else "",
                ]
                approach = "\n".join(part for part in approach_parts if part)
                matching_submission = next((sub for sub in submissions if sub.get("title") == chosen_challenge), {})
                submitter_name = (matching_submission.get("submitter") or {}).get("name") if matching_submission else ""
                solutions.insert(
                    0,
                    {
                        "id": f"solution_{token}",
                        "challenge": chosen_challenge,
                        "author": author,
                        "helper": author,
                        "submitter": submitter_name,
                        "approach": approach or what_features,
                        "difficulty": difficulty,
                        "what_features": what_features,
                        "how_components": how_components,
                        "ai_tools_used": ai_tools_used,
                        "so_what_benefits": so_what_benefits,
                        "upvotes": 0,
                        "comments": 0,
                        "status": "Draft",
                        "created_at": datetime.utcnow().isoformat(),
                    },
                )
                save_solutions(solutions)
                st.success("Solution submitted! 🧩")
                rerun_app()

submissions_changed = False
for submission in submissions:
    previous = submission.get("id")
    ensure_submission_id(submission)
    if submission.get("id") != previous:
        submissions_changed = True
if submissions_changed:
    save_submissions(submissions)

solutions_changed = False
for idea in solutions:
    previous = idea.get("id")
    ensure_solution_id(idea)
    if idea.get("id") != previous:
        solutions_changed = True
if solutions_changed:
    save_solutions(solutions)

selected_challenge = find_submission_by_identifier(submissions, challenge_param, challenge_title_param)
selected_solution = find_solution_by_identifier(solutions, solution_param, solution_challenge_param)

if selected_challenge:
    st.markdown("### 🔥 Challenge Spotlight")
    back_cols = st.columns([1, 4])
    if back_cols[0].button("← Back to Challenge Feed", key="back_challenge_detail"):
        clear_query_params("challenge_id", "challenge_title")
        rerun_app()
    render_submission_card(selected_challenge, submissions, solutions, st.session_state.get("active_solution_target"))
    st.divider()

if selected_solution:
    st.markdown("### 🧩 Idea Spotlight")
    back_cols = st.columns([1, 4])
    if back_cols[0].button("← Back to Solution Ideas", key="back_solution_detail"):
        clear_query_params("solution_id", "solution_challenge")
        rerun_app()
    render_solution_detail_card(selected_solution)
    st.markdown("#### Edit Solution")
    challenge_titles = [sub.get("title", "Untitled") for sub in submissions] or [selected_solution.get("challenge", "Untitled")]
    current_challenge = selected_solution.get("challenge")
    default_idx = challenge_titles.index(current_challenge) if current_challenge in challenge_titles else 0
    with st.form("edit_solution_form"):
        edited_challenge = st.selectbox("Challenge", challenge_titles, index=default_idx)
        edited_author = st.text_input("Author", value=selected_solution.get("author", ""))
        edited_helper = st.text_input("Helper", value=selected_solution.get("helper") or selected_solution.get("author", ""))
        edited_difficulty = st.selectbox(
            "Difficulty",
            ["Easy", "Medium", "Hard", "Critical"],
            index=["Easy", "Medium", "Hard", "Critical"].index(selected_solution.get("difficulty", "Medium")) if selected_solution.get("difficulty") in ["Easy", "Medium", "Hard", "Critical"] else 1,
        )
        edited_approach = st.text_area("Approach", value=selected_solution.get("approach", ""))
        edited_ai_tools = st.text_area("AI tools used", value=selected_solution.get("ai_tools_used", ""))
        edited_benefits = st.text_area("So what (benefits / impact)", value=selected_solution.get("so_what_benefits", ""))
        save_edit = st.form_submit_button("Save Solution", use_container_width=True)
        if save_edit:
            selected_solution["challenge"] = edited_challenge
            selected_solution["author"] = edited_author
            selected_solution["helper"] = edited_helper or edited_author
            selected_solution["difficulty"] = edited_difficulty
            selected_solution["approach"] = edited_approach
            selected_solution["ai_tools_used"] = edited_ai_tools
            selected_solution["so_what_benefits"] = edited_benefits
            selected_solution["submitter"] = selected_solution.get("submitter") or edited_author
            save_solutions(solutions)
            st.success("Solution updated.")
            rerun_app()
    st.divider()

render_leaderboard_and_blueprint(submissions)

st.subheader("Live Challenges")
selected_challenge_id = selected_challenge.get("id") if selected_challenge else None
if submissions:
    active_solution_target = st.session_state.get("active_solution_target")
    for submission in submissions:
        if selected_challenge_id and ensure_submission_id(submission) == selected_challenge_id:
            continue
        render_submission_card(submission, submissions, solutions, active_solution_target)
else:
    st.info("No submissions yet. Be the first to share a challenge!")

st.subheader("Solution Ideas")
if solutions:
    for idea in solutions:
        st.markdown(f"**{idea.get('challenge')}** — {idea.get('author')} ({idea.get('difficulty')})\n\n{idea.get('approach')}")
else:
    st.info("No solution cards yet.")
