# Running Resume AI with Streamlit

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App
```bash
streamlit run app_streamlit.py
```

The app will automatically open in your browser at `http://localhost:8501`

## Features

### 📄 Analyze Resume
- Upload PDF or DOCX resumes
- Automatically extract:
  - Skills
  - Work experience
  - Education
  - Contact information
  - Summary

### 🎯 Match Resume to Job
- Paste job descriptions
- Get detailed match scoring:
  - Overall match percentage
  - Skills match (40% weight)
  - Experience match (40% weight)
  - Keywords match (20% weight)
- See matched vs missing skills

### ✨ Refine Resume
- Get AI-powered suggestions
- Recommendations organized by category
- Export results as JSON

## Deployment

### Local Development
```bash
streamlit run app_streamlit.py
```

### Docker
```bash
docker build -t resume-ai-streamlit .
docker run -p 8501:8501 resume-ai-streamlit
```

### Cloud Platforms

**Streamlit Cloud (Free tier available):**
```bash
git push  # Push to GitHub
# Then deploy via https://share.streamlit.io
```

**Heroku:**
```bash
# Add Procfile:
# web: streamlit run app_streamlit.py --logger.level=error

git push heroku main
```

**AWS/GCP/Azure:**
- Use docker image
- Mount to port 8501
- No database needed (stateless)

## Configuration

Environment variables (`.env`):
```
PROJECT_NAME=Resume AI
API_V1_STR=/api/v1
MAX_UPLOAD_SIZE=10485760
OPENAI_API_KEY=your_key_here
```

## Session State

The app maintains session state across interactions:
- `resume_data`: Parsed resume from upload
- `job_data`: Analyzed job description
- `match_results`: Match calculation results

Clear session by refreshing the page or clicking "Clear Cache" in Streamlit menu.

## Performance Tips

- For large files, increase Streamlit's upload limit:
  ```bash
  streamlit run app_streamlit.py --client.maxUploadSize=50
  ```

- Cache expensive operations:
  ```python
  @st.cache_resource
  def load_model():
      # ...
  ```

## Troubleshooting

**Port already in use:**
```bash
streamlit run app_streamlit.py --server.port=8502
```

**Memory issues:**
- Use smaller embedding models
- Limit file sizes
- Clear session state regularly

**File upload errors:**
- Check file size limits
- Verify disk space
- Check file permissions

## Benefits Over FastAPI Version

✅ No frontend development needed  
✅ Faster prototyping and deployment  
✅ Built-in UI components  
✅ Easier state management  
✅ Native file upload handling  
✅ One-command deployment (Streamlit Cloud)  
✅ Hot reloading during development  
✅ Built-in metrics and charts support  

## Migration Notes

If migrating from FastAPI:
- Existing services work unchanged
- No need for separate frontend
- Session state replaces backend state management
- Streamlit handles CORS automatically
