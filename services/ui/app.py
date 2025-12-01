# YESAICAN LAB .. the place where problems meet solution , Painpoint meets Cure , People help people
# Main Application Entry Point

from __future__ import annotations
import base64
import html
import json
import mimetypes
import os
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Iterable, List, Optional
from urllib.parse import urlencode, urlparse

import streamlit as st

from services.ui.utils.meta_store import load_json as load_meta_json
from services.ui.utils.style import render_nav_bar_app
from services.ui.theme_manager import get_theme, set_theme
from typing import Dict, List, Any


os.environ.setdefault("STREAMLIT_TELEMETRY_DISABLED", "true")
os.environ.setdefault("STREAMLIT_BROWSER_GATHER_USAGE_STATS", "false")

BUILDERS_TOOLBOX = [
    {
        "name": "Chatbot_agent",
        "description": "Generic conversations, FAQs, onboarding, or support flows.",
    },
    {"name": "KYC agents", "description": "Identity verification workflows across regulated product launches."},
    {
        "name": "Agent builder",
        "description": "Rapid prototyping of new assistants with shared orchestration patterns.",
    },
    {
        "name": "hf faces",
        "description": "Leveraging Hugging Face models and datasets for search or summarization templates.",
    },
    {
        "name": "Persona chatbot",
        "description": "Role-based dialogs (e.g., mentor, coach, analyst) for future automation needs.",
    },
]

# Page configuration
st.set_page_config(
    page_title="Home | YESAICAN LAB",
    page_icon="🎉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Prepare the hard-coded title image asset that replaces the uploader flow.
TITLE_IMAGE_PATH = Path(__file__).parent / "assets" / "uploaded_logo.png"

def _load_title_image_data() -> tuple[str, str]:
    if not TITLE_IMAGE_PATH.exists():
        return "", "image/png"
    mime_type, _ = mimetypes.guess_type(TITLE_IMAGE_PATH)
    mime_type = mime_type or "image/png"
    with TITLE_IMAGE_PATH.open("rb") as fh:
        return base64.b64encode(fh.read()).decode(), mime_type

TITLE_IMAGE_BASE64, TITLE_IMAGE_MIME_TYPE = _load_title_image_data()

# Sync yes_theme with the shared theme manager so all toggles stay aligned
shared_theme = get_theme()
st.session_state["yes_theme"] = st.session_state.get("yes_theme", shared_theme)
if st.session_state["yes_theme"] != shared_theme:
    st.session_state["yes_theme"] = shared_theme
# Keep the page toggle state in sync with the active theme (nav toggle included)
desired_toggle_state = st.session_state["yes_theme"] == "dark"
if st.session_state.get("theme_toggle") != desired_toggle_state:
    st.session_state["theme_toggle"] = desired_toggle_state
# Keep theme in sync with the toggle state before rendering CSS
if "theme_toggle" in st.session_state:
    st.session_state["yes_theme"] = "dark" if st.session_state["theme_toggle"] else "light"
auth_user = st.session_state.get("auth_user")

# Hide Streamlit sidebar
st.markdown("""
    <style>
    [data-testid="stSidebar"],
    section[data-testid="stSidebar"],
    div[data-testid="stSidebarNav"],
    nav[data-testid="stSidebarNav"] {
        display: none !important;
        visibility: hidden !important;
    }
    [data-testid="stAppViewContainer"] {
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

LIGHT_CSS = """
    <style>
    html, body, .block-container, [data-testid="stAppViewContainer"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    .left-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        color: #0f172a;
        box-shadow: 6px 0 24px rgba(255, 0, 102, 0.1);
        border: 2px solid #ff0066;
        height: fit-content;
    }
    .right-box {
        background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: -6px 0 24px rgba(0, 212, 255, 0.1);
        border: 2px solid #00d4ff;
    }
    .nav-button {
        display: block;
        width: 100%;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #ff0066 0%, #ff3366 100%);
        color: white;
        text-decoration: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(255, 0, 102, 0.3);
        transition: all 0.3s;
        border: none;
        cursor: pointer;
    }
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(255, 0, 102, 0.4);
    }
    .nav-button-blue {
        background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.3);
    }
    .nav-button-blue:hover {
        box-shadow: 0 8px 24px rgba(0, 212, 255, 0.4);
    }
    .hero-wrapper {
        text-align: center;
        max-width: 1100px;
        margin: 0 auto 2rem;
        padding: 1rem 0;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 900;
        color: #ff0066;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 12px rgba(255, 0, 102, 0.2);
    }
    .hero-subtitle {
        font-size: 20px;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .hero-body-text {
        font-size: 18px;
        line-height: 1.8;
        color: #0f172a;
        margin-bottom: 1.5rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 2px solid #ff0066;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(255, 0, 102, 0.1);
        transition: all 0.3s;
    }
    .feature-card-blue {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 2px solid #00d4ff;
        box-shadow: 0 4px 12px rgba(0, 212, 255, 0.2);
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(255, 0, 102, 0.2);
    }
    .feature-title {
        font-size: 22px;
        font-weight: 700;
        color: #ff0066;
        margin-bottom: 0.8rem;
    }
    .feature-title-blue {
        color: #00d4ff;
    }
    .feature-text {
        font-size: 16px;
        line-height: 1.8;
        color: #0f172a;
    }
    .feature-text-white {
        color: #e2e8f0;
    }
    .stButton > button {
        border: none !important;
        cursor: pointer;
        padding: 14px 28px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        color: #fff !important;
        background: linear-gradient(135deg, #ff0066 0%, #ff3366 100%) !important;
        box-shadow: 0 8px 24px rgba(255, 0, 102, 0.35);
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        filter: brightness(1.1);
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(255, 0, 102, 0.45) !important;
    }
    ul.feature-list {
        list-style: none;
        padding-left: 0;
    }
    ul.feature-list li {
        padding: 0.5rem 0;
        font-size: 16px;
        line-height: 1.8;
        color: #334155;
    }
    ul.feature-list li:before {
        content: "✓ ";
        color: #ff0066;
        font-weight: 700;
        margin-right: 0.5rem;
    }
    ul.feature-list-white li {
        color: #e2e8f0;
    }
    ul.feature-list-white li:before {
        color: #00d4ff;
    }
    footer {
        text-align: center;
        padding: 2rem;
        color: #64748b;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 3rem;
        border-top: 2px solid #e2e8f0;
    }
    </style>
"""

DARK_CSS = """
    <style>
    html, body, .block-container, [data-testid="stAppViewContainer"] {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
    }
    .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    .left-box {
        background: radial-gradient(circle at top left, #0f172a, #1e293b);
        border-radius: 20px;
        padding: 3rem 2rem;
        color: #f1f5f9;
        box-shadow: 6px 0 24px rgba(0,0,0,0.45);
        border: 2px solid #1e293b;
    }
    .right-box {
        background: linear-gradient(180deg, #1e293b, #0f172a);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: -6px 0 24px rgba(0,0,0,0.35);
        border: 2px solid #1e293b;
    }
    .nav-button {
        display: block;
        width: 100%;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        text-decoration: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 16px;
        text-align: center;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.6);
        transition: all 0.3s;
        border: none;
        cursor: pointer;
    }
    .nav-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.5);
    }
    .nav-button-blue {
        background: linear-gradient(135deg, #06b6d4 0%, #0ea5e9 100%);
        box-shadow: 0 6px 18px rgba(8,145,178,0.5);
    }
    .nav-button-blue:hover {
        box-shadow: 0 12px 28px rgba(14, 165, 233, 0.5);
    }
    .hero-wrapper {
        text-align: center;
        max-width: 1100px;
        margin: 0 auto 2rem;
        padding: 1rem 0;
    }
    .hero-title {
        font-size: 42px;
        font-weight: 900;
        color: #f0f9ff;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 18px rgba(59,130,246,0.6);
    }
    .hero-subtitle {
        font-size: 20px;
        font-weight: 600;
        color: #93c5fd;
        margin-bottom: 1.5rem;
    }
    .hero-body-text {
        font-size: 18px;
        line-height: 1.8;
        color: #e2e8f0;
        margin-bottom: 1.5rem;
    }
    .feature-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.3);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.35);
        transition: all 0.3s;
    }
    .feature-card-blue {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid rgba(14, 165, 233, 0.4);
        box-shadow: 0 8px 24px rgba(14,165,233,0.3);
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 32px rgba(0,0,0,0.45);
    }
    .feature-title {
        font-size: 22px;
        font-weight: 700;
        color: #f0abfc;
        margin-bottom: 0.8rem;
    }
    .feature-title-blue {
        color: #67e8f9;
    }
    .feature-text {
        font-size: 16px;
        line-height: 1.8;
        color: #e2e8f0;
    }
    .feature-text-white {
        color: #e2e8f0;
    }
    .stButton > button {
        border: none !important;
        cursor: pointer;
        padding: 14px 28px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border-radius: 14px !important;
        color: #fff !important;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        box-shadow: 0 12px 32px rgba(37, 99, 235, 0.45);
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        filter: brightness(1.05);
        transform: translateY(-2px);
        box-shadow: 0 16px 36px rgba(37, 99, 235, 0.55) !important;
    }
    ul.feature-list {
        list-style: none;
        padding-left: 0;
    }
    ul.feature-list li {
        padding: 0.5rem 0;
        font-size: 16px;
        line-height: 1.8;
        color: #cbd5f5;
    }
    ul.feature-list li:before {
        content: "✓ ";
        color: #38bdf8;
        font-weight: 700;
        margin-right: 0.5rem;
    }
    ul.feature-list-white li {
        color: #cbd5f5;
    }
    ul.feature-list-white li:before {
        color: #38bdf8;
    }
    footer {
        text-align: center;
        padding: 2rem;
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 3rem;
        border-top: 1px solid rgba(148,163,184,0.2);
    }
    </style>
"""


PAGES_DIR = Path(__file__).parent / "pages"
LAUNCH_PORT = os.getenv("LAUNCH_PORT") or "8502"
ACRONYM_TOKENS = {
    "ai",
    "ml",
    "hf",
    "kyc",
    "aml",
    "cio",
    "cto",
    "ceo",
    "cfo",
    "ce",
    "api",
    "ops",
    "llm",
    "rex",
    "ui",
    "ux",
    "crm",
    "ev",
}


def _normalize_launch_base(raw_value: Optional[str]) -> str:
    fallback = f"http://localhost:{LAUNCH_PORT}"
    candidate = (raw_value or "").strip()
    if not candidate:
        return fallback
    if not re.match(r"^https?://", candidate):
        candidate = f"http://{candidate}"
    candidate = candidate.rstrip("/")
    parsed = urlparse(candidate)
    if parsed.scheme and parsed.netloc:
        host = f"{parsed.scheme}://{parsed.netloc}"
        if parsed.port is None and LAUNCH_PORT:
            host = f"{host}:{LAUNCH_PORT}"
        return host
    return fallback


def _slugify_page_stem(stem: str) -> str:
    tokens = [token for token in re.split(r"[_\s]+", stem) if token]
    if not tokens:
        return f"/{stem.lower()}"
    normalized: list[str] = []
    for token in tokens:
        lower = token.lower()
        if lower in ACRONYM_TOKENS:
            normalized.append(lower)
        else:
            normalized.append(lower)
    return f"/{'_'.join(normalized)}"


def load_page_slugs(pages_dir: Path) -> dict[str, str]:
    slugs: dict[str, str] = {}
    if not pages_dir.exists():
        return slugs
    for entry in pages_dir.iterdir():
        if not entry.is_file() or entry.suffix != ".py":
            continue
        if entry.name.startswith("_") or ".ok" in entry.name or entry.name.endswith(".bak"):
            continue
        slugs[entry.stem] = _slugify_page_stem(entry.stem)
    return slugs


LAUNCH_BASE_URL = _normalize_launch_base(
    os.getenv("LAUNCH_BASE_URL") or os.getenv("LAUNCH_HOST") or "http://119.9.127.11:8054/"
)
CHALLENGE_FORM_BASE_URL = os.getenv(
    "HOW_CAN_AI_HELP_FORM_BASE",
    "http://119.9.127.11:8054/how_can_ai_help",
)
PAGE_SLUGS = load_page_slugs(PAGES_DIR)

# PAGE_PLACEHOLDER_TEMPLATE = """import streamlit as st
# from services.ui.utils.style import render_nav_bar_app

# st.set_page_config(
#     page_title="{page_title}",
#     page_icon="🗂️",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# render_nav_bar_app(show_nav_buttons=False)

# # --- Glowing Neon YES AI CAN Community Sign ---
# st.markdown("""
# <style>
# .neon-sign {
#     margin: 40px auto 20px auto;
#     padding: 25px 35px;
#     width: 95%;
#     max-width: 1800px;
#     text-align: center;
#     font-family: 'Arial Black', sans-serif;
#     font-size: 42px;
#     line-height: 1.3;
#     color: #ffffff;
#     border: 4px solid #ff0066;
#     border-radius: 25px;

#     background: rgba(10, 10, 30, 0.85);

#     /* NEON OUTLINE */
#     box-shadow:
#         0 0 8px #ff0066,
#         0 0 15px #ff0033,
#         0 0 25px #0066ff,
#         0 0 45px rgba(0,102,255,0.7),
#         inset 0 0 15px rgba(255,255,255,0.2);

#     /* GLOW ANIMATION */
#     animation: neonGlow 2.6s infinite alternate;
# }

# @keyframes neonGlow {
#     0% {
#         box-shadow:
#             0 0 6px #ff0066,
#             0 0 12px #ff0033,
#             0 0 20px #0066ff,
#             0 0 35px rgba(0,102,255,0.6),
#             inset 0 0 10px rgba(255,255,255,0.15);
#     }
#     100% {
#         box-shadow:
#             0 0 12px #ff99cc,
#             0 0 28px #ff0066,
#             0 0 45px #0099ff,
#             0 0 65px rgba(0,153,255,0.85),
#             inset 0 0 18px rgba(255,255,255,0.35);
#     }
# }
# </style>

# <div class="neon-sign">
# 🏠 The YES AI CAN Community LAB <br>
# <span style="font-size:26px; font-weight:normal;">
# The Community Place where Great People help other People be more Productive, Creative, Better and Happier — while helping Others bring their Ideas to Life.
# </span>
# </div>
# """, unsafe_allow_html=True)


# <div class="neon-sign">
# 🏠 The YES AI CAN Community LAB <br>
# <span style="font-size:26px; font-weight:normal;">
# The Community Place where Great People help other People be more Productive, Creative, Better and Happier — while helping Others bring their Ideas to Life.
# </span>
# </div>
# """, unsafe_allow_html=True)


# st.title("{page_title}")
# st.info("This placeholder page was auto-created. Update `{file_path}` with real content.")
# """
# ... (Lines 468-518: setup functions) ...

PAGE_PLACEHOLDER_TEMPLATE = '''import streamlit as st
from services.ui.utils.style import render_nav_bar_app

st.set_page_config(
    page_title="{page_title}",
    page_icon="🗂️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

render_nav_bar_app(show_nav_buttons=False)

# --- Placeholder content for auto-generated pages ---
st.title("{page_title}")
st.info("This placeholder page was auto-created. Update `{file_path}` with real content.")
'''

def _resolve_page_path(page_path: str) -> Path:
    path_obj = Path(page_path)
    if not path_obj.is_absolute():
        path_obj = Path(__file__).parent / path_obj
    return path_obj


def ensure_page_file(page_path: str, title: str | None = None) -> Path | None:
    """Create a placeholder Streamlit page when a referenced page does not exist."""
    if not page_path or not page_path.endswith(".py"):
        return None
    target_path = _resolve_page_path(page_path)
    if target_path.exists():
        return target_path
    target_path.parent.mkdir(parents=True, exist_ok=True)
    page_title = title or target_path.stem.replace("_", " ").title()
    try:
        relative_path = target_path.relative_to(Path(__file__).parent)
    except ValueError:
        relative_path = target_path.name
    target_path.write_text(
        PAGE_PLACEHOLDER_TEMPLATE.format(
            page_title=page_title,
            file_path=relative_path,
        ),
        encoding="utf-8",
    )
    PAGE_SLUGS[target_path.stem] = _slugify_page_stem(target_path.stem)
    return target_path


def ensure_page_file_for_key(page_key: str) -> None:
    if not page_key:
        return
    candidate = f"pages/{page_key}.py"
    ensure_page_file(candidate)

def render_theme_styles():
    css = DARK_CSS if st.session_state.get("yes_theme", "dark") == "dark" else LIGHT_CSS
    st.markdown(css, unsafe_allow_html=True)

# Call the theme renderer (keep this line outside the function definition)
render_theme_styles()

# --- Full-Width Title Image ---
st.markdown("""
<style>
.fullwidth-title-wrap {
    position: relative;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding-top: 16px;
    margin: 0 auto 10px;
}

.fullwidth-title {
    width: clamp(270px, 30vw, 900px);
    max-width: 1000px;
    border-radius: 32px;
    box-shadow:
        0 0 25px rgba(0, 200, 255, 0.75),
        0 0 55px rgba(255, 0, 200, 0.55);
    display: block;
    margin: 0 auto;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="fullwidth-title-wrap">', unsafe_allow_html=True)

if TITLE_IMAGE_BASE64:
    st.markdown(
        f'<img src="data:{TITLE_IMAGE_MIME_TYPE};base64,{TITLE_IMAGE_BASE64}" class="fullwidth-title">',
        unsafe_allow_html=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

# Title logo upload controls
st.session_state.setdefault("show_title_logo_uploader", False)
upload_col, upload_info_col = st.columns([1, 3])
with upload_col:
    if st.button("📤 Upload new title logo", key="upload_title_logo_btn"):
        st.session_state["show_title_logo_uploader"] = True
with upload_info_col:
    st.caption(
        "Update the hero image that shows above by uploading a PNG / JPG / WEBP / SVG file."
    )

if st.session_state["show_title_logo_uploader"]:
    uploaded_title_logo = st.file_uploader(
        "Choose a title logo image",
        type=["png", "jpg", "jpeg", "webp", "svg"],
        key="title_logo_upload_input",
        help="This image replaces the hero logo across the app.",
    )
    if uploaded_title_logo:
        TITLE_IMAGE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TITLE_IMAGE_PATH, "wb") as handle:
            handle.write(uploaded_title_logo.getbuffer())
        st.success("✅ Title logo saved. Refreshing the page…")
        st.session_state["show_title_logo_uploader"] = False
        st.rerun()

# def render_theme_styles():
#     css = DARK_CSS if st.session_state.get("yes_theme", "dark") == "dark" else LIGHT_CSS
#     st.markdown(css, unsafe_allow_html=True)

# # Call the theme renderer (keep this line outside the function definition)
# render_theme_styles()

# # --- Realistic Tube Neon Sign (Version D) ---
# st.markdown("""
# <style>

# /* Outer neon frame */
# .neon-container {
#     margin: 55px auto 50px auto;
#     padding: 70px 80px;
#     width: 95%;
#     max-width: 1500px;
#     text-align: center;
#     background: rgba(4, 8, 20, 0.90);
#     border-radius: 45px;
#     border: 10px solid #00bfff;
#     box-shadow:
#         0 0 20px #00bfff,
#         0 0 40px #00e1ff,
#         0 0 80px rgba(0,200,255,0.95),
#         0 0 140px rgba(0,200,255,0.75),
#         inset 0 0 20px rgba(0,200,255,0.25);
#     position: relative;
# }

# /* Inner glowing pink frame */
# .neon-container:before {
#     content: "";
#     position: absolute;
#     top: 22px; left: 22px; right: 22px; bottom: 22px;
#     border: 7px solid #ff008c;
#     border-radius: 30px;
#     box-shadow:
#         0 0 12px #ff40b5,
#         0 0 25px #ff008c,
#         0 0 60px rgba(255,0,153,0.9),
#         inset 0 0 25px rgba(255,255,255,0.25);
# }

# /* Title */
# .neon-title {
#     font-size: 82px;
#     font-weight: 900;
#     color: white;
#     text-shadow:
#         0 0 6px #fff,
#         0 0 14px #66d9ff,
#         0 0 28px #00bfff,
#         0 0 55px #0099ff;
#     position: relative;
# }

# .neon-title .home-icon {
#     filter: drop-shadow(0 0 5px #00e1ff)
#             drop-shadow(0 0 15px #00e1ff);
# }

# /* Subtitle */
# .neon-subtitle {
#     font-size: 68px;
#     font-weight: 900;
#     color: #b5eaff;
#     position: relative; /* REQUIRED */
#     text-shadow:
#         0 0 8px #b5eaff,
#         0 0 18px #66d9ff,
#         0 0 32px #33ccff,
#         0 0 55px #00bfff;
# }

# /* Tagline */
# .neon-tagline {
#     font-size: 34px;
#     font-weight: 700;
#     color: #ffbbff;
#     text-shadow:
#         0 0 6px #ff99ff,
#         0 0 14px #ff66ff;
# }

# /* Description */
# .neon-description {
#     font-size: 30px;
#     color: white;
#     line-height: 1.45;
#     text-shadow:
#         0 0 5px #ff66cc,
#         0 0 12px #ff0099;
# }

# </style>

# <div class="neon-container">

#     <div class="neon-title">
#         <span class="home-icon">🏠</span> The YES AI CAN Community LAB
#     </div>

#     <div class="neon-tagline">
#         The place where problems meet solution — Painpoint meets Cure — People help People
#     </div>

#     <div class="neon-description">
#         The Community Place where Great People help other People be more<br>
#         Productive–Creative, Better and Happier — while helping Others bring<br>
#         their Ideas to Life.
#     </div>

# </div>

# """, unsafe_allow_html=True)



BASE_CSS = """
<style>
.quick-access-card {
    margin-top: 1rem;
    margin-bottom: 1.5rem;
    padding: 25px 24px;
    border-radius: 20px;
    border: 1px solid rgba(56,189,248,0.45);
    background: rgba(15,23,42,0.85);
    box-shadow: 0 18px 42px rgba(15,23,42,0.35);
}
.quick-access-card.light {
    background: rgba(248,250,252,0.95);
    border-color: rgba(14,165,233,0.35);
}
.quick-access-card h3 {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 0.35rem;
    color: #f472b6;
}
.quick-access-card p {
    color: rgba(226,232,240,0.85);
    margin-bottom: 1rem;
}
.quick-access-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
    margin-top: 0.5rem;
}
@media (max-width: 768px) {
    .quick-access-grid {
        grid-template-columns: 1fr;
    }
}
.quick-access-card .stButton>button {
    width: 100%;
    border: none;
    border-radius: 16px;
    padding: 0.95rem 1rem;
    font-weight: 700;
    font-size: 1rem;
    color: #fff;
    background: linear-gradient(135deg, #ff1b6b, #45caff);
    box-shadow: 0 18px 35px rgba(255,27,107,0.35);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.quick-access-card .stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 22px 45px rgba(69,202,255,0.35);
}
.neon-divider {
    width: 100%;
    height: 2px;
    margin: 1.75rem 0 1.5rem;
    background: linear-gradient(90deg, rgba(15,23,42,0), rgba(56,189,248,0.85), rgba(15,23,42,0));
    box-shadow: 0 0 20px rgba(56,189,248,0.5);
}
.nav-center-wrapper {
    margin-top: 0.5rem;
    border-radius: 22px;
    border: 1px solid rgba(56,189,248,0.35);
    padding: 1.75rem;
    background: linear-gradient(135deg, rgba(2,6,23,0.95), rgba(15,23,42,0.9));
    box-shadow: 0 25px 60px rgba(14,165,233,0.15);
}
.nav-center-wrapper.light {
    background: linear-gradient(135deg, rgba(248,250,252,0.95), rgba(226,232,240,0.95));
    border-color: rgba(14,165,233,0.45);
    box-shadow: 0 20px 50px rgba(15,23,42,0.15);
}
.nav-center-header {
    text-align: center;
    margin-bottom: 1.25rem;
}
.nav-center-header h2 {
    font-size: 32px;
    font-weight: 800;
    color: #00d4ff;
    margin-bottom: 0.3rem;
}
.nav-center-header p {
    color: rgba(226,232,240,0.85);
    margin: 0;
}
.nav-center-wrapper.light .nav-center-header h2 {
    color: #0f172a;
}
.nav-center-wrapper.light .nav-center-header p {
    color: #475569;
}
.nav-command-grid {
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}
.nav-mini-block {
    border-radius: 16px;
    padding: 0.25rem;
    background: rgba(15,23,42,0.4);
    box-shadow: inset 0 0 15px rgba(14,165,233,0.12);
}
.nav-center-wrapper.light .nav-mini-block {
    background: rgba(248,250,252,0.8);
}
.nav-mini-block .stButton>button {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(248,113,143,0.65);
    background: linear-gradient(135deg, #ff0a8a, #ff4d4d);
    color: #fff;
    font-weight: 700;
    font-size: 1.05rem;
    padding: 0.85rem 1rem;
    box-shadow: 0 18px 36px rgba(255,77,109,0.4);
    transition: all 0.2s ease;
}
.nav-mini-block .stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 25px 45px rgba(255,77,109,0.45);
}
.nav-mini-desc {
    margin-top: 0.35rem;
    font-size: 0.9rem;
    color: rgba(226,232,240,0.8);
}
.nav-center-wrapper.light .nav-mini-desc {
    color: #475569;
}
.nav-bottom-grid {
    margin-top: 2.5rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.25rem;
}
.challenge-form-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}
.challenge-form-card {
    border: 1px solid rgba(59,130,246,0.35);
    border-radius: 18px;
    padding: 1.25rem;
    background: rgba(15,23,42,0.85);
    box-shadow: 0 18px 36px rgba(15,23,42,0.35);
}
.challenge-form-card.light {
    background: #ffffff;
    border-color: rgba(59,130,246,0.25);
    box-shadow: 0 10px 24px rgba(15,23,42,0.15);
}
.challenge-form-card h4 {
    margin-bottom: 0.35rem;
    color: #f472b6;
}
.challenge-form-meta {
    font-size: 0.9rem;
    color: rgba(148,163,184,0.9);
    margin-bottom: 0.5rem;
}
.challenge-form-card.light .challenge-form-meta {
    color: #475569;
}
.challenge-attachment-list {
    list-style: none;
    padding-left: 0;
    margin-bottom: 0.5rem;
}
.challenge-attachment-list li {
    font-size: 0.83rem;
    color: rgba(148,163,184,0.9);
}
.challenge-form-card.light .challenge-attachment-list li {
    color: #475569;
}
.challenge-form-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 0.75rem;
}
.challenge-form-actions a {
    flex: 1;
    text-align: center;
    padding: 0.55rem 0.75rem;
    border-radius: 10px;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
}
.challenge-form-actions .primary {
    background: linear-gradient(135deg, #f43f5e, #ec4899);
    color: white;
}
.challenge-form-actions .secondary {
    background: rgba(59,130,246,0.18);
    color: #93c5fd;
}
.challenge-form-card.light .challenge-form-actions .secondary {
    background: rgba(59,130,246,0.08);
    color: #2563eb;
}
.nav-bottom-card {
    border: 1px solid rgba(148,163,184,0.25);
    border-radius: 16px;
    padding: 1.25rem;
    background: rgba(15,23,42,0.7);
    color: rgba(226,232,240,0.85);
    box-shadow: inset 0 0 14px rgba(148,163,184,0.2);
}
.nav-bottom-card h4 {
    margin-bottom: 0.4rem;
}
.nav-bottom-card .project-entry {
    margin-top: 0.75rem;
    padding-top: 0.65rem;
    border-top: 1px solid rgba(148,163,184,0.3);
}
.nav-bottom-card .project-entry strong {
    display: block;
    font-size: 1rem;
    color: #fcd34d;
    margin-bottom: 0.2rem;
}
.nav-bottom-card .project-meta {
    font-size: 0.9rem;
    color: rgba(226,232,240,0.8);
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-bottom: 0.35rem;
}
.nav-bottom-card .project-score {
    font-weight: 700;
    color: #34d399;
}
.nav-bottom-card .project-scores {
    display: flex;
    gap: 0.65rem;
    font-size: 0.9rem;
    color: rgba(148,163,184,0.9);
}
.nav-bottom-card .builder-list {
    padding-left: 1.1rem;
    margin: 0.35rem 0 0;
    color: rgba(226,232,240,0.85);
}
.nav-bottom-card .builder-list li {
    margin-bottom: 0.25rem;
    font-size: 0.95rem;
}
.nav-bottom-card .chip-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    margin-top: 0.65rem;
}
.nav-bottom-card .search-chip {
    background: rgba(59,130,246,0.2);
    color: #bfdbfe;
    border-radius: 999px;
    padding: 0.2rem 0.8rem;
    font-size: 0.85rem;
}
.nav-bottom-card .search-footer {
    margin-top: 0.75rem;
    font-size: 0.85rem;
    color: rgba(148,163,184,0.9);
}
.neon-table {
    margin-top: 1.2rem;
    border-radius: 18px;
    border: 1px solid rgba(14,165,233,0.45);
    background: rgba(5,13,26,0.95);
    box-shadow: 0 25px 60px rgba(14,165,233,0.15), inset 0 0 25px rgba(14,165,233,0.1);
    padding: 1.25rem 1.5rem;
    animation: fadeInNeon 0.45s ease;
}
.neon-table.light {
    background: rgba(248,250,252,0.95);
    border-color: rgba(14,165,233,0.4);
    box-shadow: 0 20px 50px rgba(15,23,42,0.15);
}
.neon-table-title {
    font-size: 1.15rem;
    font-weight: 700;
    color: #7dd3fc;
    margin-bottom: 0.75rem;
    letter-spacing: 0.5px;
}
.neon-table.light .neon-table-title {
    color: #2563eb;
}
.neon-table-grid {
    display: grid;
    gap: 0;
    align-items: stretch;
}
.neon-table-header {
    background: linear-gradient(90deg, rgba(14,165,233,0.8), rgba(59,130,246,0.8));
    color: #f8fafc;
    border-radius: 12px;
    margin-bottom: 0.65rem;
    box-shadow: 0 10px 30px rgba(14,165,233,0.35);
}
.neon-table-cell {
    padding: 0.75rem 0.65rem;
    font-size: 0.95rem;
    color: rgba(226,232,240,0.95);
    border-right: 1px solid rgba(15,23,42,0.4);
    word-break: break-word;
    min-height: 52px;
    display: flex;
    align-items: center;
}
.neon-table-cell:last-child {
    border-right: none;
}
.neon-table.light .neon-table-cell {
    color: #0f172a;
    border-right: 1px solid rgba(148,163,184,0.35);
}
.neon-table-row {
    background: rgba(15,23,42,0.75);
    border-radius: 12px;
    margin-bottom: 0.5rem;
    border: 1px solid rgba(59,130,246,0.25);
    box-shadow: 0 15px 30px rgba(2,6,23,0.45);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.neon-table-row:hover {
    transform: translateY(-2px);
    box-shadow: 0 18px 35px rgba(59,130,246,0.35);
    border-color: rgba(14,165,233,0.6);
}
.neon-table.light .neon-table-row {
    background: rgba(248,250,252,0.9);
    border-color: rgba(148,163,184,0.35);
}
.neon-table-action {
    display: inline-block;
    padding: 0.45rem 1.1rem;
    border-radius: 999px;
    background: linear-gradient(135deg, #ff0a8a, #ff4d4d);
    color: #fff;
    font-weight: 700;
    text-decoration: none;
    font-size: 0.9rem;
    box-shadow: 0 10px 24px rgba(255,77,109,0.4);
}
.neon-action-secondary {
    display: inline-block;
    margin-top: 0.25rem;
    font-size: 0.85rem;
    color: rgba(148,163,184,0.9);
    text-decoration: none;
}
.neon-table.light .neon-action-secondary {
    color: #475569;
}
.action-stack {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.2rem;
}
.table-tag {
    display: inline-block;
    padding: 0.15rem 0.65rem;
    border-radius: 999px;
    font-size: 0.78rem;
    margin-right: 0.3rem;
    margin-bottom: 0.3rem;
    background: rgba(14,165,233,0.15);
    color: #bae6fd;
}
.neon-table.light .table-tag {
    background: rgba(14,165,233,0.15);
    color: #0369a1;
}
.status-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.2rem 0.75rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #f8fafc;
    background: rgba(59,130,246,0.35);
    border: 1px solid rgba(59,130,246,0.8);
}
.status-badge.success {
    background: rgba(34,197,94,0.35);
    border-color: rgba(34,197,94,0.8);
}
.status-badge.warning {
    background: rgba(250,204,21,0.3);
    border-color: rgba(250,204,21,0.8);
    color: #1f2937;
}
.status-badge.danger {
    background: rgba(248,113,113,0.3);
    border-color: rgba(248,113,113,0.8);
}
.status-badge.info {
    background: rgba(6,182,212,0.35);
    border-color: rgba(6,182,212,0.8);
}
.neon-table-empty {
    padding: 1rem;
    text-align: center;
    color: rgba(226,232,240,0.7);
    font-style: italic;
}
.neon-table.light .neon-table-empty {
    color: #475569;
}
@keyframes fadeInNeon {
    from {
        opacity: 0;
        transform: translateY(6px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
"""

st.markdown(BASE_CSS, unsafe_allow_html=True)
# Home page should not display nav buttons
render_nav_bar_app(show_nav_buttons=False)


def go_to_page(page_path: str) -> None:
    """Navigate to another app page safely."""
    if page_path.endswith(".py"):
        ensure_page_file(page_path)
    try:
        st.switch_page(page_path)
    except Exception as exc:
        st.warning(f"Unable to open {page_path}: {exc}")


def render_section_link(description: str, page: str, button_label: str) -> None:
    st.markdown(f"<p class='nav-section-description'>{description}</p>", unsafe_allow_html=True)
    if st.button(button_label, key=f"nav_btn_{button_label}"):
        go_to_page(page)


def render_quick_access(auth_user: dict | None, origin: str = "default") -> None:
    card_class = "quick-access-card"
    if st.session_state.get("yes_theme", "dark") != "dark":
        card_class += " light"
    st.markdown(f"<div class='{card_class}'>", unsafe_allow_html=True)
    st.markdown("<h3>⚡ Quick Access</h3><p>Primary launchpad for profiles, challenges, solutions, and global search.</p>", unsafe_allow_html=True)
    if auth_user:
        st.success("✅ You're logged in — jump into **Login / My Space** to manage your projects.")
    else:
        st.info("🔐 Already registered? Head to **Login / My Space** to access your personal dashboard.")
        if st.button(
            "Go to Login / My Space",
            key=f"qa_login_button_{origin}",
            use_container_width=True,
        ):
            go_to_page("pages/login_portal.py")
    actions = [
        ("👤 Create Profile", "pages/human_stack.py"),
        ("🧱 Submit a Challenge", "pages/how_can_ai_help.py"),
        ("💡 Propose a Solution", "pages/solution_submit.py"),
        ("🔍 Search All", "pages/search.py"),
    ]
    rows = [actions[i : i + 2] for i in range(0, len(actions), 2)]
    for idx, row in enumerate(rows):
        cols = st.columns(2)
        for col, (label, path) in zip(cols, row):
            with col:
                if st.button(label, key=f"qa_{origin}_{label}_{idx}_{path}", use_container_width=True):
                    go_to_page(path)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)


def render_login_cta(auth_user: dict | None) -> None:
    message = (
        f"Logged in as **{auth_user.get('name', auth_user.get('email'))}**. Head into the submission workspace to add your challenge."
        if auth_user
        else "Register or log in to submit your challenge and track solutions."
    )
    st.markdown(f"✅ {message}")


def render_help_intro() -> None:
    st.markdown(
        """
        <div class="neon-table" style="margin-bottom:1.5rem;">
            <div class="neon-table-title" style="font-size:1.4rem;">
                🔥 1- Submit your painpoints or ideas to improve your tasks 
                    2- Find Great people and Team who will build FOR and WITH You a Solution that will put a Smile on your Face  
                    3- and if it s a great solution , We will share it in the Production Library for US and for our Customers- By putting all our ideas and talents Together , We all Build a  better Services , a Better Company Culture and Business, get More Happier Customers and Build a Better World !
            </div>
            <p style="color:rgba(226,232,240,0.9);">
                Share real customer or team pain points, let Ambassadors propose AI cures, and convert the best submissions into Customer ONE projects.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_primary_navigation_buttons() -> None:
    st.markdown("### 🔗 Page Shortcuts")
    nav_items = [
        ("👤 Human Stack", "pages/human_stack.py", "See every profile, skill, and SME."),
        ("📁 Project Hub", "pages/project_hub.py", "Review prototypes and MVPs."),
        ("🧩 Challenge Hub", "pages/challenge_hub.py", "Submit challenges, upload attachments, and track signals."),
        ("🤝 Submit Solution", "pages/solution_submit.py", "Select a challenge and add your AI blueprint."),
        ("🤖 Production Ready Agent Library", "pages/agent_library.py", "From Customer ZERO to Customer One agents."),
        ("🧠 Ontology & Patterns", "pages/ontology_patterns.py", "Reusable logic + frameworks."),
        ("📚 Docs & Learning", "pages/documentation_learning.py", "Guides, tutorials, learning paths."),
        ("🌍 Community & Ambassadors", "pages/community_ambassadors.py", "Badges, cohorts, contributors."),
        ("⚙️ Admin & REX 2.0", "pages/admin_rex.py", "Ops telemetry and exports."),
        ("🔍 Global Search", "pages/search.py", "Unified search across everything."),
        ("🔥 AI Can Help", "pages/how_can_ai_help.py", "Submit or solve real challenges."),
    ]
    for label, path, desc in nav_items:
        if st.button(label, key=f"primary_nav_{label}"):
            go_to_page(path)
        st.caption(desc)


def render_form_navigation_buttons() -> None:
    st.markdown("### 🧭 Jump into Forms & Workspaces")
    actions = [
        ("🔥 Submit a Challenge", "pages/how_can_ai_help.py", "Share a workflow or customer pain point in the AI Can Help intake form."),
        ("🧩 Add Proposed Solution", "pages/how_can_ai_help.py", "Scroll to the solution form to capture your AI approach."),
        ("🧱 Submit a Project", "pages/project_hub.py", "Publish prototypes, MVPs, and Customer ONE builds."),
        ("🚀 Convert to Project", "pages/project_hub.py", "Open Project Hub to transform approved challenges into projects."),
        ("👤 Create / Update Profile", "pages/human_stack.py", "Maintain your Human Stack card so teammates can find you."),
        ("🤖 Add or Launch Agent", "pages/agent_library.py", "Register agent builds or launch production-ready copilots."),
        ("🔐 Login / My Space", "pages/login_portal.py", "Access your saved submissions and private workspace."),
    ]
    for idx in range(0, len(actions), 2):
        row = actions[idx : idx + 2]
        cols = st.columns(len(row))
        for col, (label, page, desc) in zip(cols, row):
            with col:
                if st.button(label, key=f"form_nav_{slugify_label(label)}", use_container_width=True):
                    go_to_page(page)
                st.caption(desc)


SAMPLE_HELP_SUBMISSIONS = [
    {
        "title": "Sync RAX billing with customer billing format",
        "submitter": {
            "name": "Jon",
            "department": "Billing",
            "region": "APAC",
            "role": "Billing Ops",
        },
        "description": "Need a formatter that aligns any customer-specific billing layout to the Rackspace billing schema automatically.",
        "attachments": [],
        "category": "Finance",
        "difficulty": "Easy",
        "impact": "Medium",
        "task_type": ["Automation"],
        "confidentiality": "Internal",
        "upvotes": 0,
        "comments": 0,
        "urgency": 6.0,
        "impact_score": 6.5,
        "similar_agents": ["Credit Appraisal Agent"],
        "preferred_action": "both",
    },
    {
        "title": "Automate Monthly Billing Reconciliation",
        "submitter": {
            "name": "Jordan Lee",
            "department": "Finance Ops",
            "region": "AMER",
            "role": "Billing Analyst",
        },
        "description": "Manual spreadsheet matching for 12 regions. Need AI to reconcile invoices vs. ERP exports.",
        "attachments": ["billing_rules.pdf", "ledger.csv"],
        "category": "Finance",
        "difficulty": "Medium",
        "impact": "High",
        "task_type": ["Repetitive", "Document-heavy"],
        "confidentiality": "Internal",
        "upvotes": 42,
        "comments": 9,
        "urgency": 8.7,
        "impact_score": 9.2,
        "similar_agents": ["Credit Appraisal Agent"],
        "preferred_action": "convert",
    },
    {
        "title": "Predict Ticket Escalations for Managed Cloud",
        "submitter": {
            "name": "Sasha Ortiz",
            "department": "Customer Support",
            "region": "EMEA",
            "role": "Support Lead",
        },
        "description": "Need AI triage to flag noisy tickets + propose workflows before hitting L3.",
        "attachments": ["ticket_export.csv"],
        "category": "Support",
        "difficulty": "Hard",
        "impact": "Critical",
        "task_type": ["Data-heavy", "Customer-facing"],
        "confidentiality": "Public",
        "upvotes": 58,
        "comments": 14,
        "urgency": 9.5,
        "impact_score": 8.9,
        "similar_agents": ["IT Troubleshooter Agent"],
        "preferred_action": "open",
    },
    {
        "title": "OpenStack Deployment Readiness Validator",
        "submitter": {
            "name": "James O’Donnell",
            "department": "Cloud Infra",
            "region": "EMEA",
            "role": "Engineering Lead",
        },
        "description": "Create an automated validator that ingests deployment logs and flags blockers before change windows.",
        "attachments": ["readiness_logs.tar.gz"],
        "category": "Engineering",
        "difficulty": "Hard",
        "impact": "Critical",
        "task_type": ["Automation", "Infra"],
        "confidentiality": "Internal",
        "upvotes": 62,
        "comments": 12,
        "urgency": 9.7,
        "impact_score": 9.1,
        "similar_agents": ["Infra Validator Agent"],
        "preferred_action": "open",
    },
    {
        "title": "Customer Renewal Risk Insights",
        "submitter": {
            "name": "Laura Chen",
            "department": "Sales Ops",
            "region": "AMER",
            "role": "Sales Strategist",
        },
        "description": "Surface risk signals from renewal notes + CRM data to prioritize customer save motions.",
        "attachments": ["renewal_notes.docx"],
        "category": "Sales",
        "difficulty": "Medium",
        "impact": "High",
        "task_type": ["Document-heavy", "Revenue"],
        "confidentiality": "Internal",
        "upvotes": 34,
        "comments": 11,
        "urgency": 8.1,
        "impact_score": 9.4,
        "similar_agents": ["Sales Copilot Agent"],
        "preferred_action": "convert",
    },
    {
        "title": "Onboarding Ticket Auto-Categorizer",
        "submitter": {
            "name": "Rachel Gomez",
            "department": "HR Ops",
            "region": "AMER",
            "role": "People Ops Lead",
        },
        "description": "Auto-label onboarding requests into policy, hardware, security, or manager actions to reduce handling delays.",
        "attachments": ["onboarding_tasks.csv"],
        "category": "HR",
        "difficulty": "Medium",
        "impact": "High",
        "task_type": ["Workflow", "Classification"],
        "confidentiality": "Internal",
        "upvotes": 28,
        "comments": 6,
        "urgency": 7.9,
        "impact_score": 8.5,
        "similar_agents": ["HR Routing Agent"],
        "preferred_action": "convert",
    },
    {
        "title": "Predict Capacity Exhaustion in Infra",
        "submitter": {
            "name": "Santiago Rivera",
            "department": "Data Center Engineering",
            "region": "LATAM",
            "role": "Infra Reliability Lead",
        },
        "description": "Need proactive alerts for storage/CPU exhaustion so we can rebalance workloads before we breach thresholds.",
        "attachments": ["metrics_export.json"],
        "category": "Engineering",
        "difficulty": "Hard",
        "impact": "Critical",
        "task_type": ["Forecasting", "Automation"],
        "confidentiality": "Internal",
        "upvotes": 77,
        "comments": 20,
        "urgency": 9.6,
        "impact_score": 9.9,
        "similar_agents": ["Capacity Forecast Agent"],
        "preferred_action": "open",
    },
    {
        "title": "Auto-Generate Security Incident Reports",
        "submitter": {
            "name": "Karim Haddad",
            "department": "Security Ops",
            "region": "AMER",
            "role": "SOC Lead",
        },
        "description": "Create compliance-ready incident summaries from SOC event streams without manual reformatting.",
        "attachments": ["soc_events.csv"],
        "category": "Security",
        "difficulty": "Medium",
        "impact": "High",
        "task_type": ["Document-heavy", "Compliance"],
        "confidentiality": "Internal",
        "upvotes": 48,
        "comments": 13,
        "urgency": 8.8,
        "impact_score": 9.3,
        "similar_agents": ["SOC Copilot"],
        "preferred_action": "convert",
    },
    {
        "title": "Reduce Chat Support Handle Time",
        "submitter": {
            "name": "Marco Li",
            "department": "Support",
            "region": "APAC",
            "role": "Chat Ops Lead",
        },
        "description": "Need a copilot that recommends macros + shortens chat resolution time for Tier 1 agents.",
        "attachments": ["chat_transcripts.zip"],
        "category": "Support",
        "difficulty": "Medium",
        "impact": "High",
        "task_type": ["Customer-facing"],
        "confidentiality": "Internal",
        "upvotes": 36,
        "comments": 9,
        "urgency": 8.4,
        "impact_score": 8.7,
        "similar_agents": ["Chat Assist Agent"],
        "preferred_action": "convert",
    },
    {
        "title": "Auto-Extract Partner Contract Data",
        "submitter": {
            "name": "Oliver Grant",
            "department": "Legal Ops",
            "region": "EMEA",
            "role": "Legal Manager",
        },
        "description": "Need clause extraction + reasoning notes from PDFs so legal teams can prep partner packages faster.",
        "attachments": ["partner_contracts.pdf"],
        "category": "Legal",
        "difficulty": "Medium",
        "impact": "Medium",
        "task_type": ["Document-heavy"],
        "confidentiality": "Internal",
        "upvotes": 19,
        "comments": 3,
        "urgency": 7.2,
        "impact_score": 7.9,
        "similar_agents": ["OCR Extractor Agent"],
        "preferred_action": "open",
    },
]

SAMPLE_HELP_SOLUTIONS = [
    {
        "challenge": "Sync RAX billing with customer billing format",
        "author": "Elon Musk",
        "approach": "“Billing Rocket Formatter” — rule-driven column matcher + auto-normalizer aligning every customer schema to RAX format.",
        "difficulty": "Easy",
        "upvotes": 11,
        "comments": 2,
        "status": "Draft",
    },
    {
        "challenge": "Automate Monthly Billing Reconciliation",
        "author": "John Lennon",
        "approach": "“Imagine Ledger” — LLM + deterministic journal matcher that reconciles misaligned entries with reasoning + audit trail.",
        "difficulty": "Medium",
        "upvotes": 51,
        "comments": 12,
        "status": "Prototype",
    },
    {
        "challenge": "Predict Ticket Escalations for Managed Cloud",
        "author": "Paul McCartney",
        "approach": "“HelpDesk Harmony” — sentiment trajectory predictor + escalation-sequence classifier trained on chat history.",
        "difficulty": "Hard",
        "upvotes": 67,
        "comments": 16,
        "status": "Prototype",
    },
    {
        "challenge": "OpenStack Deployment Readiness Validator",
        "author": "George Harrison",
        "approach": "“Here Comes the Sun Validator” — DAG-based infra readiness checker + anomaly patterns from logs.",
        "difficulty": "Medium",
        "upvotes": 44,
        "comments": 9,
        "status": "Draft",
    },
    {
        "challenge": "Customer Renewal Risk Insights",
        "author": "Ringo Starr",
        "approach": "“Octopus’s Risk Garden” — churn scoring + renewal call summarizer using high-confidence LLM extraction.",
        "difficulty": "Medium",
        "upvotes": 29,
        "comments": 7,
        "status": "Draft",
    },
    {
        "challenge": "Onboarding Ticket Auto-Categorizer",
        "author": "Fei-Fei Li",
        "approach": "Vision-LLM hybrid for classification of onboarding docs + HR workflow routing.",
        "difficulty": "Easy",
        "upvotes": 61,
        "comments": 14,
        "status": "MVP Ready",
    },
    {
        "challenge": "Predict Capacity Exhaustion in Infra",
        "author": "Geoffrey Hinton",
        "approach": "“Neural Capacity Oracle” — time-series deep learner predicting exhaustion with early warning signals.",
        "difficulty": "Hard",
        "upvotes": 73,
        "comments": 18,
        "status": "Prototype",
    },
    {
        "challenge": "Auto-Generate Security Incident Reports",
        "author": "Timnit Gebru",
        "approach": "“FairSecure Reporter” — bias-aware incident summarizer + compliance-aligned reporting engine.",
        "difficulty": "Medium",
        "upvotes": 46,
        "comments": 11,
        "status": "Draft",
    },
    {
        "challenge": "Reduce Chat Support Handle Time",
        "author": "Andrew Ng",
        "approach": "“FastTrack Support Tutor” — intent detector + automatic macro suggestion copilot.",
        "difficulty": "Medium",
        "upvotes": 38,
        "comments": 10,
        "status": "MVP",
    },
    {
        "challenge": "Auto-Extract Partner Contract Data",
        "author": "Richard Feynman",
        "approach": "“The Feynman Extractor” — explainable clause parser that exposes plain-English reasoning steps.",
        "difficulty": "Medium",
        "upvotes": 55,
        "comments": 13,
        "status": "Draft",
    },
]

HOW_CAN_AI_HELP_URL = "http://119.9.127.11:8054/how_can_ai_help"
PROJECT_HUB_URL = "http://119.9.127.11:8054/project_hub"


CHALLENGE_FEED_ROWS = [
    {
        "title": "Sync RAX billing with customer billing format",
        "submitter": {"name": "Jon", "department": "Billing", "region": "APAC"},
        "metadata_display": "Billing • APAC — Finance",
        "attachments": [],
        "urgency": 6.0,
        "impact_score": 6.5,
        "similar_agents": ["Credit Appraisal Agent"],
        "upvotes": 0,
        "comments": 0,
        "action_display": "AI Can Help • Convert",
    },
    {
        "title": "Automate Monthly Billing Reconciliation",
        "submitter": {"name": "Jordan Lee", "department": "Finance Ops", "region": "AMER"},
        "metadata_display": "Finance Ops • AMER — Finance",
        "attachments": ["billing_rules.pdf", "ledger.csv"],
        "urgency": 8.7,
        "impact_score": 9.2,
        "similar_agents": ["Credit Appraisal Agent"],
        "upvotes": 42,
        "comments": 9,
        "action_display": "Convert",
    },
    {
        "title": "Predict Ticket Escalations for Managed Cloud",
        "submitter": {"name": "Sasha Ortiz", "department": "Customer Support", "region": "EMEA"},
        "metadata_display": "Customer Support • EMEA — Support",
        "attachments": ["ticket_export.csv"],
        "urgency": 9.5,
        "impact_score": 8.9,
        "similar_agents": ["IT Troubleshooter Agent"],
        "upvotes": 58,
        "comments": 14,
        "action_display": "Open",
    },
    {
        "title": "OpenStack Deployment Readiness Validator",
        "submitter": {"name": "James O'Donnell", "department": "Cloud Infra", "region": "EMEA"},
        "metadata_display": "Cloud Infra • EMEA — Engineering",
        "attachments": ["readiness_logs.tar.gz"],
        "urgency": 9.7,
        "impact_score": 9.1,
        "similar_agents": ["Infra Validator Agent"],
        "upvotes": 62,
        "comments": 12,
        "action_display": "Open",
    },
    {
        "title": "Customer Renewal Risk Insights",
        "submitter": {"name": "Laura Chen", "department": "Sales Ops", "region": "AMER"},
        "metadata_display": "Sales Ops • AMER — Sales",
        "attachments": ["renewal_notes.docx"],
        "urgency": 8.1,
        "impact_score": 9.4,
        "similar_agents": ["Sales Copilot Agent"],
        "upvotes": 34,
        "comments": 11,
        "action_display": "Convert",
    },
    {
        "title": "Onboarding Ticket Auto-Categorizer",
        "submitter": {"name": "Rachel Gomez", "department": "HR Ops", "region": "AMER"},
        "metadata_display": "HR Ops • AMER — People",
        "attachments": ["onboarding_tasks.csv"],
        "urgency": 7.9,
        "impact_score": 8.5,
        "similar_agents": ["HR Routing Agent"],
        "upvotes": 28,
        "comments": 6,
        "action_display": "Convert",
    },
    {
        "title": "Predict Capacity Exhaustion in Infra",
        "submitter": {"name": "Santiago Rivera", "department": "Data Center Eng", "region": "LATAM"},
        "metadata_display": "Data Center Eng • LATAM",
        "attachments": ["metrics_export.json"],
        "urgency": 9.6,
        "impact_score": 9.9,
        "similar_agents": ["Capacity Forecast Agent"],
        "upvotes": 77,
        "comments": 20,
        "action_display": "Open",
    },
    {
        "title": "Auto-Generate Security Incident Reports",
        "submitter": {"name": "Karim Haddad", "department": "Security Ops", "region": "AMER"},
        "metadata_display": "Security Ops • AMER",
        "attachments": ["soc_events.csv"],
        "urgency": 8.8,
        "impact_score": 9.3,
        "similar_agents": ["SOC Copilot"],
        "upvotes": 48,
        "comments": 13,
        "action_display": "Convert",
    },
    {
        "title": "Reduce Chat Support Handle Time",
        "submitter": {"name": "Marco Li", "department": "Support", "region": "APAC"},
        "metadata_display": "Support • APAC",
        "attachments": ["chat_transcripts.zip"],
        "urgency": 8.4,
        "impact_score": 8.7,
        "similar_agents": ["Chat Assist Agent"],
        "upvotes": 36,
        "comments": 9,
        "action_display": "Convert",
    },
    {
        "title": "Auto-Extract Partner Contract Data",
        "submitter": {"name": "Oliver Grant", "department": "Legal Ops", "region": "EMEA"},
        "metadata_display": "Legal Ops • EMEA",
        "attachments": ["partner_contracts.pdf"],
        "urgency": 7.2,
        "impact_score": 7.9,
        "similar_agents": ["OCR Extractor Agent"],
        "upvotes": 19,
        "comments": 3,
        "action_display": "Open",
    },
    {
        "title": "Digitize Field Safety Rounds",
        "submitter": {"name": "Aisha Patel", "department": "Field Ops", "region": "APAC"},
        "metadata_display": "Field Ops • APAC — Safety",
        "attachments": ["safety_checklist.pdf"],
        "urgency": 8.3,
        "impact_score": 8.6,
        "similar_agents": ["Field Ops Monitor"],
        "upvotes": 22,
        "comments": 5,
        "action_display": "AICANHELP",
    },
    {
        "title": "Predict Partner Performance",
        "submitter": {"name": "Miguel Santos", "department": "Partner Success", "region": "LATAM"},
        "metadata_display": "Partner Success • LATAM — Growth",
        "attachments": ["partner_data.xlsx"],
        "urgency": 7.7,
        "impact_score": 8.1,
        "similar_agents": ["Partner Pulse Agent"],
        "upvotes": 31,
        "comments": 7,
        "action_display": "Convert",
    },
    {
        "title": "Personalize Onboarding Playbooks",
        "submitter": {"name": "Nia Thompson", "department": "People & Culture", "region": "AMER"},
        "metadata_display": "People & Culture • AMER — Experience",
        "attachments": ["playbook_template.docx"],
        "urgency": 7.0,
        "impact_score": 7.8,
        "similar_agents": ["Onboarding Router"],
        "upvotes": 14,
        "comments": 4,
        "action_display": "AICANHELP",
    },
    {
        "title": "Automate Compliance Evidence",
        "submitter": {"name": "Kenji Yamamoto", "department": "Risk & Compliance", "region": "EMEA"},
        "metadata_display": "Risk & Compliance • EMEA — Governance",
        "attachments": ["audit_log.zip"],
        "urgency": 8.9,
        "impact_score": 9.0,
        "similar_agents": ["Policy Checker"],
        "upvotes": 39,
        "comments": 11,
        "action_display": "Convert",
    },
    {
        "title": "Real-time Cloud Cost Radar",
        "submitter": {"name": "Priya Malik", "department": "Cloud Economics", "region": "Global"},
        "metadata_display": "Cloud Economics • Global",
        "attachments": ["cost_report.csv"],
        "urgency": 8.5,
        "impact_score": 8.8,
        "similar_agents": ["Capacity Forecast Agent"],
        "upvotes": 46,
        "comments": 13,
        "action_display": "Open",
    },
    {
        "title": "a talent directory with projet portfolio",
        "submitter": {"name": "Ben", "department": "Cx", "region": "World"},
        "metadata_display": "Cx • World",
        "attachments": [],
        "urgency": 6.0,
        "impact_score": 6.5,
        "similar_agents": [],
        "upvotes": 0,
        "comments": 0,
        "action_display": "AICANHELP",
    },
]


def _build_sample_submission_lookup() -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    for record in SAMPLE_HELP_SUBMISSIONS:
        title = str(record.get("title", "")).strip().lower()
        if title:
            lookup[title] = record
    return lookup


SAMPLE_SUBMISSION_LOOKUP = _build_sample_submission_lookup()


def find_sample_submission(title: str | None) -> dict | None:
    if not title:
        return None
    return SAMPLE_SUBMISSION_LOOKUP.get(title.strip().lower())


def _build_sample_solution_lookup() -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    for record in SAMPLE_HELP_SOLUTIONS:
        title = str(record.get("challenge", "")).strip().lower()
        if title:
            lookup[title] = record
    return lookup


SAMPLE_SOLUTION_LOOKUP = _build_sample_solution_lookup()


def find_sample_solution(challenge: str | None) -> dict | None:
    if not challenge:
        return None
    return SAMPLE_SOLUTION_LOOKUP.get(challenge.strip().lower())


PROPOSED_SOLUTION_ROWS = [
    {
        "challenge": "Sync RAX billing with customer billing format",
        "submitter": "Jon",
        "helper": "Elon Musk",
        "approach": "“Billing Rocket Formatter” — rule-driven column matcher + auto-normalizer that aligns any customer billing schema to RAX format",
        "difficulty": "Easy",
        "upvotes": 11,
        "comments": 2,
        "status": "Draft",
    },
    {
        "challenge": "Automate Monthly Billing Reconciliation",
        "submitter": "Jordan Lee",
        "helper": "John Lennon",
        "approach": "“Imagine Ledger” — LLM + deterministic journal matcher that reconciles mismatched entries using reasoning + audit trace",
        "difficulty": "Medium",
        "upvotes": 51,
        "comments": 12,
        "status": "Prototype",
    },
    {
        "challenge": "Predict Ticket Escalations for Managed Cloud",
        "submitter": "Sasha Ortiz",
        "helper": "Paul McCartney",
        "approach": "“HelpDesk Harmony” — sentiment trajectory predictor + escalation-sequence classifier trained on chat history",
        "difficulty": "Hard",
        "upvotes": 67,
        "comments": 16,
        "status": "Prototype",
    },
    {
        "challenge": "OpenStack Deployment Readiness Validator",
        "submitter": "James O’Donnell",
        "helper": "George Harrison",
        "approach": "“Here Comes the Sun Validator” — DAG-based infra readiness checker + anomaly patterns from logs",
        "difficulty": "Medium",
        "upvotes": 44,
        "comments": 9,
        "status": "Draft",
    },
    {
        "challenge": "Customer Renewal Risk Insights",
        "submitter": "Laura Chen",
        "helper": "Ringo Starr",
        "approach": "“Octopus’s Risk Garden” — churn scoring + renewal call summarizer using high-confidence LLM extraction",
        "difficulty": "Medium",
        "upvotes": 29,
        "comments": 7,
        "status": "Draft",
    },
    {
        "challenge": "Onboarding Ticket Auto-Categorizer",
        "submitter": "Rachel Gomez",
        "helper": "Fei-Fei Li",
        "approach": "Vision-LLM hybrid for classification of onboarding docs + HR workflow routing",
        "difficulty": "Easy",
        "upvotes": 61,
        "comments": 14,
        "status": "MVP Ready",
    },
    {
        "challenge": "Predict Capacity Exhaustion in Infra",
        "submitter": "Santiago Rivera",
        "helper": "Geoffrey Hinton",
        "approach": "“Neural Capacity Oracle” — time-series deep learner predicting storage/CPU exhaustion with early warnings",
        "difficulty": "Hard",
        "upvotes": 73,
        "comments": 18,
        "status": "Prototype",
    },
    {
        "challenge": "Auto-Generate Security Incident Reports",
        "submitter": "Karim Haddad",
        "helper": "Timnit Gebru",
        "approach": "“FairSecure Reporter” — bias-free incident summarizer + compliance-aligned reporting engine",
        "difficulty": "Medium",
        "upvotes": 46,
        "comments": 11,
        "status": "Draft",
    },
    {
        "challenge": "Reduce Chat Support Handle Time",
        "submitter": "Marco Li",
        "helper": "Andrew Ng",
        "approach": "“FastTrack Support Tutor” — intent detector + automatic macro suggestion engine",
        "difficulty": "Medium",
        "upvotes": 38,
        "comments": 10,
        "status": "MVP",
    },
    {
        "challenge": "Auto-Extract Partner Contract Data",
        "submitter": "Oliver Grant",
        "helper": "Richard Feynman",
        "approach": "“The Feynman Extractor” — explainable clause parser that shows reasoning steps in plain English",
        "difficulty": "Medium",
        "upvotes": 55,
        "comments": 13,
        "status": "Draft",
    },
    {
        "challenge": "Digitize Field Safety Rounds",
        "submitter": "Aisha Patel",
        "helper": "Ada Lovelace",
        "approach": "“Safety Sentinel” — a mobile-first checklist reporter that normalizes inspections into AI-augmented dashboards.",
        "difficulty": "Medium",
        "upvotes": 24,
        "comments": 6,
        "status": "Prototype",
        "ai_tools_used": ["mobile forms", "vision QA"],
    },
    {
        "challenge": "Predict Partner Performance",
        "submitter": "Miguel Santos",
        "helper": "Grace Hopper",
        "approach": "“Partner Pulse” — regression ensemble feeding partner health signals into actionable alerts for the Success team.",
        "difficulty": "Medium",
        "upvotes": 33,
        "comments": 9,
        "status": "Prototype",
        "ai_tools_used": ["regression", "partner graph"],
    },
    {
        "challenge": "Personalize Onboarding Playbooks",
        "submitter": "Nia Thompson",
        "helper": "Fei-Fei Li",
        "approach": "“Welcome AI” — LLM-driven playbooks tuned per role, region, and learning preference with embedded feedback loops.",
        "difficulty": "Easy",
        "upvotes": 17,
        "comments": 5,
        "status": "MVP",
        "ai_tools_used": ["LLM", "feedback classifier"],
    },
    {
        "challenge": "Automate Compliance Evidence",
        "submitter": "Kenji Yamamoto",
        "helper": "Timnit Gebru",
        "approach": "“Governance Archivist” — plugin that collets logs, rewrites compliance narratives, and surfaces risks via structured exports.",
        "difficulty": "Hard",
        "upvotes": 42,
        "comments": 10,
        "status": "Draft",
        "ai_tools_used": ["LLM", "policy extractor"],
    },
    {
        "challenge": "Real-time Cloud Cost Radar",
        "submitter": "Priya Malik",
        "helper": "Geoffrey Hinton",
        "approach": "“Nebula Ledger” — anomaly detector + explainable forecast that hits product, finance, and EngOps avatars.",
        "difficulty": "Hard",
        "upvotes": 49,
        "comments": 14,
        "status": "Prototype",
        "ai_tools_used": ["time-series", "neural net", "capacity forecast"],
    },
    {
        "challenge": "a talent directory with projet portfolio",
        "submitter": "Ben",
        "helper": "Dzoan",
        "approach": "• What: YES AI a community driven LAB where problems and painpoint finds solutions and Cure ! • How: team of multitalent experts , poc , agent library • AI tools: opensource model , regression , random forest",
        "difficulty": "Medium",
        "upvotes": 5,
        "comments": 1,
        "status": "Draft",
        "ai_tools_used": ["open source model", "regression", "random forest"],
    },
]

DEFAULT_AGENT_CATALOG = [
    (
        "Agent Factory",
        "🧩 Agent Builder",
        "🧩 Agent Builder",
        "Build custom agents by combining functions from HF and existing agents like LEGO blocks.",
        "Available",
        "🧩",
        True,
        "dzoan.nguyen@rackspace.com",
        "2025-11-27",
        "v1.0.0",
    ),
    (
        "Model Operations",
        "🤖 Hugging Face Tools",
        "🤖 HF Agent Wrapper",
        "Pure HuggingFace operations — Local HF models + HF API. Lightweight, HF-focused solution for all HF tasks.",
        "Available",
        "🤖",
        False,
        "dzoan.nguyen@rackspace.com",
        "2025-11-27",
        "v1.0.0",
    ),
    (
        "Executive Dashboards",
        "🚗 Boardroom Intelligence",
        "🚗 CEO driver DASHBOARD",
        "Real-time AI cockpit for CEOs to steer revenue, cash, ops, and market moves.",
        "Available",
        "🚗",
        False,
        "dzoan.nguyen@rackspace.com",
        "2025-11-27",
        "v1.0.0",
    ),
    (
        "Retail Banking Suite",
        "Retail Banking Suite",
        "💬 Chatbot Assistant",
        "Context-aware embedded assistant.",
        "Available",
        "💬",
        False,
        "dzoan.nguyen@rackspace.com",
        "2025-11-27",
        "v1.0.0",
    ),
    (
        "Support & Security",
        "🧠 Troubleshooting",
        "🧠 IT Troubleshooter Agent",
        "First-principles + case-memory incident solver.",
        "Available",
        "🧠",
        False,
        "dzoan.nguyen@rackspace.com",
        "2025-11-27",
        "v1.0.0",
    ),
]

ALLOWED_AGENT_ROUTE_NAMES = {
    "agent_builder",
    "hf_agent_wrapper",
    "ceo_driver_dashboard",
    "chatbot_assistant",
    "it_troubleshooter_agent",
}


def compute_route_name(agent_label: str) -> str:
    clean = "".join(ch if ch.isalnum() or ch in (" ", "_") else " " for ch in agent_label)
    clean = "_".join(clean.lower().split())
    return clean or "agent"


def load_agent_catalog() -> list[tuple]:
    agents_path = Path(__file__).parent / "data" / "agents.json"
    if agents_path.exists():
        try:
            with open(agents_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
                catalog = []
                for agent in data:
                    name = agent.get("agent", agent.get("name", "Agent"))
                    route = compute_route_name(name)
                    if route not in ALLOWED_AGENT_ROUTE_NAMES:
                        continue
                    catalog.append(
                        (
                            agent.get("sector", agent.get("industry", "Cross-Industry")),
                            agent.get("industry", agent.get("sector", "")),
                            name,
                            agent.get("description", ""),
                            agent.get("status", "Available"),
                            agent.get("emoji", "🤖"),
                            agent.get("requires_login", False),
                            agent.get("author", "dzoan.nguyen@rackspace.com"),
                            agent.get("created_at", datetime.now().strftime("%Y-%m-%d")),
                            agent.get("version", "v1.0.0"),
                        )
                    )
                if catalog:
                    return catalog
        except Exception:
            pass
    return DEFAULT_AGENT_CATALOG


AGENTS = load_agent_catalog()
CUSTOM_AGENT_LAUNCHES: dict[str, str] = {}


def load_feedback_store() -> dict:
    return load_meta_json("feedback.json", {})


feedback_data = load_feedback_store()

SAMPLE_HUMANS = [
    {
        "id": "human_dzoan_1",
        "name": "dzoan nguyen tran",
        "department": "cloud architect",
        "region": "APAC",
        "skills": [
            "cloud",
            "ai",
            "blockchain engineer and mostly architect of a BETTER WORLD",
        ],
        "ai_services": ["kpi-briefs", "scenario-simulator", "risk-radar"],
        "contributions": {"projects": 0, "agents": 0},
        "ai_contributions": "",
        "created_at": "2025-01-01",
        "updated_at": "2025-02-01",
        "sme_level": "⭐⭐⭐⭐ Expert",
    },
    {
        "id": "human_jarvis_1",
        "name": "jarvis",
        "department": "accounting",
        "region": "Americas",
        "skills": ["account"],
        "ai_services": [
            "incident-summarizer",
            "openstack-validator",
            "capacity-forecast",
        ],
        "contributions": {"projects": 0, "agents": 0},
        "ai_contributions": "",
        "created_at": "2025-01-03",
        "updated_at": "2025-02-03",
        "sme_level": "⭐⭐⭐ Skilled",
    },
    {
        "id": "human_jlennon",
        "name": "John Lennon",
        "department": "Innovation & Strategy",
        "region": "UK / EMEA",
        "skills": [
            "Creative AI",
            "Generative Models",
            "Prompt Artistry",
            "Vision AI",
        ],
        "ai_services": [
            "prd-copilot",
            "feature-impact",
            "campaign-writer",
            "experiment-planner",
        ],
        "contributions": {"projects": 3, "agents": 2},
        "ai_contributions": (
            "3 generative agents (“ImagineGPT”), 2 creativity frameworks, "
            "1 RAG music dataset"
        ),
        "created_at": "2024-05-01",
        "updated_at": "2025-02-10",
        "sme_level": "⭐⭐⭐⭐ Expert",
    },
    {
        "id": "human_pmccartney",
        "name": "Paul McCartney",
        "department": "Customer Experience & Solutions",
        "region": "UK / EMEA",
        "skills": ["Voice AI", "Multimodal ML", "Human-AI Interaction"],
        "ai_services": [
            "support-copilot",
            "ticket-triage",
            "escalation-predictor",
            "incident-summarizer",
        ],
        "contributions": {"projects": 4, "agents": 2},
        "ai_contributions": (
            "4 voice-cloning demos, 2 sentiment-analysis agents, "
            "1 “Hey Jude AI Assistant”"
        ),
        "created_at": "2024-04-12",
        "updated_at": "2025-02-08",
        "sme_level": "⭐⭐⭐⭐⭐ Principal",
    },
    {
        "id": "human_gharrison",
        "name": "George Harrison",
        "department": "Engineering & Automation",
        "region": "APAC",
        "skills": ["Workflow Automation", "Agent Orchestration", "Calm Design"],
        "ai_services": [
            "openstack-validator",
            "capacity-forecast",
            "drift-detector",
            "sre-playbooks",
        ],
        "contributions": {"projects": 3, "agents": 2},
        "ai_contributions": (
            "2 automation agents (“Here Comes the Flow”), "
            "3 AI-integrated pipelines"
        ),
        "created_at": "2024-03-05",
        "updated_at": "2025-01-15",
        "sme_level": "⭐⭐⭐ Skilled",
    },
    {
        "id": "human_rstarr",
        "name": "Ringo Starr",
        "department": "Support & Operations",
        "region": "AMER",
        "skills": [
            "Reliability Engineering",
            "Monitoring AI",
            "LLM Guardrails",
        ],
        "ai_services": [
            "alert-dedup",
            "incident-summarizer",
            "sla-monitor",
            "routing-optimizer",
        ],
        "contributions": {"projects": 3, "agents": 1},
        "ai_contributions": (
            "3 ops copilots, 1 anomaly detection agent "
            "“Octopus’s Ops Copilot”"
        ),
        "created_at": "2024-02-10",
        "updated_at": "2024-12-20",
        "sme_level": "⭐⭐ Advanced Beginner",
    },
    {
        "id": "human_ylecun",
        "name": "Yann LeCun",
        "department": "Meta AI",
        "region": "North America",
        "skills": [
            "Self-Supervised Learning",
            "Deep Learning",
            "Autonomy",
        ],
        "ai_services": [
            "feature-store",
            "model-monitor",
            "prompt-library",
            "rag-builder",
        ],
        "contributions": {"projects": 4, "agents": 4},
        "ai_contributions": "Co-inventor of CNNs, global AI research leadership",
        "created_at": "2024-01-01",
        "updated_at": "2025-02-02",
        "sme_level": "⭐⭐⭐⭐⭐ Principal",
    },
    {
        "id": "human_dhassabis",
        "name": "Demis Hassabis",
        "department": "Google DeepMind",
        "region": "UK / Europe",
        "skills": ["AGI", "Reinforcement Learning", "Model Alignment"],
        "ai_services": [
            "scenario-simulator",
            "risk-radar",
            "kpi-briefs",
            "rag-builder",
        ],
        "contributions": {"projects": 6, "agents": 5},
        "ai_contributions": "AlphaGo, AlphaFold, frontier model breakthroughs",
        "created_at": "2024-01-05",
        "updated_at": "2025-02-03",
        "sme_level": "⭐⭐⭐⭐⭐ Principal",
    },
    {
        "id": "human_emusk",
        "name": "Elon Musk",
        "department": "Tesla / SpaceX / xAI",
        "region": "Global",
        "skills": ["AI Safety", "Robotics", "Simulation", "Autonomy"],
        "ai_services": [
            "sre-playbooks",
            "scenario-simulator",
            "policy-checker",
            "capacity-forecast",
        ],
        "contributions": {"projects": 5, "agents": 2},
        "ai_contributions": "Autonomous systems, humanoid robots, xAI Grok",
        "created_at": "2024-05-20",
        "updated_at": "2025-01-02",
        "sme_level": "⭐⭐⭐⭐ Expert",
    },
]


# SAMPLE_HUMANS = [
#     {
#         "id": "dzoan_1",
#         "name": "dzoan nguyen tran",
#         "department": "cloud architect",
#         "region": "APAC",
#         "skills": ["cloud", "ai", "blockchain engineer and mostly architect of a BETTER WORLD"],
#         "ai_services": ["kpi-briefs", "scenario-simulator", "risk-radar"],
#         "contributions": {"projects": 0, "agents": 0},
#         "ai_contributions": "",
#         "created_at": "2025-01-01",
#         "updated_at": "2025-02-01",
#         "sme_level": "⭐⭐⭐⭐ Expert",
#     },
#     {
#         "id": "jarvis_1",
#         "name": "jarvis",
#         "department": "accounting",
#         "region": "Americas",
#         "skills": ["account"],
#         "ai_services": ["incident-summarizer", "openstack-validator", "capacity-forecast"],
#         "contributions": {"projects": 0, "agents": 0},
#         "ai_contributions": "",
#         "created_at": "2025-01-03",
#         "updated_at": "2025-02-03",
#         "sme_level": "⭐⭐⭐ Skilled",
#     },
#     {
#         "name": "John Lennon",
#         "department": "Innovation & Strategy",
#         "region": "UK / EMEA",
#         "skills": ["Creative AI", "Generative Models", "Prompt Artistry", "Vision AI"],
#         "ai_services": ["prd-copilot", "feature-impact", "campaign-writer", "experiment-planner"],
#         "contributions": {"projects": 3, "agents": 2},
#         "ai_contributions": "3 generative agents (“ImagineGPT”), 2 creativity frameworks, 1 RAG music dataset",
#         "created_at": "2024-05-01",
#         "updated_at": "2025-02-10",
#         "sme_level": "⭐⭐⭐⭐ Expert",
#     },
#     {
#         "name": "Paul McCartney",
#         "department": "Customer Experience & Solutions",
#         "region": "UK / EMEA",
#         "skills": ["Voice AI", "Multimodal ML", "Human-AI Interaction"],
#         "ai_services": ["support-copilot", "ticket-triage", "escalation-predictor", "incident-summarizer"],
#         "contributions": {"projects": 4, "agents": 2},
#         "ai_contributions": "4 voice-cloning demos, 2 sentiment-analysis agents, 1 “Hey Jude AI Assistant”",
#         "created_at": "2024-04-12",
#         "updated_at": "2025-02-08",
#         "sme_level": "⭐⭐⭐⭐⭐ Principal",
#     },
#     {
#         "name": "George Harrison",
#         "department": "Engineering & Automation",
#         "region": "APAC",
#         "skills": ["Workflow Automation", "Agent Orchestration", "Calm Design"],
#         "ai_services": ["openstack-validator", "capacity-forecast", "drift-detector", "sre-playbooks"],
#         "contributions": {"projects": 3, "agents": 2},
#         "ai_contributions": "2 automation agents (“Here Comes the Flow”), 3 AI-integrated pipelines",
#         "created_at": "2024-03-05",
#         "updated_at": "2025-01-15",
#         "sme_level": "⭐⭐⭐ Skilled",
#     },
#     {
#         "name": "Ringo Starr",
#         "department": "Support & Operations",
#         "region": "AMER",
#         "skills": ["Reliability Engineering", "Monitoring AI", "LLM Guardrails"],
#         "ai_services": ["alert-dedup", "incident-summarizer", "sla-monitor", "routing-optimizer"],
#         "contributions": {"projects": 3, "agents": 1},
#         "ai_contributions": "3 ops copilots, 1 anomaly detection agent (“Octopus’s Ops Copilot”)",
#         "created_at": "2024-02-10",
#         "updated_at": "2024-12-20",
#         "sme_level": "⭐⭐ Advanced Beginner",
#     },

#     {
#         "name": "Yann LeCun",
#         "department": "Meta AI",
#         "region": "North America",
#         "skills": ["Self-Supervised Learning", "Deep Learning", "Autonomy"],
#         "ai_services": ["feature-store", "model-monitor", "prompt-library", "rag-builder"],
#         "contributions": {"projects": 4, "agents": 4},
#         "ai_contributions": "Co-inventor of CNNs, global AI research leadership",
#         "created_at": "2024-01-01",
#         "updated_at": "2025-02-02",
#         "sme_level": "⭐⭐⭐⭐⭐ Principal",
#     },
#     {
#         "name": "Demis Hassabis",
#         "department": "Google DeepMind",
#         "region": "UK / Europe",
#         "skills": ["AGI", "Reinforcement Learning", "Model Alignment"],
#         "ai_services": ["scenario-simulator", "risk-radar", "kpi-briefs", "rag-builder"],
#         "contributions": {"projects": 6, "agents": 5},
#         "ai_contributions": "AlphaGo, AlphaFold, frontier model breakthroughs",
#         "created_at": "2024-01-05",
#         "updated_at": "2025-02-03",
#         "sme_level": "⭐⭐⭐⭐⭐ Principal",
#     },

#     {
#         "name": "Elon Musk",
#         "department": "Tesla / SpaceX / xAI",
#         "region": "Global",
#         "skills": ["AI Safety", "Robotics", "Simulation", "Autonomy"],
#         "ai_services": ["sre-playbooks", "scenario-simulator", "policy-checker", "capacity-forecast"],
#         "contributions": {"projects": 5, "agents": 2},
#         "ai_contributions": "Autonomous systems, humanoid robots, xAI Grok",
#         "created_at": "2024-05-20",
#         "updated_at": "2025-01-02",
#         "sme_level": "⭐⭐⭐⭐ Expert",
#     },

# ]


SAMPLE_PROJECTS = [
    {
        "title": "Renewable Finance Copilot",
        "authors": ["Avery Chen", "Mia Patel"],
        "business_area": "Green Energy",
        "summary": "Forecast capital flows & compliance across global farms.",
        "created_at": "2024-09-02",
        "status": "MVP",
        "upvotes": 18,
        "comments": 6,
    },
    {
        "title": "CX Sentiment Heatmap",
        "authors": ["Lila Moreno"],
        "business_area": "Customer Success",
        "summary": "Streaming sentiment insights for Rackspace customer boards.",
        "created_at": "2024-07-25",
        "status": "Incubation",
        "upvotes": 11,
        "comments": 4,
    },
]


def _build_sample_project_lookup() -> dict[str, dict]:
    lookup: dict[str, dict] = {}
    for record in SAMPLE_PROJECTS:
        title = str(record.get("title", "")).strip().lower()
        if title:
            lookup[title] = record
    return lookup


SAMPLE_PROJECT_LOOKUP = _build_sample_project_lookup()


def find_sample_project(title: str | None) -> dict | None:
    if not title:
        return None
    return SAMPLE_PROJECT_LOOKUP.get(title.strip().lower())


SAMPLE_PATTERNS = [
    {
        "name": "Credit Explainability Pattern",
        "description": "Ensure every credit decision ships with policy rationale + SHAP.",
        "domain": "Finance",
        "use_cases": ["Retail Lending", "SMB Working Capital"],
        "author": "Noor Idris",
        "created_at": "2024-06-15",
    },
    {
        "name": "Global KYC Ontology",
        "description": "Entity + document graph powering AML/KYC orchestration.",
        "domain": "Compliance",
        "use_cases": ["AML", "Sanctions"],
        "author": "Mason Reed",
        "created_at": "2024-05-20",
    },
]

SAMPLE_DOCS = [
    {
        "title": "YES AI CAN Onboarding Playbook",
        "category": "Guide",
        "author": "Rackers Lab PMO",
        "updated_at": "2024-10-01",
        "read_time": "12 min",
        "rating": 4.8,
    },
    {
        "title": "HF Agent Builder Tutorial",
        "category": "Tutorial",
        "author": "Priya Desai",
        "updated_at": "2024-09-10",
        "read_time": "8 min",
        "rating": 4.6,
    },
]

SAMPLE_COMMUNITY = [
    {
        "name": "Noor Idris",
        "department": "FinOps Advisory",
        "region": "APJ",
        "skills": ["FinOps", "Compliance AI"],
        "badges": ["Ambassador L2", "AI Ethics"],
        "contributions": ["Credit Engines", "Policy Pattern"],
        "cohort": "2024A",
    },
    {
        "name": "Diego Ramos",
        "department": "Cloud Operations",
        "region": "LATAM",
        "skills": ["AIOps", "Infra Observability"],
        "badges": ["Community Builder"],
        "contributions": ["AIOps Runbooks"],
        "cohort": "2023B",
    },
]

SAMPLE_ADMIN = [
    {
        "name": "REX Metadata Exporter",
        "description": "Push JSON payloads to REX 2.0 ingestion bucket.",
        "category": "Export",
        "telemetry": "Stable",
        "updated_at": "2024-10-15",
    },
    {
        "name": "Agent Health Monitor",
        "description": "Track API uptime and GPU utilization per agent.",
        "category": "Monitoring",
        "telemetry": "Beta",
        "updated_at": "2024-09-28",
    },
]

SAMPLE_SEARCH = [
    {
        "type": "Profile",
        "title": "Avery Chen",
        "category": "Human Stack",
        "owner": "avery.chen@rackspace",
        "updated_at": "2024-10-12",
    },
    {
        "type": "Agent",
        "title": "Credit Appraisal Agent",
        "category": "Banking",
        "owner": "risk@rackspace",
        "updated_at": "2024-09-30",
    },
    {
        "type": "Pattern",
        "title": "Unified Risk Ontology",
        "category": "Ontology",
        "owner": "ontology@rackspace",
        "updated_at": "2024-08-05",
    },
]


def load_meta_records(filename: str, sample: list[dict]) -> list[dict]:
    try:
        data = load_meta_json(filename, sample)
    except Exception:
        return sample
    if not data:
        return sample
    if isinstance(data, dict):
        for key in ("items", "records", "data"):
            if key in data and isinstance(data[key], list):
                data = data[key]
                break
        else:
            data = [data]
    return data

def _normalize_record_list(data: Any) -> list[dict]:
    if not data:
        return []
    if isinstance(data, dict):
        for key in ("items", "records", "data"):
            candidate = data.get(key)
            if isinstance(candidate, list):
                return _normalize_record_list(candidate)
        return [data]
    if isinstance(data, list):
        return [entry for entry in data if isinstance(entry, dict)]
    return []


def _load_data_humans_file() -> list[dict]:
    project_root = Path(__file__).resolve().parents[2]
    data_path = project_root / "data" / "humans.json"
    if not data_path.exists():
        return []
    try:
        with open(data_path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
        return _normalize_record_list(raw)
    except Exception:
        return []

def load_human_feedback_reviews() -> Dict[str, List[Dict[str, Any]]]:
    raw = load_meta_json("human_feedback.json", {})
    normalized: Dict[str, List[Dict[str, Any]]] = {}
    if isinstance(raw, dict):
        for key, value in raw.items():
            if isinstance(value, list):
                normalized[key] = [entry for entry in value if isinstance(entry, dict)]
            elif isinstance(value, dict):
                normalized[key] = [value]
    return normalized


def parse_rating_value(value: Any, fallback: int) -> int:
    if value is None:
        return fallback
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return fallback


def render_rating_stars(score: int) -> str:
    bounded = max(0, min(5, score))
    return "★" * bounded + "☆" * (5 - bounded)


FEEDBACK_BLOCK_CSS = """
<style>
.feedback-block {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 4px;
    padding-top: 4px;
    max-width: 260px;
}

.feedback-stars {
    color: #ffd700;
    text-shadow: 0 0 6px #ffdd55, 0 0 12px #ffbb00;
    animation: starPulse 1.8s infinite ease-in-out;
    font-size: 18px;
}

.feedback-text {
    color: #cbd5e1;
    font-size: 13px;
    line-height: 1.2;
    width: 100%;
    word-wrap: break-word;
}

@keyframes starPulse {
    0% { opacity: 0.6; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.15); }
    100% { opacity: 0.6; transform: scale(1); }
}
</style>
"""


def render_feedback_block(rating: int, comment: str | None) -> str:
    bounded = max(0, min(5, rating))
    stars = "⭐" * bounded if bounded > 0 else "☆☆☆☆☆"
    text = (comment or "").replace("\n", " ").strip()
    if not text:
        text = "No feedback yet."
    snippet = text[:120] + ("..." if len(text) > 120 else "")
    safe_text = html.escape(snippet)
    return (
        "<div class='feedback-block'>"
        f"<div class='feedback-stars'>{stars}</div>"
        f"<div class='feedback-text'>{safe_text}</div>"
        "</div>"
    )


def load_human_stack_directory_records() -> list[dict]:
    meta_records = load_meta_records("humans.json", [])
    data_records = _load_data_humans_file()
    combined: list[dict] = []
    seen: set[str] = set()

    def add_record(record: dict) -> None:
        key_candidate = str(record.get("id") or record.get("email") or record.get("name") or "").strip().lower()
        if key_candidate and key_candidate in seen:
            return
        if key_candidate:
            seen.add(key_candidate)
        combined.append(record)

    for dataset in (meta_records, data_records):
        for record in dataset:
            if isinstance(record, dict):
                add_record(record)

    return combined


def format_tags(values: Iterable[str] | None) -> str:
    if not values:
        return "—"
    if isinstance(values, str):
        values = [values]
    tags = []
    for val in values:
        if val:
            tags.append(f"<span class='table-tag'>{html.escape(str(val))}</span>")
    return "".join(tags) or "—"


def describe_attachment_list(values: Iterable[Any] | None) -> str:
    if not values:
        return "<ul class='challenge-attachment-list'><li>—</li></ul>"
    if isinstance(values, str):
        values = [values]
    items: list[str] = []
    for raw in values:
        if isinstance(raw, dict):
            label = raw.get("name") or raw.get("path")
        else:
            label = str(raw)
        if label:
            items.append(f"<li>{html.escape(label)}</li>")
    if not items:
        items.append("<li>—</li>")
    return f"<ul class='challenge-attachment-list'>{''.join(items)}</ul>"


def build_status_badge(text: str, variant: str = "info") -> str:
    safe = html.escape(text or "—")
    return f"<span class='status-badge {variant}'>{safe}</span>"


PAGE_SLUGS.update(
    {
        "how_can_ai_help": PAGE_SLUGS.get("how_can_ai_help", "/how_can_ai_help"),
        "howcanaihelp": PAGE_SLUGS.get("howcanaihelp", "/howcanaihelp"),
        "solutionform": PAGE_SLUGS.get("solutionform", "/solutionform"),
        "human_stack": PAGE_SLUGS.get("human_stack", "/human_stack"),
        "project_hub": PAGE_SLUGS.get("project_hub", "/project_hub"),
        "ontology_twin": PAGE_SLUGS.get("ontology_twin", "/ontology_twin"),
    }
)

#new
def normalize_challenge_row(item: dict) -> list[str]:
    """Build a display-ready row for a submission, ensuring we always show data."""
    try:
        challenge_id = ensure_challenge_anchor(item)
        submitter = item.get("submitter") or {}
        submitter_name = submitter.get("name", "—")
        department = submitter.get("department", "—")
        region = submitter.get("region", "—")
        submitter_text = f"{html.escape(submitter_name)}<br><small>{html.escape(department)} • {html.escape(region)}</small>"

        dept_region = " • ".join(
            part.strip()
            for part in (str(submitter.get("department", "")), str(submitter.get("region", "")))
            if part and part.strip()
        )
        metadata_lines: list[str] = []
        if dept_region:
            metadata_lines.append(html.escape(dept_region.lower()))
        category = item.get("category")
        if category:
            metadata_lines.append(html.escape(str(category)))
        difficulty = item.get("difficulty")
        if difficulty:
            metadata_lines.append(html.escape(str(difficulty)))
        metadata = "<br>".join(metadata_lines) or "—"

        attachments = describe_attachment_list(item.get("attachments"))
        social = f"👍 {item.get('upvotes', 0)} • 💬 {item.get('comments', 0)}"
        similar = format_tags(item.get("similar_agents"))

        challenge_launch = build_challenge_form_url(item)
        convert_params = {
            "convert_submission_id": challenge_id,
            "source_submission_id": challenge_id,
            "convert_submission_title": item.get("title"),
            "convert_submission_description": item.get("description"),
            "convert_submission_category": item.get("category"),
            "convert_submission_difficulty": item.get("difficulty"),
            "convert_submission_submitter": submitter.get("name"),
            "convert_submission_department": submitter.get("department"),
            "convert_submission_region": submitter.get("region"),
            "convert_submission_upvotes": item.get("upvotes"),
            "convert_submission_comments": item.get("comments"),
            "convert_submission_urgency": item.get("urgency"),
            "convert_submission_impact": item.get("impact_score"),
        }
        convert_href = build_page_url("project_hub", convert_params)
        convert_launch = ensure_absolute_page_url(convert_href)
        spec_page_key = get_challenge_spec_page(item.get("title"))
        if spec_page_key:
            spec_href = build_page_url(spec_page_key, {"challenge_id": challenge_id})
            spec_launch = ensure_absolute_page_url(spec_href)
            action_html = build_action_triple_stack(
                "AI Can Help",
                challenge_launch,
                "Convert",
                convert_launch,
                "Open",
                spec_launch,
            )
        else:
            action_html = build_action_stack(
                "AI Can Help",
                challenge_launch,
                "Convert",
                convert_launch,
            )

        return [
            html.escape(item.get("title", "—")),
            submitter_text,
            metadata,
            attachments,
            f"{item.get('urgency', 0):.1f}",
            f"{item.get('impact_score', 0):.1f}",
            similar,
            social,
            action_html,
        ]
    except Exception:
        return ["—"] * 9



def build_page_url(page_key: str, params: dict[str, Any] | None = None) -> str:
    if page_key not in PAGE_SLUGS:
        ensure_page_file_for_key(page_key)
    if page_key not in PAGE_SLUGS:
        PAGE_SLUGS[page_key] = _slugify_page_stem(page_key)
    base = PAGE_SLUGS.get(page_key)
    if not base:
        base = _slugify_page_stem(page_key)
    if not params:
        return base
    cleaned = {k: v for k, v in params.items() if v not in (None, "", False)}
    if not cleaned:
        return base
    return f"{base}?{urlencode(cleaned, doseq=True)}"


def ensure_absolute_page_url(url: str) -> str:
    if not url:
        return LAUNCH_BASE_URL
    if url.startswith(("http://", "https://")):
        return url
    if url.startswith("/"):
        return f"{LAUNCH_BASE_URL}{url}"
    return f"{LAUNCH_BASE_URL}/{url.lstrip('/')}"


def ensure_solution_anchor(idea: dict) -> str:
    if idea.get("id"):
        return str(idea["id"])
    raw = (
        f"{idea.get('challenge', '')}|"
        f"{idea.get('author', '')}|"
        f"{idea.get('created_at', '')}|"
        f"{(idea.get('approach') or '')[:64]}"
    )
    digest = hashlib.sha1(raw.encode("utf-8", "ignore")).hexdigest()[:10]
    anchor = f"solution_{digest}"
    idea["id"] = anchor
    return anchor


def ensure_challenge_anchor(item: dict) -> str:
    if item.get("id"):
        return str(item["id"])
    submitter = item.get("submitter", {})
    raw = (
        f"{item.get('title', '')}|"
        f"{submitter.get('name', '')}|"
        f"{submitter.get('department', '')}|"
        f"{(item.get('description') or '')[:64]}"
    )
    digest = hashlib.sha1(raw.encode("utf-8", "ignore")).hexdigest()[:10]
    anchor = f"challenge_{digest}"
    item["id"] = anchor
    return anchor


def slugify_label(value: str | None, default: str = "project") -> str:
    if not value:
        return default
    cleaned = re.sub(r"[^0-9a-zA-Z]+", " ", value).strip().lower()
    return "_".join(cleaned.split()) or default


def ensure_project_anchor(item: dict) -> str:
    if item.get("id"):
        return str(item["id"])
    anchor = slugify_label(item.get("title"), "project")
    item["id"] = anchor
    return anchor


def build_challenge_form_url(item: dict) -> str:
    challenge_id = ensure_challenge_anchor(item)
    submitter = item.get("submitter", {}) or {}
    params = {
        "challenge_id": challenge_id,
        "challenge_title": item.get("title"),
        "challenge_description": item.get("description"),
        "challenge_category": item.get("category"),
        "challenge_difficulty": item.get("difficulty"),
        "challenge_urgency": item.get("urgency"),
        "challenge_impact": item.get("impact_score"),
        "submitter_name": submitter.get("name"),
        "submitter_department": submitter.get("department"),
        "submitter_region": submitter.get("region"),
        "submitter_role": submitter.get("role"),
    }
    cleaned = {k: v for k, v in params.items() if v not in (None, "", [])}
    if not cleaned:
        return CHALLENGE_FORM_BASE_URL
    return f"{CHALLENGE_FORM_BASE_URL}?{urlencode(cleaned)}"


def build_challenge_view_url(item: dict) -> str:
    sample = find_sample_submission(item.get("title"))
    candidate = dict(sample) if sample else dict(item)
    # ensure nested submitter is retained even when sample is missing fields
    submitter = candidate.get("submitter") or item.get("submitter")
    if submitter:
        candidate["submitter"] = submitter
    preferred_fields = [
        "description",
        "category",
        "difficulty",
        "impact",
        "impact_score",
        "urgency",
        "attachments",
        "similar_agents",
        "task_type",
        "confidentiality",
    ]
    for field in preferred_fields:
        if candidate.get(field) in (None, "", []):
            fallback_val = item.get(field)
            if fallback_val not in (None, "", []):
                candidate[field] = fallback_val
    params = {
        "challenge_id": ensure_challenge_anchor(candidate),
        "challenge_title": candidate.get("title"),
        "challenge_description": candidate.get("description"),
        "challenge_category": candidate.get("category"),
        "challenge_difficulty": candidate.get("difficulty"),
        "challenge_urgency": candidate.get("urgency"),
        "challenge_impact": candidate.get("impact_score"),
        "submitter_name": candidate.get("submitter", {}).get("name"),
        "submitter_department": candidate.get("submitter", {}).get("department"),
        "submitter_region": candidate.get("submitter", {}).get("region"),
    }
    return ensure_absolute_page_url(build_page_url("solutionform", params))


def build_project_view_url(project: dict) -> str:
    sample = find_sample_project(project.get("title"))
    candidate = dict(sample) if sample else dict(project)
    preferred_fields = [
        "summary",
        "description",
        "business_area",
        "category",
        "status",
        "phase",
        "created_at",
        "upvotes",
        "comments",
    ]
    for field in preferred_fields:
        if candidate.get(field) in (None, "", []):
            fallback_val = project.get(field)
            if fallback_val not in (None, "", []):
                candidate[field] = fallback_val
    project_id = ensure_project_anchor(project)
    owners = project.get("authors") or project.get("owner_name") or project.get("owner_email")
    if isinstance(owners, (list, tuple, set)):
        owner_text = ", ".join(str(owner) for owner in owners if owner)
    else:
        owner_text = owners or ""
    params = {
        "project_id": project_id,
        "project_title": candidate.get("title"),
        "project_summary": candidate.get("summary") or candidate.get("description"),
        "project_area": candidate.get("business_area") or candidate.get("category"),
        "project_status": candidate.get("status") or candidate.get("phase"),
        "project_created": candidate.get("created_at"),
        "project_owner": owner_text,
        "project_upvotes": candidate.get("upvotes"),
        "project_comments": candidate.get("comments"),
    }
    cleaned = {k: v for k, v in params.items() if v not in (None, "", [])}
    if not cleaned:
        return PROJECT_HUB_URL
    return f"{PROJECT_HUB_URL}?{urlencode(cleaned)}"


def build_solution_view_url(entry: dict) -> str:
    idea: dict[str, Any] = dict(entry)
    idea.setdefault("helper", idea.get("author"))
    idea.setdefault("submitter", idea.get("author"))
    solution_id = ensure_solution_anchor(idea)
    params = {
        "solution_id": solution_id,
        "solution_challenge": idea.get("challenge"),
        "challenge_title": idea.get("challenge"),
        "solution_author": idea.get("author"),
        "solution_helper": idea.get("helper"),
        "solution_submitter": idea.get("submitter"),
        "solution_approach": idea.get("approach"),
        "solution_difficulty": idea.get("difficulty"),
        "solution_status": idea.get("status"),
        "solution_upvotes": idea.get("upvotes"),
        "solution_comments": idea.get("comments"),
    }
    cleaned = {k: v for k, v in params.items() if v not in (None, "", [])}
    return build_page_url("how_can_ai_help", cleaned)


def build_action_button(label: str, href: str = "#") -> str:
    return f"<a class='neon-table-action' href='{html.escape(href)}'>{html.escape(label)}</a>"


def build_action_stack(primary: str, href: str, secondary: str = "View", secondary_href: str | None = None) -> str:
    target = secondary_href or href
    return (
        "<div class='action-stack'>"
        f"{build_action_button(primary, href)}"
        f"<a class='neon-action-secondary' href='{html.escape(target)}'>{html.escape(secondary)}</a>"
        "</div>"
    )


def build_action_triple_stack(
    primary: str,
    primary_href: str,
    secondary: str,
    secondary_href: str,
    tertiary: str,
    tertiary_href: str,
) -> str:
    """Render a 3-button stack: primary, secondary, tertiary."""
    return (
        "<div class='action-stack'>"
        f"{build_action_button(primary, primary_href)}"
        f"<a class='neon-action-secondary' href='{html.escape(secondary_href)}'>{html.escape(secondary)}</a>"
        f"<a class='neon-action-secondary' href='{html.escape(tertiary_href)}'>{html.escape(tertiary)}</a>"
        "</div>"
    )


def build_challenge_action(item: dict, help_href: str, convert_href: str) -> str:
    mode = str(item.get("preferred_action", "")).lower()
    if mode == "convert":
        return build_action_button("Convert", convert_href)
    if mode == "open":
        return build_action_button("Open", help_href)
    return build_action_stack("AI Can Help", help_href, "Convert", convert_href)


def render_star_rating(value: float | int | None) -> str:
    try:
        rating = max(0.0, min(5.0, float(value or 0)))
    except (TypeError, ValueError):
        rating = 0.0
    full = int(round(rating))
    stars = "★" * full + "☆" * (5 - full)
    return f"<span>{stars} <small style='color:#94a3b8;'>({rating:.1f})</small></span>"


def format_date(value: str | None) -> str:
    if not value:
        return "—"
    try:
        dt = datetime.fromisoformat(value.replace("Z", ""))
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return value[:10]


def render_neon_table(
    title: str,
    columns: List[str],
    rows: List[List[str]],
    empty_message: str,
    column_widths: List[str] | None = None,
) -> None:
    theme_class = "neon-table"
    if st.session_state.get("yes_theme", "dark") != "dark":
        theme_class += " light"
    col_count = len(columns)
    if column_widths and len(column_widths) == col_count:
        widths = " ".join(column_widths)
        grid_style = f"grid-template-columns: {widths};"
    else:
        grid_style = f"grid-template-columns: repeat({col_count}, minmax(140px, 1fr));"
    header_html = "".join(f"<div class='neon-table-cell'>{col}</div>" for col in columns)
    if rows:
        row_blocks = []
        for row in rows:
            cells = "".join(f"<div class='neon-table-cell'>{cell}</div>" for cell in row)
            row_blocks.append(f"<div class='neon-table-grid neon-table-row' style='{grid_style}'>{cells}</div>")
        rows_html = "".join(row_blocks)
    else:
        rows_html = f"<div class='neon-table-empty'>{empty_message}</div>"
    st.markdown(
        f"""
        <div class="{theme_class}">
            <div class="neon-table-title">{title}</div>
            <div class="neon-table-grid neon-table-header" style="{grid_style}">
                {header_html}
            </div>
            {rows_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# def render_builders_toolbox_table() -> None:
#     builder_entry = next(
#         (agent for agent in BUILDERS_TOOLBOX if agent.get("name", "").lower() == "agent builder"),
#         None,
#     )
#     if not builder_entry:
#         return
#     columns = ["Agent / Tool", "Reusable For", "🚀 Action"]
#     rows = [
#         [
#             html.escape(builder_entry["name"]),
#             html.escape(builder_entry["description"]),
#             build_action_button("Build new Agent", build_page_url("agent_builder")),
#         ]
#     ]
#     render_neon_table(
#         "🏗️ BUILDERS TOOLBOX : Reuse Existing AI Products to build New AI products",
#         columns,
#         rows,
#         "Use the Agent Builder to assemble a new AI product.",
#         column_widths=["1fr", "2.5fr", "0.8fr"],
#     )


def build_placeholder_submission_from_solution(solution: dict) -> dict:
    return {
        "title": solution.get("challenge"),
        "description": solution.get("approach"),
        "submitter": {
            "name": solution.get("helper_submitter") or "—",
            "department": "",
            "region": "",
        },
        "category": solution.get("category") or "—",
        "difficulty": solution.get("difficulty", "Medium"),
        "attachments": [],
        "urgency": 0,
        "impact_score": 0,
        "similar_agents": [],
        "upvotes": 0,
        "comments": 0,
        "preferred_action": "open",
    }


def load_matched_challenge_solution_pairs(limit: int = 10) -> list[tuple[dict | None, dict | None]]:
    submissions_source = load_meta_records("how_ai_help_submissions.json", SAMPLE_HELP_SUBMISSIONS)
    solutions_source = load_meta_records("how_ai_help_solutions.json", SAMPLE_HELP_SOLUTIONS)
    title_to_submission: dict[str, dict] = {}
    for submission in submissions_source:
        title = submission.get("title")
        if title:
            title_to_submission[title.strip().lower()] = submission
    pairs: list[tuple[dict | None, dict | None]] = []
    seen_ids: set[str] = set()
    for solution in solutions_source:
        challenge_title = str(solution.get("challenge", "")).strip()
        if not challenge_title:
            continue
        submission = title_to_submission.get(challenge_title.lower())
        if not submission:
            placeholder = build_placeholder_submission_from_solution(solution)
            submission = placeholder
        seen_ids.add(ensure_challenge_anchor(submission))
        pairs.append((submission, solution))
        if len(pairs) >= limit:
            break
    if len(pairs) < limit:
        for submission in submissions_source:
            if ensure_challenge_anchor(submission) in seen_ids:
                continue
            pairs.append((submission, None))
            seen_ids.add(ensure_challenge_anchor(submission))
            if len(pairs) >= limit:
                break
    return pairs[:limit]

def render_builders_toolbox_table() -> None:
    builder_entry = next(
        (agent for agent in BUILDERS_TOOLBOX if agent.get("name", "").lower() == "agent builder"),
        None,
    )
    if not builder_entry:
        return
    columns = ["Agent / Tool", "Reusable For", "🚀 Action"]
    rows = [
        [
            html.escape(builder_entry["name"]),
            html.escape(builder_entry["description"]),
            build_action_button("Build new Agent", build_page_url("agent_builder")),
        ]
    ]
    render_neon_table(
        "🏗️ BUILDERS TOOLBOX : Reuse Existing AI Products to build New AI products",
        columns,
        rows,
        "Use the Agent Builder to assemble a new AI product.",
        column_widths=["1fr", "2.5fr", "0.8fr"],
    )

def render_help_submission_table() -> list[dict]:
    submissions = load_meta_records("how_ai_help_submissions.json", CHALLENGE_FEED_ROWS)
    solutions = load_meta_records("how_ai_help_solutions.json", PROPOSED_SOLUTION_ROWS)
    helper_map: dict[str, set[str]] = {}
    for sol in solutions:
        title = str(sol.get("challenge", "")).strip().lower()
        helper_name = sol.get("helper") or sol.get("author")
        if title and helper_name:
            helper_map.setdefault(title, set()).add(str(helper_name))
    rows: list[list[str]] = []
    for item in submissions:
        submitter = item.get("submitter") or {}
        item_title_lower = str(item.get("title", "")).strip().lower()
        ensure_challenge_anchor(item)
        submitter_text = (
            f"{html.escape(submitter.get('name', '—'))}"
            f"<br><small>{html.escape(submitter.get('department', '—'))} • {html.escape(submitter.get('region', '—'))}</small>"
        )
        submitter_dept = submitter.get("department", "—")
        submitter_region = submitter.get("region", "—")
        metadata_val = item.get("metadata_display") or f"{submitter_dept} • {submitter_region}"
        metadata = html.escape(metadata_val)
        attachments = describe_attachment_list(item.get("attachments"))
        helpers = sorted(helper_map.get(item_title_lower, []))
        helpers_html = format_tags(helpers) if helpers else "—"
        similar = format_tags(item.get("similar_agents"))
        detail_url = build_challenge_view_url(item)
        action_html = build_action_button(
            "AICANHELP",
            build_page_url(
                "how_can_ai_help",
                {
                    "challenge_title": item.get("title"),
                    "solution_challenge": item.get("title"),
                },
            ),
        )

        rows.append(
            [
                html.escape(item.get("title", "—")),
                submitter_text,
                metadata,
                attachments,
                f"{item.get('urgency', 0):.1f}",
                f"{item.get('impact_score', 0):.1f}",
                similar,
                helpers_html,
                action_html,
            ]
        )
    render_builders_toolbox_table()

    submit_uri = build_page_url("how_can_ai_help")
    st.markdown(
        f"<div style='margin-bottom:0.75rem; text-align:right;'><a class='nav-button' style='display:inline-block;max-width:260px;text-align:center;' href='{submit_uri}' target='_blank'>🔥 Submit Challenge</a></div>",
        unsafe_allow_html=True,
    )
    columns = [
        "📝 Challenge",
        "🧍 Submitter",
        "🧠 Metadata",
        "📎 Attachments",
        "⚡ Urgency",
        "🎯 Impact",
        "🤖 Similar Existing Products",
        "🤝 Helpers",
        "🚀 Action",
    ]
    render_neon_table(
        "🔥 TABLE 1 — Current Challenges and Pain Points / Builders just click on AICANHELP to Take Action",
        columns,
        rows,
        "Fully aligned to the AI Solution list.",
    )
    st.markdown(
        "<p style='margin-top:0.5rem; color:rgba(226,232,240,0.85); font-size:0.9rem;'>Builders it's time to help by clicking</p>",
        unsafe_allow_html=True,
    )
    return submissions


def render_help_solution_table() -> None:
    rows: list[list[str]] = []
    submissions = load_meta_records("how_ai_help_submissions.json", CHALLENGE_FEED_ROWS)
    submission_titles = {str(item.get("title", "")).strip().lower() for item in submissions if item.get("title")}
    solutions = load_meta_records("how_ai_help_solutions.json", PROPOSED_SOLUTION_ROWS)
    for entry in solutions:
        challenge_title = str(entry.get("challenge", "")).strip().lower()
        if submission_titles and challenge_title not in submission_titles:
            continue
        ensure_solution_anchor(entry)
        detail_url = build_solution_view_url(entry)
        submitter_name = entry.get("submitter") or entry.get("author") or "—"
        helper_name = entry.get("helper") or entry.get("author") or "—"
        rows.append(
            [
                html.escape(entry.get("challenge", "—")),
                html.escape(submitter_name),
                html.escape(helper_name),
                html.escape(entry.get("approach", "—")),
                html.escape(", ".join(entry.get("ai_tools_used", []))) if entry.get("ai_tools_used") else "—",
                html.escape(", ".join(entry.get("new_ai_tools_created", []))) if entry.get("new_ai_tools_created") else "—",
                build_status_badge(entry.get("status", "Draft"), "info"),
                build_action_button("View Idea", detail_url),
            ]
        )
    columns = [
        "📝 Challenge",
        "🧍 Submitter",
        "🤝 Helper",
        "🧩 Proposed AI Approach",
        "🤖 AI tools Reused",
        "🛠️ New AI Tools created",
        "📊 Status",
        "🚀 Action",
    ]
    solution_uri = build_page_url("solutionform")
    st.markdown(
        f"<div style='margin-bottom:0.75rem; text-align:right;'><a class='nav-button nav-button-blue' style='display:inline-block;max-width:260px;text-align:center;' href='{solution_uri}' target='_blank'>🤝 Propose a Solution</a></div>",
        unsafe_allow_html=True,
    )
    render_neon_table(
        "🧩 TABLE 2 — Proposed Cures and Solutions",
        columns,
        rows,
        "Every challenge above has a matching solution below.",
    )


def render_challenge_form_cards(challenges: list[dict]) -> None:
    if not challenges:
        return
    st.markdown(
        """
        <div class="neon-table" style="margin-top:1.5rem;">
            <div class="neon-table-title">🧾 Challenge Intake Forms (Mockups)</div>
            <p style="color:rgba(148,163,184,0.9);margin-bottom:0.5rem;">
                Each card opens the dedicated challenge intake workspace with details prefilled from the mock submissions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    theme_light = st.session_state.get("yes_theme", "dark") != "dark"
    st.markdown("<div class='challenge-form-grid'>", unsafe_allow_html=True)
    body_color = "#0f172a" if theme_light else "rgba(226,232,240,0.9)"
    signal_color = "#1e293b" if theme_light else "rgba(226,232,240,0.85)"
    for item in challenges:
        submitter = item.get("submitter", {}) or {}
        challenge_launch = build_challenge_form_url(item)
        challenge_href = ensure_absolute_page_url(challenge_launch)
        challenge_id = ensure_challenge_anchor(item)
        convert_params = {
            "convert_submission_id": challenge_id,
            "source_submission_id": challenge_id,
            "convert_submission_title": item.get("title"),
            "convert_submission_description": item.get("description"),
            "convert_submission_category": item.get("category"),
            "convert_submission_difficulty": item.get("difficulty"),
            "convert_submission_submitter": submitter.get("name"),
            "convert_submission_department": submitter.get("department"),
            "convert_submission_region": submitter.get("region"),
            "convert_submission_upvotes": item.get("upvotes"),
            "convert_submission_comments": item.get("comments"),
            "convert_submission_urgency": item.get("urgency"),
            "convert_submission_impact": item.get("impact_score"),
        }
        convert_href = build_page_url("project_hub", convert_params)
        convert_launch = ensure_absolute_page_url(convert_href)
        attachments = describe_attachment_list(item.get("attachments"))
        similar = format_tags(item.get("similar_agents"))
        metadata = (
            f"{build_status_badge(item.get('category', 'General'), 'info')} "
            f"{build_status_badge(item.get('difficulty', 'Medium'), 'warning')}"
        )
        card_class = "challenge-form-card light" if theme_light else "challenge-form-card"
        st.markdown(
            f"""
            <div class="{card_class}">
                <h4>{html.escape(item.get('title', 'Untitled'))}</h4>
                <div class="challenge-form-meta">
                    {html.escape(submitter.get('name', '—'))} • {html.escape(submitter.get('department', '—'))} • {html.escape(submitter.get('region', '—'))}
                </div>
                <div>{metadata}</div>
                <div style="margin-top:0.5rem;color:{body_color};">{html.escape(item.get('description', '')[:160])}</div>
                {attachments}
                <div style="font-size:0.9rem;color:{signal_color};">
                    ⚡ {item.get('urgency', 0):.1f} • 🎯 {item.get('impact_score', 0):.1f} • 👍 {item.get('upvotes', 0)} • 💬 {item.get('comments', 0)}
                </div>
                <div style="margin-top:0.3rem;">{similar}</div>
                <div class="challenge-form-actions">
                    <a class="primary" href="{challenge_href}" target="_blank">AI Can Help</a>
                    <a class="secondary" href="{convert_launch}" target="_blank">Convert to Project</a>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def render_project_hub_section() -> None:
    projects = load_meta_records("projects.json", SAMPLE_PROJECTS)
    rows: list[list[str]] = []
    for project in projects[:5]:
        owners = project.get("authors") or project.get("owner_name") or project.get("owner_email")
        if isinstance(owners, (list, tuple, set)):
            owner_text = ", ".join(str(owner) for owner in owners if owner)
        else:
            owner_text = owners or "—"
        area = project.get("business_area") or project.get("category") or "—"
        status_value = project.get("phase") or project.get("status") or "Idea"
        status_text = str(status_value)
        status_variant = "success" if status_text.lower() in {"mvp", "launched", "production", "prod"} else "info"
        created = format_date(project.get("created_at"))
        signals = f"👍 {project.get('upvotes', 0)} • 💬 {project.get('comments', 0)}"
        summary = project.get("summary") or project.get("description") or ""
        description = html.escape(summary[:120] + ("…" if summary and len(summary) > 120 else ""))
        project_launch = build_project_view_url(project)
        rows.append(
            [
                f"{html.escape(project.get('title', '—'))}<br><small>{description}</small>",
                html.escape(owner_text),
                html.escape(area),
                build_status_badge(status_text, status_variant),
                created,
                signals,
                build_action_button("View Project", project_launch),
            ]
        )
    columns = [
        "🧱 Project",
        "👥 Owners",
        "🏢 Area",
        "📊 Phase",
        "📅 Created",
        "⭐ Signals",
        "🚀 Action",
    ]
    render_neon_table("📁 Project Hub — Live POC Nursery ", columns, rows, "Add your first project to the hub.")


def render_help_insights(submissions: list[dict]) -> None:
    total = len(submissions)
    top = sorted(submissions, key=lambda x: x.get("upvotes", 0), reverse=True)[:3]
    highlights = "".join(
        f"<li><strong>{html.escape(item.get('title','—'))}</strong> — 👍 {item.get('upvotes',0)} | ⚡ {item.get('urgency',0):.1f} | 🎯 {item.get('impact_score',0):.1f}</li>"
        for item in top
    )
    submit_href = build_page_url("how_can_ai_help")
    st.markdown(
        f"""
        <div style="margin-bottom:1rem; text-align:right;">
            <a class="primary" href="{submit_href}" target="_blank">Submit your challenge</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="neon-table" style="margin-top:1.5rem;">
            <div class="neon-table-title">🏆 Kaggle-Style Leaderboard Signals</div>
            <ul style="color:rgba(226,232,240,0.9);line-height:1.7;margin-bottom:1rem;">
                {highlights}
            </ul>
            <p style="color:rgba(148,163,184,0.95);">
                Total challenges: <strong>{total}</strong> • Auto-computed ranking blends upvotes, urgency, impact, and discussion velocity.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_ai_auto_blueprint() -> None:
    st.markdown(
        """
        <div class="neon-table" style="margin-top:1.5rem;">
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


def render_help_hub_layer(auth_user: dict | None = None) -> None:
    # st.markdown(
    #     """
    #     <div class=\"nav-mini-block\" style=\"margin-top:1.25rem;\">
    #         <div style=\"font-weight:700;font-size:1rem;\">👤 Builder team directory</div>
    #         <div class=\"nav-mini-desc\">Discover multi-skill Rackers powering every build.</div>
    #         <div style=\"margin-top:0.5rem;font-weight:600;\">👤 Our Human Stack — Your Champions</div>
    #     </div>
    #     """,
    #     unsafe_allow_html=True,
    # )
    render_future_modules()
    render_human_stack_table()
    st.markdown("<div class='neon-divider'></div>", unsafe_allow_html=True)

    render_help_insights(CHALLENGE_FEED_ROWS)
    render_ai_auto_blueprint()

    submissions = render_help_submission_table()
    render_help_solution_table()
    render_project_hub_section()
    # Duplicate card layout (Challenge Intake Forms) removed to keep focus on Table 1 feed.
    # render_challenge_form_cards(submissions)

def render_human_stack_table():
    # 1) Load + merge humans.json with SAMPLE_HUMANS plus persistence layer
    records = load_human_stack_directory_records()
    AI_SERVICE_TAGS = [
        "billing-formatter",
        "reconciliation-agent",
        "fp&a-forecast",
        "invoice-anomaly",
        "renewal-risk",
        "proposal-writer",
        "pricing-guardrails",
        "nba-recommender",
        "ticket-triage",
        "escalation-predictor",
        "support-copilot",
        "incident-summarizer",
        "openstack-validator",
        "capacity-forecast",
        "drift-detector",
        "sre-playbooks",
        "soc-reporter",
        "alert-dedup",
        "phishing-triage",
        "policy-checker",
        "onboarding-router",
        "talent-matcher",
        "skills-graph",
        "engagement-sentiment",
        "contract-extractor",
        "risk-summarizer",
        "policy-bot",
        "dpa-checker",
        "prd-copilot",
        "feature-impact",
        "campaign-writer",
        "experiment-planner",
        "feature-store",
        "model-monitor",
        "prompt-library",
        "rag-builder",
        "staffing-forecast",
        "routing-optimizer",
        "sla-monitor",
        "vendor-scorecard",
        "ceo-dashboard",
        "kpi-briefs",
        "scenario-simulator",
        "risk-radar",
    ]
    merged: list[dict] = []
    seen: set[str] = set()

    for person in records:
        key = (person.get("id") or person.get("email") or person.get("name") or "").lower()
        if key:
            seen.add(key)
        merged.append(person)

    for sample in SAMPLE_HUMANS:
        key = sample.get("name", "").lower()
        if key and key in seen:
            continue
        merged.append(sample)
        if key:
            seen.add(key)

    records = merged

    # Ensure every profile has AI services; if missing, assign deterministic picks from the taxonomy
    for person in records:
        ai_services = person.get("ai_services") or []
        if not ai_services:
            seed_val = int(hashlib.sha1(str(person.get("name") or person.get("email") or person.get("id") or "").encode("utf-8", "ignore")).hexdigest(), 16)
            assigned = [AI_SERVICE_TAGS[(seed_val + i) % len(AI_SERVICE_TAGS)] for i in range(3)]
            person["ai_services"] = assigned

    st.markdown(FEEDBACK_BLOCK_CSS, unsafe_allow_html=True)

    # 2) Build the skill / service / department universe for the search bar
    all_skills: set[str] = set()
    all_services: set[str] = set()
    all_departments: set[str] = set()

    for person in records:
        # ---- Skills ----
        skills = person.get("skills") or []
        if isinstance(skills, str):
            skills = [skills]
        for s in skills:
            if s:
                all_skills.add(str(s))

        # ---- AI services attached to this profile ----
        services = person.get("ai_services") or []
        if isinstance(services, str):
            services = [services]
        for svc in services:
            if svc:
                all_services.add(str(svc))

        # ---- Department ----
        dept = person.get("department")
        if dept:
            all_departments.add(str(dept))

    # Optionally enrich services with the global AI service catalog if it exists
    try:
        catalog = AI_SERVICE_CATALOG  # type: ignore[name-defined]
    except NameError:
        catalog = []

    for svc in catalog or []:
        name = svc.get("name")
        if name:
            all_services.add(str(name))
        for tag in svc.get("search_tags", []) or []:
            if tag:
                all_services.add(str(tag))

    sorted_skills = sorted(all_skills)
    sorted_services = sorted(all_services)
    sorted_departments = sorted(all_departments)

    # Skills ∪ AI-services ∪ Departments → one unified search list
    search_options = sorted(set(sorted_skills) | set(sorted_services) | set(sorted_departments))

    # 3) Header + search UI
    st.markdown(
        """
        <h3 style="margin-bottom:0.5rem;">👥 Human Stack Directory</h3>
        <p style="color:#94a3b8; font-size:0.95rem; margin-bottom:1rem;">
            Find the right people to help you be GREAT. Filter by <b>skills</b>, 
            <b>AI-augmented services / products</b>, or <b>department</b>, then open their profile.
        </p>
        """,
        unsafe_allow_html=True,
    )

    col_search, col_stats = st.columns([3, 1])
    with col_search:
        selected_filters = st.multiselect(
            "Search by skills, products, or department:",
            options=search_options,
            default=[],
            placeholder="e.g. AI Billing Reconciliation, Ticket Triage Copilot, OpenStack, Finance …",
            label_visibility="collapsed",
        )
    with col_stats:
        st.markdown(
            f"<div style='text-align:right; padding-top:10px; color:#00f2ff; font-weight:700;'>{len(records)} Profiles Active</div>",
            unsafe_allow_html=True,
        )

    # 4) Filter records based on selected filters (skills OR ai_services OR department)
    if selected_filters:
        selected_set = set(selected_filters)
        filtered: list[dict] = []
        for person in records:
            skills = person.get("skills") or []
            if isinstance(skills, str):
                skills = [skills]

            services = person.get("ai_services") or []
            if isinstance(services, str):
                services = [services]

            dept = person.get("department") or ""

            # Tags that represent this person for filtering
            tag_set = set(str(s) for s in skills) | set(str(svc) for svc in services)
            if dept:
                tag_set.add(str(dept))

            # If any selected tag matches, keep the person
            if tag_set & selected_set:
                filtered.append(person)
    else:
        filtered = records

    # 5) Build table rows
    feedback_store = load_human_feedback_reviews()
    rows: list[list[str]] = []
    for person in filtered:
        seed_val = int(hashlib.sha1(str(person.get("name") or person.get("email") or person.get("id") or "").encode("utf-8", "ignore")).hexdigest(), 16)
        fallback_rating = 3 + (seed_val % 3)
        profile_key = str(person.get("id") or person.get("email") or person.get("name") or "").strip()
        reviews = feedback_store.get(profile_key, [])
        latest_review = reviews[-1] if reviews else None
        review_count = len(reviews)
        rating_score = fallback_rating
        if latest_review:
            rating_score = parse_rating_value(latest_review.get("rating"), fallback_rating)
        bounded_rating = max(0, min(5, rating_score))
        if review_count:
            feedback_label = f"{review_count} feedback"
            if review_count != 1:
                feedback_label += "s"
        else:
            feedback_label = "No feedback yet"
        latest_comment = str(latest_review.get("comment") if latest_review else "")
        badge_html = render_feedback_block(bounded_rating, latest_comment)
        badge_html += (
            f"<div style='font-size:12px; color:#94a3b8; margin-top:2px;'>"
            f"{bounded_rating}/5 · 💬 {feedback_label}"
            "</div>"
        )

        profile_href = build_page_url(
            "human_stack",
            {
                "profile_id": person.get("id"),
                "profile_email": person.get("email"),
            },
        )

        rows.append(
            [
                html.escape(person.get("name", "—")),
                html.escape(person.get("department", "—")),
                html.escape(person.get("region", "—")),
                format_tags(person.get("skills")),
                format_tags(person.get("ai_services")),
                badge_html,
                build_action_button("View Profile", profile_href),
            ]
        )

    # 6) Columns + render
    columns = [
        "👤 Name",
        "🏢 Department",
        "🌍 Region",
        "🧩 Skills / Expertise",
        "🧱 Products Built",
        "🏅 Badge of Honor & Feedback",
        "🚀 Action",
    ]

    total_profiles = len(rows)
    filter_suffix = "" if not selected_filters else f" (filtered by {len(selected_filters)} tag(s))"
    table_title = f"👥 Human Stack Directory — {total_profiles} Profiles{filter_suffix}"

    render_neon_table(
        table_title,
        columns,
        rows,
        "No Rackers match those skills or service needs yet. Try a different combination.",
        column_widths=[
            "minmax(160px, 1fr)",
            "minmax(150px, 0.9fr)",
            "minmax(140px, 0.9fr)",
            "minmax(220px, 1.3fr)",
            "minmax(320px, 2fr)",  # Products built column wider for one-line tags
            "minmax(200px, 1.1fr)",
            "minmax(140px, 0.9fr)",
        ],
    )

# def render_human_stack_table():
#     # 1) Load + merge humans.json with SAMPLE_HUMANS (keep your existing logic)
#     records = load_meta_records("humans.json", SAMPLE_HUMANS)
#     merged: list[dict] = []
#     seen: set[str] = set()
#     for person in records:
#         key = (person.get("id") or person.get("email") or person.get("name") or "").lower()
#         if key:
#             seen.add(key)
#         merged.append(person)
#     for sample in SAMPLE_HUMANS:
#         key = sample.get("name", "").lower()
#         if key and key in seen:
#             continue
#         merged.append(sample)
#         if key:
#             seen.add(key)
#     records = merged

#     # 2) Build the skill universe for the search bar
#     all_skills: set[str] = set()
#     all_services: set[str] = set()
#     all_departments: set[str] = set()
#     for person in records:
#         skills = person.get("skills") or []
#         if isinstance(skills, str):
#             skills = [skills]
#         for s in skills:
#             if s:
#                 all_skills.add(str(s))
#         services = person.get("ai_services") or []
#         if isinstance(services, str):
#             services = [services]
#         for svc in services:
#             if svc:
#                 all_services.add(str(svc))
#         dept = person.get("department")
#         if dept:
#             all_departments.add(str(dept))
#     sorted_skills = sorted(all_skills)
#     sorted_services = sorted(all_services)
#     sorted_departments = sorted(all_departments)
#     search_options = sorted(
#         set(sorted_skills) | set(sorted_services) | set(sorted_departments)
#     )

#     # 3) Header + search UI
#     st.markdown(
#         """
#         <h3 style="margin-bottom:0.5rem;">👥 Human Stack Directory</h3>
#         <p style="color:#94a3b8; font-size:0.95rem; margin-bottom:1rem;">
#             Find the right people to help you be GREAT. Filter by skills, check contributions, and open their profile.
#         </p>
#         """,
#         unsafe_allow_html=True,
#     )

#     col_search, col_stats = st.columns([3, 1])
#     with col_search:
#         selected_filters = st.multiselect(
#             "Search by skills, products, or department:",
#             options=search_options,
#             default=[],
#             placeholder="billing-formatter, support-copilot, OpenStack, Finance …",
#             label_visibility="collapsed",
#         )
#     with col_stats:
#         st.markdown(
#             f"<div style='text-align:right; padding-top:10px; color:#00f2ff; font-weight:700;'>{len(records)} Profiles Active</div>",
#             unsafe_allow_html=True,
#         )

#     # 4) Filter records based on selected filters (skills OR ai_services OR department)
#     if selected_filters:
#         selected_set = set(selected_filters)
#         filtered: list[dict] = []
#         for person in records:
#             skills = person.get("skills") or []
#             if isinstance(skills, str):
#                 skills = [skills]
#             services = person.get("ai_services") or []
#             if isinstance(services, str):
#                 services = [services]
#             dept = person.get("department") or ""
#             tag_set = set(str(s) for s in skills) | set(str(svc) for svc in services)
#             if dept:
#                 tag_set.add(str(dept))
#             if tag_set & selected_set:
#                 filtered.append(person)
#     else:
#         filtered = records

#     # 5) Build table rows
#     rows: list[list[str]] = []
#     for person in filtered:
#         contributions = person.get("contributions") or {}
#         project_count = contributions.get("projects", 0)
#         agent_count = contributions.get("agents", 0)
#         profile_href = build_page_url(
#             "human_stack",
#             {
#                 "profile_id": person.get("id"),
#                 "profile_email": person.get("email"),
#             },
#         )

#         rows.append(
#             [
#                 html.escape(person.get("name", "—")),
#                 html.escape(person.get("department", "—")),
#                 html.escape(person.get("region", "—")),
#                 format_tags(person.get("skills")),
#                 format_tags(person.get("ai_services")),
#                 f"{format_date(person.get('created_at'))} / {format_date(person.get('updated_at'))}",
#                 build_status_badge(person.get("sme_level", "Skilled"), "success"),
#                 build_action_button("View Profile", profile_href),
#             ]
#         )

#     # 6) Columns + render
#     columns = [
#         "👤 Name",
#         "🏢 Department",
#         "🌍 Region",
#         "🧩 Skills / Expertise",
#         "🧱 Projects Built",
#         "📅 Joined / Updated",
#         "⭐ SME Level",
#         "🚀 Action",
#     ]
#     total_profiles = len(rows)
#     filter_suffix = "" if not selected_filters else f" (filtered by {len(selected_filters)} tag(s))"
#     table_title = f"👥 Human Stack Directory — {total_profiles} Profiles{filter_suffix}"

#     render_neon_table(table_title, columns, rows, "No Rackers match those skills yet. Try a different combination.")


# def render_human_stack_table():
#     # 1) Load + merge humans.json with SAMPLE_HUMANS (keep your existing logic)
#     records = load_meta_records("humans.json", SAMPLE_HUMANS)
#     merged: list[dict] = []
#     seen: set[str] = set()
#     for person in records:
#         key = (person.get("id") or person.get("email") or person.get("name") or "").lower()
#         if key:
#             seen.add(key)
#         merged.append(person)
#     for sample in SAMPLE_HUMANS:
#         key = sample.get("name", "").lower()
#         if key and key in seen:
#             continue
#         merged.append(sample)
#         if key:
#             seen.add(key)
#     records = merged

#     # 2) Build the skill universe for the search bar
#     all_skills: set[str] = set()
#     for person in records:
#         skills = person.get("skills") or []
#         if isinstance(skills, str):
#             skills = [skills]
#         for s in skills:
#             if s:
#                 all_skills.add(str(s))
#     sorted_skills = sorted(all_skills)

#     # 3) Header + search UI
#     st.markdown(
#         """
#         <h3 style="margin-bottom:0.5rem;">👥 Human Stack Directory</h3>
#         <p style="color:#94a3b8; font-size:0.95rem; margin-bottom:1rem;">
#             Find the right people to help you be GREAT. Filter by skills, check contributions, and open their profile.
#         </p>
#         """,
#         unsafe_allow_html=True,
#     )

#     col_search, col_stats = st.columns([3, 1])
#     with col_search:
#         selected_skills = st.multiselect(
#             "Search skills (Add/Remove chips):",
#             options=sorted_skills,
#             default=[],
#             placeholder="Type a skill (e.g., OpenStack, Billing, Generative AI)…",
#             label_visibility="collapsed",
#         )
#     with col_stats:
#         st.markdown(
#             f"<div style='text-align:right; padding-top:10px; color:#00f2ff; font-weight:700;'>{len(records)} Profiles Active</div>",
#             unsafe_allow_html=True,
#         )

#     # 4) Filter records based on selected skills (OR logic)
#     if selected_skills:
#         selected_set = set(selected_skills)
#         filtered: list[dict] = []
#         for person in records:
#             skills = person.get("skills") or []
#             if isinstance(skills, str):
#                 skills = [skills]
#             skill_set = set(str(s) for s in skills)
#             if skill_set & selected_set:
#                 filtered.append(person)
#     else:
#         filtered = records

#     # 5) Build table rows
#     rows: list[list[str]] = []
#     for person in filtered:
#         contributions = person.get("contributions") or {}
#         project_count = contributions.get("projects", 0)
#         agent_count = contributions.get("agents", 0)
#         profile_href = build_page_url(
#             "human_stack",
#             {
#                 "profile_id": person.get("id"),
#                 "profile_email": person.get("email"),
#             },
#         )

#         summary = f"🧱 {project_count} / 🤖 {agent_count}"
#         ai_contrib = person.get("ai_contributions")
#         if ai_contrib:
#             summary = f"{summary}<br><small>{html.escape(ai_contrib)}</small>"

#         rows.append(
#             [
#                 html.escape(person.get("name", "—")),
#                 html.escape(person.get("department", "—")),
#                 html.escape(person.get("region", "—")),
#                 format_tags(person.get("skills")),
#                 summary,
#                 f"{format_date(person.get('created_at'))} / {format_date(person.get('updated_at'))}",
#                 build_status_badge(person.get("sme_level", "Skilled"), "success"),
#                 build_action_button("View Profile", profile_href),
#             ]
#         )

#     # 6) Columns + render
#     columns = [
#         "👤 Name",
#         "🏢 Department",
#         "🌍 Region",
#         "🧩 Skills / Expertise",
#         "🧪 Contributions",
#         "📅 Joined / Updated",
#         "⭐ SME Level",
#         "🚀 Action",
#     ]
#     total_profiles = len(rows)
#     filter_suffix = "" if not selected_skills else f" (filtered by {len(selected_skills)} skill(s))"
#     table_title = f"👥 Human Stack Directory — {total_profiles} Profiles{filter_suffix}"

#     render_neon_table(table_title, columns, rows, "No Rackers match those skills yet. Try a different combination.")


# def render_human_stack_table():
#     records = load_meta_records("humans.json", SAMPLE_HUMANS)

#     # ---------------------------------------------------------
#     # STEP 1 — MERGE FIRST
#     # ---------------------------------------------------------
#     merged, seen = [], set()
#     for person in records:
#         key = (person.get("id") or person.get("email") or person.get("name") or "").lower()
#         if key:
#             seen.add(key)
#         merged.append(person)

#     for sample in SAMPLE_HUMANS:
#         key = sample.get("name", "").lower()
#         if key and key not in seen:
#             merged.append(sample)
#             seen.add(key)

#     records = merged

#     # ---------------------------------------------------------
#     # STEP 2 — RED CHIP SEARCH BAR (NO JS)
#     # ---------------------------------------------------------
#     st.markdown("### 🔎 Search champions by skillset")

#     # CSS
#     st.markdown("""
#     <style>
#     .chip {
#         background:#ff3b30; color:white; padding:6px 12px;
#         border-radius:18px; margin:4px; display:inline-flex;
#         gap:6px; align-items:center; font-size:0.85rem;
#     }
#     .chip-x {
#         font-weight:bold; cursor:pointer;
#     }
#     </style>
#     """, unsafe_allow_html=True)

#     # Collect skills
#     all_skills = {s.strip() for p in records for s in (p.get("skills") or []) if s.strip()}

#     # State
#     st.session_state.setdefault("chip_skills", [])
#     chips = st.session_state["chip_skills"]

#     # TEXT FIELD + ADD BUTTON
#     new_skill = st.text_input("Add skill filter:", placeholder="ex: AI, FinOps, Python…")

#     add_col, _ = st.columns([1,4])
#     with add_col:
#         if st.button("➕ Add skill"):
#             if new_skill and new_skill not in chips:
#                 chips.append(new_skill)
#                 st.session_state["chip_skills"] = chips

#     # DISPLAY CHIPS
#     if chips:
#         chip_html = "".join(
#             f"<span class='chip'>{skill} "
#             f"<span class='chip-x'>×</span></span>"
#             for skill in chips
#         )
#         st.markdown(chip_html, unsafe_allow_html=True)

#         # REMOVE CHIP BUTTONS
#         for skill in chips:
#             if st.button(f"Remove {skill}", key=f"rm_{skill}"):
#                 chips.remove(skill)
#                 st.session_state["chip_skills"] = chips
#                 st.rerun()

#     # ---------------------------------------------------------
#     # FILTER RECORDS
#     # ---------------------------------------------------------
#     if chips:
#         records = [
#             p for p in records
#             if any(skill in (p.get("skills") or []) for skill in chips)
#         ]

#     # ---------------------------------------------------------
#     # STEP 3 — BUILD TABLE (unchanged)
#     # ---------------------------------------------------------
#     rows = []
#     for person in records:
#         contributions = person.get("contributions") or {}
#         summary = f"🧱 {contributions.get('projects', 0)} / 🤖 {contributions.get('agents', 0)}"
#         ai_contrib = person.get("ai_contributions")
#         if ai_contrib:
#             summary += f"<br><small>{html.escape(ai_contrib)}</small>"

#         profile_href = build_page_url(
#             "human_stack",
#             {"profile_id": person.get("id"), "profile_email": person.get("email")},
#         )

#         rows.append([
#             html.escape(person.get("name", "—")),
#             html.escape(person.get("department", "—")),
#             html.escape(person.get("region", "—")),
#             format_tags(person.get("skills")),
#             summary,
#             f"{format_date(person.get('created_at'))} / {format_date(person.get('updated_at'))}",
#             build_status_badge(person.get("sme_level", "Skilled"), "success"),
#             build_action_button("View Profile", profile_href),
#         ])

#     # ---------------------------------------------------------
#     # STEP 4 — RENDER TABLE
#     # ---------------------------------------------------------
#     render_neon_table(
#         "👤 Our Human Stack — Your Champions",
#         ["👤 Name","🏢 Department","🌍 Region","🧩 Skills / Expertise",
#          "🧪 Projects Built","📅 Joined / Updated","⭐ SME Level","🚀 Action"],
#         rows,
#         "No Rackers have registered yet.",
#         column_widths=[
#             "minmax(180px, 1fr)", "minmax(150px, 0.9fr)", "minmax(120px, 0.8fr)",
#             "minmax(260px, 1.6fr)", "minmax(170px, 1fr)", "minmax(190px, 1fr)",
#             "minmax(130px, 0.7fr)", "minmax(150px, 0.8fr)"
#         ],
#     )


# def render_human_stack_table():
#     records = load_meta_records("humans.json", SAMPLE_HUMANS)

#     # ---------------------------------------------------------
#     # STEP 1 — MERGE FIRST (avoids ellipsis + stray rows)
#     # ---------------------------------------------------------

#     merged: list[dict] = []
#     seen: set[str] = set()
#     for person in records:
#         key = (person.get("id") or person.get("email") or person.get("name") or "").lower()
#         if key:
#             seen.add(key)
#         merged.append(person)
#     for sample in SAMPLE_HUMANS:
#         key = sample.get("name", "").lower()
#         if key and key in seen:
#             continue
#         merged.append(sample)
#         if key:
#             seen.add(key)
#     records = merged
#     rows = []
#     for person in records:
#         contributions = person.get("contributions") or {}
#         project_count = contributions.get("projects", 0)
#         agent_count = contributions.get("agents", 0)
#         profile_href = build_page_url(
#             "human_stack",
#             {
#                 "profile_id": person.get("id"),
#                 "profile_email": person.get("email"),
#             },
#         )
#         summary = f"🧱 {project_count} / 🤖 {agent_count}"
#         ai_contrib = person.get("ai_contributions")
#         if ai_contrib:
#             summary = f"{summary}<br><small>{html.escape(ai_contrib)}</small>"
#         rows.append(
#             [
#                 html.escape(person.get("name", "—")),
#                 html.escape(person.get("department", "—")),
#                 html.escape(person.get("region", "—")),
#                 format_tags(person.get("skills")),
#                 summary,
#                 f"{format_date(person.get('created_at'))} / {format_date(person.get('updated_at'))}",
#                 build_status_badge(person.get("sme_level", "Skilled"), "success"),
#                 build_action_button("View Profile", profile_href),
#             ]
#         )
#     columns = [
#         "👤 Name",
#         "🏢 Department",
#         "🌍 Region",
#         "🧩 Skills / Expertise",
#         "🧪 Contributions",
#         "📅 Joined / Updated",
#         "⭐ SME Level",
#         "🚀 Action",
#     ]
#     total_profiles = len(rows)
#     table_title = f"👤 Our Human Stack — Your Champions "
#     column_widths = [
#         "minmax(180px, 1fr)",  # name
#         "minmax(150px, 0.9fr)",  # department
#         "minmax(120px, 0.8fr)",  # region
#         "minmax(260px, 1.6fr)",  # skills / expertise
#         "minmax(170px, 1fr)",  # contributions summary
#         "minmax(190px, 1fr)",  # created/updated
#         "minmax(130px, 0.7fr)",  # level
#         "minmax(150px, 0.8fr)",  # action
#     ]
#     render_neon_table(
#         table_title,
#         columns,
#         rows,
#         "No Rackers have registered yet.",
#         column_widths=column_widths,
#     )


AGENT_PAGE_HINTS = {
    "agent_builder": "agent_builder",
    "hf_agent_wrapper": "hf_inspector",
    "agent_manager": "hf_inspector",
    "ceo_driver_dashboard": "ceo_driver_dashboard",
    "chatbot_assistant_agent": "chatbot_assistant",
    "it_troubleshooter_agent": "troubleshooter_agent",

}


# Map challenge titles -> page keys for dedicated spec pages
CHALLENGE_SPEC_PAGES: dict[str, str] = {
    "sync rax billing with customer billing format": "challenge_sync_rax_billing",
    "automate monthly billing reconciliation": "challenge_automate_monthly_billing_reconciliation",
    "predict ticket escalations for managed cloud": "challenge_predict_ticket_escalations_for_managed_cloud",
    "openstack deployment readiness validator": "challenge_openstack_deployment_readiness_validator",
    "customer renewal risk insights": "challenge_customer_renewal_risk_insights",
    "onboarding ticket auto-categorizer": "challenge_onboarding_ticket_auto_categorizer",
    "predict capacity exhaustion in infra": "challenge_predict_capacity_exhaustion_in_infra",
    "auto-generate security incident reports": "challenge_auto_generate_security_incident_reports",
    "reduce chat support handle time": "challenge_reduce_chat_support_handle_time",
    "auto-extract partner contract data": "challenge_auto_extract_partner_contract_data",
}


def get_challenge_spec_page(title: str | None) -> str | None:
    """Return the page key for the given challenge title, if known."""
    if not title:
        return None
    key = title.strip().lower()
    return CHALLENGE_SPEC_PAGES.get(key)


def normalize_launch_target(target: str | None) -> str:
    if not target:
        return ""
    value = target.strip()
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    if value.startswith("pages/"):
        key = Path(value).stem
        return PAGE_SLUGS.get(key, _slugify_page_stem(key))
    if value.startswith("/"):
        return value
    cleaned = value.strip("/")
    hinted = AGENT_PAGE_HINTS.get(cleaned)
    if hinted and hinted in PAGE_SLUGS:
        return PAGE_SLUGS[hinted]
    if cleaned in PAGE_SLUGS:
        return PAGE_SLUGS[cleaned]
    return f"/{cleaned}"


def generate_agent_page_candidates(route_name: str) -> list[str]:
    candidates: list[str] = []
    for name in (route_name, route_name.strip("_")):
        if name and name not in candidates:
            candidates.append(name)
    suffixes = ("_agent", "_dashboard", "_assistant", "_copilot", "_wizard")
    for suffix in suffixes:
        if route_name.endswith(suffix):
            trimmed = route_name[: -len(suffix)]
            if trimmed and trimmed not in candidates:
                candidates.append(trimmed)
    hinted = AGENT_PAGE_HINTS.get(route_name)
    if hinted and hinted not in candidates:
        candidates.append(hinted)
    return candidates


def resolve_agent_launch_path(route_name: str, overrides: dict[str, str]) -> str:
    for candidate in generate_agent_page_candidates(route_name):
        override = overrides.get(candidate)
        if override:
            return override
        hinted = AGENT_PAGE_HINTS.get(candidate)
        if hinted:
            hinted_override = overrides.get(hinted)
            if hinted_override:
                return hinted_override
            if hinted in PAGE_SLUGS:
                return PAGE_SLUGS[hinted]
        if candidate in PAGE_SLUGS:
            return PAGE_SLUGS[candidate]
    return ""


def render_agent_library_table(current_agents, feedback_data):
    records = load_meta_records("agents.json", [])
    rows = []

    if not records:
        fallback = []
        for agent_tuple in current_agents:
            author = "Rackers Lab"
            created_at = datetime.now().strftime("%Y-%m-%d")
            version = "v1.0.0"
            if len(agent_tuple) >= 10:
                (
                    sector,
                    industry,
                    agent_name,
                    desc,
                    status,
                    emoji,
                    requires_login,
                    author,
                    created_at,
                    version,
                ) = agent_tuple
            elif len(agent_tuple) == 7:
                sector, industry, agent_name, desc, status, emoji, requires_login = agent_tuple
            else:
                sector, industry, agent_name, desc, status, emoji = agent_tuple
                requires_login = False
            fallback.append(
                {
                    "industry": industry or sector,
                    "name": agent_name,
                    "author": author,
                    "created_at": created_at,
                    "version": version,
                    "description": desc,
                    "status": status,
                    "requires_login": requires_login,
                }
            )
        records = fallback

    base_launch_targets = {
        "agent_builder": "agent_builder",
        "hf_agent_wrapper": "hf_inspector",
        "hf_wrapper": "hf_inspector",
        "agent_manager": "hf_inspector",
        "chatbot_assistant": "chatbot_assistant",
        "real_estate_evaluator_agent": "real_estate_evaluator",
        "real_estate_evaluator": "real_estate_evaluator",
        "real_estate_evaluator_copy": "real_estate_evaluator_copy",
        "ceo_driver_dashboard": "ceo_driver_dashboard",

    }
    launch_overrides: dict[str, str] = {}
    for key, raw_target in base_launch_targets.items():
        normalized = normalize_launch_target(raw_target)
        if normalized:
            launch_overrides[key] = normalized
    for key, raw_target in CUSTOM_AGENT_LAUNCHES.items():
        normalized = normalize_launch_target(raw_target)
        if normalized:
            launch_overrides[key] = normalized

    for agent in records:
        name = agent.get("name") or agent.get("agent")
        industry = agent.get("industry") or agent.get("sector", "Cross-Industry")
        description = agent.get("description", "")
        route_name = compute_route_name(name or "agent")
        fb = feedback_data.get(name, {"rating": 0, "users": 0, "comments": []})
        rating_html = render_star_rating(fb.get("rating"))
        comments = len(fb.get("comments", []))
        launch_path = resolve_agent_launch_path(route_name, launch_overrides)
        if launch_path:
            if launch_path.startswith(("http://", "https://")):
                href = launch_path
            elif launch_path.startswith("/"):
                href = launch_path
            else:
                href = f"{LAUNCH_BASE_URL}{launch_path}"
            action = build_action_stack("Launch", href, "Edit / View")
        else:
            action = "<div class='action-stack'><span class='status-badge warning'>Coming Soon</span></div>"
        challenge_text = agent.get("challenge") or description
        rows.append(
            [
                html.escape(industry),
                html.escape(name or "—"),
                html.escape(agent.get("author", "dzoan.nguyen@rackspace")),
                format_date(agent.get("created_at")),
                html.escape(agent.get("version", "v1.0.0")),
                html.escape(challenge_text),
                f"👥 {fb.get('users', 0)}",
                f"💬 {comments}",
                rating_html,
                action,
            ]
        )

    columns = [
        "🏭 Industry",
        "🤖 Agent Name",
        "👤 Author",
        "📅 Created On",
        "🔁 Version",
        "📄 Challenge",
        "👥 Users",
        "💬 Comments",
        "⭐ Rating",
        "🚀 Action",
    ]
    render_neon_table(" Production Ready AI Agent Library", columns, rows, "Agents will appear once published to the library.")


def render_ontology_table():
    records = load_meta_records("patterns.json", SAMPLE_PATTERNS)
    rows = []
    for pattern in records:
        pattern_slug = compute_route_name(pattern.get("name", "pattern"))
        pattern_href = build_page_url(
            "ontology_patterns",
            {
                "pattern": pattern_slug,
            },
        )
        rows.append(
            [
                html.escape(pattern.get("name", "—")),
                html.escape(pattern.get("description", "—")),
                html.escape(pattern.get("domain", "—")),
                format_tags(pattern.get("use_cases")),
                html.escape(pattern.get("author", "Rackers Lab")),
                format_date(pattern.get("created_at")),
                build_action_button("Open Pattern", pattern_href),
            ]
        )
    columns = [
        "🧠 Pattern Name",
        "📄 Description",
        "🏢 Domain",
        "🧪 Use Cases",
        "👤 Author",
        "📅 Created On",
        "🚀 Action",
    ]
    render_neon_table("🧠 Ontology & Pattern Library", columns, rows, "Add the first ontology asset to unlock this grid.")


def render_digital_twin_preview():
    units = [
        {"Business Unit": "Sales & Marketing", "Region": "Global", "Head": "Avery Chen"},
        {"Business Unit": "Engineering", "Region": "Global", "Head": "Fei-Fei Li"},
        {"Business Unit": "Operations", "Region": "EMEA", "Head": "Kenji Yamamoto"},
        {"Business Unit": "Service Delivery", "Region": "Global", "Head": "Diego Ramos"},
        {"Business Unit": "Customer Success", "Region": "AMER", "Head": "Nia Thompson"},
        {"Business Unit": "Finance", "Region": "Global", "Head": "Priya Malik"},
    ]
    rows = [
        [
            html.escape(unit["Business Unit"]),
            unit["Region"],
            unit["Head"],
            build_action_button("View Twin connections", build_page_url("ontology_twin", {"bu": unit["Business Unit"]})),
        ]
        for unit in units
    ]
    columns = ["🏢 Business Unit", "🌍 Region", "👤 Head", "🚀 Action"]
    render_neon_table(
        "🧬 My Company Digital Twin — Ontology Layer",
        columns,
        rows,
        "Open the Digital Twin page to manage Business Units and relationships.",
    )

    if st.button("🔗 Open Digital Twin Form", key="open_digital_twin"):
        go_to_page("pages/ontology_twin.py")


def render_docs_table():
    records = load_meta_records("docs.json", SAMPLE_DOCS)
    rows = []
    for doc in records:
        doc_slug = compute_route_name(doc.get("title", "doc"))
        doc_href = build_page_url(
            "documentation_learning",
            {
                "doc": doc_slug,
            },
        )
        rows.append(
            [
                html.escape(doc.get("title", "—")),
                html.escape(doc.get("category", "Guide")),
                html.escape(doc.get("author", "Rackers Lab")),
                format_date(doc.get("updated_at")),
                html.escape(doc.get("read_time", "—")),
                render_star_rating(doc.get("rating")),
                build_action_button("Read", doc_href),
            ]
        )
    columns = [
        "📘 Document Title",
        "📁 Category",
        "👤 Author",
        "📅 Last Updated",
        "⏱️ Reading Time",
        "⭐ Rating",
        "🚀 Action",
    ]
    render_neon_table("📚 Documentation & Learning", columns, rows, "Docs will appear once published to the YES AI CAN shelf.")


def render_community_table():
    records = load_meta_records("community.json", SAMPLE_COMMUNITY)
    rows = []
    for member in records:
        member_slug = compute_route_name(member.get("name", "member"))
        member_href = build_page_url(
            "community_ambassadors",
            {
                "member": member_slug,
            },
        )
        rows.append(
            [
                html.escape(member.get("name", "—")),
                html.escape(member.get("department", "—")),
                html.escape(member.get("region", "—")),
                format_tags(member.get("skills")),
                format_tags(member.get("badges")),
                format_tags(member.get("contributions")),
                html.escape(member.get("cohort", "—")),
                build_action_button("View Profile", member_href),
            ]
        )
    columns = [
        "👑 Ambassador / Contributor",
        "🏢 Department",
        "🌍 Region",
        "🧩 Skillset Focus",
        "🎖️ Badges / Achievements",
        "📦 Contributions",
        "📅 Cohort / Year",
        "🚀 Action",
    ]
    render_neon_table("🌍 Community & Ambassadors", columns, rows, "Ambassador cohorts will populate here.")


def render_admin_tools_table():
    records = load_meta_records("admin_tools.json", SAMPLE_ADMIN)
    rows = []
    for tool in records:
        telemetry = (tool.get("telemetry") or "").lower()
        variant = "success" if telemetry == "stable" else "warning"
        tool_slug = compute_route_name(tool.get("name", "tool"))
        tool_href = build_page_url(
            "admin_rex",
            {
                "tool": tool_slug,
            },
        )
        rows.append(
            [
                html.escape(tool.get("name", "—")),
                html.escape(tool.get("description", "—")),
                html.escape(tool.get("category", "Ops")),
                build_status_badge(tool.get("telemetry", "Beta"), variant),
                format_date(tool.get("updated_at")),
                build_action_button("Open", tool_href),
            ]
        )
    columns = [
        "⚙️ Tool / Feature",
        "📄 Description",
        "🔧 Category",
        "📊 Telemetry Status",
        "📅 Last Updated",
        "🚀 Action",
    ]
    render_neon_table("⚙️ Admin Tools / REX 2.0", columns, rows, "Admin stacks will surface here once configured.")


def render_global_search_table():
    records = load_meta_records("search_index.json", SAMPLE_SEARCH)
    rows = []
    for result in records:
        search_href = build_page_url(
            "search",
            {
                "query": result.get("title"),
                "type": result.get("type"),
            },
        )
        rows.append(
            [
                html.escape(result.get("type", "—")),
                html.escape(result.get("title", "—")),
                html.escape(result.get("category", "—")),
                html.escape(result.get("owner", "—")),
                format_date(result.get("updated_at")),
                build_action_button("Open", search_href),
            ]
        )
    columns = [
        "🔍 Result Type",
        "🏷️ Name / Title",
        "📂 Category",
        "👤 Owner",
        "📅 Last Updated",
        "🚀 Action",
    ]
    render_neon_table("🔍 Unified Search Index", columns, rows, "Search index will refresh once metadata is ingested.")


def render_hero_section(auth_user: dict | None) -> None:
    st.markdown("<div class='left-box'>", unsafe_allow_html=True)
    st.markdown(
        """
        <style>
        /* Overall dark background for the neon effect */
        body {
            background-color: #0d0d1a !important;
        }

        .neon-sign-wrapper {
            margin: 50px auto;
            padding: 30px;
            width: 90%;
            max-width: 900px;
            box-sizing: border-box;
            position: relative;
            border-radius: 20px;
            border: 4px solid #00ffff;
            box-shadow:
                0 0 10px #00ffff,
                0 0 30px #00ffff,
                0 0 60px #00ffff,
                0 0 100px rgba(0, 255, 255, 0.5);
        }

        .neon-sign-inner {
            background-color: #1a0d1a;
            padding: 40px 30px;
            border-radius: 15px;
            border: 3px solid #ff00ff;
            box-shadow:
                0 0 8px #ff00ff,
                0 0 20px #ff00ff,
                0 0 40px rgba(255, 0, 255, 0.5);
        }

        .neon-title,
        .neon-subtitle {
            font-family: 'Arial Black', sans-serif;
            font-weight: 900;
            color: #ffffff;
            text-align: center;
            margin: 0;
            margin-bottom: 0.2em;
            text-shadow:
                0 0 5px #ff00ff,
                0 0 15px #ff00ff,
                0 0 25px rgba(255, 0, 255, 0.8),
                0 0 40px rgba(255, 0, 255, 0.6);
        }

        .neon-title {
            font-size: 3.5em;
        }

        .neon-subtitle {
            font-size: 3.2em;
        }

        .neon-description {
            font-family: 'Segoe UI', sans-serif;
            font-size: 1.5em;
            line-height: 1.4;
            color: #ffffff;
            text-align: center;
            max-width: 700px;
            margin: 0.8em auto 0;
            text-shadow:
                0 0 4px #ff00ff,
                0 0 10px rgba(255, 0, 255, 0.7);
        }

        .neon-home-icon {
            font-size: 1.2em;
            vertical-align: middle;
            margin-right: 0.15em;
            filter: drop-shadow(0 0 8px #00ffff) drop-shadow(0 0 16px #00ffff);
        }
        </style>

        <div class="neon-sign-wrapper">
            <div class="neon-sign-inner">
                <div class="neon-title">
                    <span class="neon-home-icon">🏠</span> The YES AI CAN
                </div>
                <div class="neon-subtitle">Community LAB</div>
                <div class="neon-description">
                    The Community Place where Great People help other People be more<br>
                    Productive–Creative, Better and Happier — while helping Others bring<br>
                    their Ideas to Life.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">YES AI CAN is built to:</div>
            <ul class="feature-list">
                <li>Map global AI & domain expertise.</li>
                <li>Showcase prototypes, MVPs, and production launches.</li>
                <li>Provide neon-fast zero-code tooling for explainable agents.</li>
                <li>Accelerate reuse from Customer ZERO to Customer ONE.</li>
                <li>Connect Ambassadors, SMEs, and dreamers across regions.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="feature-card feature-card-blue">
            <div class="feature-title feature-title-blue">💡 Why Now?</div>
            <p class="feature-text feature-text-white">
                Rackspace has <strong style="color:#00d4ff;">5,000+ hidden superpowers.</strong>
                YES AI CAN discovers them and gives every Racker the platform to say “YES, AI CAN.”
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">🧱 What You Can Do Here</div>
            <h4>💬 As a User — Life Improver</h4>
            <p><strong>Submit a Pain Point or Workflow — “How Can AI Help?”</strong><br>
            Share any challenge, repetitive task, manual workflow, or inefficiency in your daily work.<br>
            Your submission becomes a real challenge for the community to solve — together.</p>
            <p><strong>Report Any Pain Point, Improvement Need, or Idea</strong><br>
            Tell the community what slows you down, what’s broken, or what could be better.<br>
            Every idea becomes fuel for the next internal AI tool, automation, or workflow upgrade.</p>
            <h4>🛠️ As a Solution Finder or Builder — Solve Real Rackers’ Problems</h4>
            <p>Step in to help your teammates by designing or proposing AI-powered solutions.<br>
            Use zero-code tools or your technical skills to:</p>
            <ul class="feature-list">
                <li>Automate repetitive tasks</li>
                <li>Streamline complex workflows</li>
                <li>Improve accuracy and efficiency</li>
                <li>Reduce frustration</li>
                <li>Make someone’s day easier — and happier</li>
            </ul>
            <p>Every problem submitted is an opportunity for you to build something impactful.</p>
            <h4>👉 Next Action: Create Your Human Stack Profile</h4>
            <p><strong>👤 Create your Human Stack Profile</strong> — Showcase your skills, domain expertise, role & department, resume, AI experience, and the projects you’ve built or contributed to.<br>
            Your profile helps others find you, collaborate with you, and invite you to solve challenges that match your strengths.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)


def render_navigation_center(current_agents, feedback_data, auth_user) -> None:
    wrapper_class = "nav-center-wrapper"
    if st.session_state.get("yes_theme", "dark") != "dark":
        wrapper_class += " light"
    st.markdown(f"<div class='{wrapper_class}'>", unsafe_allow_html=True)
    st.markdown("<div class='nav-command-grid'>", unsafe_allow_html=True)
    sections = [
        {
            "icon": "🤖",
            "label": "Agent Library",
            "description": "Launch Customer ZERO agents or publish to Customer ONE.",
            "page": "pages/agent_library.py",
            "renderer": lambda: render_agent_library_table(current_agents, feedback_data),
        },
        {
            "icon": "🧬",
            "label": "Digital Twin",
            "description": "Explore the My Company Digital Twin ontology layer.",
            "page": "pages/ontology_twin.py",
            "renderer": render_digital_twin_preview,
        },
        {
            "icon": "🧠",
            "label": "Ontology & Patterns",
            "description": "Reusable logic, prompts, and governance templates.",
            "page": "pages/ontology_patterns.py",
            "renderer": render_ontology_table,
        },
        {
            "icon": "📚",
            "label": "Docs & Learning",
            "description": "Playbooks, guides, and Ambassador learning paths.",
            "page": "pages/documentation_learning.py",
            "renderer": render_docs_table,
        },
        {
            "icon": "🌍",
            "label": "Community & Ambassadors",
            "description": "Cohorts, events, leaderboards, and badges.",
            "page": "pages/community_ambassadors.py",
            "renderer": render_community_table,
        },
        {
            "icon": "⚙️",
            "label": "Admin & REX 2.0",
            "description": "Ops telemetry, exports, and integration feeds.",
            "page": "pages/admin_rex.py",
            "renderer": render_admin_tools_table,
        },
        # Global Search temporarily disabled (cf. request).
        # {
        #     "icon": "🔍",
        #     "label": "Global Search",
        #     "description": "Fuzzy search across profiles, projects, agents, and tags.",
        #     "page": "pages/search.py",
        #     "renderer": render_global_search_table,
        # },
    ]
    for section in sections:
        st.markdown("<div class='nav-mini-block'>", unsafe_allow_html=True)
        key = f"nav_center_{section['label'].lower().replace(' ', '_')}"
        target_page = section.get("page")
        if st.button(f"{section['icon']} {section['label']}", key=key, use_container_width=True):
            if target_page:
                go_to_page(target_page)
        st.markdown(f"<div class='nav-mini-desc'>{section['description']}</div>", unsafe_allow_html=True)
        renderer: Callable[[], None] | None = section.get("renderer")
        if renderer:
            renderer()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_future_modules():
    latest_project = {
        "title": "Who knows what / done what directory",
        "owner": "Ben",
        "tags": ["US product • World", "US product • World"],
        "status": "—",
        "scores": ["6.0", "6.5"],
    }
    popular_terms = [
        "Human Stack",
        "Agent builder",
        "Billing intelligence",
        "Neon ChatOps",
        "Automation Champions",
    ]
    new_members = [
        {"name": "Ben", "role": "CX Operations • World"},
        {"name": "Sunda", "role": "Product Strategy • Global"},
        {"name": "JOn", "role": "Growth & Partnerships"},
        {"name": "Avery Chen", "role": "Customer Success • Americas"},
        {"name": "Mia Patel", "role": "Cloud Economics • Global"},
    ]
    new_challengers = [
        {"name": "Li Wei", "focus": "Automation & Infra Ops"},
        {"name": "Harper Brooks", "focus": "Zero Trust Observability"},
        {"name": "Nadia Karim", "focus": "Human-in-the-loop Workflows"},
        {"name": "Jonah Reyes", "focus": "Edge & Retail Innovation"},
        {"name": "Kaya Morgan", "focus": "AI for Field Engineering"},
    ]
    existing_builders = [
        {"name": "Ada Lovelace", "focus": "Systems Architecture"},
        {"name": "John Lennon", "focus": "Creative AI Strategy"},
        {"name": "Fei-Fei Li", "focus": "Vision & LLM Ops"},
        {"name": "Geoffrey Hinton", "focus": "Predictive Infrastructure"},
        {"name": "Timnit Gebru", "focus": "Ethics & Compliance"},
    ]

    st.markdown("<div class='nav-bottom-grid'>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="nav-bottom-card">
            <h4>🔥 Trending Agents</h4>
            <p>Track which neon builds are earning the most traction across customers.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="nav-bottom-card">
            <h4>🆕 Latest Projects</h4>
            <p>Fresh prototypes, MVPs, and production launches from Rackers worldwide.</p>
            <div class="project-entry">
                <strong>{html.escape(latest_project['title'])}</strong>
                <div class="project-meta">
                    <span>By {html.escape(latest_project['owner'])}</span>
                    <span>{html.escape(latest_project['tags'][0])}</span>
                    <span>{html.escape(latest_project['tags'][1])}</span>
                    <span>{html.escape(latest_project['status'])}</span>
                </div>
                <div class="project-scores">
                    <span class="project-score">{html.escape(latest_project['scores'][0])}</span>
                    <span class="project-score">{html.escape(latest_project['scores'][1])}</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----------------------------
    # New Members (Table Style)
    # ----------------------------

    members_columns = ["Name", "Department / Region"]
    members_rows = [
        ["Ben", "CX Operations • World"],
        ["Sunda", "Product Strategy • Global"],
        ["Jon", "Growth & Partnerships"],
        ["Avery Chen", "Customer Success • Americas"],
        ["Mia Patel", "Cloud Economics • Global"],
    ]

    render_neon_table(
        "New Members — Welcome to YES AI CAN Lab",
        members_columns,
        members_rows,
        "No new members yet."
    )

    # ----------------------------
    # New Challengers (Table Style)
    # ----------------------------

    challengers_columns = ["Name", "Focus Area"]
    challengers_rows = [
        ["Li Wei", "Automation & Infra Ops"],
        ["Harper Brooks", "Zero Trust Observability"],
        ["Nadia Karim", "Human-in-the-loop Workflows"],
        ["Jonah Reyes", "Edge & Retail Innovation"],
        ["Kaya Morgan", "AI for Field Engineering"],
    ]

    render_neon_table(
        "New Challengers — Bold Minds Solving Pain Points",
        challengers_columns,
        challengers_rows,
        "No challengers found."
    )

    # ----------------------------
    # Builders (Table Style)
    # ----------------------------

    builders_columns = ["Name", "Area of Expertise"]
    builders_rows = [
        ["Ada Lovelace", "Systems Architecture"],
        ["John Lennon", "Creative AI Strategy"],
        ["Fei-Fei Li", "Vision & LLM Ops"],
        ["Geoffrey Hinton", "Predictive Infrastructure"],
        ["Timnit Gebru", "Ethics & Compliance"],
    ]

    render_neon_table(
        "Core Builders — Experts Advancing the YES AI CAN Lab",
        builders_columns,
        builders_rows,
        "No builders yet."
    )


    # st.markdown(
    #     f"""
    #     <div class="nav-bottom-card">
    #         <h4>New members</h4>
    #         <p>Welcome the builders, designers, and SMEs joining the YES AI CAN lab.</p>
    #         <ul class="builder-list">
    #             {''.join(f"<li>{member['name']} — {member['role']}</li>" for member in new_members)}
    #         </ul>
    #         <p class="search-footer">These members are ready to collaborate across CX, Product, and Ops.</p>
    #     </div>
    #     """,
    #     unsafe_allow_html=True,
    # )

    # st.markdown(
    #     f"""
    #     <div class="nav-bottom-card">
    #         <h4>New Challengers</h4>
    #         <p>Fresh faces solving today’s pain points with bold questions.</p>
    #         <div>
    #             <strong>Challengers:</strong>
    #             <ul class="builder-list">
    #                 {''.join(f"<li>{challenger['name']} — {challenger['focus']}</li>" for challenger in new_challengers)}
    #             </ul>
    #         </div>
    #         <div style="margin-top:0.5rem;">
    #             <strong>Existing builders:</strong>
    #             <ul class="builder-list">
    #                 {''.join(f"<li>{builder['name']} — {builder['focus']}</li>" for builder in existing_builders)}
    #             </ul>
    #         </div>
    #     </div>
    #     """,
    #     unsafe_allow_html=True,
    # )

    # st.markdown(
    #     """
    #     <div class="nav-bottom-card">
    #         <h4>💡 Popular Searches</h4>
    #         <p>See the topics, industries, and use cases everyone is exploring.</p>
    #         <div style="margin-top:0.6rem;">
    #             Search for any keyword, then try the chips below.
    #         </div>
    #     """,
    #     unsafe_allow_html=True,
    # )

    # search_value = st.text_input(
    #     "Search keywords",
    #     value="",
    #     placeholder="e.g. AI automation, billing, community, agent ops",
    #     key="nav_popular_search_bar",
    #     label_visibility="collapsed",
    # )

    # chips_html = "".join(f"<span class='search-chip'>{term}</span>" for term in popular_terms)
    # st.markdown(f"<div class='chip-row'>{chips_html}</div>", unsafe_allow_html=True)
    # if search_value:
    #     st.markdown(
    #         f"<p class='search-footer'>Searching for <strong>{html.escape(search_value)}</strong></p>",
    #         unsafe_allow_html=True,
    #     )
    # else:
    #     st.markdown(
    #         "<p class='search-footer'>See the topics, industries, and use cases everyone is exploring.</p>",
    #         unsafe_allow_html=True,
    #     )

    # st.markdown("</div>", unsafe_allow_html=True)
    # st.markdown("</div>", unsafe_allow_html=True)
# ============================================================
# MAIN LAYOUT: LEFT PANEL (Hero) + RIGHT PANEL (Navigation)
# ============================================================

# Global hero replaced by the neon sign rendered above.
# Two-column layout
c1, c2 = st.columns([1.1, 1.9], gap="large")

# LEFT PANEL — Hero Message
with c1:
    st.markdown("<div class='left-box'>", unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🌌 What YES AI CAN Is</div>
            <p class="feature-text">
                YES AI CAN is Rackspace’s AI Foundry + Community Agent Factory, built to:
            </p>
            <ul class="feature-list">
                <li>🧠 Mine our global superpowers — map every skill, SME, and domain expert</li>
                <li>🔍 Collect real business pain points — Kaggle-style challenge submissions</li>
                <li>🚀 Turn problems into agents — Customer ZERO → Customer ONE blueprints</li>
                <li>🪄 Give zero-code tools for creating explainable AI agents instantly</li>
                <li>🤝 Connect Ambassadors, SMEs, engineers, and innovators</li>
                <li>♻️ Accelerate reuse through a shared, governed agent library</li>
                <li>🏗️ Power the next generation of OpenStack + private AI solutions</li>
                <li>🌏 Unite Rackers globally into one open innovation community</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-card feature-card-blue">
            <div class="feature-title feature-title-blue">💡 Why We Exist</div>
            <p class="feature-text feature-text-white">
                Rackspace has 5,000+ hidden superpowers — unique skills, ideas, and lived experiences waiting to be unlocked. YES AI CAN is the place where those superpowers become visible: in profiles, in projects, in prototypes, in agents, in solutions, and in community.
            </p>
            <p class="feature-text feature-text-white" style="margin-top: 1rem;">
                Our mission: Give every Racker — regardless of background — the confidence, tools, and platform to say: <strong style="color: #00d4ff;">“YES, AI CAN — and so can I.”</strong>
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🧩 Challenge & Solution Flow</div>
            <p><strong>As User / Live Improver</strong></p>
            <ul class="feature-list">
                <li>Submit any pain point or workflow (“How Can AI Help?”)</li>
                <li>Report improvement needs or new ideas to the community</li>
            </ul>
            <p><strong>As Solution Finder / Builder</strong></p>
            <ul class="feature-list">
                <li>Help Rackers solve real-life problems</li>
                <li>Build AI tools that improve tasks, workflows, and happiness</li>
            </ul>
            <p><strong>Next action</strong></p>
            <p>Create your Human Stack Profile (skills, experience, resume, expertise)</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-card">
            <div class="feature-title">🧱 What You Can Do Here</div>
            <h4>💬 As a User — Live Improver</h4>
            <p><strong>Submit a Pain Point or Workflow — “How Can AI Help?”</strong><br>
            Share any challenge, repetitive task, manual workflow, or inefficiency in your daily work.<br>
            Your submission becomes a real challenge for the community to solve — together.</p>
            <p><strong>Report Any Pain Point, Improvement Need, or Idea</strong><br>
            Tell the community what slows you down, what’s broken, or what could be better.<br>
            Every idea becomes fuel for the next internal AI tool, automation, or workflow upgrade.</p>
            <h4>🛠️ As a Solution Finder or Builder — Solve Real Rackers’ Problems</h4>
            <p>Step in to help your teammates by designing or proposing AI-powered solutions.<br>
            Use zero-code tools or your technical skills to:</p>
            <ul class="feature-list">
                <li>Automate repetitive tasks</li>
                <li>Streamline complex workflows</li>
                <li>Improve accuracy and efficiency</li>
                <li>Reduce frustration</li>
                <li>Make someone’s day easier — and happier</li>
            </ul>
            <p>Every problem submitted is an opportunity for you to build something impactful.</p>
            <h4>👉 Next Action: Create Your Human Stack Profile</h4>
            <p><strong>👤 Create your Human Stack Profile</strong> — Showcase your skills, domain expertise, role & department, resume, AI experience, and the projects you’ve built or contributed to.<br>
            Your profile helps others find you, collaborate with you, and invite you to solve challenges that match your strengths.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="feature-card feature-card-blue">
            <div class="feature-title feature-title-blue">🚀 Built for You</div>
            <p class="feature-text feature-text-white">
                Whether you're an engineer, analyst, salesperson, manager, operator, or creator — YES AI CAN is your footstool into AI, designed for zero fear, zero barriers, zero cost, maximum clarity, maximum support, maximum impact.
            </p>
            <p class="feature-text feature-text-white" style="margin-top: 1rem;">
                This is how Rackspace builds a future where AI is safe, transparent, explainable, human-centered, and globally collaborative.
            </p>
            <p class="feature-text feature-text-white" style="margin-top: 1rem; text-align: center; font-size: 18px; font-weight: 600; color: #00d4ff;">
                🫂 Welcome to the Future of Human-Centered AI at Rackspace<br>
                Here, ideas turn into prototypes. Prototypes turn into agents. Agents turn into products. And Rackers turn into creators.
            </p>
        </div>
    """, unsafe_allow_html=True)
    render_primary_navigation_buttons()
    # Duplicate call with similar content exists elsewhere; keeping left panel lighter by
    # skipping the extra “Jump into Forms & Workspaces” block for now.
    # render_form_navigation_buttons()

    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT PANEL — Navigation and Home Page Layers
with c2:
    st.markdown("<div class='right-box'>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="nav-center-header" style="margin-bottom:1rem;">
            <h2>🏠 HOW CAN AI HELP </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    render_help_intro()
    render_login_cta(auth_user)
    render_quick_access(auth_user, origin="right")
    render_help_hub_layer(auth_user)

    status_col, toggle_col = st.columns([3, 1])
    with status_col:
        if auth_user:
            st.markdown(f"✅ Logged in as **{auth_user.get('name', auth_user.get('email'))}**")
        else:
            st.markdown("🔐 Not logged in — visit *Login / My Space* to personalize")
    with toggle_col:
        is_dark = st.session_state.get("yes_theme") == "dark"
        theme_toggle = st.toggle("🌗 Dark Mode", value=is_dark, key="theme_toggle")
        new_theme = "dark" if theme_toggle else "light"
        if new_theme != st.session_state["yes_theme"]:
            st.session_state["yes_theme"] = new_theme
            set_theme(new_theme)
            rerun_fn = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)
            if rerun_fn:
                rerun_fn()

    render_navigation_center(AGENTS, feedback_data, auth_user)

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
    <footer>
        💎 YES AI CAN — Rackers Lab & Community |  Made with ❤️ by Dzoan.nguyen@Rackspace.com
    </footer>
""", unsafe_allow_html=True)
