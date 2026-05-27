# Cartel or Creative Destruction? — Replication Code

Companion code for the working paper
**"Cartel or Creative Destruction? Eigenvector Asymmetry as a Spectral
Diagnostic for Schumpeterian Market Structure"**
([PDF](../../papers/2026-04-22-cartel-schumpeter.pdf)).

## What's here

```
sea.py             core factor-model simulation + spectral statistics
make_table.py      reproduces Table 2 (Monte Carlo means)
make_figures.py    reproduces Figures 1-3
requirements.txt   numpy, matplotlib
```

## Run

```bash
cd code/cartel-schumpeter
pip install -r requirements.txt

python make_table.py        # prints Table 2 to stdout
python make_figures.py .    # writes figure1/2/3.png into cwd
```

## API

```python
from sea import simulate, spectral_stats, run_regime, REGIMES

# one simulated market
Sigma = simulate(beta=[1.5]*6, sigma_f=1.0)
xi, a, v1 = spectral_stats(Sigma)

# Monte Carlo over one regime
xis, as_, _ = run_regime("Schumpeter", REGIMES["Schumpeter"], seeds=100)
```

## Notes

- Seeds are deterministic: same run gives same numbers.
- Sample sizes match the paper (N=6, T=500, 100 seeds).
- If your numbers deviate, check your numpy/BLAS version; the
  eigendecomposition is stable but the RNG stream is not cross-version.
