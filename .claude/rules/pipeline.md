---
paths:
  - pipeline/**
---

## Pipeline Code — Ark-Owned Architecture

Pipeline code controls the parse → cleanup → validate → promote workflow. Changes here have corpus-wide impact.

BEFORE modifying pipeline code:
1. Write or update a memo in `memos/` documenting the rationale
2. Run validation on test data BEFORE and AFTER the change
3. Batch tools (5+ books) require architecture review

Ownership:
- `pipeline/parse/` — Ark only (parser architecture)
- `pipeline/validate/` — Ark only (validation semantics)
- `pipeline/promote/` — Ark only (promotion gate)
- `pipeline/cleanup/` — Photius may write bounded tools; Ark reviews batch tools

Extraction method selection:
- Scripture pages: Docling (primary)
- Scripture edge cases: pdftotext (sanctioned verifier/fallback)
- Notes/footnotes pages: pdftotext (primary)

Parser/cleanup boundary:
- Verse-boundary recovery → Parse stage
- Study-article separation → Parse stage
- Heading purity → Parse + Validate
- Fused possessives/punctuation → Parse-time normalization
- Bounded fused-word cleanup → Cleanup stage
- Ambiguous OCR/source verification → Cleanup sidecar + human review
