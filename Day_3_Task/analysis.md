# Agentic AI: Foundations and Open-Source Practice

## Day 1 Task: From Prompt to Action

### Project: FindItAI — College Lost & Found Agent

---

## 1. Scenario

For this task, I created a small college Lost & Found scenario called **FindItAI**.

The system contains records of items that have been found on the college campus.

A student can ask questions such as:

* Where was the black water bottle found?
* Was a scientific calculator found?
* Where was the student ID card found?

The system uses an external Python tool called `find_lost_item()` to search the Lost & Found records.

---

## 2. External Tool

The external tool used in this project is:

```text
find_lost_item(item_name)
```

The tool searches a small predefined Lost & Found database.

Example records include:

| Item                  | Location          | Status |
| --------------------- | ----------------- | ------ |
| Black Water Bottle    | Library 2nd Floor | Found  |
| Blue Umbrella         | College Canteen   | Found  |
| Scientific Calculator | Block C Lab       | Found  |
| Black USB Drive       | Seminar Hall      | Found  |
| Student ID Card       | Main Office       | Found  |

The tool returns the matching record as plain text.

---

## 3. What is an LLM?

LLM stands for **Large Language Model**.

An LLM is a model trained on large amounts of text so that it can understand natural-language questions and generate responses.

In this project, the LLM receives a user's question and generates an answer.

For example:

```text
User:
What should a student do after losing an important item on campus?

        ↓

LLM

        ↓

Generated answer
```

The plain LLM does not directly access the college Lost & Found database.

---

## 4. What is an Agent?

An AI agent is a system in which an LLM can decide what action should be taken to complete a task.

In this project, the agent can decide that the `find_lost_item()` tool is required.

The basic flow is:

```text
User Question
      ↓
LLM
      ↓
Decides whether a tool is needed
      ↓
Tool Call
      ↓
Tool Result
      ↓
LLM
      ↓
Final Answer
```

Therefore, the agent is not simply generating text. It can use an external tool as part of the process.

---

## 5. What is a Tool?

A tool is an external function or service that an AI system can call to perform an action or retrieve information.

In FindItAI, the tool is:

```text
find_lost_item(item_name)
```

The LLM itself does not contain the Lost & Found records.

Instead, it can request the tool to search the records.

---

## 6. What is a Tool Call?

A tool call happens when the LLM decides that an external tool is needed and generates a request for that tool.

For example, for the question:

```text
Where was the black water bottle found?
```

the model can generate a tool call similar to:

```text
Tool name:
find_lost_item

Arguments:
{
    "item_name": "black water bottle"
}
```

The Python program then executes the actual function.

---

## 7. What is a Tool Schema?

The tool schema tells the LLM what tool is available and how the tool should be called.

The schema contains information such as:

* Tool name
* Description
* Parameter name
* Parameter type
* Required parameters

Example:

```text
Tool name:
find_lost_item

Parameter:
item_name

Type:
string

Required:
yes
```

The schema does not execute the tool.

It only describes the tool to the LLM.

---

## 8. Complete Agent Flow

For the question:

```text
Where was the black water bottle found?
```

the complete flow is:

### Step 1 — User asks a question

```text
Where was the black water bottle found?
```

### Step 2 — LLM receives the question

The LLM also receives the description of the available tool.

### Step 3 — LLM decides that the tool is needed

The LLM requests:

```text
find_lost_item(
    item_name="black water bottle"
)
```

### Step 4 — Python executes the tool

The Python function searches the Lost & Found records.

### Step 5 — Tool returns the result

```text
Item: Black Water Bottle
Location: Library 2nd Floor
Status: Found
```

### Step 6 — Result is sent back to the LLM

The tool result is added to the conversation as a tool message.

### Step 7 — LLM generates the final answer

The LLM converts the tool result into a natural-language response.

Example:

```text
The black water bottle was found on the Library 2nd Floor.
```

---

## 9. Why Does the Tool Return Plain Text?

The tool returns plain text because the LLM needs a simple, readable result that can be included in the conversation.

For example:

```text
Item: Black Water Bottle
Location: Library 2nd Floor
Status: Found
```

The LLM can easily understand this information and use it to generate the final response.

A real production system could instead return structured JSON, database records, or another machine-readable format.

---

## 10. Plain LLM vs Tool-Enabled Agent

| Feature                                  | Plain LLM    | Tool-Enabled Agent |
| ---------------------------------------- | ------------ | ------------------ |
| Receives user question                   | Yes          | Yes                |
| Generates language                       | Yes          | Yes                |
| Uses external tool                       | No           | Yes                |
| Accesses Lost & Found records            | No           | Yes                |
| Can retrieve specific stored information | Not directly | Yes                |
| Tool call visible in program             | No           | Yes                |
| Final natural-language answer            | Yes          | Yes                |

---

## 11. Observation 1 — General Question

Question:

```text
What should a student do after losing an important item on campus?
```

This question is general and does not require the college Lost & Found database.

Therefore, a plain LLM can provide a general response without calling the tool.

This demonstrates that not every question requires an external tool.

---

## 12. Observation 2 — Black Water Bottle

Question:

```text
Where was the black water bottle found?
```

This question requires information from the college Lost & Found records.

The tool-enabled agent calls:

```text
find_lost_item("black water bottle")
```

The tool returns:

```text
Item: Black Water Bottle
Location: Library 2nd Floor
Status: Found
```

The LLM then uses this result to generate the final answer.

This demonstrates how a tool can provide specific external information to the LLM.

---

## 13. Observation 3 — Scientific Calculator

Question:

```text
Was a scientific calculator found, and where?
```

The tool searches the records and returns:

```text
Item: Scientific Calculator
Location: Block C Lab
Status: Found
```

The agent can then use the result to answer the question.

This demonstrates that the same tool can be reused for different user questions.

---

## 14. Observation 4 — Missing Item

An additional test can be performed with:

```text
Was my red smartwatch found?
```

The item is not present in the sample database.

The tool returns:

```text
No matching item was found for 'red smartwatch'.
```

This demonstrates that a tool can also return a negative result when no matching record exists.

---

## 15. Why is the Tool Useful?

The tool is useful because the Lost & Found information is specific to the college.

The LLM may know general information about lost-and-found procedures, but it does not automatically know the current records stored in the Python database.

The tool provides the missing information.

Therefore:

```text
LLM = Understands and generates language

Tool = Provides specific external information

Agent = Connects the reasoning process with the tool
```

---

## 16. Suitability of the Approach

The tool-enabled approach is suitable when the question requires information that is stored outside the LLM.

Examples include:

* College Lost & Found records
* Current database information
* Weather data
* Stock information
* Product inventory
* Student records
* Search systems

For general questions, a plain LLM may be sufficient.

For questions requiring specific external data, a tool-enabled agent can provide a mechanism for retrieving that information.

---

## 17. Conclusion

This experiment demonstrates the difference between a plain LLM and a tool-enabled agent.

A plain LLM receives a question and generates an answer from its learned capabilities and the information provided in the prompt.

A tool-enabled agent can additionally use an external function.

In FindItAI, the LLM identifies when the Lost & Found tool is useful, sends the required item name, receives the tool result, and then produces a final natural-language answer.

The experiment helped demonstrate the basic relationship:

```text
Agent = LLM + Tools + Loop
```

The project shows how an LLM can move from simply generating text to interacting with an external system.
