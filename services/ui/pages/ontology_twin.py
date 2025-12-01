"""Digital Twin / Ontology page surfaced from the YES AI CAN home experience."""

from __future__ import annotations

import html
from typing import Any, Dict, Iterable, List

import streamlit as st

from ontology.examples import build_example_graph
from ontology.registry import OntologyRegistry
from services.ui.utils.style import render_nav_bar_app

st.set_page_config(
    page_title="My Company Digital Twin",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

render_nav_bar_app(show_nav_buttons=True)

BUSINESS_UNITS: List[Dict[str, Any]] = [
    {
        "name": "Sales & Marketing",
        "region": "Global",
        "head": "Avery Chen",
        "missions": [
            "Capture customer pain points + renewal risks",
            "Translate field signals into qualified challenges",
            "Share packaged wins with customers",
        ],
        "systems": ["Salesforce", "GTM Planner", "Renewal Radar"],
        "signals": ["NPS delta", "Forecast accuracy", "Pipeline-to-delivery time"],
        "alliances": ["Product & Solutions", "Customer Success"],
    },
    {
        "name": "Product & Solutions",
        "region": "Global",
        "head": "Mia Patel",
        "missions": [
            "Curate backlog of “How Can AI Help” submissions",
            "Design Customer ZERO prototypes with SMEs",
            "Publish reusable Ontology + Pattern assets",
        ],
        "systems": ["Jira Discovery", "Pattern Library", "Ontology Vault"],
        "signals": ["Prototype velocity", "Pattern reuse", "Ambassador engagement"],
        "alliances": ["Engineering", "Sales & Marketing", "Ontology Guild"],
    },
    {
        "name": "Engineering & Delivery",
        "region": "Americas / EMEA",
        "head": "George Harrison",
        "missions": [
            "Operate Agent Factory + ModelOps stack",
            "Convert proven solutions into production pods",
            "Guardrail security, compliance, observability",
        ],
        "systems": ["Agent Factory", "ModelOps Plane", "Deployment Radar"],
        "signals": ["Lead time", "Defect escape rate", "GPU consumption"],
        "alliances": ["Product & Solutions", "Operations", "Security"],
    },
    {
        "name": "Operations / Cloud Services",
        "region": "Global",
        "head": "Kenji Yamamoto",
        "missions": [
            "Run OpenStack, Managed Cloud, and Ops Centers",
            "Feed telemetry into predictive capacity models",
            "Close the loop on automation adoption",
        ],
        "systems": ["OpenStack Control Plane", "Observability Mesh", "Field Ops Portal"],
        "signals": ["Capacity runway", "Incident MTTR", "Automation adoption"],
        "alliances": ["Engineering & Delivery", "Security", "Customer Success"],
    },
    {
        "name": "Customer Success",
        "region": "Global",
        "head": "Nia Thompson",
        "missions": [
            "Shepherd every live account through value playbooks",
            "Capture “voice of the Racker” happy / unhappy flows",
            "Sponsor Customer ONE journeys",
        ],
        "systems": ["SuccessHub", "Community Lab", "Champion Network"],
        "signals": ["Time-to-value", "Champion participation", "Save motions"],
        "alliances": ["Sales & Marketing", "Operations", "Human Stack"],
    },
    {
        "name": "Security, Risk & Compliance",
        "region": "Global",
        "head": "Karim Haddad",
        "missions": [
            "Own policy guardrails + AI governance center",
            "Certify datasets, prompts, and agent actions",
            "Coordinate escalations with SOC + Legal",
        ],
        "systems": ["Policy Checker", "SOC Copilot", "Risk Radar"],
        "signals": ["Control coverage", "Incident SLA", "Policy freshness"],
        "alliances": ["Engineering & Delivery", "Operations", "Legal"],
    },
]

RELATIONSHIPS: List[Dict[str, Any]] = [
    {
        "source": "Sales & Marketing",
        "target": "Product & Solutions",
        "flow": "Customer briefings → challenge charters",
        "artefacts": ["Challenge intake packet", "Voice of customer clips"],
        "cadence": "Weekly",
    },
    {
        "source": "Product & Solutions",
        "target": "Engineering & Delivery",
        "flow": "Approved backlog → build pods",
        "artefacts": ["AI blueprint", "Ontology spec", "Risk notes"],
        "cadence": "Sprint",
    },
    {
        "source": "Engineering & Delivery",
        "target": "Operations / Cloud Services",
        "flow": "Release candidates → deployment plans",
        "artefacts": ["Runbook", "Capacity ask", "Observability hooks"],
        "cadence": "Sprint / release",
    },
    {
        "source": "Operations / Cloud Services",
        "target": "Customer Success",
        "flow": "Operational telemetry → adoption playbooks",
        "artefacts": ["Adoption board", "SLO drift alerts"],
        "cadence": "Daily",
    },
    {
        "source": "Customer Success",
        "target": "Sales & Marketing",
        "flow": "Customer ONE references → revenue stories",
        "artefacts": ["Success briefs", "Metrics pack"],
        "cadence": "Monthly",
    },
    {
        "source": "Security, Risk & Compliance",
        "target": "All units",
        "flow": "Policy + guardrails + sign-offs",
        "artefacts": ["Control checklist", "Audit-ready package"],
        "cadence": "Per launch",
    },
]

SUPPORTING_LAYERS = [
    {
        "label": "Data / Telemetry",
        "items": ["Observability Mesh", "Renewal Risk Graph", "Capacity Twins", "Customer Feedback Store"],
        "color": "#7dd3fc",
    },
    {
        "label": "AI Assets",
        "items": ["Agent Library", "Ontology Patterns", "Human Stack Graph", "Prompt / Policy Vault"],
        "color": "#f472b6",
    },
    {
        "label": "Engagement Rituals",
        "items": ["Challenge triage", "Show-and-tell", "Customer ONE reviews", "Guardrail board"],
        "color": "#c084fc",
    },
]


def _normalize(value: Any) -> str:
    if isinstance(value, list):
        value = value[0] if value else ""
    return str(value or "").strip()


def _find_unit(name: str | None) -> Dict[str, Any] | None:
    if not name:
        return None
    target = name.lower()
    for entry in BUSINESS_UNITS:
        if entry["name"].lower() == target:
            return entry
    return None


def _render_chip_row(values: Iterable[str], accent: str) -> str:
    chips = []
    for value in values:
        safe = html.escape(str(value))
        chips.append(
            f"<span style='background:{accent};color:#0f172a;padding:4px 10px;border-radius:999px;font-size:0.85rem;margin:0 0.4rem 0.4rem 0;display:inline-block;'>{safe}</span>"
        )
    return "".join(chips)


def render_metrics() -> None:
    total_units = len(BUSINESS_UNITS)
    total_flows = len([r for r in RELATIONSHIPS if r["source"] != "Security, Risk & Compliance"])
    guardrail_flows = len([r for r in RELATIONSHIPS if r["source"] == "Security, Risk & Compliance"])
    col1, col2, col3 = st.columns(3)
    col1.metric("Business Units mapped", total_units)
    col2.metric("Operational flows stitched", total_flows)
    col3.metric("Guardrail touchpoints", guardrail_flows)


def render_unit_detail(unit: Dict[str, Any]) -> None:
    st.markdown("### 🧬 Focused Business Unit")
    col_a, col_b = st.columns([1.5, 1])
    with col_a:
        st.markdown(f"#### {unit['name']} — {unit['region']}")
        st.write(f"**Executive owner:** {unit['head']}")
        st.markdown("**Mission threads:**")
        for mission in unit["missions"]:
            st.markdown(f"- {mission}")
    with col_b:
        st.markdown("**Alliances**")
        st.markdown(_render_chip_row(unit["alliances"], "#7dd3fc"), unsafe_allow_html=True)
        st.markdown("**Systems**")
        st.markdown(_render_chip_row(unit["systems"], "#f472b6"), unsafe_allow_html=True)
        st.markdown("**Signals**")
        st.markdown(_render_chip_row(unit["signals"], "#c084fc"), unsafe_allow_html=True)


def render_relationship_table() -> None:
    st.markdown("### 🔗 Flow map across the twin")
    for rel in RELATIONSHIPS:
        st.markdown(
            f"**{rel['source']} ⟶ {rel['target']}** &nbsp;&nbsp;·&nbsp;&nbsp; {rel['flow']}<br>"
            f"<small>Cadence: {rel['cadence']} · Artefacts: {', '.join(rel['artefacts'])}</small>",
            unsafe_allow_html=True,
        )


def render_supporting_layers() -> None:
    st.markdown("### 🪄 Enabling layers")
    cols = st.columns(len(SUPPORTING_LAYERS))
    for column, layer in zip(cols, SUPPORTING_LAYERS):
        with column:
            column.markdown(
                f"""
                <div style="border-radius:16px;border:1px solid rgba(255,255,255,0.2);padding:1rem;background:#0f172a;">
                    <div style="font-weight:700;color:{layer['color']};margin-bottom:0.5rem;">{layer['label']}</div>
                    <ul style="padding-left:1.1rem;margin:0;">
                        {''.join(f"<li style='margin-bottom:0.2rem;color:#cbd5f5;'>{html.escape(item)}</li>" for item in layer['items'])}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_ontology_snapshot() -> None:
    registry = build_example_graph(OntologyRegistry())
    graph = registry.all()
    st.markdown("### 🧠 Registry snapshot (sample data)")
    cols = st.columns(2)
    for idx, node in enumerate(graph):
        target_col = cols[idx % 2]
        attributes = node["attributes"]
        title = attributes.get("name") or attributes.get("title") or node["type"]
        with target_col.expander(f"{node['type']} — {title}"):
            st.json(node)


st.title("🧬 My Company Digital Twin — Ontology Layer")
st.caption("Palantir-style living map of business units, flows, AI assets, and policy guardrails.")

render_metrics()

query_params = st.query_params
requested = _normalize(query_params.get("bu") or query_params.get("business_unit"))
fallback_unit = BUSINESS_UNITS[0]["name"]
default_unit = _find_unit(requested) or BUSINESS_UNITS[0]

selected_name = st.selectbox(
    "Choose a Business Unit to explore",
    options=[unit["name"] for unit in BUSINESS_UNITS],
    index=[unit["name"] for unit in BUSINESS_UNITS].index(default_unit["name"]),
)

if not requested or requested.lower() != selected_name.lower():
    st.query_params = {"bu": selected_name}

current_unit = _find_unit(selected_name) or default_unit
render_unit_detail(current_unit)
render_relationship_table()
render_supporting_layers()
render_ontology_snapshot()

st.markdown("---")
st.info(
    "Looking for the editable form? The legacy `/pages/my_company_digital_twin.py` page "
    "still exposes the lightweight CRUD prototype. This view focuses on storytelling."
)
