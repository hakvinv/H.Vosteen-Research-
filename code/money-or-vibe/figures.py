"""
Reproducible figures for Money vs Vibe post
Author: Hakvin Vosteen, 2026
Run: python3 figures.py
Outputs: ./*.pdf and ./*.png
Requirements: matplotlib >= 3.5, numpy >= 1.20
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'

# ============================================
# HOOK FIGURE: Two utility surfaces, no exchange rate
# Two separate optimization landscapes
# ============================================

fig, ax = plt.subplots(figsize=(5.5, 2.8))

x = np.linspace(0, 10, 100)
# Money-Person utility: money matters, vibe is residual
u_money = 0.9 * x
# Vibe-Person utility: vibe matters, money is residual
u_vibe = 0.9 * x

ax.plot(x, u_money, 'k-', linewidth=2.5, label='Money-Person: $U = U(M)$')
ax.plot(x, u_vibe, 'k--', linewidth=2.5, label='Vibe-Person: $U = U(V)$')

# Show that they are in different spaces
ax.fill_between(x, 0, u_money, alpha=0.15, color='black')
ax.fill_between(x, 0, u_vibe, alpha=0.15, color='gray')

ax.set_xlabel('asset accumulated', fontsize=10)
ax.set_ylabel('utility', fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(loc='upper left', fontsize=9, frameon=False)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Annotation
ax.annotate('no exchange rate\nbetween the two', xy=(7, 2),
            xytext=(7, 2), fontsize=9, ha='center', style='italic')

plt.tight_layout()
plt.savefig('hook_fig.pdf', bbox_inches='tight')
print("hook_fig done")

# ============================================
# MAIN FIGURE: The conflict diagram
# Two people arguing, with their utility functions drawn
# ============================================

fig, ax = plt.subplots(figsize=(6, 4.5))

# Money-Person arrow path
t = np.linspace(0, 1, 50)
money_path_x = 1 + 4 * t
money_path_y = 1 + 4 * t
ax.plot(money_path_x, money_path_y, 'k-', linewidth=2, alpha=0.8)
ax.annotate('', xy=(5, 5), xytext=(4.7, 4.7),
            arrowprops=dict(arrowstyle='->', color='black', lw=2))

# Vibe-Person arrow path
vibe_path_x = 1 + 4 * t
vibe_path_y = 5 - 4 * t * 0.3  # different direction
ax.plot(vibe_path_x, vibe_path_y, 'k--', linewidth=2, alpha=0.8)
ax.annotate('', xy=(5, 3.8), xytext=(4.7, 3.85),
            arrowprops=dict(arrowstyle='->', color='black', lw=2))

# Labels
ax.text(0.3, 1, 'Money\nPerson', fontsize=11, ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='black'))
ax.text(0.3, 5, 'Vibe\nPerson', fontsize=11, ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='gray', linestyle='--'))

ax.text(5.3, 5, 'maximizes M', fontsize=10, ha='left', va='center')
ax.text(5.3, 3.8, 'maximizes V', fontsize=10, ha='left', va='center')

# Conflict zone
ax.text(3, 4.4, 'they argue here\nbut talk past each other', fontsize=9,
        ha='center', style='italic', color='black',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#f0f0f0', edgecolor='none'))

ax.set_xlim(-0.5, 8)
ax.set_ylim(0, 6.5)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.savefig('conflict_fig.pdf', bbox_inches='tight')
print("conflict_fig done")

# ============================================
# THIRD FIGURE: Inter-Personal Utility Comparison failure
# Show that V_A and M_B cannot be compared
# ============================================

fig, ax = plt.subplots(figsize=(6, 4.2))

# Two utility surfaces in 2D
M = np.linspace(0, 10, 100)
V = np.linspace(0, 10, 100)
M_grid, V_grid = np.meshgrid(M, V)

# Money-Person preference: weights money heavily
U_money_person = 0.9 * M_grid + 0.1 * V_grid

# Vibe-Person preference: weights vibe heavily  
U_vibe_person = 0.1 * M_grid + 0.9 * V_grid

# Show indifference curves
levels = [2, 4, 6, 8]
cs1 = ax.contour(M_grid, V_grid, U_money_person, levels=levels,
                  colors='black', linestyles='-', linewidths=1.5)
cs2 = ax.contour(M_grid, V_grid, U_vibe_person, levels=levels,
                  colors='gray', linestyles='--', linewidths=1.5)

ax.clabel(cs1, inline=True, fontsize=8, fmt='%d')
ax.clabel(cs2, inline=True, fontsize=8, fmt='%d')

# Mark two example positions
ax.plot(8, 2, 'ko', markersize=12)
ax.annotate('Banker:\nhigh M, low V', xy=(8, 2), xytext=(7.5, 0.3), fontsize=9, ha='center')

ax.plot(2, 8, 'ko', markersize=12, markerfacecolor='white')
ax.annotate('Berliner Künstler:\nlow M, high V', xy=(2, 8), xytext=(2.5, 9), fontsize=9, ha='center')

ax.set_xlabel('Money Capital ($M$)', fontsize=11)
ax.set_ylabel('Vibe Capital ($V$)', fontsize=11)
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Legend manually
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='black', lw=1.5, linestyle='-', label='Money-Person curves'),
    Line2D([0], [0], color='gray', lw=1.5, linestyle='--', label='Vibe-Person curves')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=9, frameon=False)

plt.tight_layout()
plt.savefig('utility_fig.pdf', bbox_inches='tight')
print("utility_fig done")
