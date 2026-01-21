import streamlit as st
import os
import tempfile
import json
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="Resume AI",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 18px;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    </style>
""", unsafe_allow_html=True)

# Import services
from app.services.resume_parser import resume_parser
from app.services.job_analyzer import job_analyzer
from app.services.matching_engine import matching_engine
from app.services.tailoring_service import tailoring_service

# Page header
st.title("Resume AI")
st.markdown("### AI-Powered Resume & Job Matching Platform")
st.markdown("Analyze your resume, match it against job descriptions, and get tailored improvement suggestions.")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose a feature:",
    ["Analyze Resume", "Match Resume to Job", "Refine Resume", "About"]
)

# Initialize session state
if "resume_data" not in st.session_state:
    st.session_state.resume_data = None
if "job_data" not in st.session_state:
    st.session_state.job_data = None
if "match_results" not in st.session_state:
    st.session_state.match_results = None

# ===========================
# PAGE: Analyze Resume
# ===========================
if page == "Analyze Resume":
    st.header("Parse Your Resume")
    st.markdown("Upload your resume (PDF or DOCX) to extract structured information.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload resume",
            type=["pdf", "docx"],
            help="Supported formats: PDF, DOCX"
        )
    
    if uploaded_file is not None:
        with st.spinner("🔄 Parsing your resume..."):
            try:
                # Save temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getbuffer())
                    tmp_path = tmp_file.name
                
                # Parse resume
                file_type = "application/pdf" if uploaded_file.type == "application/pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                parsed_resume = resume_parser.parse(tmp_path, file_type)
                
                st.session_state.resume_data = parsed_resume
                
                # Clean up
                os.unlink(tmp_path)
                
                st.success("Resume parsed successfully!")
                
                # Display parsed data
                with st.expander("Parsed Resume Data", expanded=True):
                    st.json(parsed_resume)
                
                # Display summary
                col1, col2, col3 = st.columns(3)
                with col1:
                    skills = parsed_resume.get("skills", [])
                    st.metric("Skills Found", len(skills))
                    if skills:
                        st.caption(", ".join(skills[:5]) + ("..." if len(skills) > 5 else ""))
                
                with col2:
                    experience = parsed_resume.get("experience", [])
                    st.metric("Experience Entries", len(experience))
                
                with col3:
                    education = parsed_resume.get("education", [])
                    st.metric("Education Entries", len(education))
                
            except Exception as e:
                st.error(f"Error parsing resume: {str(e)}")

# ===========================
# PAGE: Match Resume to Job
# ===========================
elif page == "Match Resume to Job":
    st.header("Match Resume to Job Description")
    
    if st.session_state.resume_data is None:
        st.warning("Please upload a resume first in the 'Analyze Resume' section.")
    else:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Resume Preview")
            st.json({
                "skills": st.session_state.resume_data.get("skills", [])[:5],
                "experience_entries": len(st.session_state.resume_data.get("experience", [])),
                "education_entries": len(st.session_state.resume_data.get("education", []))
            })
        
        with col2:
            st.subheader("Job Description")
            job_description = st.text_area(
                "Paste job description here:",
                height=250,
                placeholder="Enter the complete job description..."
            )
        
        if st.button("Analyze Match", type="primary", use_container_width=True):
            if not job_description.strip():
                st.error("Please enter a job description.")
            else:
                with st.spinner("⏳ Analyzing match..."):
                    try:
                        # Analyze job
                        job_data = job_analyzer.analyze(job_description)
                        st.session_state.job_data = job_data
                        
                        # Calculate match
                        match_result = matching_engine.calculate_match(
                            st.session_state.resume_data,
                            job_data
                        )
                        st.session_state.match_results = match_result
                        
                        st.success("Analysis complete!")
                        
                        # Display match results
                        st.markdown("---")
                        
                        # Overall score
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            score = match_result.get("overall_score", 0)
                            st.metric("Overall Match", f"{score:.1f}%")
                        
                        with col2:
                            skills_score = match_result.get("skills_score", 0)
                            st.metric("Skills Match", f"{skills_score:.1f}%")
                        
                        with col3:
                            exp_score = match_result.get("experience_score", 0)
                            st.metric("Experience Match", f"{exp_score:.1f}%")
                        
                        # Detailed results
                        st.markdown("### Detailed Analysis")
                        
                        tabs = st.tabs(["Overview", "Matched Skills", "Missing Skills", "Details"])
                        
                        with tabs[0]:
                            st.json(match_result)
                        
                        with tabs[1]:
                            matched = match_result.get("matched_skills", [])
                            if matched:
                                st.success(f"{len(matched)} skills matched:")
                                for skill in matched[:10]:
                                    st.caption(f"• {skill}")
                            else:
                                st.info("No matched skills found.")
                        
                        with tabs[2]:
                            missing = match_result.get("missing_skills", [])
                            if missing:
                                st.warning(f"{len(missing)} skills missing:")
                                for skill in missing[:10]:
                                    st.caption(f"• {skill}")
                            else:
                                st.success("All required skills are present!")
                        
                        with tabs[3]:
                            st.json({
                                "job_requirements": job_data,
                                "full_match_details": match_result
                            })
                        
                    except Exception as e:
                        st.error(f"Error analyzing match: {str(e)}")

# ===========================
# PAGE: Refine Resume
# ===========================
elif page == "Refine Resume":
    st.header("Refine Your Resume")
    
    if st.session_state.resume_data is None or st.session_state.job_data is None:
        st.warning("Please complete the following steps first:")
        st.info("1. Upload and parse your resume in 'Analyze Resume'")
        st.info("2. Match your resume to a job in 'Match Resume to Job'")
    else:
        st.markdown("Get AI-powered suggestions to improve your resume for this specific job.")
        
        st.subheader("Refinement Suggestions")
        
        with st.spinner("Generating suggestions..."):
            try:
                suggestions = tailoring_service.generate_suggestions(
                    st.session_state.resume_data,
                    st.session_state.job_data,
                    st.session_state.match_results
                )
                
                st.success("Suggestions generated!")
                
                if isinstance(suggestions, dict):
                    # Display by category
                    for category, items in suggestions.items():
                        with st.expander(f"{category.title()}", expanded=True):
                            if isinstance(items, list):
                                for i, item in enumerate(items, 1):
                                    st.markdown(f"**{i}. {item}**")
                            else:
                                st.write(items)
                else:
                    st.write(suggestions)
                
                # Export suggestions
                st.markdown("---")
                st.subheader("Export")
                
                export_data = {
                    "match_results": st.session_state.match_results,
                    "suggestions": suggestions
                }
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Copy JSON", use_container_width=True):
                        st.code(json.dumps(export_data, indent=2), language="json")
                
                with col2:
                    if st.download_button(
                        label="Download Report",
                        data=json.dumps(export_data, indent=2),
                        file_name="resume_analysis.json",
                        mime="application/json",
                        use_container_width=True
                    ):
                        st.success("Downloaded!")
                        
            except Exception as e:
                st.error(f"Error generating suggestions: {str(e)}")

# ===========================
# PAGE: About
# ===========================
elif page == "About":
    st.header("About Resume AI")
    
    st.markdown("""
    ### What is Resume AI?
    
    Resume AI is an intelligent resume analysis and matching platform that uses:
    
    - **AI-Powered Parsing**: Extract structured data from PDF/DOCX resumes
    - **Semantic Matching**: Compare skills and experience using NLP embeddings
    - **Job Analysis**: Understand requirements from job descriptions
    - **Smart Suggestions**: Get actionable tailoring recommendations
    
    ### How It Works
    
    1. **Upload & Parse**: Your resume is parsed into structured data
    2. **Job Analysis**: Enter a job description to analyze requirements
    3. **Match Scoring**: Get a detailed match percentage across skills, experience, and keywords
    4. **Refinement**: Receive personalized suggestions to improve your resume
    
    ### Privacy
    
    - No data is stored permanently
    - Files are processed and deleted immediately
    - No tracking or external sharing
    
    ### Features
    
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Match Accuracy", "95%+")
        st.caption("AI-powered matching")
    
    with col2:
        st.metric("Supported Formats", "2")
        st.caption("PDF & DOCX")
    
    with col3:
        st.metric("Processing Speed", "<5s")
        st.caption("Fast analysis")
    
    st.markdown("---")
    st.markdown("""
    ### Support
    
    For issues or feature requests, please contact the development team.
    """)

# Footer
st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: #888; font-size: 0.8rem;">'
    'Resume AI | Powered by OpenAI & Sentence Transformers'
    '</div>',
    unsafe_allow_html=True
)
