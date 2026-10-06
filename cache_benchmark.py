import requests
import time

URL = "http://127.0.0.1:8000/generate"

query = "What is machine learning?"

print("\n========== CACHE BENCHMARK ==========\n")

# First request — should be a MISS
start = time.perf_counter()

response1 = requests.post(
    URL,
    json={"prompt": query}
)

miss_latency = time.perf_counter() - start

print("Request 1")
print("Status:", response1.status_code)
print(f"Latency: {miss_latency:.3f}s")
print("Response:", response1.json())


# Second request — should be a HIT
start = time.perf_counter()

response2 = requests.post(
    URL,
    json={"prompt": query}
)

hit_latency = time.perf_counter() - start

print("\nRequest 2")
print("Status:", response2.status_code)
print(f"Latency: {hit_latency:.3f}s")
print("Response:", response2.json())


print("\n========== RESULT ==========")

print(f"Cache MISS latency: {miss_latency:.3f}s")
print(f"Cache HIT latency:  {hit_latency:.3f}s")

if hit_latency > 0:
    speedup = miss_latency / hit_latency
    print(f"Speedup: {speedup:.2f}x")

print("============================")