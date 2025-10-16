# Mini-RAG: Local Document Search Engine

This project is a lightweight, local-only Retrieval-Augmented Generation (RAG) system that allows you to perform semantic searches on a collection of PDF documents. It operates entirely on your local machine without needing external APIs, LLMs, or API keys.

## Features

-   **Local First**: All processing, from embedding to searching, happens locally.
-   **PDF Ingestion**: Automatically processes all PDF files from a specified directory.
-   **Text Chunking**: Splits document text into manageable, overlapping chunks for effective retrieval.
-   **Semantic Search**: Uses state-of-the-art sentence transformers to understand the meaning of your query and find the most relevant text passages.
-   **CLI Interface**: A robust command-line tool to query your documents.
-   **Web UI**: An intuitive Streamlit-based chat interface for a more interactive experience.
-   **Reproducible**: Minimal dependencies and clear setup instructions.

## Project Structure

```
mini-rag/
├── data/                 # Place your PDF files here
├── index/                # Stores the generated FAISS index and metadata
├── src/                  # Source code for different modules
│   ├── ingest.py         # PDF loading and text chunking
│   ├── embed.py          # Embedding generation and index creation
│   └── search.py         # Search logic
├── rag.py                # Main CLI entrypoint
├── app.py                # Streamlit web application
├── requirements.txt      # Project dependencies
└── README.md             # This file
```

## Setup Instructions

**Prerequisites:** Python 3.10+

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-link>
    cd mini-rag
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    # On Windows, use: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *The first time you run the application, the `sentence-transformers` library will download the embedding model (~230MB), which requires an internet connection.*

4.  **Add Your Documents:**
    -   Create a directory named `data`.
    -   Place the PDF files you want to query inside the `data/` directory. For testing, you can use any 5 PDFs.

## How to Run

The system first needs to **build an index** from your documents. This is a one-time process. The index is automatically created the first time you run either the CLI or the Streamlit app.

### 1. Using the CLI (`rag.py`)

The CLI is perfect for quick queries or integration into scripts.

**First Run (Builds the index and queries):**
Open your terminal and run:
```bash
python rag.py --query "What is the maximum operating temperature?"
```

CLI: You can now run your query with a custom threshold. For example, to only see results with a score of 0.7 or higher:
```bash
python rag.py --query "your query" --threshold 0.7
```

**Subsequent Runs (Uses the existing index):**
```bash
python rag.py --query "Which sensors are mentioned in the documents?"
```

**JSON Output:**
To get a structured JSON output, add the `--json` flag. This will also save the output to `results.json`.
```bash
python rag.py --query "What is the maximum operating temperature?" --json
```

### 2. Using the Streamlit Web App (`app.py`)

The web app provides a user-friendly chat interface.

**To launch the app, run:**
```bash
streamlit run app.py
```

Your browser should open with the application running. The first time you launch it, it will build the index from the documents in the `data/` folder, which may take a minute. After that, you can start asking questions.

## Design Decisions & Assumptions

-   **Embedding Model (`all-MiniLM-L6-v2`):** This model was chosen because it offers an excellent balance between performance and size. It's fast, effective for semantic similarity, and runs easily on a standard CPU.
-   **Vector Store (`FAISS`):** FAISS (Facebook AI Similarity Search) is a highly efficient library for vector search. `IndexFlatL2` is used, which is a simple and exact search index. We normalize the embeddings so that the L2 distance search is equivalent to a cosine similarity search, which is standard practice for semantic retrieval.
-   **PDF Parsing (`pdfplumber`):** Chosen over `PyPDF2` because it is generally more robust at extracting text, especially from complex layouts with tables and columns.
-   **Chunking Strategy:** A simple fixed-size character-based chunking with overlap is implemented. The overlap ensures that sentences or ideas are not split awkwardly across two chunks, improving the chances of relevant retrieval.
-   **Index Persistence:** The FAISS index and chunk metadata are saved to the `./index/` directory. This avoids the need to re-process all PDFs on every run, making subsequent queries much faster.

## Future Improvements (To-Do List)

-   **Advanced Chunking:** Implement more sophisticated chunking strategies, such as recursive character splitting or semantic chunking, to better respect document structure.
-   **Re-ranking:** Add a re-ranking step after the initial retrieval (e.g., using a cross-encoder model) to improve the relevance of the top results.
-   **Evaluation Suite:** Build a simple evaluation framework using a set of question-answer pairs to measure the recall of the retrieval system.
-   **Add a "G" to RAG:** Integrate a local LLM (like Llama 3 or Phi-3) to generate a natural language answer based on the retrieved context, completing the full RAG pipeline.
-   **Asynchronous Indexing:** For the Streamlit app, move the index-building process to a background task so the UI remains responsive.