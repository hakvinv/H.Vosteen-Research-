# H. Vosteen Research – Canonical Research Registry

Kanonisches, versioniertes Register für Working Papers, Preprints und Essays von
Hakvin Vosteen. Jeder Eintrag besitzt eine stabile Concept-ID, eine eigene
Zitierseite und einen nachvollziehbaren Zeitstempel.

**Öffentliche Registry:** <https://hakvinv.github.io/H.Vosteen-Research-/>

## Nutzung, Zitation und Provenienz

- Zitierhinweise: [`CITATION.cff`](CITATION.cff)
- Rechte und Nutzungsvorbehalt: [`RIGHTS.md`](RIGHTS.md)
- Provenienz- und Versionsmodell: [`PROVENANCE.md`](PROVENANCE.md)
- Hash-Register der veröffentlichten Artefakte: [`MANIFEST.sha256`](MANIFEST.sha256)

Die abstrakten Ideen, Fakten und mathematischen Methoden werden nicht als
exklusives Eigentum beansprucht. Geschützt und attributionserwartend sind die
konkreten Texte, Grafiken, Modellformulierungen sowie Auswahl und Anordnung der
Materialien. Bei wissenschaftlicher oder redaktioneller Nutzung bitte immer den
kanonischen Concept Record nennen und verlinken.

## Neues Paper hinzufügen

1. PDF in `papers/` ablegen.
2. In `data/papers.json` einen Eintrag hinzufügen:

```json
{
  "concept_id": "HVR-2026-023",
  "slug": "tiktok-algorithmen",
  "title": "Algorithmen auf TikTok – was wirklich passiert",
  "authors": ["Hakvin Vosteen"],
  "date": "2026-04-21",
  "version": "1.0",
  "type": "paper",
  "abstract": "Kurze Zusammenfassung.",
  "tags": ["social-media", "algorithmen"],
  "file": "papers/2026-04-21-tiktok-algorithmen.pdf"
}
```

3. Ableitungen und Prüfsummen aktualisieren und validieren:

```bash
python3 scripts/generate_site.py
python3 scripts/generate_manifest.py
bash scripts/validate_publish.sh
```

4. Commit und Push; GitHub Pages validiert erneut und veröffentlicht danach.

### Feld-Referenz

| Feld | Pflicht | Beschreibung |
|---|---:|---|
| `concept_id` | **ja** | Dauerhafte Registry-ID `HVR-YYYY-NNN`; bei Revisionen unverändert. |
| `slug` | **ja** | Stabiler Kurzname und URL-Segment. |
| `title` | **ja** | Titel des Werks. |
| `authors` | nein | Array der Autor:innen; Default `Hakvin Vosteen`. |
| `date` | **ja** | ISO-Datum `YYYY-MM-DD`. |
| `version` | nein | Zum Beispiel `1.0` oder `2.1`. |
| `type` | nein | `paper`, `essay` oder `ssrn`. |
| `abstract` | nein | Kurzbeschreibung. |
| `tags` | nein | Themenfilter. |
| `file` | für Paper/Essay | Relativer Pfad zur PDF. |
| `links` | für SSRN | Externe oder ergänzende Links. |
| `bibkey` | nein | Eigener BibTeX-Key. |
| `draft` | nein | `true` blendet den Eintrag aus. |

## Lokale Vorschau

```bash
python3 -m http.server 8000
# http://localhost:8000
```

## Struktur

```text
.
├── index.html           # Öffentliche Registry
├── concepts/            # Generierte kanonische Seiten je Modell
├── assets/              # Layout und Client-Renderer
├── data/                # Quellen der Registry-Metadaten
├── papers/              # Veröffentlichte PDFs
├── sources/             # Archivierte LaTeX-Quellen
├── code/                # Replikationscode je Paper
├── goodies/             # Öffentliche Visuals
├── inbox/               # Drop-Zone; siehe AGENTS.md
├── scripts/             # Generatoren und Validierung
├── CITATION.cff         # Maschinenlesbarer Zitierhinweis
├── RIGHTS.md            # Rechte- und Nutzungsvorbehalt
├── PROVENANCE.md        # Provenienzmodell
├── MANIFEST.sha256      # Prüfsummen öffentlicher Artefakte
├── robots.txt           # Selektive Crawler-Regeln
└── llms.txt             # Registry- und Zitierregeln für LLM-Zugriffe
```

Ausführliche Automationsregeln stehen in [`AGENTS.md`](AGENTS.md).
