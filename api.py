from metrics import record_request
from logger import log_request
from fastapi import FastAPI
from pydantic import BaseModel
import time

from routing.router import choose_model
from llm.client import ask_llm
from semantic_cache import find_similar, add_to_cache


app = FastAPI(
    title="Intelligent LLM Gateway",
    version="1.0.0"
)


class GenerateRequest(BaseModel):
    prompt: str


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/metrics")
def metrics():
    from metrics import load_metrics

    data = load_metrics()

    requests = data["requests"]

    cache_hit_rate = (
        data["cache_hits"] / requests * 100
        if requests > 0
        else 0
    )

    average_latency = (
        data["total_latency"] / requests
        if requests > 0
        else 0
    )

    return {
        "total_requests": requests,
        "cache_hits": data["cache_hits"],
        "cache_misses": data["cache_misses"],
        "cache_hit_rate": round(cache_hit_rate, 2),
        "average_latency": round(average_latency, 4),
        "models": data["models"]
    }

@app.post("/generate")
def generate(request: GenerateRequest):

    start_time = time.perf_counter()

    question = request.prompt

    match, similarity = find_similar(question)

    if match:

        latency = time.perf_counter() - start_time

        record_request(True, latency)

        log_request(
            question,
            cache_hit=True,
            latency=latency,
            similarity=similarity
        )
        return {
            "answer": match["answer"],
            "model": None,
            "cache_hit": True,
            "similarity": similarity,
            "latency": latency
        }

    model_type = choose_model(question)

    answer = ask_llm(
        question,
        model_type=model_type
    )

    add_to_cache(question, answer)

    latency = time.perf_counter() - start_time

    record_request(True, latency)

    log_request(
        question,
        cache_hit=True,
        latency=latency,
        similarity=similarity
    )

    return {
        "answer": answer,
        "model": model_type,
        "cache_hit": False,
        "similarity": similarity,
        "latency": latency
    }