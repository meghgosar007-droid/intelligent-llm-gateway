import json
from datetime import datetime


LOG_FILE = "requests.jsonl"


def log_request(
    query,
    cache_hit,
    latency,
    model=None,
    similarity=None
):
    record = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "cache_hit": cache_hit,
        "model": model,
        "similarity": similarity,
        "latency": round(latency, 4)
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")