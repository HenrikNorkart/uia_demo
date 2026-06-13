import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sizes   = [1024, 2048, 4096, 8192, 16384, 32768]
tflops  = [181.15, 557.69, 707.06, 784.88, 741.96, 619.11]
latency = [0.01, 0.03, 0.19, 1.40, 11.86, 113.66]

labels = [f"{n:,}²" for n in sizes]

fig, ax1 = plt.subplots(figsize=(7, 4))

color_tflops  = "#1f77b4"
color_latency = "#ff7f0e"

bars = ax1.bar(labels, tflops, color=color_tflops, alpha=0.85, label="Throughput (TFLOPS)")
ax1.set_xlabel("Matrix size", fontsize=12)
ax1.set_ylabel("Throughput (TFLOPS)", color=color_tflops, fontsize=12)
ax1.tick_params(axis="y", labelcolor=color_tflops)
ax1.set_ylim(0, 950)
ax1.axhline(989, color=color_tflops, linestyle="--", linewidth=1, alpha=0.5, label="H100 FP16 peak (989 TFLOPS)")

for bar, val in zip(bars, tflops):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 15,
             f"{val:.0f}", ha="center", va="bottom", fontsize=10, color=color_tflops)

ax2 = ax1.twinx()
ax2.plot(labels, latency, color=color_latency, marker="o", linewidth=2, markersize=7, label="Latency (ms)")
ax2.set_ylabel("Latency (ms, log scale)", color=color_latency, fontsize=12)
ax2.tick_params(axis="y", labelcolor=color_latency)
ax2.set_yscale("log")
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{x:g}"))

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", fontsize=9)

ax1.set_title("H100 FP16 Matrix Multiplication Benchmark", fontsize=13, fontweight="bold")
fig.tight_layout()
fig.savefig("/workspace/benchmark_plot.pdf", dpi=150, bbox_inches="tight")
fig.savefig("/workspace/benchmark_plot.png", dpi=150, bbox_inches="tight")
print("Plot saved.")
