import time
import requests

BASE = "http://localhost:11434"

MODELS = [
    "qwen2.5:7b"
]

PROMPTS = [
    "Reply with exactly: OK",

    "In two sentences, what is an AI agent?",

    "A course costs Rs. 18,000 with a 15% scholarship. "
    "What is payable? Show the steps."
]


def run(model, prompt):

    start = time.perf_counter()

    response = requests.post(
        f"{BASE}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=600
    )

    response.raise_for_status()

    data = response.json()

    elapsed = time.perf_counter() - start

    tokens = data.get("eval_count", 0)

    rate = tokens / elapsed if elapsed else 0

    load_ms = data.get(
        "load_duration", 0
    ) / 1e6

    return (
        elapsed,
        tokens,
        rate,
        load_ms,
        data.get("response", "").strip()
    )


if __name__ == "__main__":

    for model in MODELS:

        print("=" * 70)
        print("MODEL:", model)

        for prompt in PROMPTS:

            elapsed, tokens, rate, load_ms, answer = run(
                model,
                prompt
            )

            print("\nPrompt:", prompt)

            print(
                f"Time: {elapsed:.2f} seconds"
            )

            print(
                f"Tokens: {tokens}"
            )

            print(
                f"Tokens/second: {rate:.2f}"
            )

            print(
                f"Load time: {load_ms:.2f} ms"
            )

            print(
                "Answer:",
                answer[:300]
            )