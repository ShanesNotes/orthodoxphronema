# Companion Purity & Formatting Sprint — 2026-03-13

**Author:** `ark`
**Type:** `implementation`
**Status:** `done`
**Scope:** `companion file purity`
**Workstream:** `canon-hygiene`
**Phase:** `2`
**Supersedes:** `none`
**Superseded by:** `none`

## Context

All 76 books are promoted to `canon/`. Before Phase 3 (hyperlinking & citation graph), the companion layer (`*_footnotes.md`, `*_articles.md`, `*_footnote_markers.json`) needed structural and formatting cleanup so it's reliable when backlink and citation work begins.

## Objective

Audit and repair all 214 companion files (76 footnotes + 62→76 articles + 76 markers) across the entire canon.

## Changes Made

### Phase 0: Audit Tool
- Created `pipeline/cleanup/companion_audit.py` — batch audit of all companion files
- Baseline: 0 frontmatter issues, 2698 fused headers, 59/76 marker misalignment, 48 dict + 28 bare-list markers, 14 missing article files

### Phase 1: Frontmatter Normalization (62 files)
- `content_type: study_articles` → `article` in PSA, SIR articles
- `source:` long-form → `"OSB-v1"` in 15 article files
- `status: staged` → `staging` in all 62 article files
- Added `book_name`, `promote_date`, `canon_anchors_referenced` to 13 NT article files

### Phase 2: OT Fused Header Splitting (48 files)
- Split 2,698 fused footnote headers across 48 OT files
- Every `### CH:V` now starts on its own line with blank separator
- Anchor counts verified unchanged before/after for all files
- NT confirmed clean (0 fused headers)

### Phase 3: Marker JSON Schema Unification (28 files)
- Converted 27 NT + WIS bare-list marker files to dict format
- All 76 markers now share `{book_code, reindex_date, marker_count, markers}` schema
- Each migrated marker carries `source: "migrated_from_bare_list"` provenance

### Phase 4: OT Marker Reindex from Footnotes (47 files)
- Rebuilt markers from `*_footnotes.md` anchors for 47 OT books
- Total OT markers: 198 → 2,883
- Marker type set to `"unknown"` (type recovery deferred to Phase 3)
- Original markers preserved as `"original_markers"` audit trail
- 1ES skipped (already adequate at 27/27), PSA skipped (already fixed)

### Phase 5: Empty Article Sentinel Files (14 files)
- Created 14 missing NT article files (1PE, 1TH, 1TI, 2CO, 2JN, 2TH, 2TI, 3JN, COL, GAL, HEB, JUD, PHM, PHP)
- All 76 books now have complete companion file sets

## Before / After

| Metric | Before | After |
|--------|--------|-------|
| Frontmatter issues | ~77 | 0 |
| Fused section headers | 2,698 | 0 |
| Marker/footnote alignment pass | 17 | 64 |
| Marker/footnote alignment fail | 59 | 12 |
| Marker JSON format (dict) | 48 | 76 |
| Marker JSON format (bare-list) | 28 | 0 |
| Article files | 62 | 76 |
| Missing article files | 14 | 0 |
| Total OT markers | 198 | 2,883 |

## Remaining 12 Misaligned Books (NT)

These have more markers in scripture than footnotes — the gap is missing footnote entries, not a formatting issue. Requires PDF re-extraction, not marker repair.

| Book | Markers Only | Footnotes Only | Net |
|------|-------------|----------------|-----|
| ACT | 100 | 20 | -80 |
| MRK | 67 | 4 | -63 |
| LUK | 61 | 26 | -35 |
| MAT | 53 | 36 | -17 |
| JOH | 43 | 18 | -25 |
| REV | 24 | 17 | -7 |
| ROM | 20 | 24 | +4 |
| 1PE | 5 | 14 | +9 |
| 1CO | 11 | 11 | 0 (diff sets) |
| COL | 5 | 6 | +1 |
| PHP | 4 | 6 | +2 |
| 3JN | 1 | 2 | +1 |

## Explicitly Deferred

1. **Blank-line-interrupted prose** — OT/NT footnotes have single blank lines between continuation paragraphs (pdftotext artifact). Defer until fused header fix is proven stable.
2. **NT footnote gap recovery** — ACT, MRK, LUK, JOH, MAT need re-extraction from PDF.
3. **Article body reformatting** — Some articles have long single-line paragraphs. Cosmetic.
4. **Marker type recovery** — `†`/`ω` types cannot be recovered from footnotes alone. Deferred to Phase 3.

## Validation

- `pytest tests/ -q` → 332 passed
- `companion_audit.py` → 0 frontmatter issues, 0 fused headers, 64/76 aligned
- `verify_footnotes.py --book GEN` → markers=218 = footnotes=218
- `verify_footnotes.py --book RUT` → markers=22 = footnotes=22
- `verify_footnotes.py --book PSA` → markers=131 = footnotes=131

## Tools Created

| Script | Purpose |
|--------|---------|
| `pipeline/cleanup/companion_audit.py` | Batch audit of all companion files |
| `pipeline/cleanup/normalize_companion_frontmatter.py` | Frontmatter normalization |
| `pipeline/cleanup/split_fused_footnote_headers.py` | Fused header splitting |
| `pipeline/cleanup/unify_marker_schema.py` | Marker JSON schema unification |
| `pipeline/cleanup/reindex_markers.py` (extended) | `--from-footnotes` and `--all-ot` modes |

## Completion Handshake
| Item | Status |
|------|--------|
| Files changed | done |
| Verification run | done |
| Artifacts refreshed | done (`reports/companion_audit.json`) |
| Tests green | done (332 passed) |
| Next owner | Phase 3 implementation (Ark) or NT footnote re-extraction (future sprint) |
