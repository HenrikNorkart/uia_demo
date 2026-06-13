"""Fetch the latest uia-demo run from WandB and print results as a LaTeX table."""
import wandb

api = wandb.Api()
runs = api.runs("PlanBench/uia-demo", order="-created_at", per_page=1)
run = next(iter(runs))

print(f"RUN_ID={run.id}")
print(f"RUN_NAME={run.name}")
print(f"DEVICE={run.summary.get('device', 'H100')}")
print(f"PEAK_TFLOPS={run.summary.get('peak_tflops', '')}")

for row in run.history(keys=["matrix_size", "latency_ms", "tflops"]).itertuples():
    n = int(row.matrix_size) if not __import__("math").isnan(row.matrix_size) else None
    if n:
        print(f"ROW {n} {row.latency_ms:.2f} {row.tflops:.2f}")
