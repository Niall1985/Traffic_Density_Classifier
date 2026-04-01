# # import json
# # import matplotlib.pyplot as plt
# # import matplotlib.ticker as ticker
# # import numpy as np
# # import os

# # with open("logs/pipeline_metrics_refactored_with_datetime.json", "r") as f:
# #     content = f.read().strip()

# # try:
# #     records = json.loads(content)
# # except json.JSONDecodeError:
# #     records = [json.loads(line) for line in content.splitlines() if line.strip()]

# # frames      = [r["frame"]             for r in records]
# # infer_ms    = [r["infer_ms"]          for r in records]
# # edge_to_fog = [r["edge_to_fog_ms"]    for r in records]
# # fog_proc    = [r["fog_processing_ms"] for r in records]
# # total_pipe  = [r["total_pipeline_ms"] for r in records]

# # os.makedirs("logs/plots", exist_ok=True)

# # plt.rcParams.update({
# #     "figure.facecolor": "#0e1318",
# #     "axes.facecolor":   "#0e1318",
# #     "axes.edgecolor":   "#1c2530",
# #     "axes.labelcolor":  "#c8d6e5",
# #     "axes.titlecolor":  "#ffffff",
# #     "xtick.color":      "#4a5568",
# #     "ytick.color":      "#4a5568",
# #     "grid.color":       "#1c2530",
# #     "grid.linestyle":   "--",
# #     "grid.linewidth":   0.5,
# #     "text.color":       "#c8d6e5",
# #     "font.family":      "monospace",
# # })

# # COLORS = {
# #     "infer":    "#00e5a0",  # green
# #     "edge_fog": "#378add",  # blue
# #     "fog_proc": "#f5a623",  # amber
# #     "total":    "#ff3d57",  # red
# # }

# # PLOTS = [
# #     {
# #         "key":      "infer",
# #         "x":        frames,
# #         "y":        infer_ms,
# #         "title":    "TFLite Inference Time (Edge Node)",
# #         "ylabel":   "ms",
# #         "filename": "logs/plots/01_inference_time.png",
# #         "annotate_peak": False,
# #     },
# #     {
# #         "key":      "edge_fog",
# #         "x":        frames,
# #         "y":        edge_to_fog,
# #         "title":    "Edge → Fog Latency (simulated LAN)",
# #         "ylabel":   "ms",
# #         "filename": "logs/plots/02_edge_to_fog_latency.png",
# #         "annotate_peak": False,
# #     },
# #     {
# #         "key":      "fog_proc",
# #         "x":        frames,
# #         "y":        fog_proc,
# #         "title":    "Fog Decision Engine Processing Time",
# #         "ylabel":   "ms",
# #         "filename": "logs/plots/03_fog_processing_time.png",
# #         "annotate_peak": False,
# #     },
# #     {
# #         "key":      "total",
# #         "x":        frames,
# #         "y":        total_pipe,
# #         "title":    "Total End-to-End Pipeline Latency",
# #         "ylabel":   "ms",
# #         "filename": "logs/plots/04_total_pipeline_latency.png",
# #         "annotate_peak": True,
# #     },
# # ]


# # def make_plot(x, y, color, title, ylabel, filename, annotate_peak=False):
# #     fig, ax = plt.subplots(figsize=(14, 4))
# #     fig.suptitle(
# #         f"Pipeline Latency Analysis — {title}",
# #         fontsize=12, color="#ffffff", y=1.01
# #     )

# #     # Line plot (no fill)
# #     ax.plot(x, y, color=color, linewidth=1.0, alpha=0.9)

# #     # Average line
# #     avg = np.mean(y)
# #     ax.axhline(avg, color=color, linewidth=1, linestyle="--", alpha=0.55)
# #     ax.text(
# #         x[-1], avg,
# #         f" avg: {avg:.2f}ms",
# #         color=color, fontsize=8,
# #         va="bottom", ha="right"
# #     )

# #     # Peak annotation (total pipeline only)
# #     if annotate_peak:
# #         max_idx = int(np.argmax(y))
# #         ax.annotate(
# #             f"peak: {y[max_idx]:.1f}ms",
# #             xy=(x[max_idx], y[max_idx]),
# #             xytext=(x[max_idx] + len(x) * 0.02, y[max_idx]),
# #             color=color,
# #             fontsize=8,
# #             arrowprops=dict(arrowstyle="->", color=color, lw=0.8),
# #         )

# #     ax.set_xlabel("Frame", fontsize=8)
# #     ax.set_ylabel(ylabel, fontsize=8)
# #     ax.grid(True, axis="y")
# #     ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
# #     ax.set_xlim(min(x), max(x))

# #     fig.tight_layout()
# #     fig.savefig(filename, dpi=150, bbox_inches="tight", facecolor="#0e1318")
# #     plt.close(fig)
# #     print(f"Saved: {filename}")


# # for cfg in PLOTS:
# #     make_plot(
# #         x=cfg["x"],
# #         y=cfg["y"],
# #         color=COLORS[cfg["key"]],
# #         title=cfg["title"],
# #         ylabel=cfg["ylabel"],
# #         filename=cfg["filename"],
# #         annotate_peak=cfg["annotate_peak"],
# #     )

# # print("\nAll plots saved to logs/plots/")




# import json
# import matplotlib.pyplot as plt

# # Load JSON data
# with open("logs/pipeline_metrics_refactored_with_datetime.json", "r") as f:
#     content = f.read().strip()

# try:
#     records = json.loads(content)
# except json.JSONDecodeError:
#     records = [json.loads(line) for line in content.splitlines() if line.strip()]

# # Extract values
# frames = [r["frame"] for r in records]
# infer_ms = [r["infer_ms"] for r in records]
# edge_to_fog = [r["edge_to_fog_ms"] for r in records]
# fog_proc = [r["fog_processing_ms"] for r in records]
# total_pipe = [r["total_pipeline_ms"] for r in records]


# plt.figure()
# plt.plot(frames, infer_ms)
# plt.title("Inference Time (Edge Node)")
# plt.xlabel("Frame")
# plt.ylabel("Time (ms)")
# plt.show()


# plt.figure()
# plt.plot(frames, edge_to_fog)
# plt.title("Edge to Fog Latency")
# plt.xlabel("Frame")
# plt.ylabel("Time (ms)")
# plt.show()

# plt.figure()
# plt.plot(frames, fog_proc)
# plt.title("Fog Processing Time")
# plt.xlabel("Frame")
# plt.ylabel("Time (ms)")
# plt.show()


# plt.figure()
# plt.plot(frames, total_pipe)
# plt.title("Total Pipeline Latency")
# plt.xlabel("Frame")
# plt.ylabel("Time (ms)")
# plt.show()


import json
import matplotlib.pyplot as plt
import os

# Create folder for plots
os.makedirs("logs/plots", exist_ok=True)

# Load JSON data
with open("logs/pipeline_metrics_refactored_with_datetime.json", "r") as f:
    content = f.read().strip()

try:
    records = json.loads(content)
except json.JSONDecodeError:
    records = [json.loads(line) for line in content.splitlines() if line.strip()]

# Extract values
frames = [r["frame"] for r in records]
infer_ms = [r["infer_ms"] for r in records]
edge_to_fog = [r["edge_to_fog_ms"] for r in records]
fog_proc = [r["fog_processing_ms"] for r in records]
total_pipe = [r["total_pipeline_ms"] for r in records]

def plot_graph(x, y, title, ylabel, filename):
    plt.figure()
    plt.plot(x, y, marker='o')   # line graph with markers
    plt.title(title)
    plt.xlabel("Frame")
    plt.ylabel(ylabel)
    plt.grid(True)

    plt.savefig(f"logs/plots/{filename}")
    plt.show()

# Line graphs
plot_graph(frames, infer_ms, "Inference Time (Edge Node)", "Time (ms)", "inference_time.png")
plot_graph(frames, edge_to_fog, "Edge to Fog Latency", "Time (ms)", "edge_to_fog_latency.png")
plot_graph(frames, fog_proc, "Fog Processing Time", "Time (ms)", "fog_processing_time.png")
plot_graph(frames, total_pipe, "Total Pipeline Latency", "Time (ms)", "total_pipeline_latency.png")

print("Line graphs saved in logs/plots/")