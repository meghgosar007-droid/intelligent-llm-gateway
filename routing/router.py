def choose_model(query):
    if len(query.split()) <= 10:
        return "cheap"

    return "strong"