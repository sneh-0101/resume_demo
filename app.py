import streamlit as st
import time
try:
    import utils.parser as parser
    import utils.nlp_processing as nlp_processing
    import utils.matcher as matcher
    import utils.report_generator as report_generator
    import plotly.graph_objects as go
except Exception as e:
    st.error(f"Error importing modules: {e}")
    st.stop()


# Set page configuration
st.set_page_config(
    page_title="AI Resume Matcher Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS loading function
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading CSS: {e}")

# Load the external CSS
local_css("assets/style.css")




def create_gauge_chart(score):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Match Score"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#4b6cb7"},
            'steps': [
                {'range': [0, 50], 'color': "#ffebee"},
                {'range': [50, 75], 'color': "#fff3e0"},
                {'range': [75, 100], 'color': "#e3f2fd"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

def main():
    col_header, col_logo = st.columns([4, 1])
    with col_header:
        st.title("🚀 AI Resume Analyzer & Job Matcher")
        st.markdown("### Optimize your job search with intelligent insights")

    with col_logo:
        # Theme Toggle in Header (Right Side)
        st.write("") # Spacer
        theme = st.toggle("🌙 Night Mode", value=True)

    # Dynamic Theme Injection (Now inside main so it responds to toggle state)
    if theme:
        st.markdown("""
        <style>
            :root {
                --background-color: #0E1117; /* Darkest Gray */
                --card-bg: #1F2937; /* Dark Gray */
                --text-primary: #F9FAFB; /* Light Gray */
                --text-secondary: #9CA3AF; /* Muted Gray */
                --primary-color: #6366F1; /* Indigo 500 (Brighter for dark mode) */
                --secondary-color: #60A5FA; /* Blue 400 */
                --input-bg: #374151; /* Input Fields Background */
            }
            .stApp {
                background-color: var(--background-color);
            }
            .main {
                background-color: var(--background-color);
            }
            h1, h2, h3, h4, h5, h6, p, span, div, label {
                color: var(--text-primary) !important;
            }
            .stCard {
                background-color: var(--card-bg);
                border: 1px solid #374151;
            }
            .metric-card {
                background-color: var(--card-bg) !important;
                color: var(--text-primary) !important;
            }
            .suggestion-box {
                background-color: #374151 !important;
                color: #F9FAFB !important;
                border-left: 5px solid #F59E0B;
            }
            
            /* Input Fields & Text Area Overrides */
            .stTextArea textarea, .stTextInput input {
                background-color: var(--input-bg) !important;
                color: var(--text-primary) !important;
                border-color: #4B5563 !important;
            }
            .stTextArea textarea:focus, .stTextInput input:focus {
                border-color: var(--primary-color) !important;
                box-shadow: 0 0 0 1px var(--primary-color) !important;
            }
            /* Placeholder Text Color Override */
            .stTextArea textarea::placeholder, .stTextInput input::placeholder {
                color: var(--text-secondary) !important;
                opacity: 1; /* Firefox */
            }
            
            /* File Uploader Overrides */
            .stFileUploader {
                background-color: var(--card-bg);
                padding: 15px;
                border-radius: 10px;
                border: 1px dashed #4B5563;
            }
            .stFileUploader section {
                background-color: var(--input-bg);
            }
            .stFileUploader span, .stFileUploader small {
                color: var(--text-secondary) !important;
            }
            .stFileUploader button {
                 color: var(--text-primary) !important;
            }

            /* Detailed Expander Styling */
            div[data-testid="stExpander"] details {
                border-color: #374151;
            }
            div[data-testid="stExpander"] details summary {
                background-color: var(--card-bg) !important;
                color: var(--text-primary) !important;
            }
            div[data-testid="stExpander"] details summary:hover {
                background-color: #374151 !important;
                color: #ffffff !important;
            }
            div[data-testid="stExpander"] div[role="button"] p {
                color: var(--text-primary) !important;
            }
            
            /* Detailed Button Styling */
            div[data-testid="stButton"] button {
                background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%) !important;
                color: white !important;
                border: none !important;
            }
            div[data-testid="stButton"] button p {
                color: white !important;
            }
            div[data-testid="stButton"] button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 8px rgba(0,0,0,0.15);
            }



        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
            .main {
                background-color: var(--background-color);
            }
        </style>
        """, unsafe_allow_html=True)


    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.markdown("#### 📂 Upload & Input")
        uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
        
        jd_text = st.text_area("Paste Job Description", height=250, placeholder="Paste the full job description here...")
        
        target_role = st.text_input("🎯 Target Role / Development Focus", placeholder="e.g. Senior Data Scientist")


        analyze_button = st.button("🔍 Analyze Resume")
        
        with st.expander("ℹ️ How it works"):
            st.write("""
            1. **Parsing**: We extract text from your PDF.
            2. **Processing**: We clean and tokenize content.
            3. **Hybrid Matching**: We combine TF-IDF (content similarity) and Direct Skill Mapping.
            4. **Insights**: We identify missing skills and provide specific improvement tips.
            """)

    # Initialize session state for report
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False

    if analyze_button:
        if uploaded_file is None:
            st.error("Please upload a resume first.")
        elif len(jd_text.strip()) < 50:
            st.error("Job Description is too short. Please provide more details for accurate matching.")
        else:
            with st.spinner("Analyzing profile against job requirements..."):
                time.sleep(1) # Visual effect
                
                # 1. Parse PDF
                resume_text = parser.extract_text_from_pdf(uploaded_file)
                
                if not resume_text:
                    st.error("Could not extract text. PDF might be image-based.")
                    return

                # 2. Preprocessing
                resume_clean = nlp_processing.clean_text(resume_text)
                jd_clean = nlp_processing.clean_text(jd_text)
                
                resume_lemma = nlp_processing.preprocess_text(resume_clean)
                jd_lemma = nlp_processing.preprocess_text(jd_clean)

                # 3. Skill Extraction
                resume_skills = nlp_processing.extract_skills(resume_clean)
                jd_skills = nlp_processing.extract_skills(jd_clean)
                
                matched_skills = sorted(list(set(resume_skills).intersection(set(jd_skills))))
                missing_skills = sorted(list(set(jd_skills).difference(set(resume_skills))))

                # 4. Hybrid Matching
                match_score = matcher.calculate_hybrid_score(resume_lemma, jd_lemma, resume_skills, jd_skills)
                
                # 5. Suggestions
                suggestions = nlp_processing.generate_suggestions(missing_skills)
                
                # 6. Generate Critique
                critique = nlp_processing.generate_critique(missing_skills, match_score, resume_text)

                
                # Save to session (for report gen)
                st.session_state.analysis_result = {
                    "score": match_score,
                    "matched": matched_skills,
                    "missing": missing_skills,
                    "matched": matched_skills,
                    "missing": missing_skills,
                    "suggestions": suggestions,
                    "critique": critique,
                    "filename": uploaded_file.name
                }

                st.session_state.analysis_done = True

    # Display Results if Analysis is Done
    if st.session_state.analysis_done:
        result = st.session_state.analysis_result
        
        with col2:
            st.markdown("#### 📊 Analysis Results")

            # Strategic Keywords Section (New)
            if result['missing']:
                st.markdown("### 💎 Strategic Keyword Recommendations")
                st.info("Adding these keywords can significantly improve your match score.")
                
                # Create a concise, copy-friendly format
                keywords_html = "".join([f'<span class="skill-tag missing-skill" style="cursor: pointer;" title="Add this">{skill}</span>' for skill in result['missing']])
                st.markdown(f"<div>{keywords_html}</div>", unsafe_allow_html=True)
                st.markdown("---")

            
            # Gauge Chart
            st.plotly_chart(create_gauge_chart(result['score']), use_container_width=True)
            
            # Tabs for details
            tab1, tab2, tab3 = st.tabs(["💡 Skills Gap", "✅ Matched Skills", "🚀 Improvement plan"])
            
            with tab1:
                st.write(f"**Missing Skills ({len(result['missing'])})**")
                if result['missing']:
                    missing_html = "".join([f'<span class="skill-tag missing-skill">{skill}</span>' for skill in result['missing']])
                    st.markdown(f"<div>{missing_html}</div>", unsafe_allow_html=True)
                else:
                    st.success("Perfect Match! You have all required skills.")
            
            with tab2:
                st.write(f"**Matched Skills ({len(result['matched'])})**")
                if result['matched']:
                    matches_html = "".join([f'<span class="skill-tag matched-skill">{skill}</span>' for skill in result['matched']])
                    st.markdown(f"<div>{matches_html}</div>", unsafe_allow_html=True)
                else:
                    st.info("No direct skill matches found.")

            with tab3:
                for suggestion in result['suggestions']:
                    st.markdown(f'<div class="suggestion-box">💡 {suggestion}</div>', unsafe_allow_html=True)
            
            # Detailed Resume Critique (New)
            st.markdown("---")
            st.markdown("### 📝 Detailed Resume Critique")
            with st.container():
                for point in result['critique']:
                    st.markdown(f"- {point}")


            # Download Report
            st.markdown("---")
            report_bytes = report_generator.generate_report(
                result['filename'], result['score'], result['matched'], result['missing'], result['suggestions']
            )
            
            st.download_button(
                label="📄 Download Detailed PDF Report",
                data=report_bytes,
                file_name="Resume_Analysis_Report.pdf",
                mime="application/pdf",
                help="Download a full report of this analysis."
            )

    # Future Scope Section
    st.markdown("---")
    with st.expander("🔮 Future Scope & Advanced AI Features"):
        st.markdown("""
        - **BERT/Transformer Models**: Replace TF-IDF with BERT embeddings for semantic understanding (e.g., understanding that "AI" and "Artificial Intelligence" are the same contextually).
        - **Entity Recognition (NER)**: Train a custom spaCy model to extract Education, Experience, and Certifications more accurately.
        - **LLM Integration**: Use Gemini or GPT-4 APIs to generate personalized cover letters based on the analysis.
        """)

if __name__ == "__main__":
    main()
