import os
import glob
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple
import fitz  

model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.IndexFlatL2(384)
doc_texts, doc_ids, doc_embeddings = [], [], []


def chunk_text(text, chunk_size=500, overlap=100):
    tokens = text.split()
    chunks = []
    start = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk = " ".join(tokens[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()

def load_documents():
    global doc_embeddings
    all_chunks = []
    chunk_ids = []

    for file in glob.glob("data/*.pdf"):
        full_text = extract_text_from_pdf(file)
        if not full_text:
            continue

        chunks = chunk_text(full_text, chunk_size=300, overlap=50) 
        all_chunks.extend(chunks)
        chunk_ids.extend([f"{os.path.basename(file)}_chunk_{i}" for i in range(len(chunks))])

    if not all_chunks:
        raise ValueError("No valid chunks found in PDF documents.")

    embeddings = model.encode(all_chunks)
    embeddings = np.array(embeddings)

    if embeddings.ndim != 2:
        raise ValueError(f"Embeddings shape invalid: {embeddings.shape}")

    index.add(embeddings)
    doc_texts.extend(all_chunks)
    doc_ids.extend(chunk_ids)
    doc_embeddings.extend(embeddings)


load_documents()

def get_relevant_docs(query: str, top_k: int = 3) -> Tuple[List[str], List[str]]:
    q_emb = model.encode([query])
    D, I = index.search(np.array(q_emb), top_k)
    retrieved_texts = [doc_texts[i] for i in I[0]]
    retrieved_ids = [doc_ids[i] for i in I[0]]
    return retrieved_texts, retrieved_ids


