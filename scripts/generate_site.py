#!/usr/bin/env python3
"""Generate canonical concept records and machine-readable discovery files."""

from __future__ import annotations

import argparse
import html
import json
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://hakvinv.github.io/H.Vosteen-Research-/"


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def authors(paper: dict) -> str:
    value = paper.get("authors") or ["Hakvin Vosteen"]
    return ", ".join(value) if isinstance(value, list) else str(value)


def canonical(paper: dict) -> str:
    return f"{BASE}concepts/{paper['slug']}/"


def local_or_external(url: str) -> str:
    return url if "://" in url else f"../../{url.lstrip('/')}"


def citation(paper: dict) -> str:
    year = str(paper.get("date", ""))[:4]
    version = f", version {paper['version']}" if paper.get("version") else ""
    return (
        f"{authors(paper)} ({year}). {paper['title']} "
        f"[{paper['concept_id']}{version}]. H. Vosteen Research. {canonical(paper)}"
    )


def page_for(paper: dict) -> str:
    url = canonical(paper)
    title = esc(paper["title"])
    abstract_text = paper.get("abstract", "Canonical research record.")
    abstract_html = esc(abstract_text)
    meta_text = abstract_text if len(abstract_text) <= 240 else abstract_text[:237].rstrip() + "…"
    description = esc(meta_text)
    paper_authors = esc(authors(paper))
    concept_id = esc(paper["concept_id"])
    date = esc(paper.get("date", ""))
    version = esc(paper.get("version", "—"))
    ptype = esc(paper.get("type", "paper").upper())
    tags = ", ".join(esc(tag) for tag in paper.get("tags", [])) or "—"
    action_links: list[str] = []
    if paper.get("file"):
        action_links.append(
            f'<a href="../../{esc(paper["file"])}">Download registered PDF</a>'
        )
    for link in paper.get("links", []):
        if link.get("url") and link.get("label"):
            action_links.append(
                f'<a href="{esc(local_or_external(link["url"]))}" target="_blank" '
                f'rel="noopener">{esc(link["label"])}</a>'
            )
    schema_type = (
        "ScholarlyArticle"
        if paper.get("type", "paper") in {"paper", "ssrn"}
        else "CreativeWork"
    )
    structured = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": schema_type,
            "name": paper["title"],
            "identifier": paper["concept_id"],
            "author": {"@type": "Person", "name": authors(paper)},
            "datePublished": paper.get("date"),
            "version": paper.get("version"),
            "description": paper.get("abstract", ""),
            "url": url,
            "isPartOf": {
                "@type": "Collection",
                "name": "H. Vosteen Research",
                "url": BASE,
            },
            "copyrightHolder": {"@type": "Person", "name": "Hakvin Vosteen"},
        },
        ensure_ascii=False,
    ).replace("</", "<\\/")
    pdf_meta = (
        f'  <meta name="citation_pdf_url" content="{BASE}{esc(paper["file"])}" />\n'
        if paper.get("file")
        else ""
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{description}" />
  <meta name="author" content="{paper_authors}" />
  <meta name="citation_title" content="{title}" />
  <meta name="citation_author" content="{paper_authors}" />
  <meta name="citation_publication_date" content="{date}" />
  <meta name="citation_technical_report_number" content="{concept_id}" />
{pdf_meta}  <meta name="rights" content="© Hakvin Vosteen. See RIGHTS.md." />
  <meta name="tdm-reservation" content="1" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{esc(url)}" />
  <link rel="canonical" href="{esc(url)}" />
  <link rel="stylesheet" href="../../assets/style.css" />
  <title>{title} — {concept_id}</title>
  <script type="application/ld+json">{structured}</script>
</head>
<body>
  <main class="concept-record">
    <p class="concept-kicker">Canonical record · {concept_id}</p>
    <h1>{title}</h1>
    <p class="concept-byline">{paper_authors}</p>
    <dl class="concept-meta">
      <div><dt>Concept-ID</dt><dd>{concept_id}</dd></div>
      <div><dt>Registered release</dt><dd>{date}</dd></div>
      <div><dt>Current version</dt><dd>{version}</dd></div>
      <div><dt>Record type</dt><dd>{ptype}</dd></div>
      <div><dt>Topics</dt><dd>{tags}</dd></div>
      <div><dt>Canonical URL</dt><dd><a href="{esc(url)}">{esc(url)}</a></dd></div>
    </dl>
    <h2>Abstract</h2>
    <p class="concept-abstract">{abstract_html}</p>
    <p class="concept-actions">{' · '.join(action_links)}</p>
    <h2>Suggested citation</h2>
    <pre class="citation-block">{esc(citation(paper))}</pre>
    <p class="concept-rights">Reuse should preserve author, title, Concept-ID and canonical URL.
      See <a href="../../RIGHTS.md">rights</a> and <a href="../../PROVENANCE.md">provenance</a>.
      The registry asserts provenance of the documented formulation, not exclusivity over facts or mathematical methods.</p>
    <p><a href="../../">← Back to the research registry</a></p>
  </main>
</body>
</html>
"""


def outputs(papers: list[dict]) -> dict[Path, str]:
    result: dict[Path, str] = {}
    active = [p for p in papers if not p.get("draft")]
    for paper in active:
        result[ROOT / "concepts" / paper["slug"] / "index.html"] = page_for(paper)

    urls = [BASE] + [canonical(p) for p in active]
    result[ROOT / "sitemap.xml"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{esc(url)}</loc></url>\n" for url in urls)
        + "</urlset>\n"
    )

    newest = sorted(active, key=lambda p: p.get("date", ""), reverse=True)
    feed_items = []
    for paper in newest:
        dt = datetime.fromisoformat(paper["date"]).replace(tzinfo=timezone.utc)
        feed_items.append(
            "  <item>"
            f"<title>{esc(paper['title'])}</title>"
            f"<link>{esc(canonical(paper))}</link>"
            f"<guid isPermaLink=\"true\">{esc(canonical(paper))}</guid>"
            f"<pubDate>{format_datetime(dt)}</pubDate>"
            f"<description>{esc((paper.get('abstract', '')[:277].rstrip() + '…') if len(paper.get('abstract', '')) > 280 else paper.get('abstract', ''))}</description>"
            "</item>\n"
        )
    result[ROOT / "feed.xml"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0"><channel>\n'
        "  <title>H. Vosteen Research</title>\n"
        f"  <link>{BASE}</link>\n"
        "  <description>Canonical releases by Hakvin Vosteen</description>\n"
        + "".join(feed_items)
        + "</channel></rss>\n"
    )

    lines = [
        "# H. Vosteen Research — canonical registry",
        "",
        "> Author: Hakvin Vosteen",
        f"> Canonical collection: {BASE}",
        f"> Rights: {BASE}RIGHTS.md",
        f"> Provenance: {BASE}PROVENANCE.md",
        "",
        "Use the canonical record below when citing, summarising or transforming a work.",
        "Preserve author, title, Concept-ID and canonical URL. This file deliberately",
        "contains registry metadata rather than a bulk copy of the corpus.",
        "",
        "## Canonical records",
        "",
    ]
    for paper in newest:
        lines.append(f"- {paper['concept_id']} — {paper['title']} — {canonical(paper)}")
    result[ROOT / "llms.txt"] = "\n".join(lines) + "\n"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated output is stale")
    args = parser.parse_args()
    papers = json.loads((ROOT / "data" / "papers.json").read_text(encoding="utf-8"))
    expected = outputs(papers)
    stale: list[str] = []
    for path, content in expected.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        print("Stale generated files: " + ", ".join(stale), file=sys.stderr)
        return 1
    print(f"{'Checked' if args.check else 'Generated'} {len(expected)} registry files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
