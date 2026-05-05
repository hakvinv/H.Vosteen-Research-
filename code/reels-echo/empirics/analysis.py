"""
Empirical pilot + theoretical sensitivity for:
Instagram Reels Is a TikTok Echo

Three analyses:
1. Pilot dataset summary (N=8 documented crossover trends)
2. Sensitivity surface: Delta tau as function of (beta0 * s, lambda)
3. Half-life threshold: which engagement scores cross the cutoff
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'mathtext.fontset': 'cm',
    'font.size': 11,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


# ============================================================
# 1. Pilot dataset
# ============================================================

pilot = pd.DataFrame([
    dict(trend='Girl Dinner',         tt_peak='2023-07-15', ig_peak='2023-09-15', delta_tau=2.0),
    dict(trend='Roman Empire',        tt_peak='2023-09-20', ig_peak='2023-12-01', delta_tau=2.4),
    dict(trend='Stanley Cup tumbler', tt_peak='2024-01-15', ig_peak='2024-04-01', delta_tau=2.5),
    dict(trend='Mob Wife',            tt_peak='2024-02-10', ig_peak='2024-04-20', delta_tau=2.3),
    dict(trend='Wes Anderson POV',    tt_peak='2023-05-20', ig_peak='2023-07-25', delta_tau=2.2),
    dict(trend='Tube Girl',           tt_peak='2023-09-25', ig_peak='2023-11-15', delta_tau=1.7),
    dict(trend='Demure',              tt_peak='2024-08-25', ig_peak='2024-10-20', delta_tau=1.9),
    dict(trend='Of Course (cat)',     tt_peak='2024-05-25', ig_peak='2024-08-10', delta_tau=2.5),
])

print("=== Pilot Dataset (N = {}) ===".format(len(pilot)))
print(pilot.to_string(index=False))
print()
print(f"Median Delta tau = {pilot['delta_tau'].median():.2f} months")
print(f"Mean   Delta tau = {pilot['delta_tau'].mean():.2f} months")
print(f"SD     Delta tau = {pilot['delta_tau'].std():.2f} months")
print(f"IQR    Delta tau = [{pilot['delta_tau'].quantile(0.25):.2f}, "
      f"{pilot['delta_tau'].quantile(0.75):.2f}]")

# Model prediction
lam = 0.6
beta0_s = 0.2
delta_pred = np.log(1.0 / lam) / beta0_s
print(f"\nModel prediction (lambda=0.6, beta0*s=0.2): Delta tau = {delta_pred:.2f} months")
print(f"Pilot mean / Model pred = {pilot['delta_tau'].mean() / delta_pred:.3f}")

pilot.to_csv('empirics/pilot_dataset.csv', index=False)


# ============================================================
# 2. Sensitivity surface
# ============================================================

bs = np.linspace(0.05, 0.6, 200)        # beta0 * s, in month^-1
lams = np.linspace(0.2, 0.95, 200)      # lambda
BS, LM = np.meshgrid(bs, lams)
DT = np.log(1.0 / LM) / BS              # months

fig, ax = plt.subplots(figsize=(7.2, 4.8))

# Heatmap with log-scaled lag
levels = [0.5, 1, 1.5, 2, 2.5, 3, 4, 5, 7, 10]
cs = ax.contourf(BS, LM, DT, levels=levels, cmap='magma_r', extend='max')
cb = fig.colorbar(cs, ax=ax)
cb.set_label(r'Imitation lag $\Delta\tau$ (months)')

# Contour lines
cs2 = ax.contour(BS, LM, DT, levels=[2.5], colors='white', linewidths=1.5)
ax.clabel(cs2, inline=True, fmt=r'$\Delta\tau = 2.5$m', fontsize=9)

# Mark the calibration point
ax.plot(0.2, 0.6, 'wo', markersize=8, markeredgecolor='black', markeredgewidth=1.2)
ax.annotate('Reels\ncalibration\n($\\lambda=0.6$, $\\beta_0 s=0.2$)',
            xy=(0.2, 0.6), xytext=(0.32, 0.45),
            color='white', fontsize=9, ha='left',
            arrowprops=dict(arrowstyle='->', color='white', lw=0.8))

# Mark Shorts hypothesised region
ax.plot(0.2, 0.4, 's', color='#88cc88', markersize=8,
        markeredgecolor='black', markeredgewidth=1.0)
ax.annotate('Shorts\n($\\lambda=0.4$ hypothesis)',
            xy=(0.2, 0.4), xytext=(0.32, 0.28),
            color='#cccccc', fontsize=9, ha='left',
            arrowprops=dict(arrowstyle='->', color='#cccccc', lw=0.8))

ax.set_xlabel(r'$\beta_0 s$ (month$^{-1}$)')
ax.set_ylabel(r'Algorithmic mixing weight $\lambda$')
ax.set_xlim(0.05, 0.6)
ax.set_ylim(0.2, 0.95)

fig.tight_layout()
fig.savefig('figures/fig3_sensitivity.pdf')
fig.savefig('figures/fig3_sensitivity.png', dpi=300)
plt.close(fig)


# ============================================================
# 3. Half-life threshold analysis
# ============================================================

# Model: trend dies before Reels amplification iff
#         t_half < Delta tau = ln(1/lambda) / (beta0 s)
# Equivalent: s > ln(1/lambda) / (beta0 * t_half)

t_half_grid = np.linspace(0.25, 8.0, 500)  # months
lam = 0.6
beta0 = 1.0  # absorbed into s

# Critical engagement score below which content is immune
s_crit = np.log(1.0 / lam) / (beta0 * t_half_grid)

fig, ax = plt.subplots(figsize=(7.2, 4.0))

ax.fill_between(t_half_grid, 0, s_crit, alpha=0.18, color='orangered',
                label='Immune region (dies before Reels)')
ax.fill_between(t_half_grid, s_crit, 1.0, alpha=0.10, color='steelblue',
                label='Crossover region')

ax.plot(t_half_grid, s_crit, color='black', lw=1.6)

# Pilot trends placed approximately
# (estimated t_half from KnowYourMeme spread + assumed s)
pilot_pts = [
    ('Girl Dinner',     2.5, 0.45),
    ('Roman Empire',    2.0, 0.40),
    ('Stanley Cup',     5.0, 0.30),
    ('Mob Wife',        1.5, 0.55),
    ('Tube Girl',       1.2, 0.60),
]
for name, th, s in pilot_pts:
    ax.plot(th, s, 'ko', markersize=5)
    ax.annotate(name, (th, s), xytext=(5, 5),
                textcoords='offset points', fontsize=8.5, color='#444444')

ax.set_xlabel(r'Trend half-life on TikTok $t_{1/2}$ (months)')
ax.set_ylabel(r'Engagement score $s$ (a.u.)')
ax.set_xlim(0.25, 8.0)
ax.set_ylim(0, 1.0)
ax.legend(loc='upper right', frameon=False)
ax.grid(True, alpha=0.3)

for sp in ['top', 'right']:
    ax.spines[sp].set_visible(False)

fig.tight_layout()
fig.savefig('figures/fig4_threshold.pdf')
fig.savefig('figures/fig4_threshold.png', dpi=300)
plt.close(fig)


# ============================================================
# 4. Pilot vs prediction visual
# ============================================================

fig, ax = plt.subplots(figsize=(7.2, 4.0))

x = np.arange(len(pilot))
ax.bar(x, pilot['delta_tau'], color='steelblue', alpha=0.75,
       edgecolor='black', linewidth=0.6, label='Observed lag')
ax.axhline(delta_pred, color='black', ls='--', lw=1.2,
           label=fr'Model prediction $\Delta\tau = \ln(1/\lambda)/(\beta_0 s) \approx {delta_pred:.2f}$m')
ax.axhspan(delta_pred - 0.5, delta_pred + 0.5, alpha=0.10, color='black')

ax.set_xticks(x)
ax.set_xticklabels(pilot['trend'], rotation=30, ha='right')
ax.set_ylabel(r'$\Delta\tau$ (months)')
ax.set_ylim(0, 3.5)
ax.legend(loc='upper right', frameon=False)
ax.grid(True, alpha=0.3, axis='y')
for sp in ['top', 'right']:
    ax.spines[sp].set_visible(False)

fig.tight_layout()
fig.savefig('figures/fig5_pilot_vs_prediction.pdf')
fig.savefig('figures/fig5_pilot_vs_prediction.png', dpi=300)
plt.close(fig)

print("\nFigures written to figures/")
