# The Platform Has a Food Chain. You Are In It.

**Author:** Hakvin Vosteen
**Date:** May 2026
**Status:** Working paper, ready for SSRN/arXiv submission
**Companion paper:** *Instagram Reels Is a TikTok Echo* (Vosteen, 2026)

---

## Reconstructed from carousel

This paper reconstructs the five-slide TikTok carousel posted 2026-04-10
(33K views, 2.5K likes, 1.8K saves) into a publication-format paper.

Source slides:
1. *Every Platform Has an Ecology* — five-agent diagram, master equation
2. *Creator & Sharer* — Whale dynamics, Remora timing
3. *Hater & Lurker* — Barnacle conflict optimum, Plankton invisibility
4. *Drama Aggregator & Equilibrium* — Parasite α_D > 1, Lotka-Volterra
5. *Pulling It All Together* — Cascade master equation, Nash equilibrium

Full reconstruction is in `paper.pdf` (9 pages). The five agents and their
biological analogues, extraction coefficients, and harm derivatives are
preserved exactly. The paper extends with the Lotka-Volterra numerical
solution, four testable predictions, and explicit boundary conditions.

---

## Bundle contents

```
platform-ecology/
├── paper.pdf                          Compiled paper, 9 pages
├── paper.tex                          LaTeX source
├── figures/
│   ├── fig1_ecology.pdf/png             Five-agent diagram
│   ├── fig2_whale_growth.pdf/png        Creator output, growth → burnout
│   ├── fig3_remora_timing.pdf/png       Share-time amplification, peak τ*=3h
│   ├── fig4_barnacle_conflict.pdf/png   Hater extraction, interior optimum
│   └── fig5_lotka_volterra.pdf/png      Creator-hater coexistence
├── code/
│   └── make_figures.py                Generates all 5 figures
└── README.md                          This file
```

## How to compile

```bash
pdflatex paper.tex
pdflatex paper.tex   # twice for refs
```

## How to regenerate figures

```bash
cd code/
python make_figures.py    # → figures/fig1 through fig5
```

Python deps: numpy, matplotlib.

## Citation

Vosteen, H. (2026). *The Platform Has a Food Chain. You Are In It:
An Ecological Model of Attention With Five Rational Agents.* Working Paper.
