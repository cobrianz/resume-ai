import re
from typing import Dict, List, Any

class JobAnalyzer:
    def __init__(self):
        pass

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyzes job description text to extract structured requirements.
        """
        normalized_text = self._normalize_whitespace(text)
        
        return {
            "raw_text": normalized_text,
            "required_skills": self._extract_skills(normalized_text, "required"),
            "preferred_skills": self._extract_skills(normalized_text, "preferred"),
            "responsibilities": self._extract_responsibilities(normalized_text)
        }

    def _normalize_whitespace(self, text: str) -> str:
        text = text.replace('\xa0', ' ')
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        return text.strip()

    def _extract_skills(self, text: str, type: str = "required") -> List[str]:
        """
        Extracts skills based on sections.
        This is a heuristic implementation for Phase 2.
        """
        skills = []
        
        # Define section headers based on type
        if type == "required":
            pattern = r"(?im)^[\s]*(requirements|required skills|what we look for|qualifications)[\s:]*$"
        else:
            pattern = r"(?im)^[\s]*(preferred skills|nice to have|bonus points|desired)[\s:]*$"
            
        # Find start of section
        match = re.search(pattern, text)
        if not match:
            return skills
            
        start_idx = match.end()
        
        # Find end of section (next header or end of text)
        # Simple heuristic: stop at next double newline or next common header
        # For better robustness, we look for known headers
        next_header_pattern = r"(?im)^[\s]*(responsibilities|requirements|preferred|benefits|about)[\s:]*$"
        
        # Look for the NEXT header after the current one
        next_match = re.search(next_header_pattern, text[start_idx:])
        
        if next_match:
            end_idx = start_idx + next_match.start()
        else:
            end_idx = len(text)
            
        section_content = text[start_idx:end_idx].strip()
        
        # Split by bullets or newlines
        lines = section_content.split('\n')
        for line in lines:
            line = line.strip()
            # Remove common bullet points
            line = re.sub(r'^[\-\*•\d\.]+\s*', '', line)
            if line:
                skills.append(line)
                
        return skills

    def _extract_responsibilities(self, text: str) -> List[str]:
        responsibilities = []
        pattern = r"(?im)^[\s]*(responsibilities|what you will do|duties|role overview)[\s:]*$"
        
        match = re.search(pattern, text)
        if not match:
            return responsibilities
            
        start_idx = match.end()
        
        next_header_pattern = r"(?im)^[\s]*(requirements|preferred|benefits|about)[\s:]*$"
        next_match = re.search(next_header_pattern, text[start_idx:])
        
        if next_match:
            end_idx = start_idx + next_match.start()
        else:
            end_idx = len(text)
            
        section_content = text[start_idx:end_idx].strip()
        
        lines = section_content.split('\n')
        for line in lines:
            line = line.strip()
            line = re.sub(r'^[\-\*•\d\.]+\s*', '', line)
            if line:
                responsibilities.append(line)
                
        return responsibilities

job_analyzer = JobAnalyzer()
