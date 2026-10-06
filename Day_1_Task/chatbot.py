from config import client, MODEL, QUESTIONS, banner

SYSTEM_PROMPT = """
You are a helpful college assistant.
Answer the user's question clearly.
You do not have access to the college's private course-fee database.
Do not claim that you looked up private course data.
"""


def chatbot(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    banner("SYSTEM 1: PLAIN CHATBOT")

    for question in QUESTIONS:
        print("Q:", question)
        print("A:", chatbot(question))
        print("-" * 70)