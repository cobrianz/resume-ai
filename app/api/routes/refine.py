from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
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
        refined_content = tailoring_service.refine_resume(resume_text, job_description)
        return refined_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
