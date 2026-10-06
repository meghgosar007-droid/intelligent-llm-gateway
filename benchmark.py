import time
from llm.client import ask_llm
from routing.router import choose_model


QUERIES = [
    "What is Python?",
    "What is the difference between RAM and ROM?",
    "Explain how a for loop works.",
    "Why is the sky blue?",
    "Explain gradient descent.",
    "Compare supervised and unsupervised learning.",
    "Explain the difference between TCP and UDP.",
    "Design a simple URL shortening system.",
    "Explain why transformer self-attention has quadratic complexity.",
    "Design a scalable backend architecture for a social media application."
]


def run_router_benchmark():
    results = []

    for query in QUERIES:
        print("\n" + "=" * 60)
        print(f"Query: {query}")

        model_type = choose_model(query)
        start = time.time()

        answer = ask_llm(
            query,
            model_type=model_type
        )

        latency = time.time() - start

        results.append({
            "query": query,
            "model_type": model_type,
            "latency": latency
        })

    return results


if __name__ == "__main__":
    results = run_router_benchmark()

    print("\n\nBENCHMARK SUMMARY")
    print("=" * 60)

    for result in results:
        print(
            f"{result['model_type']:>6} | "
            f"{result['latency']:.2f}s | "
            f"{result['query']}"
        )