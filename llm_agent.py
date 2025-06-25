from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def build_prompt(query: str, docs: list, sources: list) -> str:
    context = "\n\n".join(
        [f"[Source: {sources[i]}]\n{docs[i]}" for i in range(len(docs))]
    )
    prompt = f"""
You are an expert researcher. Only use the context below to answer.
Do NOT make up information. Always cite the source in [Source: doc_X] format.

Query: {query}

Context:
{context}

Answer:
- 
    """
    return prompt

def generate_answer(query: str, docs: list, sources: list) -> str:
    prompt = build_prompt(query, docs, sources)
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "InsightEngine",
        },
        model="qwen/qwen-2.5-coder-32b-instruct:free",
        messages=[{"role": "user", "content": prompt}],
    )
    return completion.choices[0].message.content, prompt

def generate_answer_stream(query: str, docs: list, sources: list):
    prompt = build_prompt(query, docs, sources)

    stream = client.chat.completions.create(
        model="qwen/qwen-2.5-coder-32b-instruct:free",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "InsightEngine",
        }
    )

    async def token_generator():
        for chunk in stream:
            token = chunk.choices[0].delta.get("content", "")
            if token:
                yield token

    return token_generator()
