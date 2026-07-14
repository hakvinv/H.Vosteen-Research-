#!/usr/bin/env python3
"""Generate a stable SHA-256 manifest for public research artefacts."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGETS = ("data", "papers", "sources", "code", "goodies")
OUTPUT = ROOT / "MANIFEST.sha256"


def build() -> str:
    files: list[Path] = []
    for name in TARGETS:
        root = ROOT / name
        if root.exists():
            files.extend(
                p for p in root.rglob("*") if p.is_file() and p.name != ".DS_Store"
            )
    lines = []
    for path in sorted(files, key=lambda p: p.relative_to(ROOT).as_posix()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(ROOT).as_posix()}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            print("MANIFEST.sha256 is stale", file=sys.stderr)
            return 1
        print("Checked MANIFEST.sha256")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"Generated MANIFEST.sha256 with {expected.count(chr(10))} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
