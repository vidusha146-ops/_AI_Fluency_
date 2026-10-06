# Day 5 – Ollama Local LLM Observations

## 1. Objective

The objective of this experiment was to understand how to run Large Language Models locally using Ollama, create custom models using Modelfiles, interact with models through REST APIs, compare different model sizes, and observe the effect of model parameters and system prompts.

---

## 2. Models Used

The following Ollama models were used during the experiment:

- `qwen2.5:1.5b`
- `qwen2.5:7b`

The 1.5B model has fewer parameters and requires less memory, while the 7B model is larger and generally provides more capable responses.

---

## 3. Model Benchmark

Both models were tested using the same prompts to compare their performance.

### Prompts Used

1. `Reply with exactly: OK`
2. `In two sentences, what is an AI agent?`
3. `A course costs Rs. 18,000 with a 15% scholarship. What is payable? Show the steps.`

### Qwen 2.5 1.5B

The 1.5B model successfully generated responses for the given prompts.

The model was able to:
- Follow simple instructions.
- Explain the concept of an AI agent.
- Perform the scholarship calculation.
- Generate responses relatively quickly.

### Qwen 2.5 7B

The 7B model was also tested using the same prompts.

The model was able to:
- Follow the given instructions.
- Explain an AI agent.
- Perform the scholarship calculation.
- Generate more detailed responses compared with the smaller model.

### Benchmark Observations

The benchmark measured:

- Total generation time
- Number of generated tokens
- Tokens per second
- Model loading time

The performance depends on the model size, available GPU/CPU resources, prompt length, and whether the model is already loaded in memory.

---

## 4. Scholarship Calculation Test

The following problem was given to the models:

> A course costs Rs. 18,000 with a 15% scholarship. What is payable?

### Calculation

Course fee = ₹18,000

Scholarship = 15%

Scholarship amount:

₹18,000 × 15 / 100 = ₹2,700

Payable amount:

₹18,000 − ₹2,700 = ₹15,300

### Expected Answer

**₹15,300**

The model should correctly calculate the payable amount as ₹15,300.

---

## 5. Modelfile Experiment

A custom model named `fee-assistant` was created using a Modelfile.

### Base Model

```text
qwen2.5:1.5b