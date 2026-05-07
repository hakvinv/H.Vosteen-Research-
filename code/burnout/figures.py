"""
Figures for Burnout v3 — Honeymoon Decay
1. hook_decay.pdf       — m(t) decay drives rho(t) rise even at constant alpha,beta
2. phase_progression.pdf — three phases of new-job lifecycle
3. mechanism_stack.pdf  — v1 + v2 + v3 contributions to drho/dt
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

# ---------------------------------------------------------------
# 1. Hook: same person, same overhead, three different m_inf values
# ---------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.8))
t = np.linspace(0, 24, 300)  # months
tau_m = 4.5  # decay constant in months

# Three matches: poor (m_inf=0.4), mid (m_inf=0.6), strong (m_inf=0.85)
configs = [(0.40, "poor match",   ":"),
           (0.60, "mid match",    "--"),
           (0.85, "strong match", "-")]

# Left: m(t)
for m_inf, label, ls in configs:
    m = m_inf + (1 - m_inf) * np.exp(-t/tau_m)
    ax1.plot(t, m, color="black", linewidth=1.4, linestyle=ls,
             label=f"$m_\\infty$={m_inf}, {label}")

ax1.set_xlabel("months in role $t$", fontsize=9)
ax1.set_ylabel(r"$m(t)$  hedonic multiplier", fontsize=9)
ax1.set_xlim(0, 24)
ax1.set_ylim(0, 1.05)
ax1.legend(frameon=False, fontsize=7.5, loc="upper right")
ax1.tick_params(labelsize=8)

# Right: rho(t) for fixed rho_0=0.6 (sustainable at start), threshold rho*=1
rho_0 = 0.6
rho_star = 1.0
for m_inf, label, ls in configs:
    m = m_inf + (1 - m_inf) * np.exp(-t/tau_m)
    rho = rho_0 / m
    ax2.plot(t, rho, color="black", linewidth=1.4, linestyle=ls,
             label=f"$m_\\infty$={m_inf}")

ax2.axhline(rho_star, color="black", linestyle=":", linewidth=0.8)
ax2.text(0.5, 1.03, r"threshold $\rho^*$", fontsize=8)

ax2.set_xlabel("months in role $t$", fontsize=9)
ax2.set_ylabel(r"$\rho^P(t) = \rho_0/m(t)$", fontsize=9)
ax2.set_xlim(0, 24)
ax2.set_ylim(0.5, 1.7)
ax2.tick_params(labelsize=8)

plt.tight_layout()
fig.savefig("/home/claude/burnout_v3/figures/hook_decay.pdf", bbox_inches="tight")
fig.savefig("/home/claude/burnout_v3/figures/hook_decay.png", bbox_inches="tight", dpi=220)
plt.close()

# ---------------------------------------------------------------
# 2. Phase progression: three-phase lifecycle
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.2, 2.8))
t = np.linspace(0, 24, 300)
tau_m = 4.5
m_inf = 0.5
m = m_inf + (1 - m_inf) * np.exp(-t/tau_m)
rho = 0.6 / m

# Shade phases
ax.axvspan(0, tau_m, alpha=0.10, color="black", linewidth=0)
ax.axvspan(tau_m, 3*tau_m, alpha=0.20, color="black", linewidth=0)
ax.axvspan(3*tau_m, 24, alpha=0.30, color="black", linewidth=0)

ax.plot(t, rho, color="black", linewidth=1.6)
ax.axhline(1.0, color="black", linestyle=":", linewidth=0.8)

# Phase labels
ax.text(tau_m/2, 1.55, "Honeymoon", ha="center", fontsize=8, style="italic")
ax.text(2*tau_m, 1.55, "Disillusionment", ha="center", fontsize=8, style="italic")
ax.text(4.5*tau_m, 1.55, "Steady state", ha="center", fontsize=8, style="italic")

ax.text(0.3, 1.02, r"$\rho^*$", fontsize=9)

ax.set_xlabel("months in role $t$", fontsize=9)
ax.set_ylabel(r"$\rho^P(t)$", fontsize=9)
ax.set_xlim(0, 24)
ax.set_ylim(0.5, 1.7)
ax.tick_params(labelsize=8)

plt.tight_layout()
fig.savefig("/home/claude/burnout_v3/figures/phase_progression.pdf", bbox_inches="tight")
fig.savefig("/home/claude/burnout_v3/figures/phase_progression.png", bbox_inches="tight", dpi=220)
plt.close()

# ---------------------------------------------------------------
# 3. Mechanism stack: how v1, v2, v3 each push rho up
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.2, 3.0))
t = np.linspace(0, 24, 300)

# v1: nothing changes (just threshold visible) - constant baseline
v1 = np.full_like(t, 0.6)

# v2: environmental drift (slow linear in log space)
v2_drift = 0.6 * np.exp(0.025 * t)  # ~30% rise over 24 months

# v3: hedonic decay
m = 0.5 + 0.5 * np.exp(-t/4.5)
v3_hedonic = 0.6 / m

# Combined: both mechanisms together
combined = v2_drift / m  # both effects multiplicative

ax.plot(t, v1,         color="black", linewidth=1.0, linestyle=":",  label="v1 (static, no time term)")
ax.plot(t, v2_drift,   color="black", linewidth=1.2, linestyle="--", label="v2 only (env drift, $m=1$)")
ax.plot(t, v3_hedonic, color="black", linewidth=1.2, linestyle="-.", label="v3 only (hedonic decay, $\\alpha=0$)")
ax.plot(t, combined,   color="black", linewidth=1.8, linestyle="-",  label="v2 + v3 combined")

ax.axhline(1.0, color="black", linestyle=":", linewidth=0.6, alpha=0.5)
ax.text(0.3, 1.02, r"$\rho^*$", fontsize=9)

ax.set_xlabel("months in role $t$", fontsize=9)
ax.set_ylabel(r"$\rho^P(t)$", fontsize=9)
ax.set_xlim(0, 24)
ax.set_ylim(0.5, 2.6)
ax.legend(frameon=False, fontsize=8, loc="upper left")
ax.tick_params(labelsize=8)

plt.tight_layout()
fig.savefig("/home/claude/burnout_v3/figures/mechanism_stack.pdf", bbox_inches="tight")
fig.savefig("/home/claude/burnout_v3/figures/mechanism_stack.png", bbox_inches="tight", dpi=220)
plt.close()

print("All v3 figures written.")
