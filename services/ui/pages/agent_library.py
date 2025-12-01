# Agent Library — Customer ZERO / Customer ONE Factory
# Catalog of all AI agents

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

st.set_page_config(
    page_title="Agent Library — YES AI CAN",
    layout="wide"
)

# Metadata storage
META_DIR = Path(__file__).parent.parent.parent.parent / ".sandbox_meta"
AGENTS_FILE = META_DIR / "agents.json"
META_DIR.mkdir(exist_ok=True)

def load_agents() -> List[Dict]:
    """Load all agents."""
    if AGENTS_FILE.exists():
        try:
            with open(AGENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def save_agents(agents: List[Dict]):
    """Save all agents."""
    with open(AGENTS_FILE, "w", encoding="utf-8") as f:
        json.dump(agents, f, ensure_ascii=False, indent=2)

def generate_id() -> str:
    """Generate a unique ID for an agent."""
    return f"agent_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(load_agents())}"

# Page header
st.title("🤖 Agent Library — Customer ZERO / Customer ONE Factory")
st.markdown("**YES AI CAN — Rackers Lab & Community**")
st.markdown("---")

# Tabs: Grid View, Add Agent, Detail View
tab1, tab2, tab3 = st.tabs(["📊 Agent Catalog", "➕ Add Agent", "🔍 Search & Filter"])

agents = load_agents()

with tab1:
    st.subheader("All AI Agents")
    
    if not agents:
        st.info("🤖 No agents yet. Add your first agent to the library!")
    else:
        # Filter by status
        status_filter = st.selectbox("Filter by Status", 
                                    ["All", "Draft", "Prototype", "Customer READY", "Production READY"])
        filtered = agents
        if status_filter != "All":
            filtered = [a for a in agents if a.get('status') == status_filter]
        
        # Display as grid
        cols = st.columns(3)
        for idx, agent in enumerate(filtered):
            with cols[idx % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                                border: 2px solid #00d4ff; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem;
                                box-shadow: 0 4px 12px rgba(0,212,255,0.1);">
                        <h3 style="color: #00d4ff; margin-bottom: 0.5rem;">{agent.get('name', 'Unknown')}</h3>
                        <p style="color: #334155; margin: 0.3rem 0;"><strong>Version:</strong> {agent.get('version', 'N/A')}</p>
                        <p style="color: #334155; margin: 0.3rem 0;"><strong>Status:</strong> {agent.get('status', 'N/A')}</p>
                        <p style="color: #334155; margin: 0.3rem 0;"><strong>Industry:</strong> {agent.get('industry', 'N/A')}</p>
                        <p style="color: #64748b; font-size: 0.9rem; margin-top: 0.5rem;">{agent.get('description', '')[:100]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("View Details", key=f"view_{agent.get('id')}"):
                        st.session_state['view_agent'] = agent.get('id')
                        st.rerun()
                    
                    if agent.get('status') == "Customer READY":
                        if st.button("🚀 Publish to Customer ONE", key=f"publish_{agent.get('id')}"):
                            st.info("🚀 Publishing to Customer ONE... (Feature coming soon)")

with tab2:
    st.subheader("Add New Agent to Library")
    
    with st.form("agent_form"):
        name = st.text_input("Agent Name *")
        version = st.text_input("Version *", value="1.0.0")
        description = st.text_area("Description *")
        industry = st.text_input("Industry *")
        
        st.markdown("### Technical Details")
        inputs = st.text_area("Inputs (comma-separated)")
        outputs = st.text_area("Outputs (comma-separated)")
        reasoning_trail = st.text_area("Reasoning Trail Fields (comma-separated)")
        confidence_explanation = st.text_area("Confidence Score Explanation")
        
        required_datasets = st.text_area("Required Datasets (comma-separated)")
        required_models = st.text_area("Required Model Weights (comma-separated)")
        deployment_notes = st.text_area("Deployment Notes")
        
        authors = st.text_input("Authors / Maintainers (comma-separated)")
        
        status = st.selectbox("Status *", 
                             ["Draft", "Prototype", "Customer READY", "Production READY"])
        
        submitted = st.form_submit_button("💾 Add Agent", use_container_width=True)
        
        if submitted:
            if not name or not version or not description or not industry:
                st.error("⚠️ Name, Version, Description, and Industry are required!")
            else:
                agent = {
                    "id": generate_id(),
                    "name": name,
                    "version": version,
                    "description": description,
                    "industry": industry,
                    "inputs": [i.strip() for i in inputs.split(',') if i.strip()] if inputs else [],
                    "outputs": [o.strip() for o in outputs.split(',') if o.strip()] if outputs else [],
                    "reasoning_trail_fields": [r.strip() for r in reasoning_trail.split(',') if r.strip()] if reasoning_trail else [],
                    "confidence_score_explanation": confidence_explanation,
                    "required_datasets": [d.strip() for d in required_datasets.split(',') if d.strip()] if required_datasets else [],
                    "required_model_weights": [m.strip() for m in required_models.split(',') if m.strip()] if required_models else [],
                    "deployment_notes": deployment_notes,
                    "authors": [a.strip() for a in authors.split(',') if a.strip()] if authors else [],
                    "status": status,
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
                
                agents.append(agent)
                save_agents(agents)
                st.success("✅ Agent added to library!")
                st.rerun()

with tab3:
    st.subheader("Search & Filter Agents")
    
    search_term = st.text_input("🔍 Search by name, description, or industry")
    filter_status = st.selectbox("Filter by Status", 
                                ["All", "Draft", "Prototype", "Customer READY", "Production READY"])
    filter_industry = st.text_input("Filter by Industry")
    
    filtered = agents
    if search_term:
        search_lower = search_term.lower()
        filtered = [a for a in filtered if 
                   search_lower in a.get('name', '').lower() or
                   search_lower in a.get('description', '').lower() or
                   search_lower in a.get('industry', '').lower()]
    
    if filter_status != "All":
        filtered = [a for a in filtered if a.get('status') == filter_status]
    
    if filter_industry:
        filtered = [a for a in filtered if 
                   filter_industry.lower() in a.get('industry', '').lower()]
    
    st.write(f"**Found {len(filtered)} agent(s)**")
    
    for agent in filtered:
        with st.expander(f"🤖 {agent.get('name')} — {agent.get('version', 'N/A')} ({agent.get('status', 'N/A')})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Description:** {agent.get('description', 'N/A')}")
                st.write(f"**Industry:** {agent.get('industry', 'N/A')}")
                st.write(f"**Status:** {agent.get('status', 'N/A')}")
                if agent.get('inputs'):
                    st.write(f"**Inputs:** {', '.join(agent.get('inputs', []))}")
                if agent.get('outputs'):
                    st.write(f"**Outputs:** {', '.join(agent.get('outputs', []))}")
            with col2:
                if agent.get('authors'):
                    st.write(f"**Authors:** {', '.join(agent.get('authors', []))}")
                if agent.get('required_datasets'):
                    st.write(f"**Required Datasets:** {', '.join(agent.get('required_datasets', []))}")
                if agent.get('required_model_weights'):
                    st.write(f"**Required Models:** {', '.join(agent.get('required_model_weights', []))}")
                st.write(f"**Created:** {agent.get('created_at', 'N/A')[:10]}")
            
            if agent.get('deployment_notes'):
                st.write(f"**Deployment Notes:** {agent.get('deployment_notes')}")
            
            if st.button("🚀 Launch in Sandbox", key=f"launch_{agent.get('id')}"):
                st.info("🚀 Launching agent in sandbox... (Feature coming soon)")
