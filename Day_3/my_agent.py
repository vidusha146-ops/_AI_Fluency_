"""Day 3: a ReAct agent written from scratch. No guards yet - it will fail on purpose."""

import sys
import os
import json

# --------------------------------------------------
# Add Day_1 and Day_3 folders to Python path
# --------------------------------------------------

DAY_1_PATH = os.path.join(os.path.dirname(__file__), "..", "Day_1")
DAY_3_PATH = os.path.dirname(__file__)

sys.path.insert(0, DAY_1_PATH)
sys.path.insert(0, DAY_3_PATH)

# --------------------------------------------------
# Import configuration and tools
# --------------------------------------------------

from config import client, MODEL, banner
from my_tools import TOOLS, TOOL_FUNCTIONS


# --------------------------------------------------
# System prompt
# --------------------------------------------------

SYSTEM_PROMPT = (
    "You are a college assistant. "
    "Use read_webpage to read any page or file the user mentions, "
    "and use calculator for every arithmetic step. "
    "Never guess a number that should come from a page. "
    "If no tool is needed, answer directly."
)


# --------------------------------------------------
# ReAct Agent
# --------------------------------------------------

def agent(question, max_steps=6, verbose=True):

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

        # Ask the LLM what to do next
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0
        )

        message = response.choices[0].message

        # --------------------------------------------------
        # If no tool is requested, return final answer
        # --------------------------------------------------

        if not message.tool_calls:
            return message.content.strip()

        # --------------------------------------------------
        # Add assistant's tool calls to conversation
        # --------------------------------------------------

        messages.append(
            {
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
            }
        )

        # --------------------------------------------------
        # Execute each requested tool
        # --------------------------------------------------

        for call in message.tool_calls:

            name = call.function.name
            arguments = {}

            try:

                # Convert JSON arguments into Python dictionary
                arguments = json.loads(
                    call.function.arguments or "{}"
                )

                # Find the requested tool
                function = TOOL_FUNCTIONS.get(name)

                if function is None:

                    result = (
                        f"Unknown tool: {name}. "
                        f"Available: {list(TOOL_FUNCTIONS)}"
                    )

                else:

                    # Execute the tool
                    result = function(**arguments)

            except json.JSONDecodeError as error:

                result = (
                    f"Argument error: {error}. "
                    "Send valid JSON."
                )

            except TypeError as error:

                result = f"Argument error: {error}"

            # --------------------------------------------------
            # Print action and observation
            # --------------------------------------------------

            if verbose:

                print(
                    f"   step {step}: "
                    f"{name}({arguments}) "
                    f"-> {str(result)[:120]}"
                )

            # --------------------------------------------------
            # Send tool result back to the model
            # --------------------------------------------------

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result)
                }
            )

    # --------------------------------------------------
    # Maximum step safety exit
    # --------------------------------------------------

    return "Stopped: maximum steps reached without a final answer."


# --------------------------------------------------
# Main program
# --------------------------------------------------

if __name__ == "__main__":

    banner("MY AGENT (no guards)")

    question = (
        "Read Day_3/notice.html and tell me the total fee "
        "for CS101 and AI202 after the merit scholarship."
    )

    print("Q:", question)

    print("A:", agent(question))