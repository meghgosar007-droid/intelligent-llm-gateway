import requests

MODEL_MAP = {
    "cheap": "llama3.2:3b",
    "strong": "llama3.2:3b",
}

def ask_llm(prompt,model_type="strong"):
    model = MODEL_MAP[model_type]
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]