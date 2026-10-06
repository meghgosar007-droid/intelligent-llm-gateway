import hashlib
import json
import os


CACHE_FILE = "cache.json"


def make_key(query):
    return hashlib.sha256(
        query.strip().lower().encode()
    ).hexdigest()


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_cached(query):
    cache = load_cache()
    key = make_key(query)

    return cache.get(key)


def save_cache(query, answer):
    cache = load_cache()
    key = make_key(query)

    cache[key] = {
        "query": query,
        "answer": answer
    }

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)