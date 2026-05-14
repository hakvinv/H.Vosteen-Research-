#!/usr/bin/env bash
# Post-publish validator. Run after processing inbox/ and before git commit.
# Fails loud on any inconsistency so nothing half-baked gets committed.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail() { echo "FAIL: $*" >&2; exit 1; }
ok()   { echo "OK:   $*"; }

# 1. Inbox contains only the allowlisted scaffolding files.
allowed_inbox="README.md template.yml _issues.md .gitkeep .DS_Store"
shopt -s nullglob
stray=()
for entry in inbox/* inbox/.[!.]*; do
  base="$(basename "$entry")"
  case " $allowed_inbox " in *" $base "*) continue ;; esac
  stray+=("$entry")
done
if (( ${#stray[@]} )); then
  fail "inbox/ not clean: ${stray[*]}"
fi
ok "inbox/ clean"

# 2. data/papers.json parses and every referenced file exists.
python3 - <<'PY'
import json, os, sys
with open("data/papers.json") as f:
    papers = json.load(f)
if not isinstance(papers, list):
    sys.exit("papers.json root must be an array")
slugs = set()
for i, p in enumerate(papers):
    for k in ("slug", "title"):
        if k not in p:
            sys.exit(f"paper[{i}] missing required field: {k}")
    if p["slug"] in slugs:
        sys.exit(f"duplicate slug: {p['slug']}")
    slugs.add(p["slug"])
    ptype = p.get("type", "paper")
    if ptype not in ("paper", "essay", "ssrn"):
        sys.exit(f"paper[{p['slug']}] invalid type: {ptype!r} (expected 'paper', 'essay', or 'ssrn')")
    if ptype == "ssrn":
        if not p.get("links"):
            sys.exit(f"paper[{p['slug']}] ssrn entry must have at least one link")
    else:
        if "file" not in p:
            sys.exit(f"paper[{p['slug']}] missing required field: file")
        if not os.path.isfile(p["file"]):
            sys.exit(f"paper[{p['slug']}] file not found: {p['file']}")
    for j, v in enumerate(p.get("versions", []) or []):
        if "file" in v and not os.path.isfile(v["file"]):
            sys.exit(f"paper[{p['slug']}] versions[{j}] file not found: {v['file']}")
    for link in p.get("links", []):
        if link.get("label") == "Code":
            expected = f"code/{p['slug']}"
            if not os.path.isdir(expected) or not os.listdir(expected):
                sys.exit(f"paper[{p['slug']}] has Code link but {expected}/ missing or empty")
            if p["slug"] not in link.get("url", ""):
                sys.exit(f"paper[{p['slug']}] Code link url does not reference slug")
print(f"papers.json: {len(papers)} entries, all files resolved")
PY
ok "papers.json valid"

# 3. Every Code link in papers.json points at a real, non-empty code/<slug>/.
#    Orphan code/<slug>/ folders (no link) are allowed — keeping the source
#    around without advertising it on the paper card is a deliberate choice.
python3 - <<'PY'
import json, os, sys
with open("data/papers.json") as f:
    papers = json.load(f)
errors = []
for p in papers:
    for l in p.get("links", []):
        if l.get("label") != "Code": continue
        url = l.get("url", "")
        slug = url.rstrip("/").rsplit("/", 1)[-1]
        path = os.path.join("code", slug)
        if not os.path.isdir(path) or not os.listdir(path):
            errors.append(f"paper[{p['slug']}] Code link points to missing/empty {path}")
if errors:
    sys.exit("\n".join(errors))
print("Code links reconciled with code/ folders")
PY
ok "Code links reconciled"

# 4. data/goodies.json (if present) parses and every file resolves.
if [ -f data/goodies.json ]; then
python3 - <<'PY'
import json, os, sys
with open("data/goodies.json") as f:
    goodies = json.load(f)
if not isinstance(goodies, list):
    sys.exit("goodies.json root must be an array")
slugs = set()
for i, g in enumerate(goodies):
    for k in ("slug", "title", "image"):
        if k not in g:
            sys.exit(f"goodie[{i}] missing required field: {k}")
    if g["slug"] in slugs:
        sys.exit(f"duplicate goodie slug: {g['slug']}")
    slugs.add(g["slug"])
    if not os.path.isfile(g["image"]):
        sys.exit(f"goodie[{g['slug']}] image not found: {g['image']}")
print(f"goodies.json: {len(goodies)} entries, all files resolved")
PY
ok "goodies.json valid"
fi

echo
echo "All checks passed."
