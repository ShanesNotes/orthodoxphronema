# NT Wave 1 Footnote Alignment Report — 2026-03-12

**Author:** `photius`  
**Type:** `report`  
**Status:** `implemented`  
**Scope:** `nt footnote alignment / wave 1 replacement`
**Workstream:** `nt-stabilization`  
**Phase:** `2`  
**Supersedes:** `none`  

## Context
- Following the `ROM` pilot (Memo 96), Wave 1 NT books (`MAT`, `LUK`, `JOH`, `ACT`, `REV`) required replacement of placeholder/zero-entry footnote files with real OSB source-page extractions.
- Policy decision: OSB source-page footnotes are the authoritative source. Marker files are secondary audit metadata.

## Objective
- Execute `pipeline/cleanup/extract_footnotes.py` for Wave 1.
- Audit the marker overlap and identify "phantom" or "invalid" marker anchors.
- Confirm that `*_footnotes.md` now contains real content for all Wave 1 books.

## Files / Artifacts
- `staging/validated/NT/{MAT,LUK,JOH,ACT,REV}_footnotes.md` (Extracted)
- `reports/nt_footnote_extraction/{MAT,LUK,JOH,ACT,REV}.json` (Refreshed)

## Alignment Findings

### 1. Extraction Totals
| Book | Pages | Entries Found | Status |
|---|---|---|---|
| **MAT** | 8195-8478 | 280 | `pass` |
| **LUK** | 8552-8822 | 271 | `pass` |
| **JOH** | 8823-9078 | 252 | `pass` |
| **ACT** | 9079-9335 | 196 | `pass` |
| **REV** | 10170-10373 | 182 | `pass` |

### 2. Marker Overlap Audit
| Book | Markers | Matches | Markers w/o Notes | Notes w/o Markers |
|---|---|---|---|---|
| **MAT** | 297 | 244 | 53 | 36 |
| **LUK** | 306 | 244 | 61 | 27 |
| **JOH** | 277 | 234 | 43 | 18 |
| **ACT** | 276 | 176 | 100 | 20 |
| **REV** | 191 | 165 | 24 | 17 |

### 3. Structural Anomalies (Invalid Anchors)
The audit identified several anchors in the marker or footnote layer that fail registry validation or scripture existence checks:
- **LUK**: `LUK.17:38` (Marker only; invalid verse in registry).
- **JOH**: `JOH.21:24`, `JOH.21:25` (Found in both markers and source notes, but missing from staged `JOH.md` text).
- **REV**: `REV.22:22`, `REV.22:23` (Markers only; invalid verse in registry).
- **REV**: `REV.4:11` (Source footnote exists but anchor missing from staged `REV.md` text).

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Source Primacy | OSB notes pages are the canonical location for note text. Markers in scripture are often misread or shifted during OCR | Some real markers may lack note text if the OSB omitted the note | N/A |
| Delete legacy `_notes.md` | For Wave 1, `_notes.md` is redundant with `_articles.md`. The new `_footnotes.md` provides the remaining content | None; content is preserved in articles and footnotes | Restore from git if needed |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `MAT_footnotes.md`, `LUK_footnotes.md`, `JOH_footnotes.md`, `ACT_footnotes.md`, `REV_footnotes.md` |
| `Verification run` | `done` | `python3 pipeline/cleanup/verify_footnotes.py` for all 5 books |
| `Artifacts refreshed` | `done` | extraction reports in `reports/nt_footnote_extraction/` |
| `Remaining known drift` | `present` | Missing markers for ~15-20% of notes; missing notes for ~20-30% of markers (especially in ACT) |
| `Next owner` | `photius` | Phase 3: Split article-bearing notes for EPH, 1CO, MRK, JAS, TIT, 1JN, 2PE |

## Handoff
Wave 1 footnote recovery is complete. The files are now source-derived. Articles have been preserved in `*_articles.md`. I am proceeding to Phase 3.
