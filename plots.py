# import json
# import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker
# import numpy as np

# with open("logs\\pipeline_metrics_refactored_with_datetime.json", "r") as f:
#     content = f.read().strip()

# try:
#     records = json.loads(content)
# except json.JSONDecodeError:
#     records = [json.loads(line) for line in content.splitlines() if line.strip()]

# frames        = [r["frame"]             for r in records]
# infer_ms      = [r["infer_ms"]          for r in records]
# edge_to_fog   = [r["edge_to_fog_ms"]    for r in records]
# fog_proc      = [r["fog_processing_ms"] for r in records]
# total_pipe    = [r["total_pipeline_ms"] for r in records]

# plt.rcParams.update({
#     "figure.facecolor":  "#0e1318",
#     "axes.facecolor":    "#0e1318",
#     "axes.edgecolor":    "#1c2530",
#     "axes.labelcolor":   "#c8d6e5",
#     "axes.titlecolor":   "#ffffff",
#     "xtick.color":       "#4a5568",
#     "ytick.color":       "#4a5568",
#     "grid.color":        "#1c2530",
#     "grid.linestyle":    "--",
#     "grid.linewidth":    0.5,
#     "text.color":        "#c8d6e5",
#     "font.family":       "monospace",
# })

# COLORS = {
#     "infer":     "#00e5a0",   # green
#     "edge_fog":  "#378add",   # blue
#     "fog_proc":  "#f5a623",   # amber
#     "total":     "#ff3d57",   # red
# }

# fig, axes = plt.subplots(4, 1, figsize=(14, 16))
# fig.suptitle("Pipeline Latency Analysis — Edge·Fog·Cloud", fontsize=14, color="#ffffff", y=0.98)
# plt.subplots_adjust(hspace=0.45)

# def plot(ax, x, y, color, title, ylabel, show_avg=True):
#     ax.plot(x, y, color=color, linewidth=0.8, alpha=0.7)
#     ax.fill_between(x, y, alpha=0.12, color=color)

#     if show_avg:
#         avg = np.mean(y)
#         ax.axhline(avg, color=color, linewidth=1, linestyle="--", alpha=0.6)
#         ax.text(
#             x[-1], avg,
#             f" avg: {avg:.2f}ms",
#             color=color, fontsize=8,
#             va="bottom", ha="right"
#         )

#     ax.set_title(title, fontsize=10, pad=8)
#     ax.set_xlabel("Frame", fontsize=8)
#     ax.set_ylabel(ylabel, fontsize=8)
#     ax.grid(True, axis="y")
#     ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
#     ax.set_xlim(min(x), max(x))

# plot(axes[0], frames, infer_ms,
#      COLORS["infer"],
#      "TFLite Inference Time (Edge Node)",
#      "ms")

# plot(axes[1], frames, edge_to_fog,
#      COLORS["edge_fog"],
#      "Edge → Fog Latency (simulated LAN)",
#      "ms")


# plot(axes[2], frames, fog_proc,
#      COLORS["fog_proc"],
#      "Fog Decision Engine Processing Time",
#      "ms")

# plot(axes[3], frames, total_pipe,
#      COLORS["total"],
#      "Total End-to-End Pipeline Latency",
#      "ms")

# # highlight max on total pipeline
# max_idx = int(np.argmax(total_pipe))
# axes[3].annotate(
#     f"peak: {total_pipe[max_idx]:.1f}ms",
#     xy=(frames[max_idx], total_pipe[max_idx]),
#     xytext=(frames[max_idx] + len(frames) * 0.02, total_pipe[max_idx]),
#     color="#ff3d57",
#     fontsize=8,
#     arrowprops=dict(arrowstyle="->", color="#ff3d57", lw=0.8)
# )

# plt.savefig("logs/latency_graphs.png", dpi=150, bbox_inches="tight",
#             facecolor="#0e1318")
# plt.show()








import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import os

with open("logs/pipeline_metrics_refactored_with_datetime.json", "r") as f:
    content = f.read().strip()

try:
    records = json.loads(content)
except json.JSONDecodeError:
    records = [json.loads(line) for line in content.splitlines() if line.strip()]

frames      = [r["frame"]             for r in records]
infer_ms    = [r["infer_ms"]          for r in records]
edge_to_fog = [r["edge_to_fog_ms"]    for r in records]
fog_proc    = [r["fog_processing_ms"] for r in records]
total_pipe  = [r["total_pipeline_ms"] for r in records]

os.makedirs("logs/plots", exist_ok=True)

plt.rcParams.update({
    "figure.facecolor": "#0e1318",
    "axes.facecolor":   "#0e1318",
    "axes.edgecolor":   "#1c2530",
    "axes.labelcolor":  "#c8d6e5",
    "axes.titlecolor":  "#ffffff",
    "xtick.color":      "#4a5568",
    "ytick.color":      "#4a5568",
    "grid.color":       "#1c2530",
    "grid.linestyle":   "--",
    "grid.linewidth":   0.5,
    "text.color":       "#c8d6e5",
    "font.family":      "monospace",
})

COLORS = {
    "infer":    "#00e5a0",  # green
    "edge_fog": "#378add",  # blue
    "fog_proc": "#f5a623",  # amber
    "total":    "#ff3d57",  # red
}

PLOTS = [
    {
        "key":      "infer",
        "x":        frames,
        "y":        infer_ms,
        "title":    "TFLite Inference Time (Edge Node)",
        "ylabel":   "ms",
        "filename": "logs/plots/01_inference_time.png",
        "annotate_peak": False,
    },
    {
        "key":      "edge_fog",
        "x":        frames,
        "y":        edge_to_fog,
        "title":    "Edge → Fog Latency (simulated LAN)",
        "ylabel":   "ms",
        "filename": "logs/plots/02_edge_to_fog_latency.png",
        "annotate_peak": False,
    },
    {
        "key":      "fog_proc",
        "x":        frames,
        "y":        fog_proc,
        "title":    "Fog Decision Engine Processing Time",
        "ylabel":   "ms",
        "filename": "logs/plots/03_fog_processing_time.png",
        "annotate_peak": False,
    },
    {
        "key":      "total",
        "x":        frames,
        "y":        total_pipe,
        "title":    "Total End-to-End Pipeline Latency",
        "ylabel":   "ms",
        "filename": "logs/plots/04_total_pipeline_latency.png",
        "annotate_peak": True,
    },
]


def make_plot(x, y, color, title, ylabel, filename, annotate_peak=False):
    fig, ax = plt.subplots(figsize=(14, 4))
    fig.suptitle(
        f"Pipeline Latency Analysis — {title}",
        fontsize=12, color="#ffffff", y=1.01
    )

    # Line plot (no fill)
    ax.plot(x, y, color=color, linewidth=1.0, alpha=0.9)

    # Average line
    avg = np.mean(y)
    ax.axhline(avg, color=color, linewidth=1, linestyle="--", alpha=0.55)
    ax.text(
        x[-1], avg,
        f" avg: {avg:.2f}ms",
        color=color, fontsize=8,
        va="bottom", ha="right"
    )

    # Peak annotation (total pipeline only)
    if annotate_peak:
        max_idx = int(np.argmax(y))
        ax.annotate(
            f"peak: {y[max_idx]:.1f}ms",
            xy=(x[max_idx], y[max_idx]),
            xytext=(x[max_idx] + len(x) * 0.02, y[max_idx]),
            color=color,
            fontsize=8,
            arrowprops=dict(arrowstyle="->", color=color, lw=0.8),
        )

    ax.set_xlabel("Frame", fontsize=8)
    ax.set_ylabel(ylabel, fontsize=8)
    ax.grid(True, axis="y")
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.set_xlim(min(x), max(x))

    fig.tight_layout()
    fig.savefig(filename, dpi=150, bbox_inches="tight", facecolor="#0e1318")
    plt.close(fig)
    print(f"Saved: {filename}")


for cfg in PLOTS:
    make_plot(
        x=cfg["x"],
        y=cfg["y"],
        color=COLORS[cfg["key"]],
        title=cfg["title"],
        ylabel=cfg["ylabel"],
        filename=cfg["filename"],
        annotate_peak=cfg["annotate_peak"],
    )

print("\nAll plots saved to logs/plots/")