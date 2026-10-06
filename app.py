import time
from llm.client import ask_llm
from routing.router import choose_model
from semantic_cache import find_similar, add_to_cache
from metrics import record_request, print_metrics
from logger import log_request

start_time = time.perf_counter()
question = input("You: ")
match, similarity = find_similar(question)
print(f"Best similarity: {similarity:.3f}")


if match:
    latency = time.perf_counter() - start_time
    print(f"\nSemantic Cache HIT ⚡")
    print(f"Similarity: {similarity:.3f}")
    print(f"Matched query: {match['query']}")
    print(f"Cache latency: {latency:.4f} seconds")
    print(f"\nLLM: {match['answer']}")
    record_request(True,latency)
    log_request(
        question,
        cache_hit=True,
        latency=latency,
        similarity=similarity
    )
else:
    print("\nSemantic Cache MISS")
    

    model_type = choose_model(question)

    print(f"Routing to: {model_type}")

    answer = ask_llm(
        question,
        model_type=model_type
    )

    add_to_cache(question, answer)
    latency = time.perf_counter() - start_time

    print("\nLLM:", answer)
    print(f"Total latency: {latency:.4f} seconds")
    record_request(False,latency,model_type)
    log_request(
        question,
        cache_hit=False,
        latency=latency,
        model=model_type,
        similarity=similarity
    )

print_metrics()