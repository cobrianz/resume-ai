import sys
import os

sys.path.append(os.getcwd())

from app.services.tailoring_service import tailoring_service

def test_tailoring():
    print("--- Testing Tailoring Engine ---")
    
    resume_text = "I am a Python Developer. I know Django."
    job_desc = "Looking for a Python Developer with Flask and AWS experience."
    missing_skills = ["Flask", "AWS"]
    
    print("\n[Input]")
    print(f"Missing Skills: {missing_skills}")
    
    suggestions, prompt = tailoring_service.generate_suggestions(resume_text, job_desc, missing_skills)
    
    print("\n[Generated Prompt Preview]")
    print(prompt[:200] + "...")
    
    print("\n[Mocked Suggestions]")
    for suggestion in suggestions:
        print(f"- Section: {suggestion['section']}")
        print(f"  Suggestion: {suggestion['suggestion']}")
        print(f"  Justification: {suggestion['justification']}")
        
    # Verification
    if "Flask" in suggestions[0]["suggestion"] or "AWS" in suggestions[0]["suggestion"]:
        print("\nSUCCESS: Suggestions addressed missing skills.")
    else:
        print("\nFAILURE: Suggestions did not address missing skills.")

    if "You are an expert career coach" in prompt:
        print("SUCCESS: Prompt constructed correctly.")
    else:
        print("FAILURE: Prompt construction failed.")

if __name__ == "__main__":
    test_tailoring()
