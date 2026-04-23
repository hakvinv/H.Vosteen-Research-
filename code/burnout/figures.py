"""
Figures for B1 — Burnout Is Not Too Much Work
Generates: hook_fig.pdf, budget.pdf
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'

# === Figure 1: rho_burn evolution over time ===
fig, ax = plt.subplots(figsize=(5.5, 3.2))

t = np.linspace(0, 100, 500)
output = 1 - 0.003 * t
overhead = 0.3 + 0.012 * t

rho = overhead / np.maximum(output, 0.01)

ax.plot(t, rho, color='black', lw=2.0, label=r'$\rho_{\mathrm{burn}}$')
ax.axhline(1, color='firebrick', ls=':', lw=1.0, alpha=0.7)
ax.text(2, 1.06, r'collapse threshold $\rho = 1$', color='firebrick', fontsize=9)

collapse_idx = np.argmin(np.abs(rho - 1))
collapse_t = t[collapse_idx]
ax.scatter([collapse_t], [1], s=80, color='firebrick', zorder=5)
ax.annotate('burnout onset', xy=(collapse_t, 1), xytext=(collapse_t+8, 0.55),
            fontsize=9, color='firebrick',
            arrowprops=dict(arrowstyle='->', lw=0.7, color='firebrick'))

ax.fill_between(t, 0, rho, where=(rho<1), alpha=0.15, color='steelblue', label='sustainable')
ax.fill_between(t, 0, rho, where=(rho>=1), alpha=0.15, color='firebrick', label='unsustainable')

ax.set_xlabel('weeks of sustained work', fontsize=10)
ax.set_ylabel(r'$\rho_{\mathrm{burn}}$ (overhead / output)', fontsize=10)
ax.set_xlim(0, 100)
ax.set_ylim(0, 2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='upper left', frameon=False, fontsize=8)
ax.grid(alpha=0.3)

fig.savefig('hook_fig.pdf', bbox_inches='tight', pad_inches=0.05)
plt.close()

# === Figure 2: energy budget decomposition ===
fig2, ax2 = plt.subplots(figsize=(6, 3.4))

categories = ['Task\nexecution', 'Context\nswitching', 'Decision\nfatigue', 'Suppressing\nintrusions', 'Maintaining\nfacade']
healthy = [60, 12, 8, 12, 8]
burnout = [25, 22, 18, 17, 18]

x = np.arange(len(categories))
width = 0.35

ax2.bar(x - width/2, healthy, width, color='steelblue', edgecolor='black', linewidth=0.5, label='sustainable')
ax2.bar(x + width/2, burnout, width, color='firebrick', edgecolor='black', linewidth=0.5, label='approaching burnout')

ax2.set_xticks(x)
ax2.set_xticklabels(categories, fontsize=9)
ax2.set_ylabel('% of total energy budget', fontsize=10)
ax2.set_ylim(0, 70)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(loc='upper right', frameon=False, fontsize=9)
ax2.grid(alpha=0.3, axis='y')

fig2.savefig('budget.pdf', bbox_inches='tight')
plt.close()
print("done")
