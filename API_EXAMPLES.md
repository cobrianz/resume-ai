# API Usage Examples

## Using cURL

### 1. Health Check
```bash
curl http://localhost:8000/health
```

### 2. Upload Resume
```bash
curl -X POST http://localhost:8000/api/v1/resume/upload \
  -F "file=@resume.pdf"
```

### 3. Analyze Job
```bash
curl -X POST http://localhost:8000/api/v1/job/analyze \
  -H "Content-Type: application/json" \
  -d '{"description": "Python Developer with 5 years experience..."}'
```

### 4. Match Resume to Job (Complete Flow)
```bash
curl -X POST http://localhost:8000/api/v1/match/ \
  -F "resume_file=@resume.docx" \
  -F "job_description=Senior Python Developer. Requirements: FastAPI, Docker..."
```

## Using Python

```python
import requests

# Match endpoint
url = "http://localhost:8000/api/v1/match/"

with open("resume.pdf", "rb") as f:
    files = {"resume_file": f}
    data = {"job_description": "Python Developer..."}
    
    response = requests.post(url, files=files, data=data)
    result = response.json()
    
    print(f"Match Score: {result['match_score']['overall_match']}%")
    print(f"Missing Skills: {result['missing_skills']}")
    
    for suggestion in result['suggestions']:
        print(f"- {suggestion['section']}: {suggestion['suggestion']}")
```

## Using JavaScript (Fetch)

```javascript
const formData = new FormData();
formData.append('resume_file', fileInput.files[0]);
formData.append('job_description', jobText);

fetch('http://localhost:8000/api/v1/match/', {
  method: 'POST',
  body: formData
})
.then(res => res.json())
.then(data => {
  console.log('Match Score:', data.match_score.overall_match);
  console.log('Suggestions:', data.suggestions);
});
```

## Response Examples

### Success Response
```json
{
  "match_score": {
    "overall_match": 78.5,
    "components": {
      "skill_match": 85.0,
      "experience_match": 75.0,
      "keyword_match": 70.0
    }
  },
  "missing_skills": ["Docker", "Kubernetes", "AWS"],
  "suggestions": [
    {
      "section": "Skills",
      "suggestion": "Add Docker, Kubernetes, AWS to your skills section.",
      "justification": "These are key requirements mentioned in the job description."
    },
    {
      "section": "Experience",
      "suggestion": "Highlight projects where you used these skills.",
      "justification": "Demonstrating practical application increases relevance score."
    }
  ]
}
```

### Error Response
```json
{
  "detail": "Invalid file type. Only PDF and DOCX are supported."
}
```
