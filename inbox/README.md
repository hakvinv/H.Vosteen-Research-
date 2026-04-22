# Inbox

Drop new papers here. An LLM automation processes this folder on a
schedule, moves files into place, updates the index, and commits.

## How to drop a paper

1. Drag the PDF into this folder.
2. (Optional but recommended) Copy `template.yml`, rename it to match the
   PDF basename, fill in a few fields.
3. (Optional) Include the matching `.tex` file. It'll be archived under
   `sources/` for reproducibility.
4. Push.

## Examples

**Minimal** — just a PDF:
```
inbox/
  cartel-or-creative-destruction.pdf
```

**Full** — PDF plus sidecar plus source:
```
inbox/
  cartel-or-creative-destruction.pdf
  cartel-or-creative-destruction.yml
  cartel-or-creative-destruction.tex
```

See `template.yml` for the available fields.
