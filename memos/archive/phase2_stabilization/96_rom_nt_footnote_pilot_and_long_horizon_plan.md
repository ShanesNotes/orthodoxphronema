# ROM NT Footnote Pilot And Long-Horizon Plan — 2026-03-11

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `nt companion extraction / footnote pilot`
**Workstream:** `nt-prep`  
**Phase:** `4`  
**Supersedes:** `95` in part  
**Superseded by:** `none`

## Context
- Memo 95 reset the NT companion lane around a new rule: extract real NT footnotes from the OSB footnote page ranges and treat marker files as secondary linkage metadata.
- Wave 1 companion splitting (`LUK`, `MAT`, `JOH`, `ACT`, `REV`) proved that legacy NT `_notes.md` files are article sources, not a reliable footnote source.
- `ROM` was selected as the first source-footnote pilot because it has manageable scope, real marker density, and a defined footnote page range in `schemas/anchor_registry.json`.

## Objective
- Prove that real NT footnotes can be recovered directly from the OSB footnote pages.
- Harden the existing extraction seam enough that wrapped cross-references do not become false note anchors.
- Produce one durable pilot report plus a long-horizon rollout sequence for the remaining NT footnote books.

## Files / Artifacts
- `pipeline/cleanup/extract_footnotes.py`
- `staging/validated/NT/ROM_footnotes.md`
- `reports/nt_footnote_extraction/ROM.json`
- `memos/95_nt_footnote_extraction_reset.md`

## Findings Or Changes
- The existing notes-page extractor was already viable for NT. A first `ROM` run immediately produced real note content from the OSB footnote pages.
- The first pilot output exposed one clear parser issue:
  - wrapped cross-reference text created a false `ROM.28:2` footnote anchor
- I hardened `pipeline/cleanup/extract_footnotes.py` in one bounded way:
  - reject anchors beyond the current book's chapter count
  - enforce monotonically increasing note anchors through the book
- After the hardening pass, `ROM.28:2` disappeared and the extractor settled into a clean pilot shape.
- `ROM` now has a real source-derived footnote artifact at `staging/validated/NT/ROM_footnotes.md`.

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `ROM` footnote extraction from OSB notes pages | `pass` | `pipeline/cleanup/extract_footnotes.py --book ROM` |
| False wrapped-reference anchor removed | `pass` | `ROM.28:2` no longer appears in `staging/validated/NT/ROM_footnotes.md` |
| Source-derived footnote inventory is nontrivial | `pass` | `137` extracted entries across all `16` chapters |
| Marker overlap is strong enough for later linkage audit | `pass` | `112 / 130` unique marker anchors matched |
| Marker layer is not clean enough to be the primary source | `pass` | `18` marker anchors lack extracted notes; `25` extracted notes lack markers |
| One invalid anchor remains in both surfaces | `warn` | `ROM.16:25` appears in both markers and extracted footnotes but fails registry validation |

## Pilot Summary
| Metric | Value |
|---|---|
| Footnote source pages | `9336-9472` |
| Extracted entries | `137` |
| Unique extracted anchors | `137` |
| Marker records | `132` |
| Unique marker anchors | `130` |
| Matching anchors | `112` |
| Missing footnotes for markers | `18` |
| Footnotes without markers | `25` |
| Chapters with notes | `16` |
| Highest-density chapters | `6 (18)`, `1 (16)`, `8 (16)`, `3 (11)`, `5 (10)` |

## Long-Horizon Plan
### Phase 1: Stabilize The Extraction Seam
- Keep `pipeline/cleanup/extract_footnotes.py` as the primary notes-page extraction path.
- Add no new heuristics until another concrete NT book exposes a real parser miss.
- Treat invalid anchors like `ROM.16:25` as audit findings first, not immediate parser problems.

### Phase 2: Replace Wave 1 Footnote Placeholders
- Use the same notes-page extraction path for:
  - `LUK`
  - `MAT`
  - `JOH`
  - `ACT`
  - `REV`
- Replace only the zero-entry placeholder `*_footnotes.md` files.
- Keep the already-accepted `*_articles.md` outputs untouched.

### Phase 3: Finish Remaining Article-Bearing NT Notes Books
- Split article-bearing legacy notes for:
  - `EPH`
  - `1CO`
  - `MRK`
  - `JAS`
  - `TIT`
  - `1JN`
  - `2PE`
- Then pair each with notes-page footnote extraction.

### Phase 4: Zero-Content NT Notes Books
- Defer the `14` zero-content legacy `_notes.md` files until source-footnote extraction reaches them.
- Do not waste time producing article splits where there is no article content to preserve.

### Phase 5: Linkage And Wikilinks Later
- Keep marker comparison as a secondary audit surface.
- Defer structured wikilink/backlink reconciliation until the real footnote corpus exists across a meaningful NT subset.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Use notes-page verse labels as the primary source | The `ROM` pilot produced a substantial real footnote corpus without depending on marker anchors | Some books may have noisier page text than `ROM` | Fall back to book-specific extraction memos if a later pilot fails |
| Keep marker files secondary | `ROM` shows strong but incomplete overlap, proving markers are useful audit metadata but not sufficient as the primary source | Linkage coverage remains incomplete until later reconciliation | Revisit only after multiple NT pilots are in hand |
| Scale to Wave 1 replacements next | The placeholder footnote files already exist and can be replaced cleanly | Larger books may expose additional wrapped-reference patterns | Patch the extractor only when a concrete false-anchor family appears |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `pipeline/cleanup/extract_footnotes.py`, `staging/validated/NT/ROM_footnotes.md`, `reports/nt_footnote_extraction/ROM.json`, `memos/96_rom_nt_footnote_pilot_and_long_horizon_plan.md`, `memos/ezra_ops_board.md`, `PROJECT_BOARD.md`, `memos/INDEX.md` |
| `Verification run` | `done` | `python3 pipeline/cleanup/extract_footnotes.py --book ROM`; `python3 pipeline/cleanup/verify_footnotes.py --book ROM` |
| `Artifacts refreshed` | `done` | pilot report, memo, ops board, project board, memo index |
| `Remaining known drift` | `present` | `ROM.16:25` is invalid in both markers and extracted footnotes; marker overlap is incomplete by design at this stage |
| `Next owner` | `ezra` | package the Wave 1 replacement sequence and hand it to Photius |

## Requested Next Action
- Ezra: use the `ROM` pilot as the acceptance threshold and dispatch a Wave 1 replacement run for `LUK`, `MAT`, `JOH`, `ACT`, and `REV`.
- Photius: run the same notes-page extraction path on the Wave 1 books and report marker overlap separately.
- Ark: stay on NT stabilization unless repeated invalid-anchor or page-range failures show a real core-pipeline issue.
