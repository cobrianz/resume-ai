import sys
import os

sys.path.append(os.getcwd())

def test_edge_cases():
    """Test edge cases for resume parser and API"""
    
    print("--- Testing Edge Cases ---")
    
    # Test 1: Empty skills/experience
    from app.services.matching_engine import matching_engine
    
    print("\n[Test 1] Empty Resume vs Valid Job")
    empty_resume = {
        "raw_text": "",
        "skills": [],
        "experience": []
    }
    valid_job = {
        "required_skills": ["Python", "SQL"],
        "responsibilities": ["Build APIs"]
    }
    
    score = matching_engine.compute_score(empty_resume, valid_job)
    print(f"Score: {score['overall_match']}")
    
    if score['overall_match'] == 0:
        print("SUCCESS: Empty resume correctly scored 0%")
    else:
        print("WARNING: Empty resume should score 0%")
    
    # Test 2: Missing sections in job
    print("\n[Test 2] Valid Resume vs Empty Job")
    valid_resume = {
        "raw_text": "Python developer",
        "skills": ["Python"],
        "experience": ["Built APIs"]
    }
    empty_job = {
        "required_skills": [],
        "responsibilities": []
    }
    
    score2 = matching_engine.compute_score(valid_resume, empty_job)
    print(f"Score: {score2['overall_match']}")
    
    if score2['overall_match'] == 0:
        print("SUCCESS: Empty job correctly scored 0%")
    else:
        print("WARNING: Empty job should score 0%")
    
    # Test 3: Chunking edge case
    from app.services.embedding_service import embedding_service
    
    print("\n[Test 3] Empty Text Chunking")
    chunks = embedding_service.chunk_text("")
    
    if len(chunks) == 0:
        print("SUCCESS: Empty text returns no chunks")
    else:
        print("FAILURE: Empty text should return empty list")
    
    print("\n[Test 4] Very Short Text Chunking")
    short_chunks = embedding_service.chunk_text("Hi")
    
    if len(short_chunks) == 1 and short_chunks[0] == "Hi":
        print("SUCCESS: Short text handled correctly")
    else:
        print("FAILURE: Short text chunking issue")

if __name__ == "__main__":
    test_edge_cases()
