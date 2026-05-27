"""Reproduce Table 2: Monte Carlo means and standard deviations."""
from __future__ import annotations

import sys

import numpy as np

from sea import REGIMES, run_regime


def main(seeds=100):
    print(f"{'Regime':<22}{'Xi (mean +/- sd)':>22}{'A (mean +/- sd)':>22}")
    print("-" * 66)
    for name in ["Competition", "Oligopol", "Cartel", "Schumpeter"]:
        xis, as_, _ = run_regime(name, REGIMES[name], seeds=seeds)
        print(
            f"{name:<22}"
            f"{xis.mean():>10.3f} +/- {xis.std():<6.3f}"
            f"{as_.mean():>10.3f} +/- {as_.std():<6.3f}"
        )

    # Cohen's d between Cartel and Schumpeter on A
    xc, ac, _ = run_regime("Cartel", REGIMES["Cartel"], seeds=seeds)
    xs, as_s, _ = run_regime("Schumpeter", REGIMES["Schumpeter"], seeds=seeds)
    pooled_sd = np.sqrt((ac.var(ddof=1) + as_s.var(ddof=1)) / 2)
    d = (as_s.mean() - ac.mean()) / pooled_sd
    print(f"\nCohen's d (Cartel vs Schumpeter, on A): {d:.1f}")


if __name__ == "__main__":
    seeds = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    main(seeds=seeds)
