# Deploy bundle — drop-in replacement for `hakvinv/H.Vosteen-Research-`

This folder is everything you need to push the redesign live on
`hakvinv.github.io/h.vosteen-research-/`. The structure mirrors your existing
repo, so the `inbox/` → `data/papers.json` workflow described in `AGENTS.md`
keeps working unchanged.

## What's in here

```
deploy/
├── index.html              # ← replaces your existing index.html
├── burnout.html            # ← replaces your existing burnout.html
├── assets/
│   ├── style.css           # ← new academic-light theme (replaces existing)
│   ├── script.js           # ← new renderer for the slim card layout
│   └── burnout.js          # ← unchanged from your repo (kept here for completeness)
└── data/, goodies/         # ← bundled local copies so you can preview locally
                              before pushing. DON'T copy these into the repo —
                              your real data/ and goodies/ are already there.
```

## What changed vs. your existing site

| Surface | Was | Now |
|---|---|---|
| Theme | Dark + auto-light, blue→violet gradient accent | Light cream paper, single oxblood accent |
| Type | System sans (16px / 1.55) | Source Serif 4 + Source Sans 3 + JetBrains Mono |
| Paper list | Cards with shadows + hover lift | Flat list, dotted rules, one line per entry |
| Default state | Abstracts always visible | Collapsed; click any entry to expand |
| Year grouping | None (flat date-sort) | Sticky `2026` header, all 2026 grouped under it |
| SSRN entries | Mixed in with the rest | Featured section at the top, oxblood accent border |
| Topic filter | Click chips at top | Same, kept the live filter behavior |
| Search & sort | Top-right of section head | Inline in the topic filter row |
| Cite | Inline BibTeX block | Same; click "Cite" toggles it |
| Goodie cards | Big rounded thumbnails | Slim 4-up grid, italic caption under each |
| Playground | Same vanilla JS canvas math | Same JS, restyled for light theme |

## Deploy steps

1. **Back up your current files** in `hakvinv/H.Vosteen-Research-` (just in case):
   - `index.html`
   - `burnout.html`
   - `assets/style.css`
   - `assets/script.js`

   `assets/burnout.js` is untouched — you don't strictly need to overwrite it,
   but the version in here is identical, so it's safe to copy over too.

2. **Copy these four files into your repo, keeping the same paths:**
   ```
   deploy/index.html         →  index.html
   deploy/burnout.html       →  burnout.html
   deploy/assets/style.css   →  assets/style.css
   deploy/assets/script.js   →  assets/script.js
   ```

3. **Don't touch `data/`, `papers/`, `goodies/`, `sources/`, `code/`, `inbox/`** —
   your existing content stays exactly where it is. The new `script.js` reads
   `data/papers.json` and `data/goodies.json` with the same shape your
   `AGENTS.md` workflow already produces.

4. **Commit + push to `main`.**
   ```bash
   git add index.html burnout.html assets/
   git commit -m "Redesign: academic light theme, slim card layout, SSRN featured"
   git push
   ```

5. GitHub Pages rebuilds (~30 s). Refresh `hakvinv.github.io/h.vosteen-research-/`.

## Local preview before pushing

This `deploy/` folder is self-contained for preview — `data/` and `goodies/`
are bundled in. From the project root:

```bash
cd deploy
python3 -m http.server 8000
# open http://localhost:8000
```

## Compatibility notes

- **CSS variables are aliased.** The new `style.css` exposes the legacy var
  names (`--text`, `--text-dim`, `--accent`, `--accent-2`, `--border`,
  `--danger`) that your existing `assets/burnout.js` reads via
  `getComputedStyle`. The playground canvas picks up the new oxblood + navy
  palette automatically — no JS change needed.

- **Element IDs preserved.** `burnout.html` keeps every ID the JS expects
  (`#obs-a`, `#obs-canvas`, `#hd-rho0`, …). It's effectively your existing
  file with new outer chrome.

- **Templates in `index.html`** — the new `script.js` looks for
  `#paper-template`, `#ssrn-template`, `#year-template`, `#goodie-template`,
  plus the containers `#paper-list`, `#ssrn-list`, `#ssrn-section`,
  `#topics-filter`, `#goodies-grid`. They're all wired up in `index.html`.

- **No new build step.** Pure HTML / CSS / vanilla JS, just like before.
  Google Fonts loaded over CDN — works offline-degraded (falls back to
  Charter / system serif).

## Reverting

Every change lives in 4 files. To roll back, restore the four files from
your previous commit:

```bash
git checkout <prev-sha> -- index.html burnout.html assets/style.css assets/script.js
git commit -m "Revert redesign"
git push
```
