import json
import pandas as pd


LOG_FILE = "requests.jsonl"


def load_logs():
    records = []

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            records.append(json.loads(line))

    return pd.DataFrame(records)


df = load_logs()

print("\n========== REQUEST ANALYSIS ==========")

print(f"Total requests: {len(df)}")

if len(df) > 0:

    cache_hit_rate = df["cache_hit"].mean() * 100

    print(f"Cache hit rate: {cache_hit_rate:.2f}%")

    print(
        f"Average latency: "
        f"{df['latency'].mean():.4f}s"
    )

    cache_df = df[df["cache_hit"] == True]

    if len(cache_df) > 0:
        print(
            f"Average cache latency: "
            f"{cache_df['latency'].mean():.4f}s"
        )

    llm_df = df[df["cache_hit"] == False]

    if len(llm_df) > 0:
        print(
            f"Average LLM latency: "
            f"{llm_df['latency'].mean():.4f}s"
        )

        print("\nModel usage:")

        print(
            llm_df["model"]
            .value_counts()
        )

print("\n======================================")