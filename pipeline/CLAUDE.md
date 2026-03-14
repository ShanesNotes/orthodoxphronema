# Pipeline — Core Processing Architecture

Ark-owned. Changes here affect the entire corpus.

## Workflow
`src.texts/osb.pdf` → parse → raw → validate (V1-V8) → validated → promote → `canon/`

## Before Any Change
1. Document rationale in a `memos/` file BEFORE implementing
2. Test on staging data before and after
3. Batch tools (5+ books) require Ark architecture review

## Extraction Methods
- Scripture: Docling (primary), pdftotext (edge-case verifier)
- Notes/footnotes: pdftotext (primary)

## Subdir Ownership
- `parse/` — Ark only
- `validate/` — Ark only
- `promote/` — Ark only
- `cleanup/` — Photius (bounded); Ark reviews batch tools
