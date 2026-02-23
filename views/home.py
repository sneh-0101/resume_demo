import streamlit as st

def show():
    # Hero Section
    st.markdown("""
        <div class="hero-section">
            <div class="hero-title">AI-Powered Resume Analysis <br>& Job Matching</div>
            <div class="hero-subtitle">
                Unlock your career potential. Upload your resume, match with job roles, 
                and get personalized improvement suggestions in seconds.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Features Grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="stCard">
                <h3>📜 Smart Parsing</h3>
                <p>Advanced PDF parsing to extract skills, experience, and education with high accuracy.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="stCard">
                <h3>🎯 Precision Matching</h3>
                <p>Hybrid matching algorithm using TF-IDF and semantic analysis to score resumes against JDs.</p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="stCard">
                <h3>🚀 Actionable Insights</h3>
                <p>Get detailed gap analysis, missing keywords, and interview preparation questions.</p>
            </div>
        """, unsafe_allow_html=True)

    # Call to Action
    st.markdown("### ready to optimize your job search?")
    if st.button("🚀 Start Analysis Now", type="primary", use_container_width=True):
        st.session_state.page_selection = "match"
        st.rerun()
