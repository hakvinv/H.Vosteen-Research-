"""
Paper-formatted bibliometric evidence figure.
Two-panel: time series (left) + excess growth bars (right)
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

with open("/tmp/openalex_results.json") as f:
    data = json.load(f)
years = data["years"]
laundering = data["results"]

baseline_data = {
    "economics": [126576, 137650, 151530, 171613, 187541, 220896, 234921, 257310, 354881, 348472, 377954],
    "social_science": [249523, 277251, 310051, 361401, 410476, 517039, 580692, 654263, 899173, 864841, 920011],
    "psychology": [118216, 127257, 142205, 158353, 180272, 212373, 233179, 260341, 356168, 351721, 395086],
}
baseline_growth = np.mean([b[-1]/b[0] for b in baseline_data.values()])

fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
linestyles = ["-", "--", "-.", ":", "-", "--", "-.", ":"]

# Left: time series
ax = axes[0]
for i, (label, counts) in enumerate(laundering.items()):
    normalized = [c/counts[0] for c in counts]
    nice = label.replace("_", " ")
    ax.plot(years, normalized, color="black", linewidth=1.0,
            linestyle=linestyles[i % len(linestyles)],
            marker="o", markersize=2.5, alpha=0.55,
            label=nice)

baseline_avg = np.mean([[b[i]/b[0] for i in range(len(years))]
                        for b in baseline_data.values()], axis=0)
ax.plot(years, baseline_avg, color="black", linewidth=2.5,
        marker="s", markersize=4.5,
        label="baseline (econ/soc/psych avg)", zorder=10)

ax.set_xlabel("year", fontsize=9)
ax.set_ylabel("research output (normalized to 2015)", fontsize=9)
ax.set_yscale("log")
ax.legend(fontsize=6.5, frameon=False, loc="upper left", ncol=2)
ax.tick_params(labelsize=8)
ax.axvline(2020, color="gray", linestyle=":", linewidth=0.7)
ax.grid(True, alpha=0.2, which="both")
ax.set_title("(a) growth trajectories vs baseline", fontsize=9, loc="left")

# Right: excess growth bars
ax = axes[1]
labels = list(laundering.keys())
ratios = [laundering[l][-1]/laundering[l][0] for l in labels]
excess = [r / baseline_growth for r in ratios]
sorted_pairs = sorted(zip(labels, excess), key=lambda x: x[1])
labels_sorted = [p[0].replace("_", " ") for p in sorted_pairs]
excess_sorted = [p[1] for p in sorted_pairs]

ax.barh(range(len(labels_sorted)), excess_sorted,
        color="black", alpha=0.7, edgecolor="black", linewidth=0.5)
ax.axvline(1.0, color="gray", linestyle="--", linewidth=1.0)

ax.set_yticks(range(len(labels_sorted)))
ax.set_yticklabels(labels_sorted, fontsize=7.5)
ax.set_xlabel("excess growth relative to baseline (=1)", fontsize=9)
ax.tick_params(labelsize=8)
ax.set_title("(b) excess growth ratios", fontsize=9, loc="left")
for i, v in enumerate(excess_sorted):
    ax.text(v + 0.15, i, f"{v:.1f}×", va="center", fontsize=7)

plt.tight_layout()
fig.savefig("/home/claude/platform_laundering/figures/bibliometric_evidence.pdf",
            bbox_inches="tight")
fig.savefig("/home/claude/platform_laundering/figures/bibliometric_evidence.png",
            bbox_inches="tight", dpi=220)
plt.close()

# Print stats for paper text
print("Stats for paper:")
print(f"Baseline growth: {baseline_growth:.2f}x")
print(f"Mean excess: {np.mean(excess):.2f}x")
print(f"Median excess: {np.median(excess):.2f}x")
print(f"Max (parasocial trust): {max(excess):.2f}x")
print()
print("Spearman correlations:")
for label, counts in laundering.items():
    rho, p = stats.spearmanr(years, counts)
    print(f"  {label:<45} rho={rho:.3f}  p={p:.4f}")
print()
print("Welch t-tests pre/post 2020:")
for label, counts in laundering.items():
    pre = counts[:5]
    post = counts[5:]
    t, p = stats.ttest_ind(pre, post, equal_var=False)
    print(f"  {label:<45} t={t:.2f}  p={p:.4f}")

print("Figure saved.")
