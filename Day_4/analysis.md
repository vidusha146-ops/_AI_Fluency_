# Day 4 Lab — Will It Fit?

## 1. Hardware Detection

* Operating System: Windows 11
* System RAM: 15.6 GB
* GPU: NVIDIA dedicated GPU
* Dedicated VRAM: 6.0 GB
* Recommended GPU memory budget: 5.4 GB

## 2. Memory Estimation

The estimator uses:

* Weights = parameters in billions × bytes per parameter
* KV cache = parameters in billions × context in K tokens × 0.02
* Total = (weights + KV cache) × 1.10

### Main 8K estimates

| Model              | Quantization | Parameters | Total Memory | Result           |
| ------------------ | ------------ | ---------: | -----------: | ---------------- |
| Qwen small         | Q4_K_M       |       1.5B |      1.20 GB | Fits comfortably |
| Granite / Qwen mid | Q4_K_M       |         8B |      6.42 GB | Does not fit     |
| Mid at FP16        | FP16         |         8B |     19.01 GB | Does not fit     |
| Large local        | Q4_K_M       |        30B |     24.09 GB | Does not fit     |
| Server class       | Q4_K_M       |        70B |     56.21 GB | Does not fit     |

## 3. Context-Length Experiment

For the 8B Q4_K_M model:

| Context | Total Memory |
| ------: | -----------: |
|      4K |      5.72 GB |
|      8K |      6.42 GB |
|     32K |     10.65 GB |
|    128K |     27.54 GB |

The weights remain constant while the estimated KV-cache memory increases with context length.

## 4. Quantization Experiment

For the 8B model at 8K context:

| Quantization | Total Memory |
| ------------ | -----------: |
| Q3_K_M       |      5.19 GB |
| Q4_K_M       |      6.42 GB |
| Q5_K_M       |      7.39 GB |
| Q8_0         |     10.21 GB |
| FP16         |     19.01 GB |

Lower-bit quantization reduces estimated memory requirements.

## 5. Ollama Experiment

Model tested:

`qwen2.5:1.5b`

Observed runtime information:

* Size: 1.2 GB
* Processor: 100% GPU
* Context: 4096 tokens

The model successfully loaded and ran entirely on the dedicated GPU.

## 6. Four-Model Comparison

| Model                    |  Parameters | Context | License    | Tool Calling                 | Ollama    |
| ------------------------ | ----------: | ------: | ---------- | ---------------------------- | --------- |
| Qwen2.5-1.5B-Instruct    |       1.54B |     32K | Apache 2.0 | Yes                          | Yes       |
| Mistral-7B-Instruct-v0.3 |         ~7B |     32K | Apache 2.0 | Function calling             | Available |
| Granite-3.3-2B-Instruct  |          2B |    128K | Apache 2.0 | Function calling             | Yes       |
| gpt-oss-20b              | 20.9B total |    128K | Apache 2.0 | Native tool/function calling | Yes       |

## 7. Scenario Analysis

### 8 GB laptop without GPU

A small Q4 model is appropriate because the estimated memory requirement is low. The 1.5B Q4_K_M test is 1.20 GB in the lab estimator.

### 24 GB GPU server

An 8B Q4 model is within the simplified 24 GB memory estimate, while the 30B Q4 model is estimated at 24.09 GB before considering practical multi-user serving overhead.

### Public GitHub capstone

The repository should clearly document the exact model/version, license, quantization, source, and redistribution/commercial-use terms.

## 8. Conclusion

The experiment demonstrates that model size alone does not determine whether a model will fit. Precision, quantization, context length, KV cache, and runtime overhead all affect memory requirements.

On the tested machine, the 1.5B Q4 model fits comfortably in the available GPU budget, while the 8B Q4 model exceeds the 5.4 GB estimated usable GPU budget.
