"""
Figures for LARP paper v2 with Cognitive Hierarchy framework.
1. cognitive_hierarchy.pdf — U-shaped vulnerability curve
2. cost_regimes.pdf — substance vs volume signaling cost
3. convergence_decay.pdf — T_L vs sigma_obs with Theranos/FTX
4. larp_taxonomy.pdf — four LARP modes mapped against k-level
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

# ---------------------------------------------------------------
# 1. U-shaped vulnerability vs observer k-level
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.5, 4.0))
k = np.linspace(0, 5, 500)
v_left = 0.85 * np.exp(-(k**1.3) / 1.4)
v_right = 0.55 * np.maximum(0, (k - 2.3)) ** 1.5 / 6
vulnerability = v_left + v_right

ax.plot(k, vulnerability, color="black", linewidth=2.0)
ax.fill_between(k, 0, vulnerability, color="black", alpha=0.08)

regimes = [
    (0.3, "Substance\nmimicry\n(Holmes)"),
    (1.8, "Most defended\nzone"),
    (4.0, "Madman\nstrategy\n(SBF)"),
]
for x, label in regimes:
    y_val = 0.85 * np.exp(-(x**1.3) / 1.4) + 0.55 * max(0, (x - 2.3))**1.5 / 6
    ax.scatter([x], [y_val], color="black", s=40, zorder=5)
    ax.annotate(label, xy=(x, y_val), xytext=(x, y_val + 0.08),
                ha="center", fontsize=8, style="italic")

ax.set_xlabel(r"observer level of reasoning $k$", fontsize=10)
ax.set_ylabel("LARP success probability", fontsize=10)
ax.set_title("U-shaped market vulnerability to LARP", fontsize=10)
ax.set_xlim(0, 5)
ax.set_ylim(0, 1.0)
ax.tick_params(labelsize=8)
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels([r"$0$ (naive)", r"$1$", r"$2$", r"$3$", r"$4$", r"$5$ (pros)"])

plt.tight_layout()
fig.savefig("figures/cognitive_hierarchy.pdf", bbox_inches="tight")
fig.savefig("figures/cognitive_hierarchy.png", bbox_inches="tight", dpi=220)
plt.close()

# ---------------------------------------------------------------
# 2. Cost regimes
# ---------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(8.5, 3.4))
y = np.linspace(0, 10, 200)

ax = axes[0]
c_H_sub = 0.3 * y**1.2
c_L_sub = 0.8 * y**1.3
ax.plot(y, c_H_sub, color="black", linewidth=1.6, label=r"$c_H(y)$  H-type")
ax.plot(y, c_L_sub, color="black", linewidth=1.6, linestyle="--", label=r"$c_L(y)$  L-type")
ax.set_xlabel(r"signal output $y$", fontsize=9)
ax.set_ylabel("cost", fontsize=9)
ax.set_title("Substance-driven signals\n(classical Spence)", fontsize=10)
ax.legend(frameon=False, fontsize=8)
ax.tick_params(labelsize=8)
ax.set_ylim(0, 25)

ax = axes[1]
c_H_vol = 1.0 * y**1.5
c_L_vol = 0.3 * y**1.2
ax.plot(y, c_H_vol, color="black", linewidth=1.6, label=r"$c_H(y)$  H-type")
ax.plot(y, c_L_vol, color="black", linewidth=1.6, linestyle="--", label=r"$c_L(y)$  L-type")
ax.set_xlabel(r"signal volume $y$", fontsize=9)
ax.set_ylabel("cost", fontsize=9)
ax.set_title("Volume-driven signals\n(inverted Spence)", fontsize=10)
ax.legend(frameon=False, fontsize=8)
ax.tick_params(labelsize=8)
ax.set_ylim(0, 35)

plt.tight_layout()
fig.savefig("figures/cost_regimes.pdf", bbox_inches="tight")
fig.savefig("figures/cost_regimes.png", bbox_inches="tight", dpi=220)
plt.close()

# ---------------------------------------------------------------
# 3. Convergence decay
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.0, 3.5))
sigma = np.linspace(0.01, 3.0, 200)
T_L = 1.0 + 12 * sigma**1.8
ax.plot(sigma, T_L, color="black", linewidth=1.8)

empirics = [
    (0.15, "open source\n(github)"),
    (0.5, "public markets\n(audited)"),
    (1.2, "crypto\n(FTX, 3yr)"),
    (1.8, "healthtech\n(Theranos, 15yr)"),
    (2.5, "defense\n(opaque)"),
]
for x, label in empirics:
    y_curve = 1.0 + 12 * x**1.8
    ax.scatter([x], [y_curve], color="black", s=30, zorder=5)
    ax.annotate(label, xy=(x, y_curve), xytext=(x+0.05, y_curve+5),
                fontsize=8, style="italic")

ax.set_xlabel(r"observation noise $\sigma_{\mathrm{obs}}$", fontsize=10)
ax.set_ylabel(r"survival time $T_L$ (years)", fontsize=10)
ax.set_title(r"L-type survival time as function of market opacity", fontsize=10)
ax.tick_params(labelsize=8)
ax.set_xlim(0, 3.0)
ax.set_ylim(0, 75)

plt.tight_layout()
fig.savefig("figures/convergence_decay.pdf", bbox_inches="tight")
fig.savefig("figures/convergence_decay.png", bbox_inches="tight", dpi=220)
plt.close()

# ---------------------------------------------------------------
# 4. LARP taxonomy
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.5, 4.0))

modes = [
    ("Mimicry-LARP",  0.5, 3,  "Holmes\n(BioTech)"),
    ("Volume-LARP",   1.5, 2,  "LinkedIn-founders"),
    ("Status-LARP",   2.0, 1,  "high-status board\n(Theranos)"),
    ("Inversion-LARP",3.5, 0,  "SBF / FTX"),
]

ax.axvspan(0, 1.0, color="black", alpha=0.05)
ax.axvspan(3.0, 5.0, color="black", alpha=0.05)
ax.text(0.5, 3.8, "naive observers", ha="center", fontsize=8, style="italic")
ax.text(4.0, 3.8, "sophisticated observers", ha="center", fontsize=8, style="italic")
ax.text(2.0, 3.8, "best-defended zone", ha="center", fontsize=8, style="italic")

for name, x, y, example in modes:
    rect = patches.FancyBboxPatch((x - 0.6, y - 0.3), 1.2, 0.6,
                                    boxstyle="round,pad=0.05",
                                    facecolor="white", edgecolor="black", linewidth=1.0)
    ax.add_patch(rect)
    ax.text(x, y + 0.05, name, ha="center", va="center", fontsize=9, fontweight="bold")
    ax.text(x, y - 0.15, example, ha="center", va="center", fontsize=7, style="italic")

ax.set_xlim(0, 5)
ax.set_ylim(-0.5, 4.2)
ax.set_xlabel(r"observer level of reasoning $k$", fontsize=10)
ax.set_yticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_xticklabels([r"$0$", r"$1$", r"$2$", r"$3$", r"$4$", r"$5$"])
ax.tick_params(labelsize=8)
ax.set_title("Four LARP modes by required observer reasoning level", fontsize=10)

plt.tight_layout()
fig.savefig("figures/larp_taxonomy.pdf", bbox_inches="tight")
fig.savefig("figures/larp_taxonomy.png", bbox_inches="tight", dpi=220)
plt.close()

print("Four figures written.")
