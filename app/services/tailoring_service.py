from typing import List, Dict, Any
import json
from openai import OpenAI
from app.core.config import settings

class TailoringService:
    def __init__(self):
        self.client = None
        if settings.OPENAI_API_KEY:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate_suggestions(
        self, 
        resume_text: str, 
        job_description: str, 
        missing_skills: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generates tailoring suggestions based on the gap between resume and job.
        """
        prompt = self._build_prompt(resume_text, job_description, missing_skills)
        
        # If OpenAI API key is configured, use real AI
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert career coach and resume writer. Provide specific, actionable suggestions in JSON format."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                # Parse AI response
                ai_text = response.choices[0].message.content
                
                # Try to extract JSON from response
                try:
                    # Look for JSON array in the response
                    start = ai_text.find('[')
                    end = ai_text.rfind(']') + 1
                    if start != -1 and end > start:
                        suggestions = json.loads(ai_text[start:end])
                        return suggestions, prompt
                except:
                    pass
                    
                # If JSON parsing fails, create structured response from text
                return self._parse_text_to_suggestions(ai_text), prompt
                
            except Exception as e:
                print(f"OpenAI API Error: {e}")
                # Fall back to mock if API fails
        
        # Fallback: Mocked response (when no API key or API fails)
        mock_suggestions = [
            {
                "section": "Skills",
                "suggestion": f"Add {', '.join(missing_skills[:3])} to your skills section." if missing_skills else "Emphasize your technical skills more prominently.",
                "justification": "These are key requirements mentioned in the job description that are missing from your resume."
            },
            {
                "section": "Experience",
                "suggestion": "Highlight projects where you used these skills.",
                "justification": "Demonstrating practical application increases relevance score."
            }
        ]
        
        if not missing_skills:
             mock_suggestions = [
                {
                    "section": "Summary",
                    "suggestion": "Emphasize your strong match in the professional summary.",
                    "justification": "You have all required skills, so focus on leadership and impact."
                }
            ]

        return mock_suggestions, prompt

    def _parse_text_to_suggestions(self, text: str) -> List[Dict[str, Any]]:
        """Parse unstructured AI text into suggestion format"""
        # Simple parsing - split by numbered points
        suggestions = []
        lines = text.split('\n')
        current_suggestion = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith(('1.', '2.', '3.', '-', '•')):
                if current_suggestion:
                    suggestions.append(current_suggestion)
                current_suggestion = {
                    "section": "General",
                    "suggestion": line.lstrip('123.-• '),
                    "justification": "AI-generated recommendation"
                }
        
        if current_suggestion:
            suggestions.append(current_suggestion)
            
        return suggestions if suggestions else [{
            "section": "General",
            "suggestion": text[:200],
            "justification": "AI-generated recommendation"
        }]

    def _build_prompt(self, resume_text: str, job_desc: str, missing_skills: List[str]) -> str:
        """
        Constructs the prompt with context injection.
        """
        prompt = f"""
You are an expert career coach and resume writer.
I will provide you with a Resume and a Job Description.
Your goal is to provide specific, actionable suggestions to tailor the resume for this job.

### Job Description
{job_desc[:1000]}... (truncated)

### Resume
{resume_text[:1000]}... (truncated)

### Missing Skills Detected
{', '.join(missing_skills) if missing_skills else 'None - good match!'}

### Instructions
1. Analyze the gap between the resume and the job description.
2. Provide 3 specific suggestions to improve the resume.
3. Suggestions should not fabricate experience, but highlight relevant existing experience.
4. Output MUST be in valid JSON format:
[
  {{
    "section": "Target Section (e.g., Skills, Experience)",
    "suggestion": "Actionable advice...",
    "justification": "Why this matters..."
  }}
]
"""
        return prompt.strip()

    def refine_resume(
        self,
        resume_text: str,
        job_description: str
    ) -> Dict[str, str]:
        """
        Rewrites the resume sections to better match the job description.
        """
        prompt = self._build_refine_prompt(resume_text, job_description)
        
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert professional resume writer. Rewrite the resume content to be more impactful and relevant to the job description. Output purely JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                ai_text = response.choices[0].message.content
                
                # Extract JSON
                try:
                    start = ai_text.find('{')
                    end = ai_text.rfind('}') + 1
                    if start != -1 and end > start:
                        return json.loads(ai_text[start:end])
                except Exception as e:
                    print(f"JSON Parse Error: {e}")
                    pass
            except Exception as e:
                print(f"OpenAI API Error: {e}")
        
        # Fallback
        return {
            "summary": "Could not generate refined summary. (API Error or Missing Key)",
            "experience": "Could not generate refined experience."
        }

    def _build_refine_prompt(self, resume_text: str, job_desc: str) -> str:
        return f"""
You are an expert resume writer.
I will provide a Resume and a Job Description.
Rewrite the "Professional Summary" and improve 3 key "Experience" bullet points to better match the job description.

### Job Description
{job_desc[:1500]}

### Resume
{resume_text[:2000]}

### Instructions
1. Rewrite the **Professional Summary** to highlight relevant skills and experience for this specific job.
2. Select 3 existing experience bullet points and rewrite them to be more results-oriented and relevant to the job.
3. Output MUST be in valid JSON format with these exact keys:
{{
  "summary": "Rewritten summary text...",
  "experience": "Markdown list of 3 rewritten bullet points..."
}}
"""

tailoring_service = TailoringService()
