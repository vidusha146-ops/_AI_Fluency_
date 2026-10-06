# Day 4 — Open LLM Memory and Licence Analysis

## 1. Scenario

My scenario is a personal/private coding assistant running locally on a computer with 16 GB RAM.

- Hardware memory budget: 16 GB
- Serving approach: Local serving using Ollama
- Purpose: Coding assistance and small AI-agent tasks
- Users: 1 personal user
- Working context: 8K tokens for the planned scenario

The goal is to determine whether small open-weight language models can fit within the available memory and how quantization and context length affect memory usage.

---

## 2. Model Memory Concepts

### Model Weights

Model weights are the parameters learned during model training.

A simplified estimate is:

Memory for weights = Number of parameters × Bytes per parameter

The bytes per parameter depend on the numerical precision.

| Precision | Approximate bytes/parameter |
|---|---:|
| FP32 | 4 |
| FP16 | 2 |
| BF16 | 2 |
| INT8 | 1 |
| INT4 | 0.5 |

Quantization reduces the number of bits used to represent model weights and therefore reduces memory requirements.

### KV Cache

The KV cache stores attention keys and values for tokens already processed by the model.

Its memory requirement increases as the context length increases.

Therefore, increasing context length can increase runtime memory even when the model weights remain unchanged.

### Context Length

Context length is the number of tokens that can be considered by the model during inference.

In my Ollama observation, the running Qwen2.5 1.5B model showed:

- Context: 4096 tokens
- Runtime size: 1.2 GB
- Processor: 100% GPU

---

## 3. Memory Estimation

The project estimator considers:

- Model parameter count
- Quantization/precision
- Context length
- KV cache
- Runtime overhead

The estimator was tested using multiple configurations.

### Llama 3.2 3B

| Configuration | Context | Estimated total |
|---|---:|---:|
| INT4 | 4K | 2.575 GB |
| INT4 | 8K | 3.045 GB |
| INT8 | 8K | 4.650 GB |

### Qwen2.5 3B

| Configuration | Context | Estimated total |
|---|---:|---:|
| INT4 | 4K | 2.196 GB |
| INT4 | 8K | 2.347 GB |

All of these simplified estimates are below the 16 GB memory budget.

---

## 4. Effect of Context Length

For Llama 3.2 3B using INT4:

| Context | Weights | KV Cache | Total |
|---:|---:|---:|---:|
| 2K | 1.605 GB | 0.235 GB | 2.340 GB |
| 4K | 1.605 GB | 0.470 GB | 2.575 GB |
| 8K | 1.605 GB | 0.940 GB | 3.045 GB |
| 16K | 1.605 GB | 1.879 GB | 3.984 GB |

The weight memory stays constant because the model and quantization do not change.

The KV-cache memory increases with context length.

---

## 5. Effect of Quantization

For Llama 3.2 3B at 8K context:

| Precision | Weight memory | KV cache | Total |
|---|---:|---:|---:|
| FP16 | 6.420 GB | 0.940 GB | 7.860 GB |
| INT8 | 3.210 GB | 0.940 GB | 4.650 GB |
| INT4 | 1.605 GB | 0.940 GB | 3.045 GB |

This demonstrates the memory benefit of quantization.

INT4 requires substantially less estimated weight memory than FP16.

---

## 6. Ollama Reality Check

The model available locally was:

`qwen2.5:1.5b`

The Ollama model list showed approximately:

- Model: qwen2.5:1.5b
- Downloaded model size: 986 MB

While the model was running, `ollama ps` showed:

- Model: qwen2.5:1.5b
- Runtime size: 1.2 GB
- Processor: 100% GPU
- Context: 4096

The downloaded model size and runtime memory are different measurements. Runtime memory includes additional inference-related memory and therefore should not be expected to exactly match the stored model size.

---

## 7. Estimate vs Reality

The estimator is a simplified planning tool.

It estimates memory from model parameters, precision, context length, KV cache and overhead.

Ollama reports the actual runtime state of the locally running model.

Therefore, the estimator should be treated as an approximate feasibility calculation rather than an exact prediction of the final runtime memory.

The observed Qwen2.5 1.5B runtime used 1.2 GB according to `ollama ps`, while the stored model shown by `ollama list` was 986 MB.

---

## 8. Open-Weight Models and Licensing

Open-weight availability means that model weights are available for users to download and run.

This does not automatically mean that every model uses a conventional open-source software licence.

For this project, model cards and official documentation should be checked before using a model in a particular application.

The models considered for comparison include:

1. Llama 3.2
2. Qwen2.5
3. Gemma 3

Their official model cards and licence/terms should be checked before deployment.

---

## 9. Suitability for My Scenario

My scenario has a 16 GB memory budget and requires local/private inference.

Small quantized models are suitable for testing this type of setup because quantization substantially reduces weight memory.

Context length also needs to be controlled because increasing context increases KV-cache memory.

The actual Ollama observation confirms that a small model such as Qwen2.5 1.5B can run locally on the available system.

---

## 10. Conclusion

This experiment demonstrates that model selection for local serving depends on more than parameter count.

Important factors include:

- Weight precision
- Quantization
- Context length
- KV-cache requirements
- Runtime overhead
- Available hardware memory
- Model licence and usage terms

The memory estimator provides a way to compare configurations before downloading a model, while Ollama provides an actual runtime observation.