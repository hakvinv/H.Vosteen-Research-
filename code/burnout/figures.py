"""
Figures for Burnout v2 — Three Fixes (after @dz comment)
1. hook_population.pdf  — distribution of rho_i shifts right over time, crossing threshold
2. observer_split.pdf   — same job, two ratios (person vs employer)
3. b_of_t.pdf           — population fraction in burnout B(t), sigmoid
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import lognorm

plt.rcParams["font.family"] = "serif"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

# ---------------------------------------------------------------
# 1. Hook figure — population distribution shifting right over time
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5.5, 2.8))
x = np.linspace(0.01, 2.5, 400)

# Three time snapshots: t=10, t=40, t=80 weeks
# Lognormal with shifting mean
for mu, label, alpha in [(-0.6, "t = 10 wk", 0.35),
                          (-0.1, "t = 40 wk", 0.55),
                          ( 0.3, "t = 80 wk", 0.85)]:
    pdf = lognorm.pdf(x, s=0.45, scale=np.exp(mu))
    ax.plot(x, pdf, color="black", linewidth=1.4, alpha=alpha, label=label)
    ax.fill_between(x, 0, pdf, where=(x > 1.0), color="black", alpha=alpha*0.25)

ax.axvline(1.0, color="black", linestyle=":", linewidth=1.0)
ax.text(1.02, 1.55, r"threshold $\rho^*$", fontsize=8, va="top")

ax.set_xlabel(r"$\rho_i = E_{\mathrm{ovr}}/E_{\mathrm{out}}$ (per person)", fontsize=9)
ax.set_ylabel("density", fontsize=9)
ax.set_xlim(0, 2.5)
ax.set_ylim(0, 1.7)
ax.legend(frameon=False, fontsize=8, loc="upper right")
ax.tick_params(labelsize=8)
plt.tight_layout()
fig.savefig("/home/claude/burnout_v2/figures/hook_population.pdf", bbox_inches="tight")
fig.savefig("/home/claude/burnout_v2/figures/hook_population.png", bbox_inches="tight", dpi=220)
plt.close()

# ---------------------------------------------------------------
# 2. Observer split — same job, two ratios
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.2, 3.4))
categories = ["Task\nexecution", "Context\nswitching", "Decision\nfatigue",
              "Suppressing\nintrusions", "Maintaining\nfacade"]
person_view  = [25, 18, 14, 18, 25]   # person counts facade as overhead
firm_view    = [50, 18, 14, 18,  0]   # firm counts facade as output (folded into task)
# Note: person view sums to 100 with facade in overhead, firm view sums to 100 with facade as output

x = np.arange(len(categories))
w = 0.36

ax.bar(x - w/2, person_view, w, color="#3a3a3a", label="Person's accounting")
ax.bar(x + w/2, firm_view,   w, color="#bdbdbd", edgecolor="black", linewidth=0.6,
       label="Firm's accounting")

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=8)
ax.set_ylabel("% of total energy budget", fontsize=9)
ax.legend(frameon=False, fontsize=8, loc="upper right")
ax.tick_params(labelsize=8)
ax.set_ylim(0, 65)
plt.tight_layout()
fig.savefig("/home/claude/burnout_v2/figures/observer_split.pdf", bbox_inches="tight")
fig.savefig("/home/claude/burnout_v2/figures/observer_split.png", bbox_inches="tight", dpi=220)
plt.close()

# ---------------------------------------------------------------
# 3. B(t) — sigmoid population fraction in burnout
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.2, 3.4))
t = np.linspace(0, 100, 300)

# Compute B(t) = P(rho_i(t) > rho_i^*) under heterogeneous threshold
# Model: log rho_i(t) = mu0 + drift*t + eps, eps~N(0,sig)
#        log rho_i^*  = mu_star + eta,    eta~N(0,sig_star)
# B(t) = Phi( (mu0 + drift*t - mu_star) / sqrt(sig^2 + sig_star^2) )
from scipy.stats import norm
mu0, drift, mu_star = -0.7, 0.012, 0.0
sig, sig_star = 0.45, 0.30

B = norm.cdf((mu0 + drift*t - mu_star) / np.sqrt(sig**2 + sig_star**2))

ax.plot(t, B, color="black", linewidth=1.6)
ax.fill_between(t, 0, B, color="black", alpha=0.10)
ax.axhline(0.5, color="black", linestyle=":", linewidth=0.8)
ax.text(2, 0.52, r"$B = 0.5$", fontsize=8)

# annotate Gallup empirical point
ax.scatter([88], [0.67], color="black", s=28, zorder=5)
ax.annotate("Gallup 2024\n67% report\nsymptoms",
            xy=(88, 0.67), xytext=(55, 0.83),
            arrowprops=dict(arrowstyle="-", linewidth=0.6, color="black"),
            fontsize=8)

ax.set_xlabel(r"weeks of sustained role $t$", fontsize=9)
ax.set_ylabel(r"$B(t)$  population fraction in burnout", fontsize=9)
ax.set_xlim(0, 100)
ax.set_ylim(0, 1)
ax.tick_params(labelsize=8)
plt.tight_layout()
fig.savefig("/home/claude/burnout_v2/figures/b_of_t.pdf", bbox_inches="tight")
fig.savefig("/home/claude/burnout_v2/figures/b_of_t.png", bbox_inches="tight", dpi=220)
plt.close()

print("All figures written to /home/claude/burnout_v2/figures/")
