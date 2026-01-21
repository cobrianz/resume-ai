import faiss
import numpy as np
from typing import List, Dict, Any, Tuple
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self):
        # Load model (downloads on first run)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384 # Dimension for all-MiniLM-L6-v2
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Simple in-memory metadata store: id -> metadata
        # In production, this would be a DB or ChromaDB
        self.metadata_store: Dict[int, Dict[str, Any]] = {}
        self.current_id = 0

    def embed_text(self, text: str) -> List[float]:
        """Generates embedding vector for text."""
        # encode returns numpy array, convert to list
        embedding = self.model.encode(text)
        return embedding.tolist()

    def add_to_index(self, text: str, metadata: Dict[str, Any]) -> int:
        """Adds text embedding to index and returns the assigned ID."""
        embedding = self.model.encode([text]) # Expects list of texts, returns (1, dim) ndarray
        
        # FAISS expects float32
        vector = np.array(embedding).astype('float32')
        self.index.add(vector)
        
        doc_id = self.current_id
        self.metadata_store[doc_id] = {
            "text": text,
            **metadata
        }
        self.current_id += 1
        
        return doc_id

    def search(self, query_text: str, k: int = 5) -> List[Dict[str, Any]]:
        """Searches for similar texts."""
        query_vector = self.model.encode([query_text]).astype('float32')
        
        distances, indices = self.index.search(query_vector, k)
        
        results = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            dist = distances[0][i]
            
            if idx != -1 and idx in self.metadata_store:
                item = self.metadata_store[idx]
                results.append({
                    "id": int(idx),
                    "score": float(dist), # L2 distance (lower is better)
                    "metadata": item
                })
                
        return results

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Splits text into chunks of approximately `chunk_size` characters with `overlap`.
        Simple sliding window approach.
        """
        if not text:
            return []
            
        chunks = []
        start = 0
        text_len = len(text)
        
        while start < text_len:
            end = start + chunk_size
            if end >= text_len:
                chunk = text[start:]
                chunks.append(chunk)
                break
            else:
                # Try to find a space to break at
                last_space = text.rfind(' ', start, end)
                if last_space != -1 and last_space > start:
                    end = last_space
                
                chunk = text[start:end]
                chunks.append(chunk)
                
                start = end - overlap
                if start < 0: start = 0 # Should not happen with positive overlap < size
                
        return chunks

# Singleton instance
embedding_service = EmbeddingService()
