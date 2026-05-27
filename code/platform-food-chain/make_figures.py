"""
Figures for: The Platform Has a Food Chain. You Are In It.
Hakvin Vosteen, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch
from matplotlib.lines import Line2D

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'cm',
    'font.size': 11,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


# ============================================================
# Fig 1: Five-agent ecology diagram
# ============================================================
def fig1_ecology_diagram():
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.set_xlim(-1.0, 5.5)
    ax.set_ylim(-0.3, 4.0)
    ax.axis('off')

    # central whale
    whale_xy = (2.25, 2.0)
    nodes = {
        'Drama\n(Parasite)':     (2.25, 3.3),
        'Sharer\n(Remora)':      (4.4, 2.7),
        'Hater\n(Barnacle)':     (4.4, 1.3),
        'Lurker\n(Plankton)':    (0.1, 2.0),
        'Creator\n(Whale)':      whale_xy,
    }

    for label, (x, y) in nodes.items():
        if 'Whale' in label:
            c = Circle((x, y), 0.55, facecolor='black', edgecolor='black', zorder=3)
            ax.add_patch(c)
            ax.text(x, y, label, ha='center', va='center',
                    color='white', fontsize=9.5, fontweight='bold', zorder=4)
        else:
            c = Circle((x, y), 0.50,
                       facecolor='#f5f5f5', edgecolor='black', lw=1.0, zorder=3)
            ax.add_patch(c)
            ax.text(x, y, label, ha='center', va='center',
                    color='black', fontsize=9, zorder=4)

    # arrows
    def arrow(p1, p2, label='', curve=0.0, ls='-'):
        a = FancyArrowPatch(p1, p2,
                            arrowstyle='-|>', mutation_scale=12,
                            lw=1.0, color='#444444',
                            connectionstyle=f'arc3,rad={curve}',
                            linestyle=ls)
        ax.add_patch(a)
        if label:
            mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
            ax.text(mx, my + 0.18, label, ha='center', fontsize=8.5,
                    color='#444444')

    # whale -> downstream agents (A_0)
    arrow((2.25, 2.55), (2.25, 2.85), '$A_0$', curve=0.0)
    arrow((2.78, 2.25), (3.95, 2.55), '$A_0$', curve=0.0)
    arrow((2.78, 1.75), (3.95, 1.45), '$A_0$', curve=0.0)
    arrow((1.72, 2.0),  (0.62, 2.0),  'drift', curve=0.0, ls='--')

    # remora amplification back
    arrow((4.05, 2.55), (3.7, 2.45), r'$\alpha_R A_0$', curve=-0.3)

    fig.savefig('figures/fig1_ecology.pdf')
    fig.savefig('figures/fig1_ecology.png', dpi=300)
    plt.close(fig)


# ============================================================
# Fig 2: Whale growth + barnacle burnout
# ============================================================
def fig2_whale_growth():
    t = np.linspace(0, 30, 600)
    # logistic growth
    A0 = 1.0 / (1 + np.exp(-0.7 * (t - 6)))
    # burnout regime after t=20
    burnout = A0.copy()
    n_star_t = 20.0
    decay = (t > n_star_t)
    burnout[decay] = A0[np.argmin(np.abs(t - n_star_t))] * np.exp(-0.08 * (t[decay] - n_star_t))

    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    # split solid before t=n_star, dashed after
    ax.plot(t[t <= n_star_t], A0[t <= n_star_t], color='black', lw=1.8)
    ax.plot(t[t > n_star_t], burnout[t > n_star_t], color='black', lw=1.5, ls='--')

    ax.text(4, 0.78, 'growth', fontsize=10)
    ax.text(13, 1.05, 'stable', fontsize=10)
    ax.text(13, 0.92, r'$n_B > n_B^{*}$', fontsize=9, color='#444444')
    ax.text(24, 0.6, 'burnout', fontsize=10, color='#444444')

    ax.set_xlim(0, 30)
    ax.set_ylim(0, 1.15)
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30])
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel('Time')
    ax.set_ylabel(r'$A_0(t)$')

    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig('figures/fig2_whale_growth.pdf')
    fig.savefig('figures/fig2_whale_growth.png', dpi=300)
    plt.close(fig)


# ============================================================
# Fig 3: Remora share-timing curve
# ============================================================
def fig3_remora_timing():
    tau = np.linspace(0, 24, 500)
    tau_star = 3.0
    lam = 0.12
    A_R = np.exp(-lam * (tau - tau_star) ** 2)

    fig, ax = plt.subplots(figsize=(7.0, 3.2))
    ax.plot(tau, A_R, color='black', lw=1.8)
    ax.fill_between(tau, 0, A_R, color='#cccccc', alpha=0.4)
    ax.axvline(tau_star, color='#888888', ls='--', lw=0.8)
    ax.text(tau_star + 0.2, 0.95, r'$\tau^{*} = 3$h', fontsize=10)

    ax.set_xlim(0, 24)
    ax.set_ylim(0, 1.1)
    ax.set_xticks([0, 6, 12, 18, 24])
    ax.set_xticklabels(['0h', '6h', '12h', '18h', '24h'])
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel(r'Share timing $\tau$ after post')
    ax.set_ylabel(r'$A_R(\tau)$')
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig('figures/fig3_remora_timing.pdf')
    fig.savefig('figures/fig3_remora_timing.png', dpi=300)
    plt.close(fig)


# ============================================================
# Fig 4: Barnacle conflict-intensity response
# ============================================================
def fig4_barnacle_conflict():
    c = np.linspace(0.001, 1.0, 500)
    alpha0 = 0.05
    beta = 0.8
    gamma = 0.5
    alpha_B = alpha0 + beta * c ** gamma

    # interior optimum c* = (alpha0 / (beta*gamma))^(1/(gamma-1))
    c_star = (alpha0 / (beta * gamma)) ** (1.0 / (gamma - 1.0))
    c_star = min(c_star, 0.95)

    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ax.plot(c, alpha_B, color='black', lw=1.8)
    ax.axhline(alpha0, color='#888888', ls=':', lw=0.7)
    ax.text(0.40, alpha0 + 0.02, r'$\alpha_{\mathrm{agree}} \approx 0.05$',
            fontsize=9, color='#444444')

    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.0)
    ax.set_xticks([0.05, 0.30, 0.55, 0.85])
    ax.set_xticklabels(['agree', 'mild', 'ratio', 'hate'])
    ax.set_yticks([0, 0.5, 1])
    ax.set_xlabel(r'Conflict intensity $c$')
    ax.set_ylabel(r'$\alpha_B(c)$')
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig('figures/fig4_barnacle_conflict.pdf')
    fig.savefig('figures/fig4_barnacle_conflict.png', dpi=300)
    plt.close(fig)


# ============================================================
# Fig 5: Lotka-Volterra creator-hater coexistence
# ============================================================
def fig5_lotka_volterra():
    # Parameters
    alpha = 1.0
    beta = 1.5
    gamma = 1.5
    delta = 1.0
    dt = 0.01
    T = 40.0
    n = int(T / dt)

    W = np.zeros(n)
    B = np.zeros(n)
    t = np.linspace(0, T, n)
    W[0] = 0.8
    B[0] = 0.4

    for i in range(n - 1):
        dW = alpha * W[i] - beta * W[i] * B[i]
        dB = delta * W[i] * B[i] - gamma * B[i]
        W[i + 1] = W[i] + dt * dW
        B[i + 1] = B[i] + dt * dB

    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    ax.plot(t, W, color='black', lw=1.5, label=r'$W(t)$: creator')
    ax.plot(t, B, color='black', lw=1.5, ls='--', label=r'$B(t)$: haters')

    ax.set_xlim(0, 40)
    ax.set_ylim(0, max(W.max(), B.max()) * 1.15)
    ax.set_xticks([0, 5, 10, 15, 20, 25, 30, 35, 40])
    ax.set_xlabel('Time')
    ax.set_ylabel('Population')
    ax.legend(loc='upper right', frameon=False)
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig('figures/fig5_lotka_volterra.pdf')
    fig.savefig('figures/fig5_lotka_volterra.png', dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    fig1_ecology_diagram()
    fig2_whale_growth()
    fig3_remora_timing()
    fig4_barnacle_conflict()
    fig5_lotka_volterra()
    print('Platform-Ecology figures written to figures/')
