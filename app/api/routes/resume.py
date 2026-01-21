from fastapi import APIRouter, File, UploadFile, HTTPException
import os
import shutil
import uuid
from app.services.resume_parser import resume_parser

router = APIRouter()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume (PDF/DOCX) and parse it into structured JSON.
    """
    allowed_types = [
        "application/pdf", 
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX are supported.")
    
    # Generate unique filename to avoid collisions
    file_ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        # Save file temporarily
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Parse resume
        parsed_data = resume_parser.parse(file_path, file.content_type)
        
        return parsed_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # Cleanup: Delete the temp file
        if os.path.exists(file_path):
            os.remove(file_path)

