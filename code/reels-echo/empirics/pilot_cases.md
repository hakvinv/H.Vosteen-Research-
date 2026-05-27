# Pilot Dataset: Cross-Platform Trend Lag (Documented Cases)

## Method

For each trend, peak dates on TikTok and Instagram Reels are estimated from:
- KnowYourMeme entry timestamps (TikTok origin date)
- Mainstream news coverage peak (proxy for TikTok mass-awareness peak)
- Instagram hashtag aggregator screenshots (when retrievable)
- Reels-focused trend reports (SocialPilot, Later, Ramdam)

**This is a pilot. All Δτ values have ±2 week uncertainty bounds.**
**Method bias: news coverage usually trails TikTok-internal peak by 1–2 weeks, so estimates are conservative lower bounds on the platform-internal peak.**

## Cases

| # | Trend                | TikTok origin | TikTok peak (est) | Reels peak (est) | Δτ (months) | Source                                |
|---|----------------------|---------------|-------------------|------------------|-------------|---------------------------------------|
| 1 | Girl Dinner          | 2023-05-11    | 2023-07-15        | 2023-09-15       | ~2.0        | KYM + WaPo, BonAppetit, Today (Jul 23)|
| 2 | Roman Empire         | 2023-08-15    | 2023-09-20        | 2023-12-01       | ~2.4        | KYM + Vogue Sep 23, Vox Nov 23        |
| 3 | Stanley Cup tumbler  | 2023-11-01    | 2024-01-15        | 2024-04-01       | ~2.5        | Viral Stanley fire video Nov 23, Reels coverage Apr 24 |
| 4 | Mob Wife aesthetic   | 2024-01-08    | 2024-02-10        | 2024-04-20       | ~2.3        | KYM Jan 24, IG Reels trend reports Apr 24 |
| 5 | Wes Anderson POV     | 2023-04-15    | 2023-05-20        | 2023-07-25       | ~2.2        | NYT May 23, Reels coverage Jul-Aug 23 |
| 6 | Tube Girl            | 2023-08-09    | 2023-09-25        | 2023-11-15       | ~1.7        | Sabrina Bahsoon's run, IG late Nov 23 |
| 7 | Demure / Mindful     | 2024-08-04    | 2024-08-25        | 2024-10-20       | ~1.9        | Jools Lebron, Reels reports Oct 24    |
| 8 | Of Course (cat)      | 2024-04-20    | 2024-05-25        | 2024-08-10       | ~2.5        | KYM, Reels reports Aug 24             |

## Summary statistics (N = 8)

- Median Δτ = 2.25 months
- Mean Δτ = 2.19 months
- IQR = [1.95, 2.43] months
- Range = [1.7, 2.5]

## Comparison to model prediction

Theoretical Δτ for typical viral content (β₀s ≈ 0.2 month⁻¹, λ ≈ 0.6) gives:

  Δτ = ln(1/0.6) / 0.2 = 2.55 months

The pilot sample's mean (2.19) and median (2.25) are within 15% of this prediction.

## Caveats — explicit

1. **N is small.** Eight cases is suggestive, not conclusive.
2. **Selection bias.** These are all well-documented mainstream-crossover trends. Trends that died on TikTok (the model's predicted "immune" class) are by construction underrepresented in this sample. Confirmation of the immune-content prediction requires a different sampling frame.
3. **Peak estimation noise.** ±2 weeks per peak gives ±1 month total Δτ uncertainty per case.
4. **Audio vs format.** Audio-only trends (e.g., a single song clip) propagate faster than format trends (e.g., dance routines, narrative templates), because audio is item-level (one DB entry) while format is concept-level (requires creator coordination). This pilot mixes both, which biases estimates toward the format-side.

## What this pilot does and does not establish

**Establishes:**
- Order-of-magnitude consistency between predicted ~2.5m lag and observed mainstream-trend lag.
- A reproducible coding scheme for cross-platform peak estimation from public sources.

**Does not establish:**
- The slope of Δτ vs s (Prediction 1). Requires per-trend engagement-score estimates, which need TikTok Research API.
- The half-life cutoff (Prediction 2). Requires sampling of trends that died on TikTok, not just crossovers.
- The λ-scaling across platforms (Prediction 3). Requires comparable Shorts data.

These remain the targets of the full study using the TikTok Research API
(academic access via vosteen@uni-bremen.de) and Apify-based Reels scraping.
