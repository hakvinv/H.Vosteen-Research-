"""Reproduce Figures 1-3 of the paper.

    figure1_phase_portrait.png
    figure2_cartel_bifurcation.png
    figure3_schumpeter_sweep.png
"""
from __future__ import annotations

import os
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from sea import N_DEFAULT, REGIMES, run_regime, simulate, spectral_stats

mpl.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.grid": True,
    "grid.alpha": 0.25,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
})

MARKERS = {
    "Competition": ("o", "#4c72b0"),
    "Oligopol":    ("s", "#55a868"),
    "Cartel":      ("^", "#c44e52"),
    "Schumpeter":  ("D", "#1f4fb0"),
}


def fig_phase_portrait(results, out):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))

    ax = axes[0]
    for name, (xis, as_, _) in results.items():
        mk, color = MARKERS[name]
        ax.scatter(xis, as_, marker=mk, color=color, alpha=0.65, s=28,
                   label=name, edgecolor="none")
    ax.set_xlabel(r"Spectral concentration $\Xi = \lambda_1 / \mathrm{tr}(\Sigma)$")
    ax.set_ylabel(r"Eigenvector asymmetry $\mathcal{A}$")
    ax.set_title(r"Phase portrait on $(\Xi, \mathcal{A})$")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(loc="upper left", frameon=False, fontsize=9)

    ax = axes[1]
    width = 0.18
    x = np.arange(N_DEFAULT)
    for i, name in enumerate(["Cartel", "Schumpeter"]):
        _, _, v1 = results[name]
        v1 = np.abs(v1) / np.linalg.norm(v1)
        color = MARKERS[name][1]
        ax.bar(x + (i - 0.5) * width * 2, v1 ** 2, width * 2,
               color=color, label=name, alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels([f"Firm {i+1}" for i in range(N_DEFAULT)])
    ax.set_ylabel(r"Eigenvector mass $v_{1,i}^2$")
    ax.set_title("Dominant eigenvector profile")
    ax.legend(frameon=False)

    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def _sweep(betas_iter, beta_factory, sigma_f=1.0, seeds=40, N=N_DEFAULT):
    """Run Monte Carlo over a parameter sweep and return (mean, sd) curves."""
    xi_m, xi_s, a_m, a_s = [], [], [], []
    for b in betas_iter:
        xs, as_ = [], []
        for s in range(seeds):
            rng = np.random.default_rng(s * 7 + int(b * 1000))
            Sigma = simulate(beta_factory(b, N), sigma_f=sigma_f, rng=rng)
            xi, a, _ = spectral_stats(Sigma)
            xs.append(xi)
            as_.append(a)
        xi_m.append(np.mean(xs)); xi_s.append(np.std(xs))
        a_m.append(np.mean(as_)); a_s.append(np.std(as_))
    return (np.array(xi_m), np.array(xi_s), np.array(a_m), np.array(a_s))


def fig_cartel_bifurcation(out):
    betas = np.linspace(0.0, 2.0, 25)
    xi_m, xi_s, a_m, a_s = _sweep(
        betas, lambda b, N: np.full(N, b), sigma_f=1.0,
    )

    fig, ax1 = plt.subplots(figsize=(7.5, 4.3))
    c1 = "#c44e52"; c2 = "#1f1f1f"
    ax1.fill_between(betas, xi_m - xi_s, xi_m + xi_s, color=c1, alpha=0.2)
    ax1.plot(betas, xi_m, color=c1, lw=2, label=r"$\Xi$")
    ax1.axhline(1 / N_DEFAULT, ls="--", color=c1, alpha=0.4, lw=1)
    ax1.set_xlabel(r"Symmetric factor loading $\beta$ (all firms)")
    ax1.set_ylabel(r"$\Xi$", color=c1)
    ax1.tick_params(axis="y", labelcolor=c1)
    ax1.set_ylim(0, 1)

    ax2 = ax1.twinx()
    ax2.fill_between(betas, a_m - a_s, a_m + a_s, color=c2, alpha=0.15)
    ax2.plot(betas, a_m, color=c2, lw=2, label=r"$\mathcal{A}$")
    ax2.axhline(1 / N_DEFAULT, ls="--", color=c2, alpha=0.4, lw=1)
    ax2.set_ylabel(r"$\mathcal{A}$", color=c2)
    ax2.tick_params(axis="y", labelcolor=c2)
    ax2.set_ylim(0, 1)

    plt.title("Cartel bifurcation: symmetric loading sweep")
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def fig_schumpeter_sweep(out):
    b0s = np.linspace(0.8, 3.5, 25)

    def factory(b0, N):
        beta = np.full(N, 0.8)
        beta[0] = b0
        return beta

    xi_m, xi_s, a_m, a_s = _sweep(b0s, factory, sigma_f=2.0)

    fig, ax1 = plt.subplots(figsize=(7.5, 4.3))
    c1 = "#1f4fb0"; c2 = "#1f1f1f"
    ax1.fill_between(b0s, xi_m - xi_s, xi_m + xi_s, color=c1, alpha=0.2)
    ax1.plot(b0s, xi_m, color=c1, lw=2, label=r"$\Xi$")
    ax1.set_xlabel(r"Innovator loading $\beta_0$ (followers fixed at 0.8)")
    ax1.set_ylabel(r"$\Xi$", color=c1)
    ax1.tick_params(axis="y", labelcolor=c1)
    ax1.set_ylim(0, 1)

    ax2 = ax1.twinx()
    ax2.fill_between(b0s, a_m - a_s, a_m + a_s, color=c2, alpha=0.15)
    ax2.plot(b0s, a_m, color=c2, lw=2, label=r"$\mathcal{A}$")
    ax2.set_ylabel(r"$\mathcal{A}$", color=c2)
    ax2.tick_params(axis="y", labelcolor=c2)
    ax2.set_ylim(0, 1)

    plt.title("Schumpeterian transition: innovator loading sweep")
    fig.tight_layout()
    fig.savefig(out)
    plt.close(fig)


def main(outdir="."):
    os.makedirs(outdir, exist_ok=True)
    results = {name: run_regime(name, REGIMES[name]) for name in REGIMES}
    fig_phase_portrait(results, os.path.join(outdir, "figure1_phase_portrait.png"))
    fig_cartel_bifurcation(os.path.join(outdir, "figure2_cartel_bifurcation.png"))
    fig_schumpeter_sweep(os.path.join(outdir, "figure3_schumpeter_sweep.png"))
    print("Figures written to", outdir)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
