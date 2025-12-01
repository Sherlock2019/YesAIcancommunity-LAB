# Documentation & Learning — YES AI CAN
# Learning resources and documentation

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Documentation & Learning — YES AI CAN",
    layout="wide"
)

# Page header
st.title("📚 Documentation & Learning")
st.markdown("**YES AI CAN — Rackers Lab & Community**")
st.markdown("---")

# Tabs: Getting Started, Guides, Resources, FAQs
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Getting Started", "📖 Guides", "📚 Resources", "❓ FAQs"])

with tab1:
    st.subheader("Getting Started with YES AI CAN")
    
    st.markdown("""
    ### Welcome to YES AI CAN!
    
    **YES AI CAN** is Rackspace's internal AI innovation ecosystem. Here's how to get started:
    
    #### Step 1: Create Your Profile
    1. Navigate to **👤 Human Stack Directory**
    2. Click **➕ Create/Edit Profile**
    3. Fill in your information:
       - Name, Department, Team, Role
       - Skills and domain expertise
       - Resume upload
       - Portfolio/GitHub links
    4. Save your profile
    
    #### Step 2: Explore Projects
    1. Go to **🧱 Project Hub**
    2. Browse existing AI projects by Rackers
    3. Filter by phase, tags, or search
    4. Star projects you find interesting
    
    #### Step 3: Test Agents
    1. Visit **🤖 Agent Library**
    2. Browse available Customer ZERO agents
    3. Launch agents in the sandbox
    4. Provide feedback and suggestions
    
    #### Step 4: Contribute
    - Submit your own projects
    - Share reusable patterns
    - Join the AI Ambassador program
    - Help build the Customer ZERO → Customer ONE library
    """)

with tab2:
    st.subheader("Learning Guides")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🧱 Project Submission Guide
        
        **How to submit a new project:**
        
        1. Go to **Project Hub** → **➕ Submit Project**
        2. Fill in project details:
           - Title and description
           - What / So What / For Who / How / Where
           - Current phase (Incubation / MVP / Production)
           - Tags and links
        3. Upload artifacts (screenshots, PDFs)
        4. Submit and share with the community
        
        ### 🤖 Agent Library Guide
        
        **How to add an agent:**
        
        1. Navigate to **Agent Library** → **➕ Add Agent**
        2. Provide agent metadata:
           - Name, version, description
           - Industry vertical
           - Inputs/outputs
           - Required datasets/models
        3. Set status (Draft / Prototype / Customer READY)
        4. Save to library
        """)
    
    with col2:
        st.markdown("""
        ### 👤 Profile Best Practices
        
        **Make your profile stand out:**
        
        - List all relevant skills (AI, ML, domain expertise)
        - Upload your resume
        - Link to GitHub/Portfolio
        - Add domain expertise tags
        - Join the AI Ambassador program
        
        ### 🧠 Ontology & Patterns
        
        **How to contribute patterns:**
        
        1. Go to **Ontology & Patterns** → **➕ Add New**
        2. Choose Pattern or Ontology Entry
        3. Provide template code and examples
        4. Tag appropriately
        5. Share with the community
        """)

with tab3:
    st.subheader("Learning Resources")
    
    st.markdown("""
    ### 📚 Internal Resources
    
    - **AI Ambassador Program**: Join to advance your AI journey
    - **Customer ZERO Agent Library**: Reusable agents for internal use
    - **Pattern Library**: Reusable AI design patterns
    - **Project Showcase**: See what other Rackers have built
    
    ### 🔗 External Resources
    
    - **OpenStack AI Documentation**: Coming soon
    - **Private AI Best Practices**: Coming soon
    - **Explainable AI Guidelines**: Coming soon
    
    ### 🎓 Training & Workshops
    
    - **AI Ambassador Monthly Meetup**: First Tuesday of each month
    - **YES AI CAN Workshop Series**: Every other Thursday
    - **Customer ZERO → Customer ONE Showcase**: Quarterly
    """)

with tab4:
    st.subheader("Frequently Asked Questions")
    
    with st.expander("What is YES AI CAN?"):
        st.write("""
        YES AI CAN is Rackspace's internal AI innovation ecosystem, built to map our global AI skills, 
        showcase AI projects, provide zero-code tools for building agents, and accelerate reuse through 
        a shared Customer ZERO agent library.
        """)
    
    with st.expander("Who can use YES AI CAN?"):
        st.write("""
        All Rackers! Whether you're technical or not, YES AI CAN gives you the tools to step into AI 
        safely, transparently, and with full support.
        """)
    
    with st.expander("How do I become an AI Ambassador?"):
        st.write("""
        Visit the **🌍 Community & Ambassadors** page and click "Apply to Ambassador Program". 
        Ambassadors help drive AI innovation across Rackspace.
        """)
    
    with st.expander("What is Customer ZERO vs Customer ONE?"):
        st.write("""
        - **Customer ZERO**: Internal agents and prototypes built by Rackers for internal use
        - **Customer ONE**: Production-ready agents that can be deployed to customers
        The Agent Library helps you move agents from ZERO to ONE.
        """)
    
    with st.expander("How do I submit a project?"):
        st.write("""
        Go to **🧱 Project Hub** → **➕ Submit Project** and fill in the project details form. 
        Include What/So What/For Who/How/Where/What Now/What Next sections.
        """)
    
    with st.expander("Can I use existing agents in my projects?"):
        st.write("""
        Yes! Browse the **🤖 Agent Library** to find reusable agents. You can launch them in the sandbox, 
        test them, and provide feedback. Customer READY agents can be published to Customer ONE.
        """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 2rem;">
        💎 YES AI CAN — Rackers Lab & Community | Made with ❤️ by Rackers
    </div>
""", unsafe_allow_html=True)
