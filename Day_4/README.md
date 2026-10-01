# Agentic AI Day 4 — Will It Fit?

## Objective

This lab estimates local LLM memory requirements and compares model sizes, context lengths, quantization levels, licences, and Ollama runtime behavior.

## Hardware

* Windows 11
* 15.6 GB system RAM
* NVIDIA GPU
* 6 GB dedicated VRAM

## Main Files

* `vram_estimate.py` — memory estimation and hardware detection
* `analysis.md` — completed lab analysis
* `README.md` — project documentation

## Ollama Test

Model:

`qwen2.5:1.5b`

Observed:

* Runtime size: 1.2 GB
* Processor: 100% GPU
* Context: 4096 tokens

## Main Finding

The tested 1.5B Q4 model fits comfortably within the available GPU budget. Larger models require substantially more memory, especially as parameter count, precision, and context length increase.

## Model Comparison

The lab compares Qwen, Mistral, IBM Granite, and gpt-oss using their published model information and licensing terms.

## Tools

* Python
* VS Code
* Ollama
* Git
* GitHub
