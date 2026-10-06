from models import MODELS

def estimate_query_difficulty(query):
    score = 0

    words = query.split()
    query_lower = query.lower()

    if len(words) > 20:
        score += 1

    if len(words) > 40:
        score += 1

    reasoning_words = [
        "why",
        "compare",
        "analyze",
        "analyse",
        "derive",
        "explain",
        "evaluate",
        "design",
    ]

    coding_words = [
        "code",
        "implement",
        "algorithm",
        "debug",
        "architecture",
        "system design",
    ]

    for word in reasoning_words:
        if word in query_lower:
            score += 1

    for word in coding_words:
        if word in query_lower:
            score += 1

    return score


def choose_model(query):
    difficulty = estimate_query_difficulty(query)

    # Convert difficulty into a minimum quality requirement
    if difficulty <= 1:
        required_quality = 0.60
    elif difficulty <= 2:
        required_quality = 0.70
    else:
        required_quality = 0.80

    candidates = []

    for model_name, profile in MODELS.items():
        if profile["quality"] >= required_quality:
            candidates.append(
                (model_name, profile["cost_per_1k_tokens"])
            )

    # Choose the qualifying model with the lowest cost
    candidates.sort(key=lambda x: x[1])

    selected_model = candidates[0][0]

    if selected_model == "llama3.2:3b":
        return "cheap"

    return "strong"