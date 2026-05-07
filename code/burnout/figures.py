"""
Figures for Burnout v4 — How to Mathematical Ragequit Your Job
1. mvt_crossing.pdf       — u(t) and A(t*) crossing at optimal t*
2. the_gap.pdf            — gap between threshold crossing and rational quit
3. comparative_statics.pdf — t* as function of switch cost c_s
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumulative_trapezoid

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

# Shared parameters
w, rho_0, m_inf, tau_m = 1.0, 0.6, 0.5, 5.0
alpha = 0.04
lam = 0.7   # so u(t) = 0 when rho = w/lam = 1.43, well above rho* = 1
rho_star = 1.0

# ---------------------------------------------------------------
# 1. MVT crossing
# ---------------------------------------------------------------
c_s, s = 3.0, 2.0
t = np.linspace(0.01, 30, 1000)
m = m_inf + (1 - m_inf) * np.exp(-t/tau_m)
rho = (rho_0 / m) * np.exp(alpha*t)
u = w - lam * rho
U = cumulative_trapezoid(u, t, initial=0)
A = (U - c_s) / (t + s)

idx = np.argmax(A)
t_star = t[idx]
u_star = u[idx]

fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.plot(t, u, color="black", linewidth=1.6, label=r"$u(t)$  current flow utility")
ax.plot(t, A, color="black", linewidth=1.6, linestyle="--", label=r"$A(t^*)$  long-run average")

ax.axvline(t_star, color="black", linestyle=":", linewidth=0.8)
ax.scatter([t_star], [u_star], color="black", s=30, zorder=5)
ax.annotate(f"$t^* = {t_star:.1f}$ months\n$u(t^*) = A(t^*)$",
            xy=(t_star, u_star),
            xytext=(t_star+1.5, u_star+0.35),
            fontsize=8.5,
            arrowprops=dict(arrowstyle="-", linewidth=0.6))

ax.axhline(0, color="black", linewidth=0.4, alpha=0.4)
ax.set_xlabel("months in role $t$", fontsize=9)
ax.set_ylabel("utility flow", fontsize=9)
ax.set_xlim(0, 25)
ax.set_ylim(-1.0, 0.6)
ax.legend(frameon=False, fontsize=8.5, loc="upper right")
ax.tick_params(labelsize=8)
plt.tight_layout()
fig.savefig("/home/claude/burnout_v4/figures/mvt_crossing.pdf", bbox_inches="tight")
fig.savefig("/home/claude/burnout_v4/figures/mvt_crossing.png", bbox_inches="tight", dpi=220)
plt.close()
print(f"Fig 1: t* = {t_star:.2f} mo, rho(t*) = {rho[idx]:.3f}")

# ---------------------------------------------------------------
# 2. The Gap — three milestones on the u(t) curve
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.2, 3.4))
ax.plot(t, u, color="black", linewidth=1.6)
ax.axhline(0, color="black", linewidth=0.4, alpha=0.4)

# Milestone 1: rho crosses rho* (= 1.0)
idx_thr = np.argmin(np.abs(rho - rho_star))
t_thr = t[idx_thr]
u_thr = u[idx_thr]

# Milestone 2: u crosses 0 ("I hate my job")
idx_u0 = np.where(u < 0)[0]
if len(idx_u0) > 0:
    t_hate = t[idx_u0[0]]
    u_hate = 0.0

# Milestone 3: optimal quit (t_star from above)

for tt, uu, label, dx, dy in [
    (t_thr,  u_thr,  f"threshold crossing\n$\\rho = \\rho^* = 1$\n$t = {t_thr:.1f}$ mo",  -1.5, -0.35),
    (t_hate, u_hate, f"\"I hate this\"\n$u = 0$\n$t = {t_hate:.1f}$ mo",                  -2.5,  0.30),
    (t_star, u_star, f"rational quit\n$u(t^*) = A(t^*)$\n$t^* = {t_star:.1f}$ mo",         2.5, -0.30),
]:
    ax.scatter([tt], [uu], color="black", s=30, zorder=5)
    ax.annotate(label, xy=(tt, uu), xytext=(tt+dx, uu+dy),
                fontsize=8, ha="center",
                arrowprops=dict(arrowstyle="-", linewidth=0.5))

# Shade the gaps
ax.axvspan(t_thr, t_hate, alpha=0.10, color="black", linewidth=0)
ax.axvspan(t_hate, t_star, alpha=0.20, color="black", linewidth=0)

ax.set_xlabel("months in role $t$", fontsize=9)
ax.set_ylabel(r"$u(t)$  flow utility", fontsize=9)
ax.set_xlim(0, 15)
ax.set_ylim(-1.0, 0.5)
ax.tick_params(labelsize=8)
plt.tight_layout()
fig.savefig("/home/claude/burnout_v4/figures/the_gap.pdf", bbox_inches="tight")
fig.savefig("/home/claude/burnout_v4/figures/the_gap.png", bbox_inches="tight", dpi=220)
plt.close()
print(f"Fig 2: t_thr={t_thr:.1f}, t_hate={t_hate:.1f}, t_star={t_star:.1f}")

# ---------------------------------------------------------------
# 3. Comparative statics — t* as function of c_s (and overlay m_inf, alpha sweeps)
# ---------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.0))

# Left: t* vs c_s, three curves for different m_inf
c_s_grid = np.linspace(0.5, 12, 50)
for m_inf_val, ls, label in [(0.4, ":", "$m_\\infty=0.4$ (poor)"),
                              (0.5, "--","$m_\\infty=0.5$ (mid)"),
                              (0.7, "-", "$m_\\infty=0.7$ (good)")]:
    t_star_arr = []
    for cs in c_s_grid:
        m_loc = m_inf_val + (1 - m_inf_val) * np.exp(-t/tau_m)
        rho_loc = (rho_0 / m_loc) * np.exp(alpha*t)
        u_loc = w - lam * rho_loc
        U_loc = cumulative_trapezoid(u_loc, t, initial=0)
        A_loc = (U_loc - cs) / (t + s)
        # check if A keeps rising at the boundary — then t* = infinity
        if A_loc[-1] > A_loc[len(A_loc)//2]:
            t_star_arr.append(np.nan)
        else:
            t_star_arr.append(t[np.argmax(A_loc)])
    ax1.plot(c_s_grid, t_star_arr, color="black", linewidth=1.4, linestyle=ls, label=label)

ax1.set_xlabel(r"switch cost $c_s$  (months of wage)", fontsize=9)
ax1.set_ylabel(r"optimal quit $t^*$  (months)", fontsize=9)
ax1.legend(frameon=False, fontsize=7.5, loc="upper left")
ax1.set_xlim(0, 12)
ax1.set_ylim(0, 30)
ax1.tick_params(labelsize=8)

# Right: t* vs alpha (env drift rate), three curves for different m_inf
alpha_grid = np.linspace(0.001, 0.10, 50)
c_s_fixed = 3.0
for m_inf_val, ls, label in [(0.4, ":", "$m_\\infty=0.4$"),
                              (0.5, "--","$m_\\infty=0.5$"),
                              (0.7, "-", "$m_\\infty=0.7$")]:
    t_star_arr = []
    for a in alpha_grid:
        m_loc = m_inf_val + (1 - m_inf_val) * np.exp(-t/tau_m)
        rho_loc = (rho_0 / m_loc) * np.exp(a*t)
        u_loc = w - lam * rho_loc
        U_loc = cumulative_trapezoid(u_loc, t, initial=0)
        A_loc = (U_loc - c_s_fixed) / (t + s)
        if A_loc[-1] > A_loc[len(A_loc)//2]:
            t_star_arr.append(np.nan)
        else:
            t_star_arr.append(t[np.argmax(A_loc)])
    ax2.plot(alpha_grid, t_star_arr, color="black", linewidth=1.4, linestyle=ls, label=label)

ax2.set_xlabel(r"env drift rate $\alpha$  (1/month)", fontsize=9)
ax2.set_ylabel(r"optimal quit $t^*$  (months)", fontsize=9)
ax2.legend(frameon=False, fontsize=7.5, loc="upper right")
ax2.set_xlim(0, 0.10)
ax2.set_ylim(0, 30)
ax2.tick_params(labelsize=8)

plt.tight_layout()
fig.savefig("/home/claude/burnout_v4/figures/comparative_statics.pdf", bbox_inches="tight")
fig.savefig("/home/claude/burnout_v4/figures/comparative_statics.png", bbox_inches="tight", dpi=220)
plt.close()

print("All v4 figures written.")
