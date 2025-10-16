import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def create_embeddings_and_index(chunks, model_name='all-MiniLM-L6-v2'):
    """
    Generates embeddings for text chunks and builds a FAISS index.
    """
    if not chunks:
        print("No chunks to process. Aborting embedding creation.")
        return None, None

    print(f"Loading embedding model: {model_name}")
    model = SentenceTransformer(model_name)
    
    # Extract text from chunks for batch embedding
    texts = [chunk['text'] for chunk in chunks]
    
    print("Generating embeddings for all chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    
    # Normalize embeddings for cosine similarity search with L2 distance
    faiss.normalize_L2(embeddings)
    
    # Build the FAISS index
    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings)
    
    print(f"FAISS index created successfully with {index.ntotal} vectors.")
    
    return index, chunks

def save_index_and_chunks(index, chunks, index_path, chunks_path):
    """Saves the FAISS index and the chunk metadata to disk."""
    print(f"Saving FAISS index to {index_path}")
    faiss.write_index(index, index_path)
    
    print(f"Saving chunk metadata to {chunks_path}")
    with open(chunks_path, 'wb') as f:
        pickle.dump(chunks, f)