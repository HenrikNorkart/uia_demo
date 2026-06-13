import torch
import wandb
import time
import socket

wandb.init(
    project="uia-demo",
    entity="PlanBench",
    name="h100-matmul-benchmark",
    config={"device": torch.cuda.get_device_name(0), "dtype": "float16"},
)

sizes = [1024, 2048, 4096, 8192, 16384, 32768]
results = []

for n in sizes:
    iters = 5 if n >= 16384 else 10
    A = torch.randn(n, n, device="cuda", dtype=torch.float16)
    B = torch.randn(n, n, device="cuda", dtype=torch.float16)

    for _ in range(2):  # warmup
        _ = A @ B
    torch.cuda.synchronize()

    t0 = time.perf_counter()
    for _ in range(iters):
        C = A @ B
    torch.cuda.synchronize()
    elapsed_ms = (time.perf_counter() - t0) / iters * 1000

    tflops = (2 * n**3) / (elapsed_ms / 1000) / 1e12

    results.append({"n": n, "latency_ms": round(elapsed_ms, 2), "tflops": round(tflops, 2)})
    wandb.log({"matrix_size": n, "latency_ms": elapsed_ms, "tflops": tflops})
    print(f"  {n}x{n}: {elapsed_ms:.2f} ms  |  {tflops:.2f} TFLOPS")

table = wandb.Table(
    columns=["Matrix Size", "Latency (ms)", "TFLOPS"],
    data=[[r["n"], r["latency_ms"], r["tflops"]] for r in results],
)
wandb.log({"results": table})
wandb.summary["peak_tflops"] = max(r["tflops"] for r in results)
wandb.summary["device"] = torch.cuda.get_device_name(0)
wandb.finish()
print("Done. Run logged to WandB.")
