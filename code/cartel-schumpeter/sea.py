"""Core simulation and spectral diagnostics for the SEA paper.

Reproduces the single-factor model of Section 2 and the spectral
observables (Xi, A) of Section 3.

    r_i(t) = beta_i f(t) + eps_i(t)
    Sigma  = sigma_f^2 beta beta^T + sigma^2 I_N
    Xi     = lambda_1 / tr(Sigma)
    A      = max_i v_{1,i}^2 / ||v_1||^2
"""
from __future__ import annotations

import numpy as np

N_DEFAULT = 6
T_DEFAULT = 500


def simulate(beta, sigma_f=1.0, sigma=0.5, T=T_DEFAULT, rng=None):
    """Draw T observations of r_i(t) and return the sample covariance."""
    rng = rng if rng is not None else np.random.default_rng()
    beta = np.asarray(beta, dtype=float)
    N = beta.size
    f = rng.normal(0.0, sigma_f, size=T)
    eps = rng.normal(0.0, sigma, size=(N, T))
    r = np.outer(beta, f) + eps
    return np.cov(r)


def spectral_stats(Sigma):
    """Return (Xi, A, v1) from a covariance matrix."""
    w, v = np.linalg.eigh(Sigma)
    idx = np.argsort(w)[::-1]
    w = w[idx]
    v = v[:, idx]
    xi = w[0] / np.sum(w)
    v1 = v[:, 0]
    a = float(np.max(v1 ** 2) / np.sum(v1 ** 2))
    return float(xi), a, v1


REGIMES = {
    "Competition": {"kind": "zero"},
    "Oligopol":    {"kind": "gauss", "mu": 0.4, "tau": 0.1},
    "Cartel":      {"kind": "uniform", "b": 1.5},
    "Schumpeter":  {"kind": "schumpeter", "b0": 2.5, "bo": 0.8, "sigma_f": 2.0},
}


def draw_beta(cfg, N=N_DEFAULT, rng=None):
    rng = rng if rng is not None else np.random.default_rng()
    k = cfg["kind"]
    if k == "zero":
        return np.zeros(N)
    if k == "gauss":
        return rng.normal(cfg["mu"], cfg["tau"], size=N)
    if k == "uniform":
        return np.full(N, cfg["b"])
    if k == "schumpeter":
        b = np.full(N, cfg["bo"])
        b[0] = cfg["b0"]
        return b
    raise ValueError(f"unknown regime kind: {k}")


def run_regime(name, cfg=None, seeds=100, N=N_DEFAULT, T=T_DEFAULT):
    """Monte Carlo over `seeds` replications. Returns arrays of (Xi, A)."""
    cfg = cfg if cfg is not None else REGIMES[name]
    sigma_f = cfg.get("sigma_f", 1.0)
    xis, as_ = [], []
    sample_v1 = None
    for s in range(seeds):
        rng = np.random.default_rng(s + hash(name) % 10_000)
        beta = draw_beta(cfg, N=N, rng=rng)
        Sigma = simulate(beta, sigma_f=sigma_f, T=T, rng=rng)
        xi, a, v1 = spectral_stats(Sigma)
        xis.append(xi)
        as_.append(a)
        if sample_v1 is None:
            sample_v1 = v1
    return np.array(xis), np.array(as_), sample_v1
