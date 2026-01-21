import streamlit as st
import os
import tempfile
import json
from pathlib import Path

st.set_page_config(
    page_title="Resume AI - Smart Resume Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    body {
        background: #f8f9ff;
    }
    
    .main {
        background: white;
        padding: 0;
    }
    
    [data-testid="stSidebar"] {
        display: none;
    }
    
    [data-testid="stAppViewContainer"] {
        padding: 0;
    }
    
    .hero {
        background: linear-gradient(180deg, #f8f9ff 0%, #ffffff 100%);
        padding: 100px 40px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .hero-content {
        max-width: 700px;
        margin: 0 auto;
    }
    
    .hero-badge {
        display: inline-block;
        padding: 8px 20px;
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 24px;
    }
    
    .hero-title {
        font-size: 56px;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 24px;
        color: #1f2937;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .hero-subtitle {
        font-size: 18px;
        color: #6b7280;
        line-height: 1.6;
        max-width: 600px;
        margin: 0 auto 40px;
    }
    
    .section-title {
        font-size: 40px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 60px;
    }
    
    .features {
        padding: 80px 40px;
        background: #f9fafb;
    }
    
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 32px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .feature-card {
        background: white;
        padding: 32px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }
    
    .feature-card h3 {
        font-size: 20px;
        margin-bottom: 12px;
    }
    
    .feature-card p {
        color: #6b7280;
        font-size: 14px;
    }
    
    .analyzer {
        padding: 80px 40px;
        background: white;
    }
    
    .analyzer-container {
        max-width: 800px;
        margin: 0 auto;
    }
    
    .score-card {
        background: white;
        padding: 32px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
    }
    
    .score-item {
        display: grid;
        grid-template-columns: 140px 1fr 60px;
        align-items: center;
        gap: 16px;
        margin-bottom: 16px;
    }
    
    .progress-bar {
        height: 8px;
        background: #f9fafb;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 1s ease;
    }
    
    .skill-tag {
        display: inline-block;
        padding: 8px 16px;
        background: #fef3c7;
        color: #92400e;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    .how-it-works {
        padding: 80px 40px;
        background: #f9fafb;
    }
    
    .steps-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 32px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .step {
        text-align: center;
    }
    
    .step-number {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        font-weight: 700;
        margin: 0 auto 20px;
    }
    
    .step h3 {
        margin-bottom: 12px;
        font-size: 18px;
    }
    
    .step p {
        color: #6b7280;
        font-size: 14px;
    }
    
    .footer {
        background: #1f2937;
        color: white;
        padding: 40px;
        text-align: center;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# Import services with error handling
try:
    from app.services.resume_parser import resume_parser
    from app.services.job_analyzer import job_analyzer
    from app.services.matching_engine import matching_engine
    from app.services.tailoring_service import tailoring_service
    services_loaded = True
except Exception as e:
    services_loaded = False
    error_msg = str(e)

# Header
st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; padding: 20px 40px; border-bottom: 1px solid #e5e7eb; background: white;">
        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 18px;">R</div>
        <span style="font-size: 24px; font-weight: 700; color: #1f2937;">Resume AI</span>
    </div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero">
        <div class="hero-content">
            <div class="hero-badge">AI-Powered Analysis</div>
            <h1 class="hero-title">Build a Job-Winning <span class="gradient-text">Resume</span> Effortlessly with AI.</h1>
            <p class="hero-subtitle">Build a standout, job-ready resume in minutes with AI. Get career-polished, and tailored content—fast, simple, and effortlessly professional.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Features Section
st.markdown("""
    <div class="features">
        <h2 class="section-title">Powerful Features</h2>
        <div class="features-grid">
            <div class="feature-card">
                <h3>Smart Parsing</h3>
                <p>Automatically extract skills, experience, and education from PDF/DOCX resumes</p>
            </div>
            <div class="feature-card">
                <h3>AI Matching</h3>
                <p>Semantic analysis with 40% skills + 40% experience + 20% keywords scoring</p>
            </div>
            <div class="feature-card">
                <h3>Smart Suggestions</h3>
                <p>Get context-aware recommendations to improve your resume for specific roles</p>
            </div>
            <div class="feature-card">
                <h3>Privacy First</h3>
                <p>Your data is never stored. All files are auto-deleted after analysis</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main Analyzer Section
st.markdown("""
    <div class="analyzer">
        <h2 class="section-title">Analyze Your Resume</h2>
        <div class="analyzer-container">
""", unsafe_allow_html=True)

if not services_loaded:
    st.error(f"Error loading services: {error_msg}")
    st.info("Please install dependencies: pip install -r requirements.txt")
    st.stop()

# Step 1: Upload Resume
st.markdown("<h3>Step 1: Upload Your Resume</h3>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx"], label_visibility="collapsed")

# Step 2: Job Description
st.markdown("<h3 style='margin-top: 32px;'>Step 2: Paste Job Description</h3>", unsafe_allow_html=True)
job_description = st.text_area(
    "Job Description",
    placeholder="Paste the job description here...\n\nExample:\nSenior Python Developer\n\nResponsibilities:\n- Build scalable REST APIs using FastAPI\n- Design database schemas\n\nRequirements:\n- 5+ years Python experience\n- Strong knowledge of FastAPI and Docker",
    height=200,
    label_visibility="collapsed"
)

# Initialize session state
if "resume_data" not in st.session_state:
    st.session_state.resume_data = None
if "job_data" not in st.session_state:
    st.session_state.job_data = None
if "match_results" not in st.session_state:
    st.session_state.match_results = None

col1, col2 = st.columns([3, 1])
with col1:
    if st.button("Analyze Resume", use_container_width=True, type="primary"):
        if uploaded_file is None:
            st.error("Please upload a resume")
        elif len(job_description.strip()) < 50:
            st.error("Please enter a job description (at least 50 characters)")
        else:
            with st.spinner("Analyzing your resume..."):
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                        tmp_file.write(uploaded_file.getbuffer())
                        tmp_path = tmp_file.name
                    
                    file_type = "application/pdf" if uploaded_file.type == "application/pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    parsed_resume = resume_parser.parse(tmp_path, file_type)
                    st.session_state.resume_data = parsed_resume
                    
                    job_data = job_analyzer.analyze(job_description)
                    st.session_state.job_data = job_data
                    
                    match_result = matching_engine.calculate_match(parsed_resume, job_data)
                    st.session_state.match_results = match_result
                    
                    os.unlink(tmp_path)
                    st.success("Analysis complete!")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")

st.markdown("</div></div>", unsafe_allow_html=True)

# Results Section
if st.session_state.match_results:
    st.markdown("""
        <div class="analyzer">
            <h3 style="margin-bottom: 32px;">Analysis Results</h3>
    """, unsafe_allow_html=True)
    
    # Match Score
    st.markdown("""<div class="score-card">""", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<h4>Match Score</h4>", unsafe_allow_html=True)
    with col2:
        score = st.session_state.match_results.get("overall_score", 0)
        st.markdown(f"<div style='font-size: 48px; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; text-align: right;'>{score:.1f}%</div>", unsafe_allow_html=True)
    
    # Score Breakdown
    st.markdown("<div style='margin-top: 32px;'>", unsafe_allow_html=True)
    
    score_items = [
        ("Skills Match", st.session_state.match_results.get("skills_score", 0)),
        ("Experience Match", st.session_state.match_results.get("experience_score", 0)),
        ("Keywords Match", st.session_state.match_results.get("keyword_score", 0)),
    ]
    
    for label, value in score_items:
        col1, col2, col3 = st.columns([2, 6, 1])
        with col1:
            st.markdown(f"<span style='font-size: 14px; color: #6b7280;'>{label}</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style='height: 8px; background: #f9fafb; border-radius: 4px; overflow: hidden;'>
                    <div style='height: 100%; background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); width: {value}%;'></div>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"<span style='font-weight: 600;'>{value:.1f}%</span>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Missing Skills
    missing_skills = st.session_state.match_results.get("missing_skills", [])
    if missing_skills:
        st.markdown("""<div class="score-card"><h4>Missing Skills</h4>""", unsafe_allow_html=True)
        skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in missing_skills[:10]])
        st.markdown(f"<div>{skills_html}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Suggestions
    st.markdown("""<div class="score-card"><h4>Tailored Suggestions</h4>""", unsafe_allow_html=True)
    suggestions = st.session_state.match_results.get("suggestions", [])
    for suggestion in suggestions[:5]:
        st.markdown(f"""
            <div style='padding: 20px; background: #f9fafb; border-radius: 12px; margin-bottom: 16px; border-left: 4px solid #667eea;'>
                <h5 style='color: #667eea; margin-bottom: 8px; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px;'>{suggestion.get('section', 'Suggestion')}</h5>
                <p style='margin-bottom: 8px; font-size: 15px;'><strong>{suggestion.get('suggestion', '')}</strong></p>
                <small style='color: #6b7280; font-style: italic;'>{suggestion.get('justification', '')}</small>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# How It Works Section
st.markdown("""
    <div class="how-it-works">
        <h2 class="section-title">How It Works</h2>
        <div class="steps-grid">
            <div class="step">
                <div class="step-number">1</div>
                <h3>Upload Resume</h3>
                <p>Upload your resume in PDF or DOCX format</p>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <h3>Add Job Description</h3>
                <p>Paste the job posting you're interested in</p>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <h3>AI Analysis</h3>
                <p>Our AI analyzes semantic match using embeddings</p>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <h3>Get Insights</h3>
                <p>Receive match score and tailored suggestions</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <p>Built with ❤ using FastAPI, SentenceTransformers, and OpenAI</p>
        <div style="margin-top: 16px; display: flex; justify-content: center; gap: 24px;">
            <a href="http://localhost:8000/docs" target="_blank" style="color: rgba(255, 255, 255, 0.8); text-decoration: none;">API Docs</a>
            <a href="https://github.com" target="_blank" style="color: rgba(255, 255, 255, 0.8); text-decoration: none;">GitHub</a>
        </div>
    </div>
""", unsafe_allow_html=True)
