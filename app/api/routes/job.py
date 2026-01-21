from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.job_analyzer import job_analyzer

router = APIRouter()

class JobDescriptionRequest(BaseModel):
    description: str

@router.post("/analyze")
async def analyze_job(payload: JobDescriptionRequest):
    """
    Analyze raw job description text and extract requirements.
    """
    try:
        return job_analyzer.analyze(payload.description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

