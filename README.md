# H. Vosteen Research – Download Hub

Statischer GitHub-Pages-Hub für Working Paper & Preprints.
Kein Buildstep, kein Framework – einfach `index.html`, ein bisschen JS und eine JSON-Datei.

## Seite aktivieren (einmalig)

1. Auf GitHub: **Settings → Pages**.
2. Unter *Source* „Deploy from a branch" wählen.
3. Branch `main` (oder der Branch, auf dem die Seite leben soll) und Ordner `/ (root)` auswählen.
4. Speichern. Nach ein paar Minuten ist die Seite unter
   `https://hakvinv.github.io/h.vosteen-research-/` erreichbar.

## Neues Paper hinzufügen

1. PDF in den Ordner `papers/` legen, z. B. `papers/2026-04-tiktok-algorithmen.pdf`.
2. In `data/papers.json` einen neuen Eintrag **oben** einfügen:

```json
{
  "slug": "tiktok-algorithmen",
  "title": "Algorithmen auf TikTok – was wirklich passiert",
  "authors": ["H. Vosteen"],
  "date": "2026-04-21",
  "version": "1.0",
  "abstract": "Kurze Zusammenfassung in 2–3 Sätzen. Taucht direkt auf der Karte auf.",
  "tags": ["social media", "algorithmen"],
  "file": "papers/2026-04-tiktok-algorithmen.pdf"
}
```

3. Commit, push – fertig. GitHub Pages baut neu.

### Feld-Referenz

| Feld       | Pflicht | Beschreibung                                         |
|------------|---------|------------------------------------------------------|
| `slug`     | nein    | Interner Kurzname, wird für BibTeX-Key benutzt.      |
| `title`    | **ja**  | Titel des Papers.                                    |
| `authors`  | nein    | Array von Autor:innen. Default: `["H. Vosteen"]`.    |
| `date`     | **ja**  | ISO-Datum `YYYY-MM-DD` – bestimmt Sortierung.        |
| `version`  | nein    | z. B. `"1.0"`, `"2.1"`. Wird als Badge angezeigt.    |
| `abstract` | nein    | 2–5 Sätze Kurzbeschreibung.                          |
| `tags`     | nein    | Array von Schlagworten für Filter.                   |
| `file`     | nein    | Pfad zur PDF, relativ zum Repo-Root.                 |
| `url`      | nein    | Optional externe URL (statt `file`).                 |
| `bibkey`   | nein    | Eigener BibTeX-Key. Sonst automatisch generiert.     |
| `draft`    | nein    | `true` blendet den Eintrag aus (nützlich für WIP).   |

## Workflow mit LaTeX-Quellen (für dich)

Schick mir einfach:

- die **LaTeX-Datei** (oder ein Zip mit `.tex` + Bildern/Bib), oder
- das **fertig kompilierte PDF**.

Ich lege PDF + Eintrag in `data/papers.json` an und pushe. Wenn du nur die
`.tex` schickst, kompiliere ich das PDF selbst und committe beides. Optional
kann auch die LaTeX-Quelle mit ins Repo unter `sources/<slug>/`, damit
alles nachvollziehbar bleibt.

## Lokale Vorschau

Weil die Seite `data/papers.json` per `fetch` lädt, muss sie über einen
kleinen HTTP-Server laufen (nicht direkt per `file://`):

```bash
python3 -m http.server 8000
# dann http://localhost:8000 im Browser öffnen
```

## Struktur

```
.
├── index.html           # Die Seite
├── assets/
│   ├── style.css        # Styling (Dark/Light automatisch)
│   └── script.js        # Lädt papers.json, Suche/Filter/BibTeX
├── data/
│   └── papers.json      # <-- Hier werden neue Paper eingetragen
├── papers/              # <-- Hier liegen die PDFs
├── sources/             # LaTeX-Quellen (Archiv)
├── code/                # Replikations-Code, je Paper ein Unterordner
├── inbox/               # Drop-Zone fuer neue Paper (siehe AGENTS.md)
├── .github/workflows/   # Pages-Deploy via GitHub Actions
├── .nojekyll            # Damit GitHub Pages nichts umbaut
├── AGENTS.md            # Anleitung fuer LLM-Automation
└── README.md
```
