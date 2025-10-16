import os
import pdfplumber
from pathlib import Path
from tqdm import tqdm

def extract_text_from_pdf(pdf_path):
    """Extracts text from a single PDF file, keeping track of page numbers."""
    text_by_page = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                # Basic cleaning: replace newlines and multiple spaces
                cleaned_text = ' '.join(text.replace('\n', ' ').split())
                text_by_page.append({"page": i + 1, "text": cleaned_text})
    return text_by_page

def chunk_text(doc_id, text_by_page, chunk_size=500, overlap=50):
    """Chunks text from a document page by page."""
    chunks = []
    chunk_id_counter = 0
    for page_data in text_by_page:
        text = page_data["text"]
        page_num = page_data["page"]
        words = text.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk_text = " ".join(words[i:i + chunk_size])
            chunks.append({
                "doc_id": doc_id,
                "page": page_num,
                "chunk_id": chunk_id_counter,
                "text": chunk_text
            })
            chunk_id_counter += 1
    return chunks

def process_pdfs_from_directory(directory_path):
    """Processes all PDFs in a directory to extract and chunk text."""
    all_chunks = []
    pdf_files = list(Path(directory_path).glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in directory: {directory_path}")
        return []

    print(f"Found {len(pdf_files)} PDF(s) to process...")
    for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
        doc_id = pdf_path.name
        text_by_page = extract_text_from_pdf(pdf_path)
        doc_chunks = chunk_text(doc_id, text_by_page)
        all_chunks.extend(doc_chunks)
        
    return all_chunks