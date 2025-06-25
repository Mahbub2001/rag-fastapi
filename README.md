# 🔍 InsightEngine – AI-Powered Document Query System

A lightweight AI micro-agent built with **FastAPI**, **FAISS**, **SentenceTransformers**, and **OpenRouter/OpenAI**, designed to retrieve insights from multiple research documents in PDF format.

---

## 🚀 Features

- 🧠 Embedding-based document retrieval (FAISS + all-MiniLM-L6-v2)
- 📄 Supports querying over multiple PDF documents
- 🧾 Structured answers with citations (`[Source: doc_X]`)
- ⚡ SQLite caching for faster repeat queries
- 🔁 Streaming responses token-by-token
- 📚 Query & response logging in SQLite
- 📦 OpenAI/OpenRouter compatible LLM backend

---

## 🧰 Tech Stack

- Python, FastAPI
- FAISS (vector search)
- sentence-transformers (`all-MiniLM-L6-v2`)
- SQLite3 for caching/logging
- OpenAI/OpenRouter LLM API
- PyMuPDF (`fitz`) for PDF text extraction

---

## 📁 Project Structure

├── data/ # Folder containing your PDF documents
├── main.py # FastAPI app with endpoints
├── retriever.py # FAISS-based document chunking & search
├── llm_agent.py # LLM prompt creation and streaming
├── db.py # SQLite caching & query logging
├── requirements.txt # Python dependencies
└── .env # API keys and environment variables


---

## ⚙️ Setup Instructions

### 1. Clone this repo

```bash
git clone https://github.com/your-username/insightengine
cd insightengine
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate    # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Add PDFs
Place at least 10 short .pdf documents inside the data/ folder.


### 4. Create .env
OPENROUTER_API_KEY=your_api_key_here

### 5. Run the API
uvicorn main:app --reload


🛠 API Usage
🔎 POST /query
Returns cached or newly generated answer.

Request:
```bash
{
  "query": "What is the conclusion of document 3?"
}
```
Response:
```bash
{
  "answer": "- The study highlights that... [Source: doc_03]",
  "sources": ["doc_03_chunk_1", "doc_01_chunk_0", "doc_02_chunk_2"]
}
```
🔁 POST /query_stream
Streams the answer token-by-token (for faster UI feedback).

💾 Caching & Logging
SQLite Cache: Stores previous queries and responses in cache.db

Logged Items:
--Query string
--Prompt content
--Final answer
--Source chunks used

✅ Requirements
Python 3.8+

No Redis required — uses SQLite-based caching and logging

🔐 Security
All model answers are grounded in retrieved documents

Prompts explicitly tell the LLM to avoid hallucinations

Example instruction:

“Only use the following context to answer. Do not make up facts. Always cite the source as [Source: doc_X].”

📦 Models & LLMs
You can use any OpenRouter-supported model, for example:

qwen/qwen-2.5-coder-32b-instruct:free

mistralai/mixtral-8x7b-instruct

meta-llama/llama-3-70b-instruct

Set the model in llm_agent.py.

🙋‍♂️ Author
Mahbub Ahmed Turza
Built as a technical assignment for AI Engineer Intern at Empowering Energy
Riyadh, Saudi Arabia — Empowering Energy Website

📝 License
MIT License — free to use, modify, and distribute.



