import requests
import time
import json
import os
from datetime import datetime
from models import MODELS

MODEL_MAP = {
    "cheap": "llama3.2:3b",
    "strong": "qwen2.5:7b",
}   
def estimate_tokens(text):
    # Rough approximation:
    # 1 token ≈ 4 characters for English text
    return max(1, len(text) // 4)

def ask_llm(prompt,model_type="strong"):
    model = MODEL_MAP[model_type]
    start_time = time.time()
    input_tokens = estimate_tokens(prompt)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    latency = time.time() - start_time

    response.raise_for_status()

    answer = response.json()["response"]

    output_tokens = estimate_tokens(answer)
    total_tokens = input_tokens + output_tokens
    cost_per_1k = MODELS[model]["cost_per_1k_tokens"]
    estimated_cost = (total_tokens / 1000) * cost_per_1k
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model_type": model_type,
        "model": model,
        "latency_seconds": round(latency, 3)
    }

    os.makedirs("logs", exist_ok=True)

    with open("logs/requests.jsonl", "a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry) + "\n")

    print(f"Model: {model}")
    print(f"Input tokens: {input_tokens}")
    print(f"Output tokens: {output_tokens}")
    print(f"Total tokens: {total_tokens}")
    print(f"Estimated cost: ${estimated_cost:.6f}")
    print(f"Latency: {latency:.2f}s")

    return answer