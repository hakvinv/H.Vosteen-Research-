"""
Figures for B3 — ADHD Is Not a Deficit
Generates: hook_fig.pdf, bimodal.pdf
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'

# === Figure 1: phase space with two attractors ===
fig, ax = plt.subplots(figsize=(5.5, 3.6))

T_grid, R_grid = np.meshgrid(np.linspace(0, 6, 100), np.linspace(0, 6, 100))
nt_basin = np.exp(-((T_grid - 3)**2 + (R_grid - 3)**2) / 2)
adhd_basin = 0.85 * np.exp(-((T_grid - 4.8)**2 + (R_grid - 4.5)**2) / 1.5)
landscape = -(nt_basin + adhd_basin)

ax.contour(T_grid, R_grid, landscape, levels=8, colors='gray', linewidths=0.5, alpha=0.5)

ax.scatter([3], [3], s=200, c='black', marker='*', zorder=5, label='neurotypical attractor')
ax.scatter([4.8], [4.5], s=200, c='firebrick', marker='*', zorder=5, label='ADHD attractor')

ax.annotate('', xy=(3.6, 3.5), xytext=(4.6, 4.3),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='steelblue'))
ax.text(4.0, 4.1, 'stimulants\n(R↓ > T↑)', fontsize=9, color='steelblue', ha='center', style='italic')

T_line = np.linspace(0, 6, 100)
ax.plot(T_line, T_line - 2, 'k--', lw=0.8, alpha=0.5)
ax.text(5.3, 3.0, r'$\Phi = T - R = 2$', fontsize=8, rotation=45, color='#666')

ax.set_xlabel(r'$T$ (transformation rate)', fontsize=10)
ax.set_ylabel(r'$R$ (filter friction)', fontsize=10)
ax.set_xlim(0, 6)
ax.set_ylim(0, 6)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='lower right', frameon=False, fontsize=8)
ax.grid(alpha=0.3)

fig.savefig('hook_fig.pdf', bbox_inches='tight', pad_inches=0.05)
plt.close()

# === Figure 2: bimodal distribution of Phi ===
fig2, ax2 = plt.subplots(figsize=(6, 3.2))

np.random.seed(7)
nt_samples = np.random.normal(0, 0.8, 700)
adhd_samples = np.random.normal(2.5, 0.7, 300)
all_samples = np.concatenate([nt_samples, adhd_samples])

ax2.hist(all_samples, bins=50, density=True, alpha=0.5, color='steelblue', edgecolor='black', linewidth=0.5)
ax2.axvline(2, color='firebrick', ls=':', lw=1.0, alpha=0.7)
ax2.text(2.05, 0.42, r'$\Phi = 2$ threshold', color='firebrick', fontsize=9)

ax2.text(0, 0.48, 'NT\nattractor', ha='center', fontsize=10, style='italic')
ax2.text(2.5, 0.30, 'ADHD\nattractor', ha='center', fontsize=10, style='italic', color='firebrick')

ax2.set_xlabel(r'$\Phi = T - R$', fontsize=10)
ax2.set_ylabel('density (population, illustrative)', fontsize=10)
ax2.set_xlim(-3, 5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(alpha=0.3)

fig2.savefig('bimodal.pdf', bbox_inches='tight')
plt.close()
print("done")
