# import faiss
# import numpy as np
# import pickle
# from sentence_transformers import SentenceTransformer

# class Searcher:
#     def __init__(self, model_name, index_path, chunks_path):
#         print("Initializing searcher...")
#         print(f"Loading model: {model_name}")
#         self.model = SentenceTransformer(model_name)
#         print(f"Loading FAISS index from: {index_path}")
#         self.index = faiss.read_index(index_path)
#         print(f"Loading chunk metadata from: {chunks_path}")
#         with open(chunks_path, 'rb') as f:
#             self.chunks = pickle.load(f)
#         print("Searcher initialized successfully.")

#     def search(self, query, k=3):
#         """
#         Performs a semantic search for a given query.
#         """
#         print(f"Searching for top {k} results for query: '{query}'")
#         # 1. Embed the query
#         query_embedding = self.model.encode([query], convert_to_numpy=True)
        
#         # 2. Normalize the query embedding (since the index is normalized)
#         faiss.normalize_L2(query_embedding)
        
#         # 3. Search the index
#         # D: distances (L2), I: indices of the nearest vectors
#         distances, indices = self.index.search(query_embedding, k)
        
#         # 4. Format results
#         results = []
#         for i in range(len(indices[0])):
#             chunk_index = indices[0][i]
#             distance = distances[0][i]
            
#             # Convert L2 distance on normalized vectors back to cosine similarity score
#             # Cosine Similarity = 1 - (L2_distance^2) / 2
#             score = 1 - (distance**2) / 2
            
#             original_chunk = self.chunks[chunk_index]
            
#             results.append({
#                 "doc_id": original_chunk['doc_id'],
#                 "page": original_chunk['page'],
#                  "score": round(float(score), 2),
#                 "text": original_chunk['text']
#             })
            
#         return results



import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

class Searcher:
    def __init__(self, model_name, index_path, chunks_path):
        print("Initializing searcher...")
        print(f"Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print(f"Loading FAISS index from: {index_path}")
        self.index = faiss.read_index(index_path)
        print(f"Loading chunk metadata from: {chunks_path}")
        with open(chunks_path, 'rb') as f:
            self.chunks = pickle.load(f)
        print("Searcher initialized successfully.")

    # MODIFIED: Added score_threshold parameter
    def search(self, query, k=3, score_threshold=0.3):
        """
        Performs a semantic search for a given query, filtering by a score threshold.
        """
        print(f"Searching for top {k} results for query: '{query}' with threshold {score_threshold}")
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)
        
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for i in range(len(indices[0])):
            chunk_index = indices[0][i]
            
            # Skip if the index is invalid (can happen in some edge cases)
            if chunk_index == -1:
                continue

            distance = distances[0][i]
            score = 1 - (distance**2) / 2
            
            # NEW: Filtering logic
            final_score = float(score)
            if final_score >= score_threshold:
                original_chunk = self.chunks[chunk_index]
                results.append({
                    "doc_id": original_chunk['doc_id'],
                    "page": original_chunk['page'],
                    "score": round(final_score, 2),
                    "text": original_chunk['text']
                })
            
        return results