import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found in .env")

client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"

questions = [
    "What should a student do after losing an important item on campus?",
    "Where was the black water bottle found?",
    "Was a scientific calculator found, and where?"
]

print("=" * 60)
print("FINDITAI - PLAIN LLM")
print("=" * 60)

for question in questions:
    print("\nQuestion:")
    print(question)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content

    print("\nPlain LLM Answer:")
    print(answer)
    print("-" * 60)