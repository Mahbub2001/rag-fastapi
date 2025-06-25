from fastapi import FastAPI
from pydantic import BaseModel
from retriever import get_relevant_docs
from llm_agent import generate_answer

app = FastAPI()

class QueryInput(BaseModel):
    query: str

class QueryOutput(BaseModel):
    answer: str
    sources: list[str]

@app.post("/query", response_model=QueryOutput)
async def query_endpoint(q: QueryInput):
    docs, sources = get_relevant_docs(q.query, top_k=3)
    answer = generate_answer(q.query, docs, sources)
    return {"answer": answer, "sources": sources}
