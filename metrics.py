import json
import os


METRICS_FILE = "metrics.json"


def load_metrics():
    if not os.path.exists(METRICS_FILE):
        return {
            "requests": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "total_latency": 0,
            "cache_latency": 0,
            "llm_latency": 0,
            "models": {}
        }

    with open(METRICS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_metrics(metrics):
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)


def record_request(cache_hit, latency, model=None):
    metrics = load_metrics()

    metrics["requests"] += 1
    metrics["total_latency"] += latency

    if cache_hit:
        metrics["cache_hits"] += 1
        metrics["cache_latency"] += latency

    else:
        metrics["cache_misses"] += 1
        metrics["llm_latency"] += latency

        if model:
            if model not in metrics["models"]:
                metrics["models"][model] = {
                    "requests": 0,
                    "total_latency": 0
                }

            metrics["models"][model]["requests"] += 1
            metrics["models"][model]["total_latency"] += latency

    save_metrics(metrics)


def print_metrics():
    metrics = load_metrics()

    requests = metrics["requests"]

    hit_rate = (
        metrics["cache_hits"] / requests * 100
        if requests > 0
        else 0
    )

    avg_latency = (
        metrics["total_latency"] / requests
        if requests > 0
        else 0
    )

    avg_cache_latency = (
        metrics["cache_latency"] / metrics["cache_hits"]
        if metrics["cache_hits"] > 0
        else 0
    )

    avg_llm_latency = (
        metrics["llm_latency"] / metrics["cache_misses"]
        if metrics["cache_misses"] > 0
        else 0
    )

    print("\n========== METRICS ==========")
    print(f"Requests:          {requests}")
    print(f"Cache hits:        {metrics['cache_hits']}")
    print(f"Cache misses:      {metrics['cache_misses']}")
    print(f"Cache hit rate:    {hit_rate:.2f}%")
    print(f"Average latency:   {avg_latency:.4f}s")
    print(f"Avg cache latency: {avg_cache_latency:.4f}s")
    print(f"Avg LLM latency:   {avg_llm_latency:.4f}s")

    print("\n---------- MODELS ----------")

    for model, data in metrics["models"].items():

        avg_model_latency = (
            data["total_latency"] / data["requests"]
            if data["requests"] > 0
            else 0
        )

        print(f"\n{model}")
        print(f"  Requests:     {data['requests']}")
        print(f"  Avg latency:  {avg_model_latency:.4f}s")

    print("=============================")