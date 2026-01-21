import sys
import os

sys.path.append(os.getcwd())

from app.services.matching_engine import matching_engine

def test_matching():
    print("--- Testing Matching Engine ---")
    
    # 1. Perfect Match Scenario
    print("\n[Scenario 1] Perfect Match")
    resume_perfect = {
        "raw_text": "Python FastAPI SQL Docker. I built REST APIs.",
        "skills": ["Python", "FastAPI", "SQL", "Docker"],
        "experience": ["Built REST APIs using FastAPI", "Managed SQL databases"]
    }
    job_perfect = {
        "required_skills": ["Python", "FastAPI", "SQL"],
        "responsibilities": ["Build REST APIs", "Manage databases"]
    }
    
    score = matching_engine.compute_score(resume_perfect, job_perfect)
    print(f"Overall Score: {score['overall_match']}")
    print(f"Components: {score['components']}")
    
    if score['overall_match'] > 85:
        print("SUCCESS: High score for perfect match.")
    else:
        print("FAILURE: Score too low for perfect match.")

    # 2. Irrelevant Match Scenario
    print("\n[Scenario 2] Irrelevant Match")
    resume_chef = {
        "raw_text": "Cooking. Knife skills. Baking bread.",
        "skills": ["Cooking", "Baking", "Knife Skills"],
        "experience": ["Head Chef at Restaurant", "Baked sourdough"]
    }
    
    score_bad = matching_engine.compute_score(resume_chef, job_perfect)
    print(f"Overall Score: {score_bad['overall_match']}")
    print(f"Components: {score_bad['components']}")
    
    if score_bad['overall_match'] < 50:
        print("SUCCESS: Low score for irrelevant match.")
    else:
        print("FAILURE: Score too high for irrelevant match.")

if __name__ == "__main__":
    test_matching()
