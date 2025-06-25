# db.py
import sqlite3
import json

DB_PATH = "query_logs.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS query_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                prompt TEXT,
                answer TEXT,
                sources TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                query TEXT PRIMARY KEY,
                response TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()


def get_cached_response(query: str):
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT response FROM cache WHERE query=?", (query,))
        row = c.fetchone()
        if row:
            return json.loads(row[0])
    return None


def cache_response(query: str, answer: str, sources: list):
    response = json.dumps({"answer": answer, "sources": sources})
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("REPLACE INTO cache (query, response) VALUES (?, ?)", (query, response))
        conn.commit()


def log_query(query: str, prompt: str, answer: str, sources: list):
    sources_str = json.dumps(sources)
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(
            "INSERT INTO query_logs (query, prompt, answer, sources) VALUES (?, ?, ?, ?)",
            (query, prompt, answer, sources_str)
        )
        conn.commit()
