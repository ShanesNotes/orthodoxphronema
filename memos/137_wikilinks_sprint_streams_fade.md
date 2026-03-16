# Wikilinks Engineering Sprint — All Streams — 2026-03-15

**Author:** `ark`
**Type:** `implementation`
**Status:** `implemented`
**Scope:** Full wikilinks sprint: schema, enrichment, bundle builder, audit, conversion, remediation
**Workstream:** `phase3-wikilinks`
**Phase:** `3`
**Supersedes:** `none`
**Superseded by:** `none`

## Context

Design doc `research/wikilinks_context_injection_design.md` specifies three-layer resolution: knowledge graph (routing) → backlink shards (storage) → pericope bundles (delivery). The backlink shard layer (Layer 2) needed enrichment with verse text, pericope context, and depth metadata to support the bundle builder (Layer 3, Stream D).

## What Was Done

### Stream F: 1CH Closure
- Verified no orphaned wikilinks target 1CH.1:43-54 (full repo search: zero matches).
- `promote.py --book 1CH --dry-run` passes all gates.
- Closure recorded in memo 135.

### A1: Schema Fix (`schemas/anchor_backlinks.json`)
- Rewrote to match actual v1 shard structure.
- Old schema had stale fields (`type`, `source_ref`, `entity`, `service`, `usage`, `author`, `work`) that no shard ever used.
- Corrected schema has: `anchor_id`, `canon_uri`, `text_tradition`, `generated_at`, `generator_version`, `links[]` with `source_file`, `line_number`, `raw_match`, `reference_type`, `context`.

### A2: v2 Schema (`schemas/anchor_backlinks_v2.json`)
- Superset of corrected v1. New fields:
  - `schema_version`: `"v2"` (const)
  - `verse_text`: canon verse text (anchor prefix stripped)
  - `pericope`: `{id, title, range, liturgical_use[]}` or `null`
  - `topic_threads`: `string[]` (initially `[]`)
  - `depth_available`: `int 1-4`

### A3: Enrichment Engine (`pipeline/graph/enrich_backlink_shards.py`)
- Loads 35,996 canon verses from `canon/{OT,NT}/*.md`
- Builds reverse pericope map from `metadata/pericope_index/*.json` (205,326 anchor mappings)
- Scans study layer to determine depth_available per book
- Enriches each v1 shard to v2 in-place
- Idempotent (skips already-v2 shards)
- Built-in spot-check on 5 anchors after enrichment
- CLI: `python3 pipeline/graph/enrich_backlink_shards.py [--domain study] [--dry-run]`

### A4: Enrichment Run
- All 6,094 study shards enriched to v2.
- Spot-checks: GEN.1:1 ✓, JOH.1:1 ✓, ROM.5:12 ✓ (PSA.50:1 and REV.1:1 have no study shards — expected).
- Idempotency verified (re-run: 0 enriched, 6,094 already v2).
- `regenerate_graph.py` backward compatible (ran successfully, DuckDB 6.3→11.3MB).

### Reference Domain Extension
- Extended `build_backlinks.py:detect_domain()` to handle `reference/` paths → `"reference"` domain.
- Prepares for Stream C (reference layer wikilink conversion).

## Files Changed (Full Session)

| File | Action |
|---|---|
| `schemas/anchor_backlinks.json` | Rewritten to match actual v1 structure |
| `schemas/anchor_backlinks_v2.json` | NEW — enriched shard schema |
| `pipeline/graph/enrich_backlink_shards.py` | NEW — enrichment engine |
| `pipeline/graph/build_pericope_bundle.py` | NEW — Layer 3 bundle builder |
| `pipeline/reference/audit_wikilinks_v2.py` | NEW — project-wide audit with orphan detection |
| `pipeline/graph/rebuild_all_backlinks.sh` | NEW — full pipeline rebuild script |
| `pipeline/graph/build_backlinks.py` | Extended `detect_domain()` for `reference/` |
| `metadata/anchor_backlinks/study/*.json` | 6,094 files enriched to v2 |
| `metadata/graph/phronema_graph.duckdb` | Regenerated with v2 shards |
| `research/bundle_pilot/*.json` | 4 pilot bundles (GEN.P001 × 4 presets) |
| `study/articles/OT/{DAN,EXO,JER,JOB}_articles.md` | OCR fused-digit orphan fixes |
| `study/footnotes/OT/JOB_footnotes.md` | JON.1:17 → JON.2:1 versification fix |
| `staging/validated/OT/JOB_footnotes.md` | JON.1:17 → JON.2:1 versification fix |
| `study/lectionary-notes/**/*.md` | 19 bare refs converted to wikilinks |
| `staging/validated/**/*_*.md` | 6 bare refs converted |
| `reports/wikilink_audit_v2.json` | NEW — project-wide audit report |
| `memos/135_memo134_review_and_dossier_refresh.md` | 1CH closure note added |

## Completion Handshake

| Item | Status | Evidence |
|---|---|---|
| Files changed | done | 2 schemas, 5 new scripts, 1 edit, 6,094 shards enriched, 4 pilot bundles, orphan fixes, 25 bare ref conversions |
| Verification run | done | dry-run, enrichment, idempotency, schema validation, graph regen, pilot test, audit v2 |
| Artifacts refreshed | done | DuckDB graph regen'd; audit report at `reports/wikilink_audit_v2.json`; dossiers unaffected |
| Remaining known drift | minor | Backlink shards need rebuild after B+C to capture new wikilinks (`rebuild_all_backlinks.sh` ready) |
| Next owner | ark | Run `rebuild_all_backlinks.sh` after agent sessions complete |

### Stream D: Pericope Bundle Builder

**D1. `pipeline/graph/build_pericope_bundle.py`:**
- Loads canon text for verse ranges from `canon/{OT,NT}/*.md`
- Extracts footnotes from `study/footnotes/` matching verse ranges via `### CH:V` headings
- Extracts article sections from `study/articles/` matching verse ranges via `*(after BOOK.CH:V)*` markers
- Resolves cross-references: scans outgoing wikilinks from footnotes/articles, looks up enriched shards
- Applies token budget truncation (canon text always included, cross-refs truncated first)
- CLI: `python3 pipeline/graph/build_pericope_bundle.py GEN.P001 [--preset devotional] [--all-presets] [--output-dir DIR]`

**D2. Four depth levels implemented:**
| Depth | Content | Implementation |
|---|---|---|
| 1 | Verse text only | Canon text extracted, cross-refs have verse_text only |
| 2 | + footnote + article + pericope framing | Study material extracted for range |
| 3 | + graph neighborhood (all cross-refs) | Higher max_cross_refs ceiling |
| 4 | + patristic (stubbed) | Same as 3 until patristic domain populated |

**D3. Four presets implemented:**
| Preset | depth | token_budget | max_cross_refs |
|---|---|---|---|
| quick | 1 | 1,000 | 4 |
| devotional | 2 | 4,000 | 12 |
| study | 3 | 8,000 | 24 |
| phronema | 4 | 16,000 | 50 |

**D4. GEN.P001 pilot results:**
| Preset | Tokens | Budget | Cross-refs | Notes |
|---|---|---|---|---|
| quick | 1,235 | 1,000 | 0 | Canon alone exceeds budget (37 verses); no refs truncated — correct |
| devotional | 3,681 | 4,000 | 12 | Under budget; theologically relevant refs (JOH.1:1, ISA.6:1, PSA.2:7) |
| study | 4,688 | 8,000 | 23 | All 23 unique outgoing links included |
| phronema | 4,688 | 16,000 | 23 | Same as study (patristic domain empty) |

Cross-reference quality verified: JOH.1:1 (Logos/creation), JOH.19:30 (Sabbath rest), MAT.11:28 (rest in Christ), ISA.63:16 (Father as Redeemer), HEB.1:8 (Son as God), LUK.1:35 (Annunciation), MAT.3:16 (Theophany). All drawn from OSB footnotes/articles for GEN.1-2.

## Files Changed (Updated)

| File | Action |
|---|---|
| `schemas/anchor_backlinks.json` | Rewritten to match actual v1 structure |
| `schemas/anchor_backlinks_v2.json` | NEW — enriched shard schema |
| `pipeline/graph/enrich_backlink_shards.py` | NEW — enrichment engine |
| `pipeline/graph/build_pericope_bundle.py` | NEW — Layer 3 bundle builder |
| `pipeline/graph/build_backlinks.py` | Extended `detect_domain()` for `reference/` |
| `metadata/anchor_backlinks/study/*.json` | 6,094 files enriched to v2 |
| `metadata/graph/phronema_graph.duckdb` | Regenerated with v2 shards |
| `research/bundle_pilot/*.json` | 4 pilot bundles (GEN.P001 × 4 presets) |
| `memos/135_memo134_review_and_dossier_refresh.md` | 1CH closure note added |

### Stream E: Wikilink Audit v2

**E1. Built `pipeline/reference/audit_wikilinks_v2.py`:**
- Project-wide scan across staging/, study/, reference/ (600 files)
- Orphan detection: validates every `[[BOOK.CH:V]]` against registry CVC
- Range validation: checks `[[BOOK.CH:V]]-W` end verse exists
- Bare ref detection: counts unconverted references
- Per-domain statistics
- CLI: `python3 pipeline/reference/audit_wikilinks_v2.py [--report reports/wikilink_audit_v2.json]`

**E2. Orphan fixes applied (5 of 8 original orphans fixed):**
- `LUK.21:2528` → `[[LUK.21:25]]-28` (OCR fused digits, DAN_articles.md)
- `EZK.37:2628` → `[[EZK.37:26]]-28` (OCR fused digits, EXO_articles.md)
- `HEB.11:3238` → `[[HEB.11:32]]-38` (OCR fused digits, JER_articles.md)
- `JON.1:17` → `[[JON.2:1]]` (LXX versification, JOB footnotes ×2)
- `PSA.111:16` → `[[PSA.111:6]]` (OCR artifact, JOB_articles.md)

**E3. Remaining orphans (2 study + 30 reference):**
- `EXO.40:34` — CVC mismatch (registry says 32, OSB may have more)
- `2KI.12:31` — CVC mismatch (MT vs LXX numbering)
- 30 reference-domain orphans in `liturgical-crossrefs.json` — systematic PSA continuous numbering (lectionary treats psalm sequences as continuous verse ranges across psalm boundaries)

**E4. Audit results (session end):**
| Domain | Wikilinks | Bare Refs | Orphans | Invalid Ranges |
|---|---|---|---|---|
| staging | 4,569 | 127 | 0 | 1 |
| study | 4,691 | 31 | 2 | 7 |
| reference | 2,601 | 466 | 32 | 20 |
| **Total** | **11,861** | **624** | **34** | **28** |

**vs session start:** wikilinks +2,642, bare refs −1,315, orphans fixed 6 (5 remaining are CVC mismatches)

**Reference orphan pattern:** 30 of 34 orphans are systematic PSA continuous numbering in `liturgical-crossrefs.json` — the lectionary treats Psalm sequences as continuous verse ranges across psalm boundaries (e.g., PSA.1:1-12 covers Psalms 1+2). These need kathisma-aware range handling, not per-psalm CVC validation.

### Ark: Remaining Bare Ref Remediation

**Bare ref analysis (624 → classified):**
| Category | Count | Action |
|---|---|---|
| `textual-variants.md` endnote labels | 447 | SKIP — structural markers, not refs |
| MT versification refs (MAL.4, JOL.4, EXO.40:34+) | 17 | SKIP — no LXX anchors exist |
| Apocryphal citations (Tb, 1En, 3Mc, TLev) | ~12 | SKIP — intentionally non-canonical |
| Reference prose (overview-of-books etc.) | 16 | CONVERTED |
| Study cross-chapter ranges | 14 | CONVERTED (manual sed) |
| Staging mirrors | 13 | CONVERTED (mirror of study fixes) |
| Embedded commentary in LEV/EXO canon | 53+19 | DATA QUALITY ISSUE — parser-stage remediation needed |

**LEV/EXO embedded commentary finding:**
- LEV has 12 mega-lines (2 with full study articles embedded, notably "SACRIFICE" in LEV.14:1 at 16,457 chars)
- EXO has 6 mega-lines (no embedded articles, just fused multi-verse lines)
- This is a V5 (article bleed) violation that was not caught pre-promotion
- Remediation: LEV needs re-extraction to separate study content; both need verse-line splitting
- Separate work item — not part of wikilinks sprint

**Invalid range endpoints (28 total):**
- All are cross-chapter ranges (e.g., `[[EXO.28:2]]-39` meaning EXO 28:2 through 29:1)
- Not errors — limitation of per-chapter CVC validation
- Future: add cross-chapter range awareness to audit tool

### Post-Conversion Pipeline Rebuild

After all conversions complete:
1. R1 re-extraction: 76 books → `metadata/r1_output/*.jsonl`
2. Backlink rebuild: 6,370 → 6,379 shards
3. Enrichment: all shards to v2
4. DuckDB graph regenerated

### Ezra: textual-variants.md Conversion

- 1,382 wikilinks created from implicit-chapter-context bare refs
- 0 invalid anchors (all pass CVC validation)
- 136 lines skipped (commentary sections with ambiguous book context)
- Conversion script: `pipeline/reference/convert_textual_variants_wikilinks.py`
- Two-pass state machine: 25-book NT sequence (917 refs) + 21-book extended sequence (465 refs)

### Final Audit Results

| Domain | Wikilinks | Bare Refs | Orphans | Invalid Ranges |
|---|---|---|---|---|
| staging | 4,582 | 114 | 0 | 6 |
| study | 4,705 | 17 | 2 | 12 |
| reference | 4,001 | 450 | 32 | 34 |
| **Total** | **13,288** | **581** | **34** | **52** |

**vs session start:** wikilinks 9,219 → 13,288 (+44%), bare refs 1,939 → 581 (−70%)

**Orphan breakdown:** 2 study (CVC mismatches), 32 reference (30 PSA kathisma + 2 data errors)

## Open Items
- **LEV/EXO parser remediation:** mega-lines + embedded study articles. Separate work item.
- **Reference PSA kathisma ranges:** Need kathisma-aware range model, not per-psalm CVC.
- **textual-variants.md:** Ezra working on implicit-chapter-context conversion (232 refs).
- **Remaining 17 study MT-versification bare refs:** Correctly non-convertible under LXX registry.
