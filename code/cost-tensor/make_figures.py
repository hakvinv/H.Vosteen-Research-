"""
Figures for: Personality Is Not Who You Are. It Is Your Cost Tensor.
Hakvin Vosteen, 2026
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman', 'DejaVu Serif'],
    'mathtext.fontset': 'cm',
    'font.size': 11,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})


def fig1_cost_vs_context():
    """Total cost as function of social familiarity, two personality types."""
    x = np.linspace(0, 10, 500)

    # high c_reject: introvert profile, decays slowly with familiarity
    introvert = 0.9 * np.exp(-0.25 * x) + 0.1

    # low ||c||_1: extrovert profile, low everywhere
    extrovert = 0.25 * np.exp(-0.4 * x) + 0.08

    threshold = 0.35

    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    ax.plot(x, introvert, color='black', lw=2.0,
            label=r'high $c_{\mathrm{reject}}$: labelled "introvert"')
    ax.plot(x, extrovert, color='black', lw=1.5, ls='--',
            label=r'low $\|\mathbf{c}_i\|_1$: labelled "extrovert"')
    ax.axhline(threshold, color='#888888', lw=0.8, ls=':')
    ax.text(9.6, threshold + 0.02, 'speak threshold',
            ha='right', fontsize=9, color='#444444')

    # silent / unlocks regions
    silent_x = x[introvert > threshold]
    if len(silent_x):
        x_unlock = silent_x[-1]
        ax.fill_between(x, 0, threshold, where=(x <= x_unlock),
                        color='lightgray', alpha=0.35)
        ax.text(x_unlock / 2, 0.06, 'silent', ha='center', fontsize=10,
                color='#444444')
        ax.text(x_unlock + 0.5, 0.18, 'unlocks', fontsize=10,
                color='#444444')

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.05)
    ax.set_xticks([0.5, 5.0, 9.5])
    ax.set_xticklabels(['stranger', 'acquaintance', 'close friend'])
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_xlabel(r'Social context (unfamiliar $\rightarrow$ familiar)')
    ax.set_ylabel(r'Total cost $\|\mathbf{c}_i\|_1$')
    ax.legend(loc='upper right', frameon=False)

    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)

    fig.tight_layout()
    fig.savefig('figures/fig1_cost_vs_context.pdf')
    fig.savefig('figures/fig1_cost_vs_context.png', dpi=300)
    plt.close(fig)


def fig2_trauma_therapy():
    """Trauma spike followed by therapeutic decay."""
    t = np.linspace(0, 20, 1000)
    baseline = 0.25
    trauma_t = 6.5
    therapy_start = 10.0

    cost = np.full_like(t, baseline)
    # small natural noise pre-trauma
    cost += 0.03 * np.sin(0.8 * t) * (t < trauma_t)
    # trauma spike
    spiked = (t >= trauma_t)
    cost[spiked] = 0.95
    # therapy phase: exponential decay back toward 0.55 (above original baseline)
    therapy = (t >= therapy_start)
    decay_t = t[therapy] - therapy_start
    cost[therapy] = 0.55 + 0.40 * np.exp(-0.2 * decay_t)

    threshold = 0.40

    fig, ax = plt.subplots(figsize=(7.0, 4.0))

    # Pre-therapy in solid, post-therapy dashed
    pre_mask = t < therapy_start
    post_mask = t >= therapy_start
    ax.plot(t[pre_mask], cost[pre_mask], color='black', lw=2.0)
    ax.plot(t[post_mask], cost[post_mask], color='black', lw=2.0, ls='--')

    ax.axhline(threshold, color='#888888', lw=0.8, ls=':')
    ax.text(19.5, threshold - 0.06, 'action threshold',
            ha='right', fontsize=9, color='#444444')

    ax.annotate('trauma event',
                xy=(trauma_t, 0.95), xytext=(trauma_t - 4, 1.06),
                fontsize=10, color='#444444',
                arrowprops=dict(arrowstyle='->', color='#888888', lw=0.8))
    ax.annotate('therapy begins',
                xy=(therapy_start, cost[np.argmin(np.abs(t - therapy_start))]),
                xytext=(therapy_start + 0.5, 1.06),
                fontsize=10, color='#444444',
                arrowprops=dict(arrowstyle='->', color='#888888', lw=0.8))

    ax.set_xlim(0, 20)
    ax.set_ylim(0, 1.20)
    ax.set_xticks([0, 4, 8, 12, 16, 20])
    ax.set_yticks([0, 0.5, 1.0])
    ax.set_xlabel('Time')
    ax.set_ylabel(r'$\|\mathbf{c}_i\|_1$')

    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)

    fig.tight_layout()
    fig.savefig('figures/fig2_trauma_therapy.pdf')
    fig.savefig('figures/fig2_trauma_therapy.png', dpi=300)
    plt.close(fig)


if __name__ == '__main__':
    fig1_cost_vs_context()
    fig2_trauma_therapy()
    print('Cost-Tensor figures written to figures/')
