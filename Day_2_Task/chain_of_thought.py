from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

question = """
Solve this problem carefully.

I have ₹500 for a college trip.

Option A costs ₹180 and takes 80 minutes.
Option B costs ₹250 and takes 60 minutes.

The event starts at 10:00 AM.

Determine:

1. Which option is cheaper?
2. How much money remains?
3. If I leave at 8:00 AM, will I reach before 10:00 AM?

Give the final answer with a short explanation.
"""

response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": question
        }
    ],
    temperature=0.3
)

print("\n===== CHAIN-OF-THOUGHT APPROACH =====\n")
print(response.choices[0].message.content)