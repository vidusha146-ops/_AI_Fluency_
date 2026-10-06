\# Agentic AI: Foundations and Open-Source Practice — Day 1



\## 1. Introduction



This project compares three approaches for building a college course-fee assistant:



1\. Plain Chatbot

2\. Rule-Based Workflow

3\. AI Agent



The same college course-fee scenario is used to understand the differences between these approaches.



\---



\## 2. Private Course-Fee Scenario



The college has private course-fee information:



| Course | Fee |

|---|---:|

| CS101 | Rs. 12,000 |

| AI202 | Rs. 18,000 |

| DS303 | Rs. 15,000 |



The assistant should be able to answer course-fee questions and handle multi-step questions involving the private data.



\---



\## 3. System 1 — Plain Chatbot



The plain chatbot uses an LLM to generate responses.



It can understand natural-language questions and generate flexible responses.



However, in this implementation, the chatbot does not have access to the private course-fee database.



Therefore, it cannot reliably look up private course fees.



\### Characteristics



\- Uses an LLM.

\- Flexible natural-language interaction.

\- No private-data tool access.

\- Does not perform controlled tool-based operations.

\- Suitable for general questions and text generation.



\---



\## 4. System 2 — Rule-Based Workflow



The rule-based workflow does not use an LLM.



It uses predefined conditions and programmed actions.



For example, the workflow contains specific rules for:



\- AI202 fee

\- CS101 + AI202 with a 10% scholarship

\- Comparing DS303 and CS101

\- Generating a welcome message



If a question does not match a predefined rule, the workflow cannot answer it.



\### Characteristics



\- Uses predefined rules.

\- No LLM required.

\- Predictable for known inputs.

\- Can access private data through programmed rules.

\- Limited flexibility.

\- Difficult to handle unexpected questions.



\---



\## 5. System 3 — AI Agent



The AI agent combines:



\- LLM

\- Tools

\- Tool-selection decisions

\- A loop that observes tool results and continues working



The agent has access to the following tools:



\### `get\_course\_fee`



Retrieves the fee for a specific course.



\### `get\_all\_courses`



Retrieves all available courses and their fees.



\### `calculator`



Performs arithmetic calculations.



The agent can decide which tool is required for a question and can use multiple tools before producing the final answer.



For example, for the scholarship question, the agent can:



1\. Retrieve the CS101 fee.

2\. Retrieve the AI202 fee.

3\. Use the calculator.

4\. Return the final result.



This demonstrates the agent loop:



\*\*LLM → Tool → Result → LLM → Tool → Result → Final Answer\*\*



\---



\## 6. Comparison Table



| Feature | Plain Chatbot | Rule-Based Workflow | AI Agent |

|---|---|---|---|

| LLM | Yes | No | Yes |

| Flexibility | High | Low | High |

| Decision-making | LLM response generation | Fixed conditions | LLM selects tools/actions |

| Tool usage | No | Programmed actions | Yes |

| Private-data access | No in this implementation | Yes | Yes through tools |

| Multi-step handling | Limited | Predefined | Yes |

| Automation | Basic | Fixed automation | Dynamic automation |

| Reliability | Depends on model response | High for predefined rules | Depends on model, tools and instructions |



\---



\## 7. Suitability Analysis



For this college course-fee scenario, an AI agent is suitable when the assistant needs to work with private data and handle questions that require multiple steps.



The agent can access private data through controlled tools instead of directly exposing the database to the user.



A rule-based workflow is useful when the possible questions and actions are predictable and known in advance.



A plain chatbot is useful when the main requirement is general conversation, explanation, or text generation without access to private course data.



Therefore, the appropriate approach depends on the requirements:



\- General conversation → Plain Chatbot

\- Predictable predefined tasks → Rule-Based Workflow

\- Private data + dynamic multi-step tasks → AI Agent



\---



\## 8. Challenge Result



\### Challenge



\*\*Question:\*\*



> I can pay Rs. 30,000. Which two courses can I take together within this budget?



\### Rule-Based Workflow



The workflow could not answer the question because no predefined rule was created for this type of budget query.



\### AI Agent



The agent used the `get\_all\_courses` tool to retrieve the private course-fee data.



It then compared the possible course pairs.



\### Valid combinations



1\. \*\*CS101 + AI202\*\*

&#x20;  - Rs. 12,000 + Rs. 18,000

&#x20;  - Total = Rs. 30,000



2\. \*\*CS101 + DS303\*\*

&#x20;  - Rs. 12,000 + Rs. 15,000

&#x20;  - Total = Rs. 27,000



The following combination exceeds the budget:



\- AI202 + DS303

\- Rs. 18,000 + Rs. 15,000

\- Total = Rs. 33,000



This demonstrates that the AI agent can dynamically select a tool, observe its result, perform multi-step processing, and provide an answer.



\---



\## 9. Conclusion



The three approaches have different purposes.



A plain chatbot is useful for general natural-language interaction and text generation.



A rule-based workflow is useful when tasks are predictable and can be represented using fixed conditions.



An AI agent is useful when a system needs to combine an LLM with tools and perform dynamic multi-step tasks.



This project demonstrates the difference between simply generating an answer, following predefined rules, and using an agent that can select tools and continue working based on tool results.

