# NT Candidate Marker Purity Pass (`1TH`, `2TH`, `2TI`, `1JN`) — 2026-03-12

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `NT staged scripture + footnote marker sidecars`
**Workstream:** `canon-hygiene`  
**Phase:** `4`  
**Supersedes:** `111`  
**Superseded by:** `none`

## Context
- Memo `111` established that `1TH`, `2TH`, `2TI`, and `1JN` were gate-ready by current dossier logic, but not yet safe for the next NT canon tranche.
- The immediate blocker was scripture-side marker residue plus marker/footnote sidecar mismatch.

## Objective
- Remove the literal stray note-letter residue that was still present in staged scripture.
- Realign the `*_footnote_markers.json` sidecars to the extracted footnote anchors so the verifier reflects current staged truth.

## Files / Artifacts
- `staging/validated/NT/1TH.md`
- `staging/validated/NT/2TI.md`
- `staging/validated/NT/1JN.md`
- `staging/validated/NT/1TH_footnote_markers.json`
- `staging/validated/NT/2TH_footnote_markers.json`
- `staging/validated/NT/2TI_footnote_markers.json`
- `staging/validated/NT/1JN_footnote_markers.json`
- `reports/1TH_promotion_dossier.json`
- `reports/2TH_promotion_dossier.json`
- `reports/2TI_promotion_dossier.json`
- `reports/1JN_promotion_dossier.json`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- Stripped the literal trailing/standalone marker residue from:
  - `1TH.1:1`
  - `1TH.4:14`
  - `2TI.1:11`
  - `2TI.4:1`
  - `1JN.2:7`
  - `1JN.2:18`
  - `1JN.2:20`
  - `1JN.2:28`
  - `1JN.3:1`
  - `1JN.4:3`
  - `1JN.5:9`
- Rebuilt the four marker sidecars from the actual extracted footnote-anchor sets so verifier truth is now exact.
- Refreshed all four promotion dossiers via dry-run and regenerated the dashboard.
- Result: all four books now pass `verify_footnotes.py` cleanly.
- Remaining NT tranche blocker shifted from marker linkage to fused-word scripture residue (`aafter`, `aliar`, `apreacher`, etc.), which is visible in the dry-run previews and older cleanup reports.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Fix marker linkage now | It was the cleanest bounded blocker on the next NT tranche | Sidecar simplification may lose historical marker-shape nuance | Rebuild from parser output if needed |
| Stop before a full fused-word sweep | The residue set is broader than the marker lane and should be handled as its own purity pass | Delays the second NT canon tranche | Take a dedicated fused-word cleanup lane next |
| Refresh dossiers/dashboard after the pass | Staged scripture changed and dry-runs rewrote dossiers | None | Re-run the generators |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/1TH.md` | pass | structural validation clean |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/2TH.md` | pass | structural validation clean |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/2TI.md` | warn | `V8` only |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/1JN.md` | warn | `V8` only |
| `python3 pipeline/cleanup/verify_footnotes.py --book 1TH` | pass | sidecar matches extracted footnotes |
| `python3 pipeline/cleanup/verify_footnotes.py --book 2TH` | pass | sidecar matches extracted footnotes |
| `python3 pipeline/cleanup/verify_footnotes.py --book 2TI` | pass | sidecar matches extracted footnotes |
| `python3 pipeline/cleanup/verify_footnotes.py --book 1JN` | pass | sidecar matches extracted footnotes |
| `python3 pipeline/promote/promote.py --book 1TH --dry-run` | pass | dossier refreshed; visible fused-word residue still present |
| `python3 pipeline/promote/promote.py --book 2TH --dry-run` | pass | dossier refreshed; visible fused-word residue still present |
| `python3 pipeline/promote/promote.py --book 2TI --dry-run` | pass | dossier refreshed; visible fused-word residue still present |
| `python3 pipeline/promote/promote.py --book 1JN --dry-run` | pass | dossier refreshed; visible fused-word residue still present |
| `python3 pipeline/tools/generate_book_status_dashboard.py` | pass | dashboard refreshed |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | three staged scripture files, four marker sidecars, four dossiers, dashboard |
| `Verification run` | `done` | targeted validators, footnote verifier, promote dry-runs |
| `Artifacts refreshed` | `done` | `reports/1TH_promotion_dossier.json`, `reports/2TH_promotion_dossier.json`, `reports/2TI_promotion_dossier.json`, `reports/1JN_promotion_dossier.json`, `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | the next NT tranche is now blocked by fused-word scripture residue rather than marker linkage |
| `Next owner` | `ezra` | route a bounded fused-word cleanup lane before the second NT canon tranche |

## Requested Next Action
- Open the next NT lane as a bounded fused-word cleanup pass on `1TH`, `2TH`, `2TI`, and `1JN`, using the old cleanup reports and current dry-run previews as the fix list.

## Handoff
**To:** `ezra`  
**Ask:** `Update the live boards so they show marker purity as closed and fused-word cleanup as the active blocker on the next NT tranche.`
