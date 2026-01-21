import sys
import os
import numpy as np

# Add project root to path BEFORE importing app
sys.path.append(os.getcwd())

from app.services.embedding_service import embedding_service

def test_embeddings():
    print("--- Initializing Embedding Service (Loading Model) ---")
    # verification that it loads
    try:
        service = embedding_service
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Add dummy data
    texts = [
        "Senior Python Developer with FastAPI experience.",
        "Junior Java Developer looking for internship.",
        "Project Manager with Agile certification.",
        "Data Scientist skilled in Python and PyTorch."
    ]
    
    print("\n--- Adding Documents ---")
    for text in texts:
        doc_id = service.add_to_index(text, {"source": "resume"})
        print(f"Added doc {doc_id}: {text[:30]}...")

    # Query
    query = "Python web developer"
    print(f"\n--- Querying: '{query}' ---")
    
    results = service.search(query, k=2)
    
    print(f"Found {len(results)} results:")
    for res in results:
        print(f"ID: {res['id']}, Score (L2): {res['score']:.4f}")
        print(f"Text: {res['metadata']['text']}")
        
    # Validation
    # "Python Developer" should be closest to "Python web developer"
    # L2 score: Lower is better.
    
    first_match_text = results[0]['metadata']['text']
    if "Python" in first_match_text:
        print("\nSUCCESS: Semantic search found relevant result.")
    else:
        print("\nFAILURE: Semantic search results unexpected.")

if __name__ == "__main__":
    test_embeddings()
