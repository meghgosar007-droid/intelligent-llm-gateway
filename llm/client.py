import os
from litellm import completion

MODEL_MAP = {
    "cheap": "gemini/gemini-3.8-flash",
    "strong": "gemini-3.8-flash",
}

def ask_llm(prompt,model_type="strong"):
    model = MODEL_MAP[model_type]
    response = completion(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt   
            }
        ],
        api_key=os.getenv("GEMINI_API_KEY")
    )

    return response.choices[0].message.content