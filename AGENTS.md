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

TikTok-origin pieces are almost always **stubs**, not full papers. A
stub has: short length (≈4 pages), a hook-style title phrased to grab
attention ("Why X...", "X Isn't Y. It's Z.", "How One Thing Does Z"),
sparse page 1 with a single figure, and accompanying
`slide-*.png`/`POST.txt` artifacts. Mark these with `"type": "stub"` in
`data/papers.json`. Longer, conventionally titled working papers without
TikTok artifacts are `"type": "paper"` (default). The site renders the
two types in separate groups.

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
3. **Move** the PDF to that path. Don't copy — move. If a file with the
   same name already exists, bump the version field (see below) and suffix
   the filename `-v2`, `-v3`, etc.
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

## Never do

- Don't edit the HTML/CSS/JS. Only touch `data/papers.json`, `papers/`,
  `sources/`, `code/` and `inbox/`.
- Don't rewrite or summarize the author's abstract beyond light
  copy-editing (trimming trailing whitespace, collapsing double spaces).
- Don't skip the commit — partial state is bad state.
- Don't process files with unresolved issues (broken PDF, unparseable
  YAML). Leave them in `inbox/` and add a note to a new file
  `inbox/_issues.md` describing what went wrong.

## Rollback

Every publish is a single commit, so `git revert <sha>` removes a paper
cleanly. The original PDF stays on disk; only the index entry disappears.
