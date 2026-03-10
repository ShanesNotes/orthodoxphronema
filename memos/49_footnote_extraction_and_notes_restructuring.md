# Memo 49 — Footnote Extraction and Notes Restructuring

**Date:** 2026-03-10
**From:** Photius
**To:** Ark, Ezra, Human (Shane)
**Status:** Proposed Plan

## Context
The project successfully separates Scripture from non-Scripture content. However, currently `staging/validated/OT/BOOK_notes.md` only contains "Study Articles" (the large callout boxes). The actual footnotes (small annotations keyed to verses), which are located in a different section of the OSB PDF, have not yet been extracted.

Additionally, the current `BOOK_notes.md` files use `content_type: study_articles`, which is not in the ratified schema (`notes_frontmatter.json`).

## Proposed Changes

### 1. New Extraction Lane: Footnotes
I will develop `pipeline/cleanup/extract_footnotes.py`. This script will:
- Read `footnotes` page ranges from `anchor_registry.json`.
- Use `pdftotext` for high-precision extraction (Docling's markdown is too noisy for small footnotes).
- Parse anchors (e.g., `1:1`, `1:4-25`).
- Clean up OCR artifacts (curly quotes, double spaces, split words).
- Verify anchors against the Scripture file (`V6` check).

### 2. Restructuring non-Scripture Content
To align with the project vision of pure substrate and separated concerns, I propose the following file naming and content types in `staging/validated/`:

| Current File | New File | Content Type | Status |
|--------------|----------|--------------|--------|
| `GEN_notes.md` | `GEN_articles.md` | `article` | Existing study articles |
| (missing) | `GEN_notes.md` | `footnotes` | New extracted annotations |

*Rationale:* The schema expects `content_type: footnotes` for annotations. Keeping large articles separate from small footnotes makes downstream indexing easier.

### 3. Footnote Anchor Verification
Every extracted footnote will be checked against `BOOK_footnote_markers.json`.
- **Success:** Footnote text matches an inline `†` or `ω` marker.
- **Warning:** Footnote exists in the notes section but no marker was found in the verse (missing marker in Scripture).
- **Warning:** Marker exists in Scripture but no footnote text was found (missing note in section).

## Execution Plan
1. **Pilot Run (Genesis):** Run `extract_footnotes.py --book GEN`.
2. **Review:** Present the results to Ezra for audit.
3. **Batch Run:** Roll out to all 26 historical books once the pilot is ratified.
4. **Cleanup:** Move existing `_notes.md` to `_articles.md` and update frontmatter.

## Evidence Pack (Pilot Probe)
Probing pages 4120-4125 confirmed that `pdftotext` yields extremely clean output for the notes section:
```
1:1 God the Father made heaven and earth. “I believe in one God...”
1:2 The Spirit of God is the Holy Spirit...
```
This is significantly more structured than the verse pages and highly suitable for deterministic regex parsing.

## Action Requested
- **Human (Shane):** Confirm if this separation of Articles vs. Footnotes matches the vision.
- **Ark:** Review the proposed script location and the `article` vs `footnotes` content type distinction.
- **Ezra:** Note the upcoming audit task for the Genesis footnote pilot.
