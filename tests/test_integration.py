import sys
import os
import requests

sys.path.append(os.getcwd())

def test_integration():
    print("--- Testing End-to-End Integration ---")
    
    url = "http://127.0.0.1:8000/api/v1/match/"
    
    # Use the sample resume we created earlier
    resume_file_path = "sample_resume.docx"
    
    if not os.path.exists(resume_file_path):
        print(f"ERROR: {resume_file_path} not found. Run create_test_files.py first.")
        return
    
    job_description = """
    Senior Python Developer
    
    Responsibilities:
    - Build scalable REST APIs using FastAPI
    - Design database schemas
    - Deploy applications using Docker
    
    Requirements:
    - 5+ years Python experience
    - Strong knowledge of FastAPI
    - Experience with Docker and Kubernetes
    - SQL database expertise
    
    Preferred Skills:
    - AWS or GCP experience
    - React knowledge
    """
    
    with open(resume_file_path, "rb") as f:
        files = {"resume_file": ("sample_resume.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        data = {"job_description": job_description}
        
        try:
            response = requests.post(url, files=files, data=data)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                print("\n[Match Score]")
                print(f"Overall: {result['match_score']['overall_match']}%")
                print(f"Components: {result['match_score']['components']}")
                
                print(f"\n[Missing Skills]")
                print(f"{result['missing_skills']}")
                
                print(f"\n[Suggestions] ({len(result['suggestions'])} items)")
                for suggestion in result['suggestions']:
                    print(f"- {suggestion['section']}: {suggestion['suggestion']}")
                
                # Validation
                if "match_score" in result and "suggestions" in result:
                    print("\nSUCCESS: Integration endpoint working correctly.")
                else:
                    print("\nFAILURE: Response missing required fields.")
            else:
                print(f"FAILURE: API returned error {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_integration()
