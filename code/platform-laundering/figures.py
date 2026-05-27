"""
Figures for Platform Information Laundering paper.
1. observer_classes.pdf — three observer types and the laundering bridge
2. laundering_pipeline.pdf — five-step pipeline
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"

# ---------------------------------------------------------------
# 1. Three observer classes — vertical layout, no overlap
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9, 6))

def box(x, y, w, h, text, fontsize=9, style="solid", facecolor="white"):
    rect = patches.Rectangle((x, y), w, h, facecolor=facecolor, edgecolor="black",
                              linewidth=1.0, linestyle=style)
    ax.add_patch(rect)
    ax.text(x + w/2, y + h/2, text, ha="center", va="center", fontsize=fontsize)

# Top: L-type producing signal
box(3.0, 9.5, 3.0, 0.9, "L-type produces platform signal $s$\n(near-zero marginal cost)", fontsize=8.5)

# Arrow down to Class B
ax.annotate("", xy=(4.5, 8.5), xytext=(4.5, 9.5),
            arrowprops=dict(arrowstyle="->", linewidth=1.0, color="black"))

# Three classes side by side
# Class A
box(0.2, 6.5, 2.8, 2.0,
    "Class A\nProfessional observer\n(VC, bank, recruiter)\n\nhigh processing capacity\nstrong incentives",
    fontsize=8)

# Class B
box(3.4, 6.5, 2.8, 2.0,
    "Class B\nRetail observer\n(platform user)\n\nlow processing capacity\nweak incentives",
    fontsize=8)

# Class C
box(6.6, 6.5, 2.8, 2.0,
    "Class C\nAggregated metric\n(likes, followers)\n\nproduced by B\nread by A as if A",
    fontsize=8, style="dashed")

# Arrow from B to C
ax.annotate("", xy=(6.6, 7.5), xytext=(6.2, 7.5),
            arrowprops=dict(arrowstyle="->", linewidth=1.0, color="black"))
ax.text(6.4, 7.85, "aggregation", ha="center", fontsize=7.5, style="italic")

# Arrow from C down and around to A — the laundering loop
ax.annotate("", xy=(8.0, 5.8), xytext=(8.0, 6.5),
            arrowprops=dict(arrowstyle="-", linewidth=1.0, color="black"))
ax.annotate("", xy=(1.6, 5.8), xytext=(8.0, 5.8),
            arrowprops=dict(arrowstyle="-", linewidth=1.0, color="black"))
ax.annotate("", xy=(1.6, 6.5), xytext=(1.6, 5.8),
            arrowprops=dict(arrowstyle="->", linewidth=1.0, color="black"))
ax.text(4.8, 5.55, "A reads C as substance proxy", ha="center", fontsize=8, style="italic")

# Decision and outcome below A
ax.annotate("", xy=(1.6, 3.7), xytext=(1.6, 6.5),
            arrowprops=dict(arrowstyle="->", linewidth=1.0, color="black"))
box(0.2, 2.8, 2.8, 0.9, "A makes decision\nbased on C", fontsize=8)
ax.annotate("", xy=(1.6, 2.0), xytext=(1.6, 2.8),
            arrowprops=dict(arrowstyle="->", linewidth=1.0, color="black"))
box(0.2, 1.1, 2.8, 0.9, "L-type extracts\nresources from A", fontsize=8, style="dashed")

# Title
ax.text(4.8, 11.0, "The three observer classes and the laundering bridge",
        ha="center", fontsize=11, style="italic")

ax.set_xlim(-0.3, 10)
ax.set_ylim(0.5, 11.5)
ax.set_aspect("equal")
for s in ["top", "bottom", "left", "right"]:
    ax.spines[s].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
fig.savefig("/home/claude/platform_laundering/figures/observer_classes.pdf", bbox_inches="tight")
fig.savefig("/home/claude/platform_laundering/figures/observer_classes.png", bbox_inches="tight", dpi=220)
plt.close()

# ---------------------------------------------------------------
# 2. Laundering pipeline
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11, 3.3))

stages = [
    ("Step 1\nSignal\nproduction",     "L-type\nposts content\n(zero substance)"),
    ("Step 2\nImpulse\nreaction",      "Users click like\n(no verification)"),
    ("Step 3\nAggregation",            "Platform sums\nimpulses to $M$"),
    ("Step 4\nMisreading",             "A reads $M$\nas substance"),
    ("Step 5\nResource\nextraction",   "L-type funded\nbased on $M$"),
]

x_positions = [0.3, 2.5, 4.7, 6.9, 9.1]
y_box = 0.4

for (label, descr), x in zip(stages, x_positions):
    rect = patches.FancyBboxPatch((x, y_box), 1.8, 1.6,
                                    boxstyle="round,pad=0.05",
                                    facecolor="white", edgecolor="black", linewidth=1.0)
    ax.add_patch(rect)
    ax.text(x + 0.9, y_box + 1.25, label, ha="center", va="center", fontsize=8, fontweight="bold")
    ax.text(x + 0.9, y_box + 0.55, descr, ha="center", va="center", fontsize=7)

for i in range(len(x_positions) - 1):
    x1 = x_positions[i] + 1.8
    x2 = x_positions[i+1]
    ax.annotate("", xy=(x2, y_box + 0.8), xytext=(x1, y_box + 0.8),
                arrowprops=dict(arrowstyle="->", linewidth=0.9, color="black"))

ax.text(5.5, 2.7, "Information laundering: cheap impulse $\\rightarrow$ expensive validation metric",
        ha="center", fontsize=10, style="italic")

ax.set_xlim(-0.2, 11.2)
ax.set_ylim(0, 3.2)
ax.set_aspect("equal")
for s in ["top", "bottom", "left", "right"]:
    ax.spines[s].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
fig.savefig("/home/claude/platform_laundering/figures/laundering_pipeline.pdf", bbox_inches="tight")
fig.savefig("/home/claude/platform_laundering/figures/laundering_pipeline.png", bbox_inches="tight", dpi=220)
plt.close()

print("Two figures written.")
