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
    for k in ("slug", "title", "file"):
        if k not in p:
            sys.exit(f"paper[{i}] missing required field: {k}")
    if p["slug"] in slugs:
        sys.exit(f"duplicate slug: {p['slug']}")
    slugs.add(p["slug"])
    if not os.path.isfile(p["file"]):
        sys.exit(f"paper[{p['slug']}] file not found: {p['file']}")
    if "type" in p and p["type"] not in ("paper", "essay"):
        sys.exit(f"paper[{p['slug']}] invalid type: {p['type']!r} (expected 'paper' or 'essay')")
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

# 3. Every non-empty code/<slug>/ has a matching Code link in papers.json.
python3 - <<'PY'
import json, os, sys
with open("data/papers.json") as f:
    papers = json.load(f)
has_code_link = {
    p["slug"] for p in papers
    for l in p.get("links", [])
    if l.get("label") == "Code"
}
if os.path.isdir("code"):
    for slug in os.listdir("code"):
        path = os.path.join("code", slug)
        if not os.path.isdir(path): continue
        if not os.listdir(path): continue
        if slug not in has_code_link:
            sys.exit(f"code/{slug}/ has content but no Code link in papers.json")
print("code/ folders reconciled with papers.json")
PY
ok "code/ folders reconciled"

echo
echo "All checks passed."
