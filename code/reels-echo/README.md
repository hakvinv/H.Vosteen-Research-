# Instagram Reels Is a TikTok Echo — Paper Bundle

**Author:** Hakvin Vosteen
**Date:** May 2026
**Version:** v2 (with empirical pilot, N=8)
**Status:** Pre-submission draft, awaiting full empirical replication

---

## What's in this bundle

```
reels-echo/
├── Vosteen_2026_Instagram_Reels_TikTok_Echo_v2.pdf    Main paper, 10 pages
├── Vosteen_2026_Instagram_Reels_TikTok_Echo_v2.tex    LaTeX source
├── figures/                                            All 5 figures (PDF + PNG @ 300dpi)
│   ├── fig1_format_size.pdf/png       Stylised diffusion curves
│   ├── fig2_lag_vs_engagement.pdf/png Lag as function of engagement
│   ├── fig3_sensitivity.pdf/png       Sensitivity surface
│   ├── fig4_threshold.pdf/png         Half-life threshold visualisation
│   └── fig5_pilot_vs_prediction.pdf/png  Pilot data overlay on theory
├── code/
│   ├── make_figures.py                Generates fig1 + fig2 from theory
│   └── pilot_data.csv                 (placeholder, see empirics/)
├── empirics/
│   ├── analysis.py                    Pilot summary + sensitivity + threshold
│   ├── pilot_dataset.csv              N=8 manually-documented crossovers
│   ├── pipeline.py                    Scaffold for full empirical study
│   └── pilot_cases.md                 Notes on the 8 pilot trends
├── CLAUDE_CHROME_BRIEF.md             Drop-in prompt for Claude in Chrome
│                                       to scale pilot N=8 → N=30 via Google Trends
└── README.md                          This file
```

---

## How to read this

The paper has three layers of evidence:

1. **Theory** (Sections 1–6). Closed-form derivation of `Δτ = ln(1/λ) / (β₀s)` from a contagion model on top of a social-graph low-pass filter. Stackelberg game gives the strategic logic. No data needed.
2. **Pilot** (Section 7). N=8 manually-documented TikTok→Reels crossover trends. Median Δτ = 2.25 months, against the model's prediction of 2.5. See `empirics/pilot_dataset.csv` and `empirics/analysis.py`.
3. **Replication protocol** (Section 8). Pre-registered design for the full empirical study using TikTok Research API + Apify Reels scraper, N≥100, hashtag-level daily counts. Scaffold in `empirics/pipeline.py`.

---

## How to compile

```bash
cd reels-echo/
pdflatex Vosteen_2026_Instagram_Reels_TikTok_Echo_v2.tex
pdflatex Vosteen_2026_Instagram_Reels_TikTok_Echo_v2.tex   # twice for refs
```

Requires: standard LaTeX with `amsmath`, `graphicx`, `hyperref`, `booktabs`, `enumitem`, `geometry`. No `microtype` (incompatible with Computer Modern).

Figures are pre-rendered in `figures/`. To regenerate:

```bash
cd code/
python make_figures.py            # → figures/fig1, fig2

cd ../empirics/
python analysis.py                # → figures/fig3, fig4, fig5
```

Python deps: `numpy`, `pandas`, `matplotlib`. Nothing exotic.

---

## How to scale the pilot to N=30 (this weekend)

The pilot has N=8. To get the empirical section publication-ready, you want N≥30.

Open Claude in Chrome, paste in `CLAUDE_CHROME_BRIEF.md`, and let it run for ~2 hours. It collects Google Trends time series for 30 named TikTok-native trends as `X tiktok` vs `X reels` pairs and produces a summary CSV.

Then merge that CSV into `empirics/pilot_dataset.csv` and rerun `analysis.py`. The fig5 plot updates automatically.

Expected: median Δτ stays in the 60–90 day band, regression of `log Δτ ~ log s` gives slope near −1.

---

## Submission targets

| Where | Format | Status |
|---|---|---|
| SSRN | this PDF, JEL D43, L13, L86 | ready after empirical N=30 |
| arXiv (cs.CY or econ.GN) | this PDF | ready now |
| Gumroad | this PDF + bundle | ready now |
| Working paper on hakvinv.github.io | this PDF + bundle | ready now |

---

## Citation

Vosteen, H. (2026). *Instagram Reels Is a TikTok Echo: A Stackelberg Imitation Model of Platform Convergence.* Working Paper.

---

## Notes for next iteration

- `λ ≈ 0.6` for Reels is taken from Meta's public 2022 systems paper. Production weights are likely user-dependent.
- The model treats `β₀s` as exogenous. In reality engagement depends on platform composition, so the estimate `Δτ ≈ 2.5m` is an upper bound on the structural component.
- Prediction 4 (authenticity moat) needs dialect/region-tagged data — the TikTok Research API exposes country and language fields.
- After the empirical study, the natural follow-up paper is "Where Reels Wins": cases where `Δτ ≪ 2.5m` (e.g. India after the TikTok ban) — the model predicts these are network-advantage-converted lags.
