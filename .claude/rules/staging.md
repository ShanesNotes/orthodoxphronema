---
paths:
  - staging/validated/**
---

## Staging Validated — Evidence-Gated Writes

Single staged scripture artifact per book. Source of truth for pre-promotion work.

BEFORE modifying any validated book:
1. Check anchor integrity (V1 uniqueness)
2. Verify chapter count (V2) and sequence (V3)
3. Confirm no article bleed (V5)
4. Run: `python3 pipeline/validate/run_validators.py staging/validated/{OT,NT}/BOOK.md`

Evidence-packaging requirement for ALL staged fixes:
- Source page reference (OSB PDF page number)
- Affected anchors (verse list)
- Validator result before/after
- Brief rationale

Ownership:
- Ark: full access
- Photius (Gemini Flash 3.0): bounded write for recovery (evidence-packaged)
- Ezra: full access (sunset path — may be phased out)

Companion files that may sit beside staged scripture:
- `BOOK_articles.md`, `BOOK_footnotes.md` — study content (also mirrored in `study/`)
- `BOOK_footnote_markers.json` — marker trace
- `BOOK_dropcap_candidates.json`, `BOOK_editorial_candidates.json` — edge-case tracking
- `BOOK_residuals.json` — remaining issues
