# Community & Ambassadors — YES AI CAN
# Showcase Ambassador cohorts and community engagement

import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

st.set_page_config(
    page_title="Community & Ambassadors — YES AI CAN",
    layout="wide"
)

# Metadata storage
META_DIR = Path(__file__).parent.parent.parent.parent / ".sandbox_meta"
HUMANS_FILE = META_DIR / "humans.json"
PROJECTS_FILE = META_DIR / "projects.json"
META_DIR.mkdir(exist_ok=True)

def load_humans() -> List[Dict]:
    """Load all humans."""
    if HUMANS_FILE.exists():
        try:
            with open(HUMANS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

def load_projects() -> List[Dict]:
    """Load all projects."""
    if PROJECTS_FILE.exists():
        try:
            with open(PROJECTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
    return []

# Page header
st.title("🌍 Community & Ambassadors")
st.markdown("**YES AI CAN — Rackers Lab & Community**")
st.markdown("---")

humans = load_humans()
projects = load_projects()

# Tabs: Ambassadors, Leaderboard, Top Projects, Events
tab1, tab2, tab3, tab4 = st.tabs(["🌟 Ambassadors", "🏆 Leaderboard", "⭐ Top Projects", "📅 Events"])

with tab1:
    st.subheader("AI Ambassador Cohorts")
    
    ambassadors = [h for h in humans if h.get('ambassador', False)]
    
    if not ambassadors:
        st.info("🌟 No ambassadors yet. Apply to become an AI Ambassador!")
    else:
        st.write(f"**Total Ambassadors: {len(ambassadors)}**")
        
        # Group by region
        regions = {}
        for amb in ambassadors:
            region = amb.get('region', 'Unknown')
            if region not in regions:
                regions[region] = []
            regions[region].append(amb)
        
        for region, amb_list in regions.items():
            st.markdown(f"### {region} ({len(amb_list)} Ambassadors)")
            cols = st.columns(3)
            for idx, amb in enumerate(amb_list):
                with cols[idx % 3]:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                                border: 2px solid #ff0066; border-radius: 12px; padding: 1rem; margin-bottom: 1rem;
                                box-shadow: 0 4px 12px rgba(255,0,102,0.1);">
                        <h4 style="color: #ff0066; margin-bottom: 0.5rem;">🌟 {amb.get('name', 'Unknown')}</h4>
                        <p style="color: #334155; margin: 0.2rem 0;"><strong>Role:</strong> {amb.get('role', 'N/A')}</p>
                        <p style="color: #334155; margin: 0.2rem 0;"><strong>Skills:</strong> {', '.join(amb.get('skills', [])[:3])}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("📝 Apply to Ambassador Program", use_container_width=True):
            st.info("📝 Ambassador application form coming soon!")

with tab2:
    st.subheader("Contribution Leaderboard")
    
    # Calculate contributions
    contributions = {}
    for human in humans:
        human_id = human.get('id')
        contributions[human_id] = {
            'name': human.get('name', 'Unknown'),
            'projects': len([p for p in projects if human.get('name') in p.get('authors', [])]),
            'skills': len(human.get('skills', [])),
            'ambassador': human.get('ambassador', False),
            'total_score': 0
        }
        # Score: projects * 10 + skills * 2 + ambassador bonus 50
        contributions[human_id]['total_score'] = (
            contributions[human_id]['projects'] * 10 +
            contributions[human_id]['skills'] * 2 +
            (50 if contributions[human_id]['ambassador'] else 0)
        )
    
    # Sort by score
    sorted_contributors = sorted(contributions.values(), key=lambda x: x['total_score'], reverse=True)
    
    st.write(f"**Top {min(10, len(sorted_contributors))} Contributors**")
    
    for idx, contrib in enumerate(sorted_contributors[:10], 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
                    border: 2px solid #00d4ff; border-radius: 12px; padding: 1rem; margin-bottom: 0.5rem;
                    box-shadow: 0 4px 12px rgba(0,212,255,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="color: #00d4ff; margin: 0;">{medal} {contrib['name']}</h4>
                    <p style="color: #334155; margin: 0.3rem 0;">Projects: {contrib['projects']} | Skills: {contrib['skills']}</p>
                </div>
                <div style="font-size: 1.5rem; font-weight: 700; color: #ff0066;">
                    {contrib['total_score']} pts
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("Top Projects by Stars")
    
    # Sort projects by stars
    sorted_projects = sorted(projects, key=lambda x: x.get('stars', 0), reverse=True)
    
    if not sorted_projects:
        st.info("⭐ No projects yet. Submit your first project!")
    else:
        for idx, project in enumerate(sorted_projects[:10], 1):
            medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"#{idx}"
            with st.expander(f"{medal} {project.get('title', 'Untitled')} — ⭐ {project.get('stars', 0)} stars"):
                st.write(f"**Description:** {project.get('description', 'N/A')}")
                st.write(f"**Authors:** {', '.join(project.get('authors', []))}")
                st.write(f"**Phase:** {project.get('phase', 'N/A')}")
                st.write(f"**Tags:** {', '.join(project.get('tags', []))}")

with tab4:
    st.subheader("Upcoming Events & Activities")
    
    st.info("📅 Event calendar coming soon! Check back for AI Ambassador meetups, workshops, and community events.")
    
    # Placeholder for events
    st.markdown("""
    ### 🎯 Upcoming Events
    
    - **AI Ambassador Monthly Meetup** — First Tuesday of each month
    - **YES AI CAN Workshop Series** — Every other Thursday
    - **Customer ZERO → Customer ONE Showcase** — Quarterly
    
    ### 📢 Announcements
    
    - New AI Ambassador cohort applications open!
    - Project Hub now supports collaborative feedback
    - Agent Library updated with latest Customer ZERO agents
    """)
