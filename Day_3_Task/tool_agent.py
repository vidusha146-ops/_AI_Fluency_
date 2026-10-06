import os
import json

from dotenv import load_dotenv
from groq import Groq

from my_tools import find_lost_item


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY was not found in .env")


# Create Groq client
client = Groq(api_key=api_key)

MODEL = "openai/gpt-oss-120b"


# Tool schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "find_lost_item",
            "description": (
                "Search the college Lost and Found records "
                "for a specific item."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": (
                            "Name of the lost item, such as "
                            "black water bottle or scientific calculator."
                        )
                    }
                },
                "required": ["item_name"]
            }
        }
    }
]


# User question
question = "Where was the black water bottle found?"


print("=" * 60)
print("FINDITAI - TOOL ENABLED AGENT")
print("=" * 60)

print("\nQuestion:")
print(question)


# Initial conversation
messages = [
    {
        "role": "user",
        "content": question
    }
]


# Ask the LLM whether a tool is needed
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    tool_choice="auto"
)


message = response.choices[0].message


# Check whether the LLM requested a tool
if message.tool_calls:

    print("\nTool call detected!")

    # Add the assistant's tool request
    messages.append(message)

    for tool_call in message.tool_calls:

        function_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        print("\nTool name:")
        print(function_name)

        print("\nArguments:")
        print(json.dumps(arguments, indent=2))


        # Execute our actual Python tool
        if function_name == "find_lost_item":

            tool_result = find_lost_item(
                arguments["item_name"]
            )

            print("\nTool result:")
            print(tool_result)


            # Give the tool result back to the LLM
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result
                }
            )


    # Ask the LLM to produce the final answer
    final_response = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )


    final_answer = (
        final_response.choices[0].message.content
    )


    print("\nFinal answer:")
    print(final_answer)


else:

    print("\nNo tool was called.")

    print("\nFinal answer:")
    print(message.content)