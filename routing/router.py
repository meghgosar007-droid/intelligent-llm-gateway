def choose_model(query):
    score = 0

    words = query.split()

    # Longer questions are more likely to need a stronger model
    if len(words) > 20:
        score += 1

    if len(words) > 40:
        score += 1

    # Reasoning-heavy requests
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

    for word in reasoning_words:
        if word in query.lower():
            score += 1

    # Coding / implementation requests
    coding_words = [
        "code",
        "implement",
        "algorithm",
        "debug",
        "architecture",
        "system design",
    ]

    for word in coding_words:
        if word in query.lower():
            score += 1

    if score >= 2:
        return "strong"

    return "cheap"