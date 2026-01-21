import requests
import os
import sys

def test_resume_upload():
    url = "http://127.0.0.1:8001/api/v1/resume/upload"
    file_path = "sample_resume.docx"
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Run create_test_files.py first.")
        sys.exit(1)

    with open(file_path, "rb") as f:
        files = {"file": ("sample_resume.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
        try:
            response = requests.post(url, files=files)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
            if response.status_code == 200:
                data = response.json()
                print("Parsed Data Keys:", data.keys())
                print("Raw Text Preview:", repr(data["raw_text"][:500])) # Print first 500 chars

                if "John Doe" in data["raw_text"]:
                    print("SUCCESS: Text extracted.")
                else:
                    print("FAILURE: Text extraction failed.")
                    
                if len(data.get("experience", [])) > 0:
                    print("SUCCESS: Experience section extracted.")
                    print("First Experience Item:", data["experience"][0])
                else:
                    print("FAILURE: Experience section empty.")

                if len(data.get("skills", [])) > 0:
                    print("SUCCESS: Skills section extracted.")
                else:
                    print("FAILURE: Skills section empty.")
            else:
                print("FAILURE: API returned error.")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_resume_upload()
