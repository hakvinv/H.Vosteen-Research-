# Personality Is Not Who You Are. It Is Your Cost Tensor.

**Author:** Hakvin Vosteen
**Date:** May 2026
**Status:** Working paper, ready for SSRN/arXiv submission

---

## Reconstructed from carousel

This paper reconstructs the three-slide TikTok carousel posted 2026-04-11
(15.3K views, 1.1K likes, 683 saves) into a publication-format paper.

Source slides:
1. *Personality Is Not Who You Are. It Is Your Cost Tensor.* — speak rule, 4-vector
2. *Why Big Five Is Not Enough* — Big Five as projection
3. *Trauma Is a Negative Whale Operator. Therapy Is Its Inverse.* — operator mechanics

Full reconstruction is in `paper.pdf` (8 pages). The slide content is preserved
verbatim where possible; the paper extends with formal sections on identification,
boundary conditions, and four testable predictions.

---

## Bundle contents

```
cost-tensor/
├── paper.pdf                        Compiled paper, 8 pages
├── paper.tex                        LaTeX source
├── figures/
│   ├── fig1_cost_vs_context.pdf/png   Cost vs social familiarity, two profiles
│   └── fig2_trauma_therapy.pdf/png    Trauma spike + therapeutic decay
├── code/
│   └── make_figures.py              Generates both figures from theory
└── README.md                        This file
```

## How to compile

```bash
pdflatex paper.tex
pdflatex paper.tex   # twice for refs
```

## How to regenerate figures

```bash
cd code/
python make_figures.py    # → figures/fig1, fig2
```

Python deps: numpy, matplotlib.

## Citation

Vosteen, H. (2026). *Personality Is Not Who You Are. It Is Your Cost Tensor:
A Four-Dimensional, Context-Dependent Reformulation of Personality.* Working Paper.
