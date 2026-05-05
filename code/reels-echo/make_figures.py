"""
Figures for: Instagram Reels Is a TikTok Echo
Hakvin Vosteen, 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# Hakvin paper aesthetic
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'cm',
    'font.size': 11,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'axes.linewidth': 0.8,
    'grid.alpha': 0.3,
    'grid.linestyle': '-',
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


def gauss(t, mu, sigma):
    return np.exp(-0.5 * ((t - mu) / sigma) ** 2)


def fig1_format_size():
    """Three-platform diffusion curves with imitation lag."""
    t = np.linspace(0, 9, 600)

    # TikTok: leader, peak at 2 months
    tiktok = 100 * gauss(t, 2.0, 1.1)

    # Reels: follower, lag ~2.5m
    reels = 60 * gauss(t, 4.5, 1.3)

    # Shorts: slower follower, lag ~4m
    shorts = 35 * gauss(t, 6.0, 1.4)

    fig, ax = plt.subplots(figsize=(7.2, 4.0))

    ax.plot(t, tiktok, color='black', lw=1.8,
            label=r'TikTok ($\lambda=1$)')
    ax.plot(t, reels, color='steelblue', lw=1.8,
            label=r'Reels ($\Delta\tau \approx 2.5$m)')
    ax.plot(t, shorts, color='darkgreen', lw=1.8, ls='--',
            label=r'YouTube Shorts ($\Delta\tau \approx 4$m)')

    # Annotate the lag
    ax.annotate('', xy=(4.5, 95), xytext=(2.0, 95),
                arrowprops=dict(arrowstyle='<->', color='#555555', lw=0.8))
    ax.text(3.25, 99, r'$\Delta\tau$', color='#555555',
            ha='center', fontsize=11)

    ax.set_xlabel('Months after TikTok trend peak')
    ax.set_ylabel('Relative format size (\\%)')
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 110)
    ax.grid(True)
    ax.legend(loc='upper right', frameon=False)

    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)

    fig.tight_layout()
    fig.savefig('figures/fig1_format_size.pdf')
    fig.savefig('figures/fig1_format_size.png', dpi=300)
    plt.close(fig)


def fig2_lag_vs_engagement():
    """Lag Delta tau as function of engagement score s."""
    s = np.linspace(0.05, 1.0, 500)
    lam = 0.6
    beta0 = 1.0  # arbitrary normalization
    delta_tau = np.log(1.0 / lam) / (beta0 * s)

    # Half-life regimes
    t_half_micro = 0.7   # ~3 weeks
    t_half_macro = 4.0   # mainstream

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    ax.plot(s, delta_tau, color='black', lw=1.8, label=r'$\Delta\tau(s)$')

    ax.axhline(t_half_micro, color='orangered', ls='--', lw=1.0,
               label=r'$t_{1/2}$ (micro-trend, 3 weeks)')
    ax.axhline(t_half_macro, color='steelblue', ls=':', lw=1.0,
               label=r'$t_{1/2}$ (mainstream, 4 months)')

    # Shade immune region
    s_crit = np.log(1.0 / lam) / (beta0 * t_half_micro)
    ax.axvspan(0.05, s_crit, alpha=0.10, color='orangered')
    ax.text(s_crit / 2, 8.5, 'Immune\nregion',
            color='#555555', ha='center', fontsize=10)

    ax.set_xlabel(r'Engagement score $s$ (month$^{-1}$)')
    ax.set_ylabel(r'Imitation lag $\Delta\tau$ (months)')
    ax.set_xlim(0.05, 1.0)
    ax.set_ylim(0, 11)
    ax.grid(True)
    ax.legend(loc='upper right', frameon=False)

    for sp in ['top', 'right']:
        ax.spines[sp].set_visible(False)

    fig.tight_layout()
    fig.savefig('figures/fig2_lag_vs_engagement.pdf')
    fig.savefig('figures/fig2_lag_vs_engagement.png', dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    fig1_format_size()
    fig2_lag_vs_engagement()
    print('Figures written to figures/')
