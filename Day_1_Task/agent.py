import json

from config import client, MODEL, QUESTIONS, banner
from tools import TOOLS, TOOL_FUNCTIONS


SYSTEM_PROMPT = """
You are a college course-fee assistant.

You have access to private college course-fee data through tools.

Never guess a course fee.

Use get_course_fee when you need the fee of a specific course.

Use get_all_courses when you need to discover all available courses.

Use calculator for arithmetic.

For budget questions asking which courses can be combined,
first use get_all_courses, then compare the possible pairs,
and use calculator when arithmetic is required.

You can use multiple tools before giving the final answer.

Explain the final answer clearly.
"""


def agent(question, max_steps=6):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # If the model does not need a tool,
        # return its final answer.
        if not message.tool_calls:
            return message.content.strip()

        # Add the assistant's tool request
        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": call.id,
                    "type": "function",
                    "function": {
                        "name": call.function.name,
                        "arguments": call.function.arguments
                    }
                }
                for call in message.tool_calls
            ]
        })

        # Execute each requested tool
        for call in message.tool_calls:

            name = call.function.name.split("<|")[0]

            arguments = json.loads(
                call.function.arguments or "{}"
            )

            function = TOOL_FUNCTIONS.get(name)

            if function is None:
                result = f"Unknown tool: {name}"
            else:
                result = function(**arguments)

            print(
                f"   step {step}: "
                f"{name}({arguments}) -> {result}"
            )

            # Give the tool result back to the model
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

    return "Stopped: maximum steps reached."


if __name__ == "__main__":

    banner("SYSTEM 3: AI AGENT")

    for question in QUESTIONS:

        print("Q:", question)

        print("A:", agent(question))

        print("-" * 70)