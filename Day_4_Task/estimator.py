"""
Day 4 - Open LLM Memory Estimator

Formula:

Weights = Parameters × Bytes per parameter

KV Cache =
2 × Layers × KV Heads × Head Dimension
× Context Tokens × KV Bytes

Total =
Weights + KV Cache + Runtime Overhead
"""

BYTES_PER_PARAM = {
    "FP32": 4.0,
    "FP16": 2.0,
    "BF16": 2.0,
    "INT8": 1.0,
    "INT4": 0.5,
}


def estimate_memory(
    params_b,
    precision,
    context_k,
    layers,
    kv_heads,
    head_dim,
    kv_precision="FP16",
    overhead_gb=0.50,
    memory_budget_gb=16.0,
):
    weight_bpp = BYTES_PER_PARAM[precision]
    kv_bpp = BYTES_PER_PARAM[kv_precision]

    weights_gb = params_b * weight_bpp

    context_tokens = context_k * 1024

    kv_bytes = (
        2
        * layers
        * kv_heads
        * head_dim
        * context_tokens
        * kv_bpp
    )

    kv_gb = kv_bytes / 1_000_000_000

    total_gb = weights_gb + kv_gb + overhead_gb

    return {
        "weights_gb": round(weights_gb, 3),
        "kv_cache_gb": round(kv_gb, 3),
        "overhead_gb": round(overhead_gb, 3),
        "total_gb": round(total_gb, 3),
        "fits": total_gb <= memory_budget_gb,
    }


def print_row(
    name,
    params_b,
    precision,
    context_k,
    layers,
    kv_heads,
    head_dim,
    memory_budget_gb=16.0,
):

    result = estimate_memory(
        params_b,
        precision,
        context_k,
        layers,
        kv_heads,
        head_dim,
        memory_budget_gb=memory_budget_gb,
    )

    print(
        f"{name:30} | "
        f"params={params_b:>4}B | "
        f"{precision:>4} | "
        f"context={context_k:>3}K | "
        f"weights={result['weights_gb']:>6.3f} GB | "
        f"KV={result['kv_cache_gb']:>6.3f} GB | "
        f"total={result['total_gb']:>6.3f} GB | "
        f"fits={result['fits']}"
    )


if __name__ == "__main__":

    print("Available memory budget: 16 GB")
    print("-" * 120)

    # Llama 3.2 3B
    # 3.21B parameters
    # 28 layers
    # 8 KV heads
    # 128 head dimension

    print_row(
        "Llama 3.2 3B Q4 @ 4K",
        3.21,
        "INT4",
        4,
        28,
        8,
        128,
    )

    print_row(
        "Llama 3.2 3B Q4 @ 8K",
        3.21,
        "INT4",
        8,
        28,
        8,
        128,
    )

    print_row(
        "Llama 3.2 3B Q8 @ 8K",
        3.21,
        "INT8",
        8,
        28,
        8,
        128,
    )

    # Qwen2.5 3B
    # 3.09B parameters
    # 36 layers
    # 2 KV heads
    # 128 head dimension

    print_row(
        "Qwen2.5 3B Q4 @ 4K",
        3.09,
        "INT4",
        4,
        36,
        2,
        128,
    )

    print_row(
        "Qwen2.5 3B Q4 @ 8K",
        3.09,
        "INT4",
        8,
        36,
        2,
        128,
    )