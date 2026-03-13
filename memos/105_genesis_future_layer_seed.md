# Genesis Future-Layer Seed — 2026-03-12

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `phase 2/3 bridge / metadata substrate / GEN exemplar`
**Workstream:** `phase3-design`  
**Phase:** `3`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- The repo had mature future-layer architecture memos (`86`, `87`, `88`) but no real derived substrate proving those contracts against live canon and companion data.
- `PSA.44` remains the preferred liturgical-rich future slice, but the current repo does not yet expose a sufficiently rich companion substrate there.
- `GEN.2:7-24` is the richest currently complete exemplar: promoted canon text, real extracted footnotes, existing pericope index, and abundant companion cross-reference material.

## Objective
- Establish the first future-layer seed as a pure derivation from canon plus companion files.
- Prove the pericope, extraction, and embedding-document contracts on one live exemplar without touching canon or staged scripture text.
- Leave DuckDB, backlink generation, BM25, and vectors downstream of a stable derived metadata layer.

## Files / Artifacts
- `pipeline/metadata/generate_pericope_index.py`
- `pipeline/metadata/build_future_seed.py`
- `pipeline/extract/{models.py,r1_extractor.py}`
- `tests/test_future_seed.py`
- `metadata/pericope_index/GEN.json`
- `metadata/r1_output/GEN.jsonl`
- `metadata/embedding_documents/GEN.jsonl`

## Findings Or Changes
- Extended the existing pericope index flow with backward-compatible future-layer keys.
  - Legacy keys (`title`, `start_anchor`, `end_anchor`, `verse_count`, `chapter_range`) remain intact.
  - New keys (`notes_anchors`, `source_companions`, `cross_ref_candidates`, `liturgical_context`, `alt_versification`, `embedding_status`, `provenance`) were added with safe defaults.
- Added a future-facing narrow R1 extractor under `pipeline/extract/`.
  - The extractor strips frontmatter, ignores structural noise, and emits the memo 86 six-field contract unchanged.
  - It normalizes OSB-style prose abbreviations such as `Jn 20:22` and `Eph 5:32` into canonical archive IDs such as `JOH.20:22` and `EPH.5:32`.
- Added a Genesis seed builder under `pipeline/metadata/`.
  - The builder reads `canon/OT/GEN.md` plus `staging/validated/OT/GEN_{footnotes,articles}.md`.
  - It enriches the `The Garden of Eden` pericope record for `GEN.2:7-24`.
  - It emits `metadata/r1_output/GEN.jsonl` and `metadata/embedding_documents/GEN.jsonl`.
- The exemplar now proves the future layer on a live slice without premature graph or vector work.
  - `metadata/pericope_index/GEN.json` carries real note anchors and cross-reference candidates for the exemplar.
  - `metadata/embedding_documents/GEN.jsonl` contains one derived retrieval-ready document with provenance and in-range footnotes.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Use `GEN.2:7-24` instead of `PSA.44` for the first seed | Genesis has the richest complete current substrate in the live repo | Less liturgical richness than the eventual Psalms slice | Add `PSA.44` as the next vertical once its companion substrate matures |
| Keep the R1 row contract exact | Memo 86 already fixed the six-field extraction shape | Some provenance must live outside row fields | Keep provenance at the artifact level, not the row level |
| Read companion inputs from `staging/validated/` via `--companion-base` | The normalized `notes/` / `articles/` trees are still placeholders | Future path swap needed | Generator already abstracts the base path; no logic rewrite required |
| Stop before graph/vector work | The goal was a pure substrate, not a full retrieval stack | Future-layer progress can look slower than it is | Use Memo 105 as the stable handoff into backlinks or retrieval later |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Narrow metadata + future-seed tests | `pass` | `pytest tests/test_metadata_format.py tests/test_future_seed.py -q` |
| Module syntax | `pass` | `python3 -m py_compile pipeline/metadata/build_future_seed.py pipeline/extract/models.py pipeline/extract/r1_extractor.py` |
| Full suite | `pass` | `pytest -q` -> `323 passed` |
| Seed build | `pass` | `python3 pipeline/metadata/build_future_seed.py --companion-base staging/validated` |
| Genesis cross-reference normalization | `pass` | `metadata/r1_output/GEN.jsonl` contains canonical IDs such as `JOH.20:22` and `EPH.5:32` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | future-layer code, tests, Memo `105`, enriched `GEN` pericope index, `GEN` R1 JSONL, `GEN` embedding JSONL |
| `Verification run` | `done` | targeted tests, full suite, py_compile, seed build |
| `Artifacts refreshed` | `done` | `metadata/pericope_index/GEN.json`, `metadata/r1_output/GEN.jsonl`, `metadata/embedding_documents/GEN.jsonl`, memo index, ops board, project board |
| `Remaining known drift` | `present` | future layer is still a one-slice seed; no backlinks, DuckDB, BM25, or vectors yet; `PSA.44` remains the preferred liturgical follow-up slice |
| `Next owner` | `ark` | Review the seed and choose the next expansion lane: broaden R1, add backlink generation, or take the second slice |
