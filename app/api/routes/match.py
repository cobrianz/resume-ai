from fastapi import APIRouter, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
from typing import Optional
import os
import shutil
import uuid

from app.services.resume_parser import resume_parser
from app.services.job_analyzer import job_analyzer
from app.services.matching_engine import matching_engine
from app.services.tailoring_service import tailoring_service

router = APIRouter()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class MatchRequest(BaseModel):
    job_description: str

@router.post("/")
async def match_resume_to_job(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    """
    Complete end-to-end matching:
    1. Parse resume
    2. Analyze job
    3. Compute match score
    4. Generate tailoring suggestions
    """
    
    # Validate file type
    allowed_types = [
        "application/pdf", 
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    if resume_file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX are supported.")
    
    # Save file temporarily
    file_ext = os.path.splitext(resume_file.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # 1. Parse Resume
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume_file.file, buffer)
            
        resume_data = resume_parser.parse(file_path, resume_file.content_type)
        
        # 2. Analyze Job
        job_data = job_analyzer.analyze(job_description)
        
        # 3. Compute Match Score
        match_result = matching_engine.compute_score(resume_data, job_data)
        
        # 4. Identify Missing Skills
        resume_skills_set = set([s.lower() for s in resume_data.get("skills", [])])
        job_skills_set = set([s.lower() for s in job_data.get("required_skills", [])])
        missing_skills = list(job_skills_set - resume_skills_set)
        
        # 5. Generate Suggestions
        suggestions, prompt = tailoring_service.generate_suggestions(
            resume_data.get("raw_text", ""),
            job_description,
            missing_skills
        )
        
        return {
            "match_score": match_result,
            "missing_skills": missing_skills,
            "suggestions": suggestions,
            "resume_text": resume_data.get("raw_text", "")
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)

