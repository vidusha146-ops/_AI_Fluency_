import json
import time
import requests

BASE = "http://localhost:11434"
MODEL = "qwen2.5:1.5b"
PROMPT = "In three sentences, explain what an AI agent is."


def list_models():
    response = requests.get(
        f"{BASE}/api/tags",
        timeout=30
    )
    response.raise_for_status()

    data = response.json()

    print("\nModels on disk:")

    for model in data.get("models", []):
        size_gb = model.get("size", 0) / 1e9
        print(f"{model['name']:<28} {size_gb:.2f} GB")


def loaded_models():
    response = requests.get(
        f"{BASE}/api/ps",
        timeout=30
    )
    response.raise_for_status()

    models = response.json().get("models", [])

    print("\nLoaded models:")

    if not models:
        print("Nothing is loaded in memory.")
        return

    for model in models:
        size_gb = model.get("size", 0) / 1e9
        print(f"{model['name']} - {size_gb:.2f} GB")


def generate_once():
    start = time.perf_counter()

    response = requests.post(
        f"{BASE}/api/generate",
        json={
            "model": MODEL,
            "prompt": PROMPT,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    elapsed = time.perf_counter() - start
    tokens = data.get("eval_count", 0)

    rate = tokens / elapsed if elapsed else 0

    print("\n[generate]")
    print(f"Time: {elapsed:.2f} seconds")
    print(f"Tokens: {tokens}")
    print(f"Tokens/second: {rate:.2f}")
    print(data.get("response", "").strip())


def chat_streaming():
    start = time.perf_counter()
    first_token = None
    pieces = []

    with requests.post(
        f"{BASE}/api/chat",
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": PROMPT
                }
            ],
            "stream": True
        },
        stream=True,
        timeout=300
    ) as response:

        response.raise_for_status()

        for line in response.iter_lines():

            if not line:
                continue

            chunk = json.loads(line)

            piece = chunk.get(
                "message", {}
            ).get("content", "")

            if piece and first_token is None:
                first_token = time.perf_counter() - start

            pieces.append(piece)

    total = time.perf_counter() - start

    answer = "".join(pieces)

    print("\n[chat streaming]")

    if first_token is not None:
        print(f"TTFT: {first_token:.2f} seconds")

    print(f"Total time: {total:.2f} seconds")
    print(f"Characters: {len(answer)}")
    print(answer.strip())


def openai_compatible():
    response = requests.post(
        f"{BASE}/v1/chat/completions",
        headers={
            "Authorization": "Bearer ollama"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": PROMPT
                }
            ],
            "temperature": 0
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    print("\n[/v1/chat/completions]")

    print(
        data["choices"][0]["message"]["content"]
    )


if __name__ == "__main__":

    list_models()

    generate_once()

    chat_streaming()

    openai_compatible()

    loaded_models()