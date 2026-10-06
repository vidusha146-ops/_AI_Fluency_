from groq import Groq
from dotenv import load_dotenv
from collections import Counter
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

question = """
A student has ₹1000.

They spend ₹250 on travel.
Then they spend ₹180 on food.
Then they receive ₹100 from a friend.

How much money do they have now?

Give only the final answer and a short explanation.
"""

answers = []

for i in range(5):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.7
    )

    answer = response.choices[0].message.content

    answers.append(answer)

    print(f"\n===== RUN {i + 1} =====")
    print(answer)


print("\n===== SELF-CONSISTENCY =====")

for i, answer in enumerate(answers, 1):
    print(f"{i}. {answer}")

counts = Counter(answers)

print("\nMost common response:")

for answer, count in counts.most_common(1):
    print(f"Count: {count}")
    print(answer)