"""
Figures for GT2 — Ghosting Isn't Cowardice. It's Math.
Generates: hook_fig.pdf, sigma_evolution.pdf
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'

# === Figure 1: equilibrium switch as sigma_R crosses 1 ===
fig, ax = plt.subplots(figsize=(5.5, 2.8))

sigma = np.linspace(0, 4, 200)
ghost_prob = 1 / (1 + np.exp(8*(sigma - 1)))

ax.plot(sigma, ghost_prob, color='black', lw=2.0)
ax.axvline(1, color='firebrick', ls=':', lw=1.0, alpha=0.7)
ax.text(1.05, 0.5, r'equilibrium switch', color='firebrick', fontsize=10, va='center')

ax.fill_between(sigma, ghost_prob, 1, where=(sigma <= 1), alpha=0.1, color='black')
ax.fill_between(sigma, 0, ghost_prob, where=(sigma >= 1), alpha=0.1, color='black')

ax.text(0.4, 0.55, 'ghosting\ndominant', ha='center', fontsize=10, style='italic')
ax.text(2.5, 0.45, 'honest goodbye\ndominant', ha='center', fontsize=10, style='italic')

ax.scatter([0.05], [0.97], s=60, c='black', marker='v', zorder=5)
ax.annotate('Tinder 2026', xy=(0.05, 0.97), xytext=(0.4, 1.08),
            fontsize=9, ha='left',
            arrowprops=dict(arrowstyle='-', lw=0.7, color='#888'))
ax.scatter([3.0], [0.04], s=60, c='black', marker='^', zorder=5)
ax.annotate('Pre-2010', xy=(3.0, 0.04), xytext=(2.6, -0.08),
            fontsize=9, ha='left')

ax.set_xlabel(r'$\sigma_R = c_{\text{silence}} / c_{\text{response}}$', fontsize=10)
ax.set_ylabel('P(ghosting)', fontsize=10)
ax.set_xlim(0, 4)
ax.set_ylim(-0.18, 1.20)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

fig.savefig('hook_fig.pdf', bbox_inches='tight', pad_inches=0.05)
plt.close()

# === Figure 2: sigma evolution over time ===
fig2, ax2 = plt.subplots(figsize=(6, 3.6))

years = np.array([1990, 2000, 2010, 2015, 2020, 2025])
sigma_vals = np.array([3.5, 3.0, 1.8, 0.5, 0.2, 0.1])

ax2.plot(years, sigma_vals, color='steelblue', lw=2.0, marker='o', markersize=7)
ax2.axhline(1, color='firebrick', ls=':', lw=1.0, alpha=0.7)
ax2.text(1992, 1.1, 'equilibrium threshold σ_R = 1', color='firebrick', fontsize=9)

ax2.annotate('Match.com\nlaunch', xy=(2000, 3.0), xytext=(1996, 3.6),
             fontsize=8, color='#444', arrowprops=dict(arrowstyle='->', lw=0.7, color='#888'))
ax2.annotate('Tinder\nlaunch', xy=(2012, 1.4), xytext=(2008, 0.6),
             fontsize=8, color='#444', arrowprops=dict(arrowstyle='->', lw=0.7, color='#888'))

ax2.set_xlabel('year', fontsize=10)
ax2.set_ylabel(r'$\sigma_R$ (estimated, illustrative)', fontsize=10)
ax2.set_xlim(1988, 2027)
ax2.set_ylim(0, 4)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(alpha=0.3)

fig2.savefig('sigma_evolution.pdf', bbox_inches='tight')
plt.close()
print("done")
