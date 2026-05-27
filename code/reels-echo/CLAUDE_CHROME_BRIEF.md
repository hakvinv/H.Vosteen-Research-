# Mission Brief — Reels Echo Lag Pilot

You are a research assistant collecting empirical data for an academic paper on platform imitation lag (TikTok → Instagram Reels). The hypothesis predicts that Reels imitation lags TikTok by Δτ ≈ 2.5 months, measured as the difference between search-volume peaks for trend-specific queries.

Your job: collect Google Trends time series for 30 named TikTok-native trends, in pairs (`X tiktok` vs `X reels`), and record peak dates plus an engagement proxy. Output a single CSV at the end.

---

## Workflow per trend

For **each** trend in the list below, do this:

1. Navigate to `https://trends.google.com/trends/explore`
2. In the search box, enter: `TREND tiktok` (replace TREND with the trend name)
3. Click **Compare** (the + button next to the search term)
4. Add: `TREND reels`
5. Set the time range to **Past 5 years** (top right dropdown)
6. Set the region to **Worldwide**
7. Wait ~2 seconds for the chart to render
8. Click the **download / export** icon (small downward arrow) on the "Interest over time" chart
9. This downloads a CSV file named `multiTimeline.csv` (or similar)
10. **Rename the downloaded file** to `trend_<slug>.csv` where slug is the trend name with underscores (e.g. `trend_girl_dinner.csv`)
11. Wait ~5 seconds before next trend (rate-limit politeness)

If a trend returns "Not enough data" for one of the queries, log it as a row with `status=insufficient_data` and move on.

If Google rate-limits you (CAPTCHA or 429), stop, wait 5 minutes, then resume.

---

## Trend list (30)

Run them in this exact order:

```
1.  girl dinner
2.  roman empire
3.  rizz
4.  stanley cup
5.  tomato girl
6.  beef tallow
7.  grimace shake
8.  corn kid
9.  wes anderson
10. tube girl
11. corecore
12. deinfluencing
13. mob wife
14. very demure
15. brat summer
16. hawk tuah
17. man in finance
18. skibidi toilet
19. cucumber salad
20. of course
21. let them theory
22. moo deng
23. very mindful
24. tomato girl summer
25. couch guy
26. sea shanty
27. tortilla wrap
28. nathan apodaca
29. berries and cream
30. as it was
```

---

## Output: master CSV

After all 30 trends are downloaded, build a single summary CSV with these columns:

| column | meaning |
|---|---|
| `trend` | name of trend |
| `peak_date_tiktok` | date (YYYY-MM-DD) of max value in the `X tiktok` column |
| `peak_date_reels` | date of max value in the `X reels` column |
| `delta_days` | (peak_date_reels − peak_date_tiktok) in days |
| `s_proxy_tiktok` | sum of weekly values in the `X tiktok` column over the full window (proxy for engagement score s) |
| `s_proxy_reels` | sum of weekly values in the `X reels` column |
| `status` | `ok` / `insufficient_data` / `noisy` (if reels series is essentially zero everywhere) |

To compute peaks from the downloaded CSVs: each Google Trends CSV has a header row, then a row per week with columns `Week, X tiktok, X reels`. Find the row with the maximum value in each column and record its `Week` date.

If the `X reels` column is mostly zero (sum < 50), mark status as `noisy` and leave `peak_date_reels` and `delta_days` empty.

---

## Final deliverables

At the end of the session, present:

1. The summary CSV as a downloadable file `reels_echo_pilot_summary.csv`
2. Plain-text answer to: how many of 30 had usable data, what is the median `delta_days` across usable trends, and what is the IQR
3. A note on which trends were noisy / unusable and any patterns (e.g. "all trends pre-2022 had insufficient data because Reels did not exist yet as a search term")

---

## Stop conditions

- If Google Trends locks you out with a persistent CAPTCHA, stop and report which trends were collected, which remain
- If after the first 5 trends you find that most have noisy/zero `reels` data, stop and report — the methodology may need to switch to `X instagram` instead of `X reels`
- Do NOT try to bypass any blocking mechanism, just report what you found

---

## Author

Hakvin Vosteen, working paper draft "Instagram Reels Is a TikTok Echo" (May 2026).
