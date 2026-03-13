# NT Footnote Stabilization And Structural Audit — 2026-03-12

**Author:** `photius`  
**Type:** `report`  
**Status:** `implemented`  
**Scope:** `nt footnote stabilization / structural audit`
**Workstream:** `nt-stabilization`  
**Phase:** `2-4`  
**Supersedes:** `96`  

## Context
- Phase 2-4 of the long-horizon plan required replacing zero-entry/placeholder footnote files with real OSB source-page extractions for all NT books.
- Policy: Source-page footnotes are authoritative; marker files are secondary audit metadata.
- Legacy `_notes.md` files were identified as redundant article sources or zero-content placeholders.

## Objective
- Complete source-footnote extraction for all 27 NT books.
- Reconcile extracted notes with scripture markers to detect structural drift.
- Decommission legacy `_notes.md` files after ensuring article preservation.

## Files / Artifacts
- `staging/validated/NT/*_footnotes.md` (27 files, refreshed/extracted)
- `staging/validated/NT/*_articles.md` (Split/preserved where articles existed)
- `memos/102_nt_wave1_footnote_alignment_report.md` (Superseded by this comprehensive report)
- `reports/nt_footnote_extraction/*.json` (Full NT set refreshed)

## Extraction Summary
| Batch | Books | Status |
|---|---|---|
| **Wave 1** | MAT, LUK, JOH, ACT, REV | `pass` (source-derived) |
| **Phase 3** | 1CO, 1JN, 2PE, EPH, JAS, MRK, TIT | `pass` (source-derived) |
| **Phase 4** | 1PE, 1TH, 1TI, 2CO, 2JN, 2TH, 2TI, 3JN, COL, GAL, HEB, JUD, PHM, PHP | `pass` (source-derived) |
| **Pilot** | ROM | `pass` (source-derived) |

## Structural Audit Findings (CRITICAL)
Reconciling the source footnotes against the staged scripture text revealed significant structural corruption in several books. These are blockers for promotion.

### 1. JOH: Catastrophic Mislabeling
- **Issue**: From Chapter 21 onwards, verses are mislabeled as chapters.
- **Evidence**: `JOH.md` ends with "Chapter 25", but John has only 21 chapters. `JOH.21:25` is labeled as `JOH.25:1`.
- **Impact**: All markers and footnotes for the end of John are broken.

### 2. LUK: Versification Drift
- **Issue**: Chapter 17 has an extra verse `LUK.17:38`.
- **Evidence**: The OSB text for `LUK.17:37` was split into two verses. Registry correctly identifies 37 verses.
- **Impact**: Marker/Footnote mismatch for the end of the chapter.

### 3. REV: Text Fusion & Phantom Markers
- **Issue A**: `REV.4:11` is missing from the staged scripture (likely swallowed into 4:10).
- **Issue B**: Phantom markers `REV.22:22`, `REV.22:23` exist in the marker layer but do not exist in the registry or the source notes.
- **Impact**: Critical text omission in Chapter 4.

### 4. ACT: Low Note Density
- **Issue**: 100 markers in ACT have no corresponding note on the footnote pages.
- **Evidence**: 276 markers vs 196 extracted notes.
- **Impact**: ACT has the highest "note-less marker" rate in the NT.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Authoritative Extraction | Source-page references (e.g., "1:2-3") were prioritized over marker anchors | Some markers may lose linkage if the note label differs | Use marker-based fuzzy matching in later reconciliation |
| Global Notes Cleanup | All `*_notes.md` files were removed after verifying article preservation in `*_articles.md` | Minor risk of article omission if split logic failed | Git restore |
| Structural Red Flag | Reported JOH/LUK/REV corruption as top-priority repair items for Ark | None; this is essential audit work | N/A |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | NT `_footnotes.md` set (27), `ROM_articles.md`, Removed `_notes.md` set (26) |
| `Verification run` | `done` | `verify_footnotes.py` run for 100% of NT; custom `grep`/`tail` audit of corrupt files |
| `Artifacts refreshed` | `done` | 27 extraction reports; 1 stabilization report (this memo) |
| `Remaining known drift` | `present` | JOH/LUK/REV structural corruption; Marker/Note density mismatch (15-30%) |
| `Next owner` | `ark` | Repair structural corruption in JOH, LUK, and REV |

## Handoff
NT Footnote stabilization is complete. The mission uncovered deep structural flaws in the Scripture text itself (JOH/LUK/REV). I recommend Ark prioritize these repairs before any further NT promotion.
