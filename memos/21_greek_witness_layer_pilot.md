# Memo 21: Greek Witness-Layer Pilot Results — 2026-03-08

**Author:** `ark`
**To:** `ezra`
**Type:** `implementation + review-request`
**Status:** `active`
**Scope:** `Greek witness infrastructure — mapping + pilot indexes`

## What Was Done

### 1. GEN Residuals Update
- Ezra ratified `GEN.14:24` and `GEN.49:2` as non-blocking `docling_issue`
- `GEN.25:34` reclassified from `docling_issue` → `osb_pdf_absent` → `osb_source_absent`: the verse is absent from both OSB witnesses (electronic PDF and verification scan)
- Confirmed `GEN.25:34` exists in both Rahlfs LXX (`Ιακωβ δὲ ἔδωκεν τῷ Ησαυ ἄρτον καὶ ἕψεμα φακοῦ...`) and Brenton English (`And Jacob gave bread to Esau, and pottage of lentiles...`)
- Brenton text was initially inserted into `GEN.md` with Human approval, then **rolled back per immutability policy** (memo 22): canon artifacts must reflect OSB as-published; Greek/Brenton are auxiliary witnesses only, not canon-rewriting sources
- GEN now at **1529/1532 verses (99.8%)**, gaps: `GEN.14:24`, `GEN.25:34`, `GEN.49:2`
- Promotion dossier regenerated after rollback
- `ratified_date` set to `2026-03-08` in sidecar; all 3 entries have per-entry `ratified: true`

### 2. Greek Source Map (`schemas/greek_source_map.json`)
Created a comprehensive book-code mapping covering all 76 Orthodox canon books:
- **49 OT books** → Rahlfs LXX SQLite `book_number` + short name
- **27 NT books** → Antoniades file name
- Includes notes on versification divergences (Psalms, Daniel recensions)
- Documents unmapped bonus books (Psalms of Solomon, Odes)

### 3. Greek Indexer (`pipeline/reference/index_greek.py`)
New script that reads from both sources and produces standardized JSON indexes:
- OT: queries LXX1.SQLite3, strips `<S>`/`<m>` markup, outputs clean polytonic Greek
- NT: parses `chapter:verse text` format from Antoniades plaintext
- Output format matches our existing Brenton index pattern (`chapters` → list of verse strings)

### 4. Pilot Indexes
Two pilot books indexed to `staging/reference/greek/`:

| Book | Source | Chapters | Verses | Script |
|------|--------|----------|--------|--------|
| GEN | Rahlfs LXX | 50 | 1531 | polytonic |
| MATT | Antoniades 1904 | 28 | 1071 | monotonic_lowercase |

**GEN verse count note:** LXX has 1531 verses vs our registry's 1532. The 1-verse difference needs investigation — likely a versification variant in one chapter. This is exactly the kind of discrepancy the witness layer is designed to catch.

## Files Created/Modified

| File | Action |
|------|--------|
| `staging/validated/OT/GEN_residuals.json` | Updated: 25:34 reclassified, ratified_date set |
| `staging/validated/OT/GEN.md` | GEN.25:34 Brenton text rolled back (memo 22) |
| `reports/GEN_promotion_dossier.json` | Regenerated after rollback |
| `schemas/greek_source_map.json` | **NEW** — book-code mapping for all 76 books |
| `pipeline/reference/index_greek.py` | **NEW** — Greek verse indexer |
| `staging/reference/greek/GEN.json` | **NEW** — pilot OT index |
| `staging/reference/greek/MATT.json` | **NEW** — pilot NT index |
| `memos/19_day10_status_and_todos.md` | Updated GEN section |
| `memos/20_greek_source_text_acquisition.md` | **NEW** — acquisition report |

## Scope Boundary (Human Directive)

Greek work is **scoped to witness-layer infrastructure only**:
- Mapping file: done
- One OT pilot (GEN): done
- One NT pilot (MATT): done
- **No full ingest yet** — remaining 74 books deferred pending Ezra review of pilot quality

## Review Requested from Ezra

1. **GEN.25:34 source absence:** The Brenton insertion was rolled back per immutability policy (memo 22). The verse is now classified as `osb_source_absent` with `ratified: true`. Greek/Brenton witnesses are documented in the sidecar's `upstream_witnesses` field but no substitute text exists in the canon artifact.

2. **Greek pilot quality:** Review `staging/reference/greek/GEN.json` — are the stripped Greek verses clean? Any residual markup artifacts? Is the chapter/verse structure correct?

3. **MATT pilot quality:** Review `staging/reference/greek/MATT.json` — the Antoniades text is monotonic (no accents). Is this acceptable for the witness layer, or should we flag it as degraded fidelity?

4. **Source map completeness:** Review `schemas/greek_source_map.json` — any missing books or incorrect mappings? Note the Daniel issue: OSB uses Theodotion but LXX1 has OG. The LXX2 database has DanTh but we haven't mapped it yet.

5. **GEN verse count discrepancy:** LXX gives 1531, registry says 1532. Worth investigating now or defer?

6. **GEN promotion readiness:** With residuals ratified and dossier regenerated, is GEN ready for your audit pass before promotion?

## Next Steps (pending Ezra review)

- Ezra audits GEN for promotion
- If pilots approved, we can index remaining books on demand (one command per book)
- Full ingest deferred until pilot review complete
- Versification mapping table for Psalms still needed before PSA extraction
