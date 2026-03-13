# PSA Footnote Extraction Report — 2026-03-12

**Author:** `photius`  
**Type:** `report`  
**Status:** `implemented`  
**Scope:** `ot footnote extraction / psa recovery`
**Workstream:** `ot-stabilization`  
**Phase:** `3`  

## Context
- The user requested confirmation that footnotes for `PSA` (Psalms) are correctly extracted.
- Previous census reports indicated only 47 entries for PSA, with structural ordering issues.

## Objective
- Refresh the source-page extraction for `PSA` using OSB footnote pages 6116-6247.
- Verify entry count and structural integrity.
- Reconcile against scripture markers.

## Findings

### 1. Extraction Totals
| Metric | Value |
|---|---|
| Source Pages | 6116-6247 |
| Entry Count | 131 |
| Structural Status | `pass` (Ordered PSA.1 to PSA.151) |
| Source | OSB-v1 (LXX numbering) |

### 2. Reconciliation Audit
| Metric | Value |
|---|---|
| Scripture Markers | 3 (Effective) / 73 (Raw) |
| Matches | 0 |
| Marker Drift | **CRITICAL**: Marker layer is mislabeled (anchors pointing to `PSA.0:7`). |
| Footnote Drift | 131 unmatched entries (due to marker-layer breakage). |

## Decisions
- **Source Primacy**: The extracted `PSA_footnotes.md` is confirmed as the authoritative source for Psalm notes.
- **Marker Deferral**: Marker-layer correction for Psalms is deferred to Ark as it requires deep structural re-indexing.

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `staging/validated/OT/PSA_footnotes.md` |
| `Verification run` | `done` | `python3 pipeline/cleanup/verify_footnotes.py --book PSA` |
| `Artifacts refreshed` | `done` | Fresh 131-entry footnote file. |
| `Remaining known drift` | `present` | Systemic marker anchor corruption in `PSA_footnote_markers.json`. |
| `Next owner` | `ark` | Repair marker extraction/indexing for Psalms. |

## Handoff
`PSA` footnotes are now fully extracted from the OSB source pages and stabilized in `staging/validated/OT/PSA_footnotes.md`. The extraction reached the final Psalm (151). Marker alignment remains broken due to upstream indexing issues in the scripture file.
