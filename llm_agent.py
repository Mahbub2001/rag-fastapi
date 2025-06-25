from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def generate_answer(query: str, docs: list, sources: list) -> str:
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

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "InsightEngine",
        },
        model="qwen/qwen-2.5-coder-32b-instruct:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content
