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

This sprint was part of a broader housekeeping session that also included:
- Dossier freshness sweep (76/76 fresh, legacy sidecar fix for ISA/LAM)
- PSA marker repair (131 anchors rebuilt from footnotes.md)
- Memo archival (189 → 32 active memos)
- Ops board cleanup (170 → 116 lines, then further slimmed by Ezra)

## Chain of Thought

### Problem Discovery
Exploration of the 228 companion files (76 footnotes + 62 articles + 76 markers + 14 missing articles) revealed five structural problems:

1. **OT footnote headers were fused inline.** 2,698 of ~5,100 section headers (53%) sat on the same line as the preceding paragraph text. Caused by `pdftotext` output not inserting line breaks before `### CH:V` markers during the original extraction. NT footnotes (extracted later with a cleaner pipeline) were clean.

2. **Marker/footnote alignment was broken.** Only 17/76 books had markers matching footnotes. Root cause: OT markers were derived from `†ω` symbols in scripture text, but those symbols were stripped during canon cleanup. NT markers came from scripture too, but the footnotes were extracted from separate PDF page ranges and covered different verse sets.

3. **Frontmatter drifted from schema.** Articles used `status: staged` (invalid — schema says `staging`), PSA/SIR used `content_type: study_articles` (should be `article`), NT articles used a long-form source string instead of `"OSB-v1"`, and NT articles lacked `book_name`/`promote_date`/`canon_anchors_referenced` fields.

4. **Marker JSON had two schemas.** 48 OT files used a dict envelope with metadata; 28 files (27 NT + WIS) used bare lists. This complicated every tool that needed to load markers.

5. **14 NT books had no article files.** Small epistles with no OSB study articles — but the absence broke inventory completeness.

### Strategy
- **Footnotes.md is authoritative** for anchor truth — it's the extracted OSB footnote content. Markers should be derived from it, not from scripture `†ω` symbols.
- **Schema-first:** fix frontmatter and JSON format before reindexing, so all downstream tools see a consistent shape.
- **Safety invariants:** count anchors before/after every transform. Never change content, only structure.
- **Audit-driven:** build the audit tool first, measure baseline, fix, remeasure.

### Execution Sequence
```
Phase 0: Audit tool + baseline         → established 5 problem categories
Phase 1: Frontmatter normalization     → 62 article files fixed
Phase 2: OT fused header splitting     → 2,698 headers fixed in 48 files
Phase 3: Marker JSON schema unify      → 28 bare-list → dict format
Phase 4: OT marker reindex             → 47 books, 198 → 2,883 markers
Phase 5: NT article sentinel files     → 14 created
Phase 4b: NT marker reindex            → 13 books, 1,938 → 1,667 markers
```

Phase 4b was added after Human directed that footnotes.md should be treated as authoritative for NT books too — the extra markers in scripture don't have corresponding footnote entries and should not inflate the marker count.

## Changes Made

### Phase 0: Audit Tool
- Created `pipeline/cleanup/companion_audit.py` — batch audit of all companion files
- Baseline: 0 frontmatter issues, 2,698 fused headers, 59/76 marker misalignment, 48 dict + 28 bare-list markers, 14 missing article files

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

### Phase 4b: NT Marker Reindex from Footnotes (13 files)
- Rebuilt markers from `*_footnotes.md` anchors for 13 NT books
- Books: MAT, MRK, LUK, JOH, ACT, ROM, 1CO, 2CO, PHP, COL, 1PE, 3JN, REV
- Total NT markers (these 13): 1,938 → 1,667
- 14 already-adequate NT books skipped (GAL, EPH, 1TH, 2TH, 1TI, 2TI, TIT, PHM, HEB, JAS, 2PE, 1JN, 2JN, JUD)
- Added `--all-nt` and `--force` flags to `reindex_markers.py`

### Phase 5: Empty Article Sentinel Files (14 files)
- Created 14 missing NT article files (1PE, 1TH, 1TI, 2CO, 2JN, 2TH, 2TI, 3JN, COL, GAL, HEB, JUD, PHM, PHP)
- All 76 books now have complete companion file sets

## Final State

| Metric | Before | After |
|--------|--------|-------|
| Frontmatter issues | ~77 | **0** |
| Fused section headers | 2,698 | **0** |
| Marker/footnote alignment pass | 17 | **76** |
| Marker/footnote alignment fail | 59 | **0** |
| Marker JSON format (dict) | 48 | **76** |
| Marker JSON format (bare-list) | 28 | **0** |
| Article files | 62 | **76** |
| Missing article files | 14 | **0** |
| Total markers (all 76 books) | ~2,535 | **4,550** |

## Prospective Implementation / Next Steps

### Ready for Phase 3
The companion layer is now structurally clean and can support:
- **R1 extraction** — footnote and article content are ready for outbound citation extraction into R1 JSONL records (Memo 86)
- **Backlink generation** — `pipeline/graph/build_backlinks.py` consumes R1 JSONL citation records to build `metadata/anchor_backlinks/BOOK.CH-V.json` shards
- **Citation graph** — DuckDB graph edges are regenerated from the backlink layer, not directly from marker inventories (Memo 87)

### Deferred Items (for Ezra to route)
1. **Blank-line-interrupted prose** — OT/NT footnotes have single blank lines between continuation paragraphs (pdftotext line-break artifact). ~4,400 instances across 76 files. Low risk to collapse now that headers are properly split, but should be a separate commit with its own verification.
2. **Marker type recovery** — All reindexed markers have `marker: "unknown"`. The original scripture-derived markers (preserved in `original_markers` audit trail) carry the real `†`/`ω` types. A reconciliation script could cross-reference original markers by anchor to recover types where they overlap. Alternatively, defer until Phase 3 when the backlink layer can resolve types from context.
3. **Article body formatting** — Some articles have long single-line paragraphs and OCR artifacts ("Onthe" in MAT, "I n" drop-cap residue). These are cosmetic and low priority relative to structural work, but should be routed through `fix_articles.py` before any article content is surfaced to end users.
4. **39 empty article sentinel files** — These correctly signal "no OSB study articles for this book." If future extraction from other page ranges surfaces articles, these sentinels should be replaced rather than appended to.

### Verification Checklist for Ezra
- [ ] `python3 pipeline/cleanup/companion_audit.py` → 76/76 pass, 0 fail, 0 frontmatter issues
- [ ] `pytest tests/ -q` → 332 passed
- [ ] Spot-check `verify_footnotes.py --book GEN` → 218=218
- [ ] Spot-check `verify_footnotes.py --book MAT` → 280=280
- [ ] Spot-check `verify_footnotes.py --book PSA` → 131=131
- [ ] Confirm `reports/companion_audit.json` is fresh
- [ ] Confirm `memos/INDEX.md` lists this memo
- [ ] Route deferred items 1-4 to appropriate lanes

## Tools Created / Extended

| Script | Purpose | New? |
|--------|---------|------|
| `pipeline/cleanup/companion_audit.py` | Batch audit of all companion files | new |
| `pipeline/cleanup/normalize_companion_frontmatter.py` | Frontmatter normalization | new |
| `pipeline/cleanup/split_fused_footnote_headers.py` | Fused header splitting | new |
| `pipeline/cleanup/unify_marker_schema.py` | Marker JSON schema unification | new |
| `pipeline/cleanup/reindex_markers.py` | `--from-footnotes`, `--all-ot`, `--all-nt`, `--force` | extended |

## Git History (12 commits, all pushed)

```
ce0114f Reindex 13 NT marker files from footnotes.md anchors
4aa427f Add companion purity sprint memo and refreshed audit report
fa9468f Reindex 47 OT marker files from footnotes.md anchors
f80a964 Create 14 missing NT article sentinel files
532cd4e Unify marker JSON schema: convert 28 bare-list files to dict format
af6f6e6 Split 2698 fused footnote headers across 48 OT files
3fcc42e Normalize companion file frontmatter across 62 article files
afc0276 Add companion file audit tool and baseline report
c501e39 Archive 155 completed memos for Phase 3 transition
4c0ae8a Update ops board: dossier sweep done, PSA repair done, repo cleanup resolved
e0917b3 Repair PSA footnote markers: rebuild 131 anchors from footnotes.md
f60af1e Regenerate all 76 dossiers and fix legacy sidecar normalization
```

## Completion Handshake
| Item | Status | Evidence |
|------|--------|---------|
| Files changed | done | 228 companion files + 5 new tools |
| Verification run | done | `companion_audit.py` → 76/76 pass |
| Artifacts refreshed | done | `reports/companion_audit.json` |
| Tests green | done | 332 passed |
| Pushed to GitHub | done | `831192b..ce0114f main -> main` |
| Next owner | `ezra` | Verify checklist, route deferred items, update ops board |
