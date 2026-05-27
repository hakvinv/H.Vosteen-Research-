"""
Figures for C3 — Why One Methyl Group Makes a Drug 1000x Stronger
Generates: hook_fig.pdf, bridge.pdf
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'

# === Figure 1: ΔΔG distribution showing magic methyl sites ===
fig, ax = plt.subplots(figsize=(5.5, 3.2))

np.random.seed(11)
ddg = np.concatenate([
    np.random.normal(0, 0.3, 70),
    np.array([2.8, -2.5, 3.5, -3.0, -4.1, 3.9, -2.7, 2.2, -3.6, 4.2])
])
np.random.shuffle(ddg)

colors = ['#888888' if abs(d) < 1.5 else 'firebrick' for d in ddg]
positions = np.arange(len(ddg))

ax.bar(positions, ddg, color=colors, width=0.8, edgecolor='none')
ax.axhline(0, color='black', lw=0.5)
ax.axhline(2, color='firebrick', ls=':', lw=0.8, alpha=0.6)
ax.axhline(-2, color='firebrick', ls=':', lw=0.8, alpha=0.6)
ax.text(82, 2.2, 'magic\nsite', color='firebrick', fontsize=8, ha='left')

ax.set_xlabel('atom position in molecule', fontsize=10)
ax.set_ylabel(r'$\Delta\Delta G_{\text{binding}}$ from CH$_3$ substitution (kcal/mol)', fontsize=9)
ax.set_xlim(-1, 82)
ax.set_ylim(-5, 5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3, axis='y')

fig.savefig('hook_fig.pdf', bbox_inches='tight', pad_inches=0.05)
plt.close()

# === Figure 2: Boltzmann bridge ===
fig2, ax2 = plt.subplots(figsize=(6, 3.4))

x = np.linspace(-3, 3, 200)
ddg_pred = x

ax2.plot(x, ddg_pred, color='steelblue', lw=2.0)
ax2.fill_between(x, ddg_pred-0.3, ddg_pred+0.3, alpha=0.2, color='steelblue')

np.random.seed(3)
n_pts = 30
x_pts = np.random.uniform(-2.5, 2.5, n_pts)
y_pts = x_pts + np.random.normal(0, 0.3, n_pts)
ax2.scatter(x_pts, y_pts, s=30, c='black', alpha=0.7, zorder=5)

ax2.set_xlabel(r'$\ln(Z_{\text{modified}} / Z_{\text{native}})$ (microstate ratio)', fontsize=10)
ax2.set_ylabel(r'$\Delta\Delta G_{\text{binding}}$ (kT units)', fontsize=10)
ax2.set_xlim(-3, 3)
ax2.set_ylim(-3.5, 3.5)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.grid(alpha=0.3)

fig2.savefig('bridge.pdf', bbox_inches='tight')
plt.close()
print("done")
