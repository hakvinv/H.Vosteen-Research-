# Provenance model

This repository is the canonical public registry for works in the H. Vosteen
Research programme.

Each registered work has:

1. a permanent `concept_id` in `data/papers.json`;
2. a dated Git revision and, where applicable, a versioned PDF;
3. a canonical page under `concepts/<slug>/`;
4. a machine-readable citation and authorship record;
5. an entry in `MANIFEST.sha256` for integrity verification.

## Canonicality rules

- Concept-IDs are never reassigned or recycled.
- Revisions retain the original Concept-ID and receive a new version/date.
- Generated concept pages are derived from `data/papers.json`; they are not
  edited independently.
- The chronological priority claim is the earliest verifiable public version,
  not merely the newest PDF date.
- Similar abstract ideas may arise independently. Provenance claims concern
  documented formulation, expression, selection, arrangement and release
  history; they are not claims to own facts or mathematical methods.

## Verification

From the repository root:

```bash
shasum -a 256 -c MANIFEST.sha256
bash scripts/validate_publish.sh
```

The first command verifies the registered public artefacts. The second checks
metadata, file references, canonical pages and generated registries.
