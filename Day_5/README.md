# Day 5 - Ollama Model Serving Lab

## Overview

This project demonstrates local LLM serving using Ollama.

## Topics

- Ollama CLI
- Model inspection
- Modelfiles
- Custom models
- REST API
- Streaming
- TTFT
- Token generation speed
- Model benchmarking
- OpenAI-compatible API
- vLLM
- PagedAttention
- Continuous batching

## Files

| File | Purpose |
|---|---|
| Modelfile | Fee assistant configuration |
| Modelfile.creative | Events announcer configuration |
| prompt_override.py | Tests program-level system prompt |
| api_demo.py | Tests Ollama REST APIs |
| bench_models.py | Compares two models |
| observations.md | Experimental results |
| requirements.txt | Python dependencies |

## Models

Model A:
qwen2.5:1.5b

Model B:
qwen2.5:7b

## Run

Install dependencies:

```powershell
pip install -r requirements.txt