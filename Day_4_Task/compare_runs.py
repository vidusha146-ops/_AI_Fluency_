from estimator import estimate_memory


BUDGET = 16.0


MODEL = {
    "params_b": 3.21,
    "layers": 28,
    "kv_heads": 8,
    "head_dim": 128,
}


def show_result(label, precision, context_k):

    result = estimate_memory(
        MODEL["params_b"],
        precision,
        context_k,
        MODEL["layers"],
        MODEL["kv_heads"],
        MODEL["head_dim"],
        memory_budget_gb=BUDGET,
    )

    print(
        f"{label:25} | "
        f"{precision:>4} | "
        f"{context_k:>4}K | "
        f"{result['weights_gb']:>6.3f} | "
        f"{result['kv_cache_gb']:>6.3f} | "
        f"{result['total_gb']:>6.3f} | "
        f"{result['fits']}"
    )


print("CONTEXT LENGTH OBSERVATION")

print(
    "Setting                  | Q    | Context | "
    "Weights | KV     | Total  | Fits"
)

print("-" * 90)

for context in [2, 4, 8, 16]:

    show_result(
        "Context length",
        "INT4",
        context,
    )


print("\nQUANTIZATION OBSERVATION")

print(
    "Setting                  | Q    | Context | "
    "Weights | KV     | Total  | Fits"
)

print("-" * 90)

for precision in ["FP16", "INT8", "INT4"]:

    show_result(
        "Quantization",
        precision,
        8,
    )