import sys
import os
import numpy as np

sys.path.append(os.getcwd())

from app.services.embedding_service import embedding_service

def test_retrieval():
    print("--- Testing Chunking & Retrieval ---")
    
    # Create a "Long" resume
    resume_text = "Contact: John Doe, Email: john@example.com\n" * 5
    resume_text += "Experience:\n"
    resume_text += "I am a baker. I bake bread. " * 20 + "\n"
    resume_text += "I am a software engineer. I write Python code using FastAPI and React. I love docker containers. " * 5 + "\n"
    resume_text += "Education: University of Baking. " * 10
    
    print(f"Total Text Length: {len(resume_text)}")
    
    # 1. Chunking
    chunks = embedding_service.chunk_text(resume_text, chunk_size=200, overlap=20)
    print(f"Generated {len(chunks)} chunks.")
    
    # 2. Indexing
    print("Indexing chunks...")
    for i, chunk in enumerate(chunks):
        embedding_service.add_to_index(chunk, {"source": "long_resume", "chunk_id": i})
        
    # 3. Retrieval
    query = "Python FastAPI experience"
    print(f"\nQuerying: '{query}'")
    results = embedding_service.search(query, k=3)
    
    for res in results:
        print(f"Score: {res['score']:.4f}, Text: {res['metadata']['text'][:50]}...")
        
    # Verification
    top_match = results[0]['metadata']['text']
    if "Python" in top_match and "FastAPI" in top_match:
        print("\nSUCCESS: Retrieved relevant software engineering chunk.")
    else:
        print("\nFAILURE: Did not retrieve relevant chunk.")

if __name__ == "__main__":
    test_retrieval()
