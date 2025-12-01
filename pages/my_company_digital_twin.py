import streamlit as st

st.set_page_config(
    page_title="My Company Digital Twin",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧬 My Company Digital Twin — Ontology Layer")
st.caption("A Palantir-style ontology representation of your organization.")

# -------------------------
# SESSION STATE INIT
# -------------------------
if "ontology_bu" not in st.session_state:
    st.session_state["ontology_bu"] = [
        {"Business Unit": "Sales & Marketing", "Region": "Global", "Head": "TBD"},
        {"Business Unit": "Product", "Region": "Global", "Head": "TBD"},
        {"Business Unit": "Engineering", "Region": "Global", "Head": "TBD"},
        {"Business Unit": "Operations", "Region": "Global", "Head": "TBD"},
        {"Business Unit": "Finance", "Region": "Global", "Head": "TBD"},
        {"Business Unit": "HR", "Region": "Global", "Head": "TBD"},
        {"Business Unit": "Customer Success", "Region": "Global", "Head": "TBD"},
    ]

if "ontology_rel" not in st.session_state:
    st.session_state["ontology_rel"] = [
        {"Input BU": "Sales & Marketing", "Output BU": "Product", "Flow": "Customer Feedback"},
        {"Input BU": "Product", "Output BU": "Engineering", "Flow": "Feature Specs / PRDs"},
        {"Input BU": "Engineering", "Output BU": "Operations", "Flow": "Deployable Services"},
        {"Input BU": "Operations", "Output BU": "Finance", "Flow": "Cost Reporting"},
        {"Input BU": "Customer Success", "Output BU": "Sales & Marketing", "Flow": "Renewal Signals"},
    ]

# -------------------------
# BUSINESS UNIT TABLE
# -------------------------
st.subheader("🏢 Business Units")

st.dataframe(st.session_state["ontology_bu"], use_container_width=True)

st.markdown("### ➕ Add Business Unit")

col1, col2, col3 = st.columns(3)
with col1:
    bu_name = st.text_input("Business Unit Name")
with col2:
    bu_region = st.text_input("Region")
with col3:
    bu_head = st.text_input("Head of Unit")

if st.button("Add BU"):
    if bu_name:
        st.session_state["ontology_bu"].append(
            {"Business Unit": bu_name, "Region": bu_region, "Head": bu_head}
        )
        st.success(f"Added Business Unit: {bu_name}")
        st.rerun()

# -------------------------
# RELATIONSHIP TABLE
# -------------------------
st.subheader("🔗 BU Relationships (Input → Output)")

st.dataframe(st.session_state["ontology_rel"], use_container_width=True)

st.markdown("### ➕ Add Relationship")

col1, col2, col3 = st.columns(3)

with col1:
    input_bu = st.selectbox(
        "Input BU",
        [b["Business Unit"] for b in st.session_state["ontology_bu"]]
    )

with col2:
    output_bu = st.selectbox(
        "Output BU",
        [b["Business Unit"] for b in st.session_state["ontology_bu"]]
    )

with col3:
    flow_desc = st.text_input("Flow Description")

if st.button("Add Relationship"):
    st.session_state["ontology_rel"].append(
        {"Input BU": input_bu, "Output BU": output_bu, "Flow": flow_desc}
    )
    st.success("Relationship added!")
    st.rerun()

# -------------------------
# GRAPH PREVIEW
# -------------------------
st.subheader("🕸 Ontology Flow Map")

for rel in st.session_state["ontology_rel"]:
    st.markdown(f"**{rel['Input BU']} → {rel['Output BU']}** — _{rel['Flow']}_")
