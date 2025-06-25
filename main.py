from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from retriever import get_relevant_docs
from llm_agent import generate_answer, generate_answer_stream
from db import init_db, log_query, cache_response, get_cached_response
import json
import asyncio

app = FastAPI()


class QueryInput(BaseModel):
    query: str

class QueryOutput(BaseModel):
    answer: str
    sources: list[str]

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/query", response_model=QueryOutput)
async def query_endpoint(q: QueryInput):
    cached = get_cached_response(q.query)
    if cached:
        return cached

    docs, sources = get_relevant_docs(q.query, top_k=3)
    answer, prompt = generate_answer(q.query, docs, sources)
    cache_response(q.query, answer, sources)
    log_query(q.query, prompt, answer, sources)
    return {"answer": answer, "sources": sources}

@app.post("/query_stream")
async def query_endpoint_stream(q: QueryInput):
    cached = get_cached_response(q.query)
    if cached:
        async def cached_stream():
            yield cached["answer"]
        return StreamingResponse(cached_stream(), media_type="text/plain")

    docs, sources = get_relevant_docs(q.query, top_k=3)
    collected_answer = ""

    async def event_generator():
        nonlocal collected_answer
        async for token in generate_answer_stream(q.query, docs, sources):
            collected_answer += token
            yield token

    async def cache_and_log():
        await asyncio.sleep(5)
        prompt = generate_answer.__globals__['build_prompt'](q.query, docs, sources)
        cache_response(q.query, collected_answer, sources)
        log_query(q.query, prompt, collected_answer, sources)

    asyncio.create_task(cache_and_log())
    return StreamingResponse(event_generator(), media_type="text/plain")
