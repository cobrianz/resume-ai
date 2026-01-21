import os
import shutil
import re
from typing import Dict, Any, List
from fastapi import UploadFile, HTTPException
import pdfplumber
import docx

class ResumeParser:
    def __init__(self):
        pass

    def extract_text(self, file_path: str, content_type: str) -> str:
        """Extracts raw text from PDF or DOCX."""
        text = ""
        try:
            if content_type == "application/pdf":
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
            elif content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(file_path)
                for para in doc.paragraphs:
                    text += para.text + "\n"
            else:
                raise ValueError("Unsupported file type")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")
        
        return self._normalize_whitespace(text)

    def _normalize_whitespace(self, text: str) -> str:
        """Cleans up extra spaces and newlines."""
        # Replace non-breaking spaces
        text = text.replace('\xa0', ' ')
        # Replace multiple spaces (not newlines) with single space
        text = re.sub(r'[ \t]+', ' ', text)
        # Replace multiple newlines with single newline
        text = re.sub(r'\n+', '\n', text)
        return text.strip()

    def parse(self, file_path: str, content_type: str) -> Dict[str, Any]:
        """Main entry point to parse resume file into structured data."""
        raw_text = self.extract_text(file_path, content_type)
        
        structured_data = self._extract_sections(raw_text)
        structured_data["raw_text"] = raw_text
        
        return structured_data

    def _extract_sections(self, text: str) -> Dict[str, List[str]]:
        """
        Heuristic-based section extraction using Regex.
        Identifies headers like 'Experience', 'Education', 'Skills' and captures content.
        """
        sections = {
            "skills": [],
            "experience": [],
            "education": [],
            "certifications": []
        }
        
        # Define keywords for sections
        # Use multiline mode to match headers that are on their own lines
        patterns = {
            "experience": r"(?im)^[\s]*(experience|employment|work history)[\s:]*$",
            "education": r"(?im)^[\s]*(education|academic|qualifications)[\s:]*$",
            "skills": r"(?im)^[\s]*(skills|technologies|technical skills)[\s:]*$",
            "certifications": r"(?im)^[\s]*(certifications?|licenses?)[\s:]*$"
        }
        
        # Find all header positions
        matches = []
        for key, pattern in patterns.items():
            for match in re.finditer(pattern, text):
                matches.append((match.start(), key))
                
        matches.sort()
        
        # If no sections found, return empty
        if not matches:
            return sections
            
        # Extract content between headers
        for i in range(len(matches)):
            start_idx, section_name = matches[i]
            # Content starts after the header (plus some margin for newlines)
            header_end = start_idx + len(section_name) # Approximate, but works for simple keywords
            # Find the actual end of the line for the header
            next_newline = text.find('\n', start_idx)
            if next_newline != -1:
                content_start = next_newline + 1
            else:
                content_start = header_end

            # End index is the start of the next section
            if i < len(matches) - 1:
                end_idx = matches[i+1][0]
            else:
                end_idx = len(text)
                
            content = text[content_start:end_idx].strip()
            
            # Simple content splitting (lines or bullets)
            # This is naive but meets Phase 1 criteria
            items = [line.strip() for line in content.split('\n') if line.strip()]
            sections[section_name].extend(items)
            
        return sections


resume_parser = ResumeParser()
