from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
import json
from app.services.tailoring_service import tailoring_service

router = APIRouter()

@router.post("/")
async def refine_resume(
    resume_text: str = Form(...),
    job_description: str = Form(...)
):
    """
    Refines the resume content based on the job description.
    """
    try:
        if not resume_text or not resume_text.strip():
            raise ValueError("Resume text is required")
        if not job_description or not job_description.strip():
            raise ValueError("Job description is required")
            
        refined_content = tailoring_service.refine_resume(resume_text, job_description)
        
        # Ensure response has required fields
        if isinstance(refined_content, dict):
            return {
                "summary": refined_content.get("summary", ""),
                "experience": refined_content.get("experience", "")
            }
        return refined_content
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Refine endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Refinement failed: {str(e)}")
