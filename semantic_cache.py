import requests
import json
import numpy as np
import redis

EMBED_MODEL = "nomic-embed-text"
SIMILARITY_THRESHOLD = 0.82

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

def get_embedding(text):
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={
            "model": EMBED_MODEL,
            "prompt": text
        }
    )

    response.raise_for_status()

    return response.json()["embedding"]


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )


def load_cache():
    data = r.get("semantic_cache")

    if data is None:
        return []

    return json.loads(data)


def save_cache(cache):
    r.set(
        "semantic_cache",
        json.dumps(cache)
    )


def find_similar(query):
    query_embedding = get_embedding(query)
    cache = load_cache()

    best_match = None
    best_score = 0

    for item in cache:
        score = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        if score > best_score:
            best_score = score
            best_match = item

    if best_score >= SIMILARITY_THRESHOLD:
        return best_match, best_score

    return None, best_score


def add_to_cache(query, answer):
    embedding = get_embedding(query)

    cache = load_cache()

    cache.append({
        "query": query,
        "answer": answer,
        "embedding": embedding
    })

    save_cache(cache)