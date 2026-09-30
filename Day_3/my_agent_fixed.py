"""Day 3: the same agent, with three guards added."""

import sys
import os
import json

# Add Day_1 and Day_3 to Python's module search path
DAY_1_PATH = os.path.join(os.path.dirname(__file__), "..", "Day_1")
DAY_3_PATH = os.path.dirname(__file__)

sys.path.insert(0, DAY_1_PATH)
sys.path.insert(0, DAY_3_PATH)

from config import client, MODEL, banner
from my_agent import SYSTEM_PROMPT
from my_tools import TOOLS, TOOL_FUNCTIONS


MAX_TOOL_CHARS = 1500
CHAR_BUDGET = 30000


def agent(question, max_steps=6, verbose=True):

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    seen_calls = {}
    chars_sent = 0

    for step in range(1, max_steps + 1):

        # Guard 3: character budget
        chars_sent += sum(
            len(str(m.get("content", "")))
            for m in messages
        )

        if chars_sent > CHAR_BUDGET:
            return (
                f"Stopped: character budget exceeded "
                f"({chars_sent} sent)."
            )

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content.strip()

        messages.append({
            "role": "assistant",
            "content": message.content or "",
            "tool_calls": [
                {
                    "id": c.id,
                    "type": "function",
                    "function": {
                        "name": c.function.name,
                        "arguments": c.function.arguments
                    }
                }
                for c in message.tool_calls
            ]
        })

        for call in message.tool_calls:

            name = call.function.name
            arguments = {}

            try:
                arguments = json.loads(
                    call.function.arguments or "{}"
                )

                function = TOOL_FUNCTIONS.get(name)

                if function is None:
                    result = (
                        f"Unknown tool: {name}. "
                        f"Available: {list(TOOL_FUNCTIONS)}"
                    )
                else:
                    result = function(**arguments)

            except json.JSONDecodeError as error:
                result = (
                    f"Argument error: {error}. "
                    "Send valid JSON."
                )

            except TypeError as error:
                result = f"Argument error: {error}"

            result = str(result)

            # Guard 1: repeat detection
            signature = (
                name,
                json.dumps(arguments, sort_keys=True)
            )

            seen_calls[signature] = (
                seen_calls.get(signature, 0) + 1
            )

            if seen_calls[signature] >= 3:
                return (
                    f"Stopped: the tool {name} was called 3 times "
                    f"with the same arguments and no progress was made. "
                    f"Last result: {result[:200]}"
                )

            # Guard 2: observation truncation
            if len(result) > MAX_TOOL_CHARS:
                result = (
                    result[:MAX_TOOL_CHARS]
                    + " ... [observation truncated]"
                )

            if verbose:
                print(
                    f"   step {step}: {name}({arguments}) "
                    f"-> {result[:120]}"
                )

            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": result
            })

    return "Stopped: maximum steps reached without a final answer."


if __name__ == "__main__":

    banner("MY AGENT (guards on)")

    questions = [
        (
            "Read Day_3/notice.html and tell me the total fee "
            "for CS101 and AI202 after the merit scholarship."
        ),

        "Read Day_3/fees.html and tell me the fee for CS101.",

        "Read Day_3/big.html and tell me how many students are listed."
    ]

    for question in questions:

        print("\nQ:", question)

        print("A:", agent(question))