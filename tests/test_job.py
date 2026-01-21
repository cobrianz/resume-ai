import requests
import json

def test_job_analysis():
    url = "http://127.0.0.1:8000/api/v1/job/analyze"
    
    # Sample Job Description
    job_desc = """
    Software Engineer
    
    About Us:
    We are a tech company.
    
    Responsibilities:
    - Build scalable APIs using FastAPI
    - Design database schemas in PostgreSQL
    - Collaborate with frontend teams
    
    Requirements:
    - 3+ years of Python experience
    - Strong knowledge of Docker and Kubernetes
    - Experience with CI/CD components
    
    Preferred Skills:
    - Experience with React or Vue.js
    - Knowledge of AWS services
    """
    
    payload = {"description": job_desc}
    
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Parsed Data Keys:", data.keys())
            
            req_skills = data.get("required_skills", [])
            print(f"\nRequired Skills ({len(req_skills)}):")
            for skill in req_skills:
                print(f"- {skill}")
                
            pref_skills = data.get("preferred_skills", [])
            print(f"\nPreferred Skills ({len(pref_skills)}):")
            for skill in pref_skills:
                print(f"- {skill}")
                
            responsibilities = data.get("responsibilities", [])
            print(f"\nResponsibilities ({len(responsibilities)}):")
            for resp in responsibilities:
                print(f"- {resp}")
                
            if len(req_skills) > 0 and len(responsibilities) > 0:
                print("\nSUCCESS: Job description analyzed correctly.")
            else:
                print("\nFAILURE: sections missing.")
        else:
            print(f"FAILURE: API returned error {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_job_analysis()
