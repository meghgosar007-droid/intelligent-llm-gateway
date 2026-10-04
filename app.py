from llm.client import ask_llm
from routing.router import choose_model

question = input("You: ")
model_type = choose_model(question)
print(f"Routing to: {model_type}")

answer = ask_llm(question, model_type=model_type)

print("\nLLM:", answer)

