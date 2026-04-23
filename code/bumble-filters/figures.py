"""
Figures for GT1 — Why Two Bumble Filters Cut Your Pool by 80 Percent
Generates: hook_fig.pdf, curse.pdf
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'

# === Figure 1: pool collapse with filter count ===
fig, ax = plt.subplots(figsize=(5.5, 3.2))

n_filters = np.arange(0, 13)
pool_70 = 100 * (0.70 ** n_filters)
pool_80 = 100 * (0.80 ** n_filters)
pool_90 = 100 * (0.90 ** n_filters)

ax.plot(n_filters, pool_70, color='firebrick', lw=2, marker='o', ms=5, label=r'$\bar{p} = 0.70$ (strict)')
ax.plot(n_filters, pool_80, color='steelblue', lw=2, marker='s', ms=5, label=r'$\bar{p} = 0.80$ (typical)')
ax.plot(n_filters, pool_90, color='darkorange', lw=2, marker='^', ms=5, label=r'$\bar{p} = 0.90$ (loose)')

ax.axhline(20, color='#888888', ls=':', lw=0.8, alpha=0.6)
ax.text(0.3, 22, '20% remaining', color='#666666', fontsize=8)
ax.axhline(5, color='#888888', ls=':', lw=0.8, alpha=0.6)
ax.text(0.3, 6.5, '5% remaining', color='#666666', fontsize=8)

ax.axvline(2, color='black', ls='--', lw=0.8, alpha=0.4)
ax.text(2.15, 90, '2 filters\n(common)', fontsize=9, va='top')

ax.set_xlabel('number of active filters', fontsize=10)
ax.set_ylabel('% of pool remaining', fontsize=10)
ax.set_xlim(0, 12)
ax.set_ylim(0, 105)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='upper right', frameon=False, fontsize=9)
ax.grid(alpha=0.3)

fig.savefig('hook_fig.pdf', bbox_inches='tight', pad_inches=0.05)
plt.close()

# === Figure 2: curse of dimensionality log scale ===
fig2, ax2 = plt.subplots(figsize=(6, 3.4))

d = np.arange(0, 21)

for criterion_strict, color, label in [
    (0.5, 'firebrick', 'each criterion: median (P=0.5)'),
    (0.7, 'steelblue', 'each criterion: P=0.7'),
    (0.85, 'darkorange', 'each criterion: P=0.85'),
]:
    surviving = criterion_strict ** d * 100
    ax2.semilogy(d, surviving, color=color, lw=2, marker='o', ms=4, label=label)

ax2.axhline(1, color='#888888', ls=':', lw=0.8)
ax2.text(0.3, 1.2, '1% of original pool', color='#666666', fontsize=8)

ax2.set_xlabel('number of independent compatibility criteria', fontsize=10)
ax2.set_ylabel('% pool surviving (log scale)', fontsize=10)
ax2.set_xlim(0, 20)
ax2.set_ylim(0.01, 200)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(loc='upper right', frameon=False, fontsize=8)
ax2.grid(alpha=0.3, which='both')

fig2.savefig('curse.pdf', bbox_inches='tight')
plt.close()
print("done")
