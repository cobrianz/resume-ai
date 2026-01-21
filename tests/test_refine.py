import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# Add project root to path
sys.path.append(os.getcwd())

from app.services.tailoring_service import tailoring_service

def test_refine_resume_mock():
    print("--- Testing Refine Resume (Mock) ---")
    
    resume_text = "Experienced software engineer with python skills."
    job_desc = "Looking for a Senior Python Developer to lead the team."
    
    # Mock the OpenAI client
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content='{"summary": "Refined summary", "experience": "Refined experience"}'))
    ]
    mock_client.chat.completions.create.return_value = mock_response
    
    # Temporarily replace client
    original_client = tailoring_service.client
    tailoring_service.client = mock_client
    
    try:
        result = tailoring_service.refine_resume(resume_text, job_desc)
        print("Result:", result)
        
        assert "summary" in result
        assert "experience" in result
        assert result["summary"] == "Refined summary"
        print("SUCCESS: Mocked refinement returned expected structure.")
        
    finally:
        tailoring_service.client = original_client

if __name__ == "__main__":
    test_refine_resume_mock()
