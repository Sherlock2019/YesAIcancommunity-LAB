# Admin & REX 2.0 Integration — YES AI CAN
# Admin views and metadata exports for REX 2.0

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

st.set_page_config(
    page_title="Admin & REX 2.0 — YES AI CAN",
    layout="wide"
)

# Metadata storage
META_DIR = Path(__file__).parent.parent.parent.parent / ".sandbox_meta"
HUMANS_FILE = META_DIR / "humans.json"
PROJECTS_FILE = META_DIR / "projects.json"
AGENTS_FILE = META_DIR / "agents.json"
PATTERNS_FILE = META_DIR / "patterns.json"
STATS_FILE = META_DIR / "stats.json"
META_DIR.mkdir(exist_ok=True)

def load_humans() -> List[Dict]:
    if HUMANS_FILE.exists():
        try:
            with open(HUMANS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def load_projects() -> List[Dict]:
    if PROJECTS_FILE.exists():
        try:
            with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def load_agents() -> List[Dict]:
    if AGENTS_FILE.exists():
        try:
            with open(AGENTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def load_patterns() -> List[Dict]:
    if PATTERNS_FILE.exists():
        try:
            with open(PATTERNS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def load_stats() -> Dict:
    if STATS_FILE.exists():
        try:
            with open(STATS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_stats(stats: Dict):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

# Page header
st.title("⚙️ Admin & REX 2.0 Integration")
st.markdown("**YES AI CAN — Rackers Lab & Community**")
st.markdown("---")

# Simple password check (in production, use proper authentication)
if 'admin_authenticated' not in st.session_state:
    password = st.text_input("🔐 Admin Password", type="password")
    if st.button("Login"):
        # Simple check - in production, use proper auth
        if password == "admin123" or password == "yesaican":  # Change this!
            st.session_state.admin_authenticated = True
            st.rerun()
    st.stop()

humans = load_humans()
projects = load_projects()
agents = load_agents()
patterns = load_patterns()
stats = load_stats()

# Update stats
stats['total_humans'] = len(humans)
stats['total_projects'] = len(projects)
stats['total_agents'] = len(agents)
stats['total_patterns'] = len(patterns)
stats['last_updated'] = datetime.now().isoformat()
save_stats(stats)

# Tabs: Overview, Users, Projects, Agents, REX Export
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "👤 Users", "🧱 Projects", "🤖 Agents", "📤 REX 2.0 Export"])

with tab1:
    st.subheader("Platform Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Rackers", stats.get('total_humans', 0))
    with col2:
        st.metric("Total Projects", stats.get('total_projects', 0))
    with col3:
        st.metric("Total Agents", stats.get('total_agents', 0))
    with col4:
        st.metric("Total Patterns", stats.get('total_patterns', 0))
    
    st.markdown("---")
    
    # Skills extraction
    all_skills = []
    for human in humans:
        all_skills.extend(human.get('skills', []))
    
    from collections import Counter
    skill_counts = Counter(all_skills)
    top_skills = skill_counts.most_common(10)
    
    st.subheader("Top Skills")
    for skill, count in top_skills:
        st.write(f"**{skill}:** {count} Rackers")
    
    # Usage metrics
    st.subheader("Usage Metrics")
    st.write(f"**Last Updated:** {stats.get('last_updated', 'N/A')}")
    st.write(f"**Ambassadors:** {len([h for h in humans if h.get('ambassador', False)])}")
    st.write(f"**Projects in Production:** {len([p for p in projects if p.get('phase') == 'Ready for Production'])}")
    st.write(f"**Customer READY Agents:** {len([a for a in agents if a.get('status') == 'Customer READY'])}")

with tab2:
    st.subheader("All Users (Human Stack)")
    
    st.write(f"**Total Users: {len(humans)}**")
    
    for human in humans:
        with st.expander(f"👤 {human.get('name', 'Unknown')} — {human.get('email', 'N/A')}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Department:** {human.get('department', 'N/A')}")
                st.write(f"**Team:** {human.get('team', 'N/A')}")
                st.write(f"**Role:** {human.get('role', 'N/A')}")
                st.write(f"**Region:** {human.get('region', 'N/A')}")
            with col2:
                st.write(f"**Skills:** {', '.join(human.get('skills', []))}")
                st.write(f"**Ambassador:** {'Yes' if human.get('ambassador') else 'No'}")
                st.write(f"**Created:** {human.get('created_at', 'N/A')[:10]}")
                st.write(f"**Updated:** {human.get('updated_at', 'N/A')[:10]}")

with tab3:
    st.subheader("All Projects")
    
    st.write(f"**Total Projects: {len(projects)}**")
    
    for project in projects:
        with st.expander(f"🧱 {project.get('title', 'Untitled')} — {project.get('phase', 'N/A')}"):
            st.write(f"**Description:** {project.get('description', 'N/A')}")
            st.write(f"**Authors:** {', '.join(project.get('authors', []))}")
            st.write(f"**Tags:** {', '.join(project.get('tags', []))}")
            st.write(f"**Stars:** {project.get('stars', 0)}")
            st.write(f"**Created:** {project.get('created_at', 'N/A')[:10]}")

with tab4:
    st.subheader("All Agents")
    
    st.write(f"**Total Agents: {len(agents)}**")
    
    for agent in agents:
        with st.expander(f"🤖 {agent.get('name', 'Unknown')} — {agent.get('status', 'N/A')}"):
            st.write(f"**Description:** {agent.get('description', 'N/A')}")
            st.write(f"**Industry:** {agent.get('industry', 'N/A')}")
            st.write(f"**Version:** {agent.get('version', 'N/A')}")
            st.write(f"**Authors:** {', '.join(agent.get('authors', []))}")
            st.write(f"**Created:** {agent.get('created_at', 'N/A')[:10]}")

with tab5:
    st.subheader("REX 2.0 Metadata Export")
    
    st.info("📤 Export metadata in REX 2.0 compatible format")
    
    export_type = st.selectbox("Export Type", 
                               ["Skills", "Agent Patterns", "Project Metadata", "Usage Metrics", "All"])
    
    if st.button("📥 Generate Export"):
        export_data = {}
        
        if export_type in ["Skills", "All"]:
            all_skills_list = []
            for human in humans:
                for skill in human.get('skills', []):
                    all_skills_list.append({
                        "skill": skill,
                        "human_id": human.get('id'),
                        "human_name": human.get('name')
                    })
            export_data['skills'] = all_skills_list
        
        if export_type in ["Agent Patterns", "All"]:
            export_data['agent_patterns'] = agents
        
        if export_type in ["Project Metadata", "All"]:
            export_data['projects'] = projects
        
        if export_type in ["Usage Metrics", "All"]:
            export_data['usage_metrics'] = {
                "total_humans": stats.get('total_humans', 0),
                "total_projects": stats.get('total_projects', 0),
                "total_agents": stats.get('total_agents', 0),
                "total_patterns": stats.get('total_patterns', 0),
                "last_updated": stats.get('last_updated')
            }
        
        if export_type == "All":
            export_data['reuse_opportunities'] = {
                "high_reuse_agents": [a for a in agents if a.get('status') in ['Customer READY', 'Production READY']],
                "popular_patterns": patterns[:10]  # Top 10 patterns
            }
        
        # Display JSON
        st.json(export_data)
        
        # Download button
        export_json = json.dumps(export_data, ensure_ascii=False, indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=export_json,
            file_name=f"rex2_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
