"""
Figures for D1 — Why a Bad Post Doesn't Tank Your Account
Generates: hook_fig.pdf, scaling.pdf

Usage: python figures.py
Output: ../figures/hook_fig.pdf, ../figures/scaling.pdf
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'

# === Figure 1: Bayesian posterior convergence ===
fig, ax = plt.subplots(figsize=(5.5, 2.8))

t = np.linspace(0, 200, 500)
prior = np.ones_like(t) * 1.0
posterior = 1.0 - 0.15 * (1 - np.exp(-t/30)) * (t > 0)
tau_R = 90

ax.plot(t, prior, color='#888888', lw=1.4, ls='--', label='prior P(class)')
ax.plot(t, posterior, color='black', lw=2.0, label='posterior after post')
ax.axvline(tau_R, color='firebrick', ls=':', lw=1.0, alpha=0.7)
ax.text(tau_R + 5, 1.02, r'$\tau_R \approx 90$ sec', color='firebrick', fontsize=10)

ax.fill_between(t, posterior, prior, where=(t <= tau_R), alpha=0.1, color='black')
ax.text(45, 0.93, 'inference\nin progress', fontsize=9, ha='center', style='italic', color='#444')

ax.set_xlabel('seconds after post', fontsize=10)
ax.set_ylabel('P(creator class)', fontsize=10)
ax.set_xlim(0, 200)
ax.set_ylim(0.78, 1.05)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)
ax.legend(loc='lower right', frameon=False, fontsize=9)

fig.savefig('hook_fig.pdf', bbox_inches='tight', pad_inches=0.05)
plt.close()

# === Figure 2: tau_R as function of KL and alpha ===
fig2, ax2 = plt.subplots(figsize=(6, 3.6))

KL = np.linspace(0.5, 6, 100)
for alpha, color, label in [(0.01, 'firebrick', r'$\alpha = 0.01$ (strict)'),
                             (0.05, 'steelblue', r'$\alpha = 0.05$ (typical)'),
                             (0.10, 'darkorange', r'$\alpha = 0.10$ (loose)')]:
    tau = -np.log(alpha) / KL * 60
    ax2.plot(KL, tau, color=color, lw=1.6, label=label)

ax2.axhline(90, color='#888888', ls=':', lw=0.8, alpha=0.6)
ax2.text(0.6, 95, 'TikTok ~90s', color='#666666', fontsize=8)
ax2.axhline(180, color='#888888', ls=':', lw=0.8, alpha=0.6)
ax2.text(0.6, 185, 'Reels ~3min', color='#666666', fontsize=8)

ax2.set_xlabel(r'KL divergence (bits) — how surprising the post was', fontsize=10)
ax2.set_ylabel(r'$\tau_R$ recovery time (seconds)', fontsize=10)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(alpha=0.3)
ax2.legend(loc='upper right', frameon=False, fontsize=9)
ax2.set_ylim(0, 600)

fig2.savefig('scaling.pdf', bbox_inches='tight')
plt.close()

print("done")
