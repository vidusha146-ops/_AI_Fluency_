from config import client, MODEL, PROVIDER

print("Python environment is working.")
print("Provider:", PROVIDER)
print("Model:", MODEL)

print("Calling the model...")

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: SETUP OK"
        }
    ],
    temperature=0
)

print("Model replied:", response.choices[0].message.content)
print("Setup check finished.")