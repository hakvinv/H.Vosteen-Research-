# AGENTS.md

Instructions for any LLM automation (Claude, Cursor background agent, cron
job, etc.) that periodically processes new papers on this repo.

## Purpose

H. Vosteen drops new working papers into `inbox/` whenever he finishes one.
Your job is to turn each inbox item into a properly indexed entry on the
public site (https://hakvinv.github.io/h.vosteen-research-/).

## Trigger

Run whenever `inbox/` is non-empty. Ignore hidden files (`.gitkeep`,
`.DS_Store`, etc.) and the `inbox/README.md`.

## Two content types

This repo holds two kinds of items:

- **Working papers** — PDFs, indexed in `data/papers.json`, served from
  `papers/`, optional source under `sources/`, optional code under
  `code/<slug>/`.
- **Goodies** — images (PNG/JPG/SVG) for the public download section,
  indexed in `data/goodies.json`, served from `goodies/`.

Decide based on the inbox file's extension: `.pdf` → paper, image → goodie.

## Expected inbox contents

Each paper appears in one of two shapes:

1. **PDF-only** — just `something.pdf`. Fall back to filename-derived slug,
   today's date, and `title` = PDF metadata title (or filename, beautified).
2. **PDF + sidecar YAML** — `something.pdf` and `something.yml` with the
   same basename. The YAML overrides any auto-detected fields. See
   `inbox/template.yml` for the full schema.

Optionally a `.tex` file with the same basename can be present; if so,
archive it alongside the PDF under `sources/<slug>.tex` so the source is
preserved.

Papers may arrive with TikTok-specific styling (dark page background,
white text — `\pagecolor[HTML]{0d1117}` + `\color{white}` in the `.tex`,
often alongside `slide-*.png` exports and a `POST.txt` caption). These
are for social media only. **The archived version on the site must be
the normal white-background rendering.** Before archiving:

- Strip `\pagecolor{...}` and `\color{white}` from the `.tex`.
- Recompile to regenerate a white-background PDF (do not publish the
  supplied dark PDF).
- Ignore `slide-*.png` and `POST.txt` — do not archive them anywhere.

Bundle `.tex` files often contain a "Code" line like
`\textbf{Code.} Replication code at \url{https://github.com/hakvinv/<some-repo>}.`
pointing to a standalone repo that does **not** exist. Strip that line
before archiving and recompile. The Code button on the paper card
(populated from `links` in `papers.json`) is the canonical pointer to
`code/<slug>/` in this repo.

TikTok-origin pieces are almost always **essays**, not full papers. A
theory essay has: short length (≈4 pages), a hook-style title phrased
to grab attention ("Why X...", "X Isn't Y. It's Z.", "How One Thing
Does Z"), sparse page 1 with a single figure, theorem + proof sketch +
corollary wrapped in explainer prose, empirical anchors, and
accompanying `slide-*.png`/`POST.txt` artifacts. Mark these with
`"type": "essay"` in `data/papers.json`. Longer, conventionally titled
working papers without TikTok artifacts are `"type": "paper"`
(default). The site renders the two types in separate groups.

Bundles dropped in a single subfolder (e.g.
`inbox/all_posts_kw_YYYY-MM-DD/<paper>/`) are allowed and should be
processed as one publish batch.

Optionally a `code/` subdirectory can be bundled alongside the paper
(either as a `<slug>_code/` folder dropped into the inbox, or a zip
archive). Move its contents to `code/<slug>/`. When a non-empty
`code/<slug>/` exists after processing, automatically append
`{"label": "Code", "url": "https://github.com/hakvinv/h.vosteen-research-/tree/main/code/<slug>"}`
to the paper's `links` array (unless a `links` entry with label `Code`
already exists).

## Processing steps (for each paper)

1. **Derive a slug**: lowercase, kebab-case, max 48 chars, stripped of
   punctuation. Either taken from the YAML `slug` field, or derived from
   the filename minus any leading date prefix.
2. **Derive a filename**: `papers/<YYYY-MM-DD>-<slug>.pdf`. The date is the
   YAML `date` field, falling back to today's date in UTC.
3. **Move** the PDF to that path. Don't copy — move. If a paper with
   the same slug already exists in `data/papers.json` (revision, not a
   new piece), this is a **version bump**, not a new card:
   - New filename: `papers/<YYYY-MM-DD>-<slug>-v2.pdf` (`-v3`, …).
   - Update the existing JSON entry in place: bump `version`, replace
     `date` and `file`, refresh the abstract.
   - Append the **previous** version to a `versions` array on the same
     entry (newest first), with `version`, `date`, `file`, and a
     short one-line `note` describing the change. The site renders
     this as an "Earlier version" disclosure under the abstract.
   - Keep the old PDF on disk — don't delete it.
4. **Archive** an accompanying `.tex` (if present) as `sources/<slug>.tex`.
5. **Append** a JSON object to `data/papers.json` (at the **top** of the
   array, so newest comes first). Use this shape:

   ```json
   {
     "slug": "cartel-schumpeter",
     "title": "Cartel or Creative Destruction?",
     "authors": ["Hakvin Vosteen"],
     "date": "2026-04-22",
     "version": "1.0",
     "type": "paper",
     "abstract": "...",
     "tags": ["industrial-organization", "spectral"],
     "file": "papers/2026-04-22-cartel-schumpeter.pdf",
     "bibkey": "vosteen2026cartel"
   }
   ```

   Fields and defaults are documented in `README.md`. Missing fields:
   prefer empty over invented. The `abstract` field is the one exception —
   if the YAML doesn't supply one, try to extract the first paragraph of
   the PDF's abstract. If you can't get one, leave it out (the UI handles
   it gracefully).
6. **Delete** the processed files from `inbox/`. Only `rm` files that you
   have actually consumed (PDF, YAML, tex). Never `rm -rf` a subfolder
   like `inbox/code/` — move its contents to the destination first
   (`code/<slug>/`), then `rmdir` the now-empty folder. If something is
   unclear, leave it in `inbox/` and add a note to `inbox/_issues.md`.
7. **Validate** by running `scripts/validate_publish.sh`. It checks that
   `inbox/` is back to scaffolding only, `data/papers.json` parses and
   every `file` path exists, and every non-empty `code/<slug>/` has a
   matching Code link (and vice versa). Do not commit if it fails.
8. **Commit** with message
   `Publish <n> paper(s): <comma-separated titles>` and push to `main`.
   The GitHub Pages workflow handles deployment.

## Processing steps for goodies (images)

For each `.png`/`.jpg`/`.jpeg`/`.svg` in `inbox/`:

1. **Slug** from YAML or filename (kebab-case, no extension).
2. **Move** the image to `goodies/<slug>.<ext>`.
3. **Append** an entry to `data/goodies.json` (newest first):
   ```json
   {
     "slug": "neurotransmitter-tier-list",
     "title": "Neurotransmitter Tier List",
     "description": "Optional caption.",
     "date": "2026-04-23",
     "tags": ["neuroscience", "tier-list"],
     "image": "goodies/neurotransmitter-tier-list.png"
   }
   ```
4. **Delete** processed files from `inbox/`.
5. Same commit-and-push convention as for papers.

## Never do

- Don't edit the HTML/CSS/JS. Only touch `data/papers.json`,
  `data/goodies.json`, `papers/`, `goodies/`, `sources/`, `code/` and
  `inbox/`.
- Don't rewrite or summarize the author's abstract beyond light
  copy-editing (trimming trailing whitespace, collapsing double spaces).
- Don't skip the commit — partial state is bad state.
- Don't process files with unresolved issues (broken PDF, unparseable
  YAML). Leave them in `inbox/` and add a note to a new file
  `inbox/_issues.md` describing what went wrong.

## Rollback

Every publish is a single commit, so `git revert <sha>` removes a paper
cleanly. The original PDF stays on disk; only the index entry disappears.
