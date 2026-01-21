from typing import Dict, List, Any
import numpy as np
from sentence_transformers import util
from app.services.embedding_service import embedding_service

class MatchingEngine:
    def __init__(self):
        self.embedder = embedding_service

    def compute_score(self, resume_data: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes a match score between a resume and a job description.
        Returns a dictionary with overall score and breakdown.
        """
        
        # 1. Skill Match (40%)
        # Compare resume skills vs job required skills
        resume_skills = resume_data.get("skills", [])
        job_skills = job_data.get("required_skills", [])
        
        # If extracted skills are empty, fall back to raw text chunks? 
        # For now, if empty, score is 0 (incentivizes parsing quality)
        if not resume_skills or not job_skills:
            skill_score = 0.0
        else:
            skill_score = self._calculate_semantic_similarity_list(resume_skills, job_skills)

        # 2. Experience Relevance (40%)
        # Compare job responsibilities vs resume experience
        resume_exp = resume_data.get("experience", [])
        job_resp = job_data.get("responsibilities", [])
        
        if not resume_exp or not job_resp:
            exp_score = 0.0
        else:
            exp_score = self._calculate_semantic_similarity_list(resume_exp, job_resp)
            
        # 3. Keyword Overlap (20%)
        # Simple Jaccard similarity or inclusion check on raw text
        # Here we check how many job keywords (skills) appear in resume text
        keyword_score = self._calculate_keyword_match(resume_data.get("raw_text", ""), job_skills)
        
        # Weighted Total
        # Weights: Skills (40%), Experience (40%), Keywords (20%)
        overall_score = (skill_score * 0.4) + (exp_score * 0.4) + (keyword_score * 0.2)
        
        return {
            "overall_match": round(overall_score * 100, 2), # 0-100 scale
            "components": {
                "skill_match": round(skill_score * 100, 2),
                "experience_match": round(exp_score * 100, 2),
                "keyword_match": round(keyword_score * 100, 2)
            }
        }

    def _calculate_semantic_similarity_list(self, list_a: List[str], list_b: List[str]) -> float:
        """
        Calculates average max similarity: for each item in list_b (job reqs),
        find the best match in list_a (resume items), and average those best scores.
        """
        if not list_a or not list_b:
            return 0.0
            
        # Embed all items
        # SentenceTransformers.encode can take a list
        embeddings_a = self.embedder.model.encode(list_a, convert_to_tensor=True)
        embeddings_b = self.embedder.model.encode(list_b, convert_to_tensor=True)
        
        # Compute cosine similarity matrix
        # tensor of shape (len(list_b), len(list_a))
        # cosine_scores[i][j] = similarity between list_b[i] and list_a[j]
        cosine_scores = util.cos_sim(embeddings_b, embeddings_a)
        
        # For each item in B (Job), find max similarity in A (Resume)
        # We want to know: "For each job requirement, how well does the resume meet it?"
        max_scores_per_req, _ = cosine_scores.max(dim=1)
        
        # Average the scores
        average_score = max_scores_per_req.mean().item()
        
        # Normalize to 0-1 (cosine sim is -1 to 1, but usually positive for text)
        return max(0.0, average_score)

    def _calculate_keyword_match(self, text: str, keywords: List[str]) -> float:
        """
        Score based on fraction of keywords present in text.
        """
        if not keywords:
            return 0.0
            
        text_lower = text.lower()
        found_count = 0
        for kw in keywords:
            # Simple substring match (could be improved with regex boundary)
            if kw.lower() in text_lower:
                found_count += 1
                
        return found_count / len(keywords)

matching_engine = MatchingEngine()
