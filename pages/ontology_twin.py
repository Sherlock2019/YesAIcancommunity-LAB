import streamlit as st

from ontology.registry import OntologyRegistry
from ontology.examples import build_example_graph

st.set_page_config(page_title="Digital Company Twin", layout="wide")

registry = OntologyRegistry()
build_example_graph(registry)

st.title("🏢 Our Digital Company Twin — Ontology Layer")

DEFAULT_BUSINESS_UNITS = [
    {"name": "Sales & Marketing", "region": "Global", "head": "Avery Chen", "purpose": "Drive demand and customer storytelling"},
    {"name": "Engineering", "region": "Global", "head": "Fei-Fei Li", "purpose": "Build and run our AI-powered platforms"},
    {"name": "Operations", "region": "EMEA", "head": "Kenji Yamamoto", "purpose": "Ensure delivery, infra, logistics"},
    {"name": "Customer Success", "region": "AMER", "head": "Nia Thompson", "purpose": "Retain and expand customer happiness"},
    {"name": "Finance", "region": "Global", "head": "Priya Malik", "purpose": "Steward capital, billing, and risk"},
]

if "digital_twin_details" not in st.session_state:
    st.session_state["digital_twin_details"] = {unit["name"]: unit.copy() for unit in DEFAULT_BUSINESS_UNITS}

if "digital_twin_tasks" not in st.session_state:
    st.session_state["digital_twin_tasks"] = {unit["name"]: [] for unit in DEFAULT_BUSINESS_UNITS}

query_params = st.experimental_get_query_params()
default_bu = query_params.get("bu", [DEFAULT_BUSINESS_UNITS[0]["name"]])[0]
unit_names = list(st.session_state["digital_twin_details"].keys())
if default_bu not in unit_names:
    default_bu = unit_names[0]

st.markdown(
    "Select a Business Unit to update its digital twin, then add or adjust the tasks and cross-BU data flows that unit owns."
)
selected_bu = st.selectbox("Business Unit", unit_names, index=unit_names.index(default_bu))
st.experimental_set_query_params(bu=selected_bu)

details = st.session_state["digital_twin_details"][selected_bu]

with st.form("digital-twin-details"):
    region_val = st.text_input("Region", value=details.get("region", ""))
    head_val = st.text_input("Head of Unit", value=details.get("head", ""))
    purpose_val = st.text_area("Purpose / Charter", value=details.get("purpose", ""))
    if st.form_submit_button("Save BU Details"):
        details.update({"region": region_val, "head": head_val, "purpose": purpose_val})
        st.success("Business unit details updated.")

st.subheader("Tasks & Connections")
tasks = st.session_state["digital_twin_tasks"].setdefault(selected_bu, [])
if tasks:
    st.table(tasks)
else:
    st.info("No tasks captured yet for this BU. Add one below.")

agent_options = ["No agent yet", "Agent Builder", "Credit Appraisal Agent", "IT Troubleshooter Agent", "Unified Risk Agent", "Supervisor Agent"]
other_units = ["None"] + [name for name in unit_names if name != selected_bu]

with st.form("digital-twin-task-form"):
    task_name = st.text_input("Task / Workflow Name")
    agent_choice = st.selectbox("Agent Used", agent_options)
    input_from = st.selectbox("Input data from", other_units)
    output_to = st.selectbox("Output data to", other_units)
    notes = st.text_area("Notes / Signals")
    if st.form_submit_button("Add Task"):
        if task_name:
            tasks.append(
                {
                    "Task": task_name,
                    "Agent": agent_choice,
                    "Input From": input_from,
                    "Output To": output_to,
                    "Notes": notes,
                }
            )
            st.success("Task recorded in the digital twin.")
            st.experimental_rerun()
        else:
            st.warning("Please provide a task name before saving.")

st.markdown("---")
st.subheader("Full Business Unit Directory")
for name in unit_names:
    record = st.session_state["digital_twin_details"][name]
    bu_tasks = st.session_state["digital_twin_tasks"].get(name, [])
    with st.expander(f"{name} — {record.get('region', 'Unknown region')}"):
        st.markdown(f"**Head:** {record.get('head', 'TBD')}")
        st.markdown(f"**Purpose:** {record.get('purpose', '—')}" )
        if bu_tasks:
            st.table(bu_tasks)
        else:
            st.info("No tasks yet.")

st.markdown("---")
st.subheader("Ontology Graph Objects")
for obj in registry.all():
    label = obj['attributes'].get('name') or obj['attributes'].get('title') or 'Untitled'
    with st.expander(f"{obj['type']} — {label}"):
        st.json(obj)
