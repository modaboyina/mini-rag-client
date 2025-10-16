import argparse
import json
import os
from src.ingest import process_pdfs_from_directory
from src.embed import create_embeddings_and_index, save_index_and_chunks
from src.search import Searcher

# --- Configuration ---
DATA_DIR = "./data"
INDEX_PATH = "./index/faiss_index.bin"
CHUNKS_PATH = "./index/chunks.pkl"
MODEL_NAME = 'all-MiniLM-L6-v2'

def build_index():
    """Builds the FAISS index from PDFs in the data directory."""
    print("Index not found. Starting the build process...")
    
    # Ensure the index directory exists
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    
    # 1. Ingest and Chunk PDFs
    chunks = process_pdfs_from_directory(DATA_DIR)
    if not chunks:
        print("No text chunks were created. Halting index build.")
        return False
        
    # 2. Create Embeddings and FAISS Index
    index, chunks_with_meta = create_embeddings_and_index(chunks, MODEL_NAME)
    if index is None:
        print("Failed to create FAISS index.")
        return False

    # 3. Save the index and chunks
    save_index_and_chunks(index, chunks_with_meta, INDEX_PATH, CHUNKS_PATH)
    print("Index built and saved successfully.")
    return True

def main():

    parser = argparse.ArgumentParser(description="A mini-RAG CLI tool for querying PDFs.")
    parser.add_argument("--query", type=str, required=True, help="The question to ask the documents.")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format.")
    # NEW: Add threshold argument
    parser.add_argument(
        "--threshold", 
        type=float, 
        default=0.3, 
        help="Minimum similarity score for a result to be considered relevant (0.0 to 1.0)."
    )
    
    args = parser.parse_args()

    # Check if the index exists, if not, build it
    if not os.path.exists(INDEX_PATH) or not os.path.exists(CHUNKS_PATH):
        if not build_index():
            return # Exit if index build fails

    # Initialize the searcher
    try:
        searcher = Searcher(MODEL_NAME, INDEX_PATH, CHUNKS_PATH)
    except Exception as e:
        print(f"Error initializing searcher: {e}")
        print("The index might be corrupted. Please delete the 'index' directory and run again to rebuild.")
        return

    # Perform the search
    results = searcher.search(args.query, k=3, score_threshold=args.threshold)

    # Format and print the output
    output_data = {"query": args.query, "results": results}

    if args.json:
        print(json.dumps(output_data, indent=2))
        with open("results.json", "w") as f:
            json.dump(output_data, f, indent=2)
        print("\nResults also saved to results.json")
    else:
        print(f"\nQuery: \"{args.query}\"\n")
        print("Top 3 Results:")
        if not results:
            print("No relevant passages found.")
        for i, res in enumerate(results):
            print("-" * 20)
            print(f"# {i+1}) doc={res['doc_id']} page={res['page']} score={res['score']:.2f}")
            print(f"   \"... {res['text']} ...\"")
        print("-" * 20)

if __name__ == "__main__":
    main()