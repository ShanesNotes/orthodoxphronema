# NT Promotion Packet (`JUD`, `PHM`) — 2026-03-13

**Author:** `ark`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `NT staged scripture + sidecar alignment + canon promotion + state refresh`
**Workstream:** `canon-hygiene`  
**Phase:** `4`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- After Memo `113`, the remaining light NT lane was to harvest the shortest promotion candidates before reopening the heavier queue.
- `JUD` and `PHM` were the tightest bounded books: both were structurally passable, but they still carried local fused-word and note-letter residue plus marker-sidecar drift.

## Objective
- Clean the remaining local scripture residue in `JUD` and `PHM`.
- Reconcile scripture marker sidecars with the extracted footnote anchors.
- Promote both books from the same staged files that were re-verified.

## Files / Artifacts
- `staging/validated/NT/JUD.md`
- `staging/validated/NT/JUD_footnote_markers.json`
- `staging/validated/NT/PHM.md`
- `staging/validated/NT/PHM_footnote_markers.json`
- `canon/NT/JUD.md`
- `canon/NT/PHM.md`
- `reports/JUD_promotion_dossier.json`
- `reports/PHM_promotion_dossier.json`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- Cleaned bounded OCR and note-letter residue in `JUD`, including:
  - `JUD.1:1` `abondservant` -> `a bondservant`
  - `JUD.1:22` `adistinction` -> `a distinction`
  - `JUD.1:24` removed the stray note-letter residue from `a from stumbling`
  - `JUD.1:25` closed the split-word spacing in `Sav ior` -> `Savior`
- Cleaned bounded OCR and note-letter residue in `PHM`, including:
  - `PHM.1:1` `aprisoner` -> `a prisoner`
  - `PHM.1:2` removed note-letter residue so `beloved a Apphia` reads `beloved Apphia`
  - `PHM.1:7` removed note-letter residue so `great joy b and consolation` reads `great joy and consolation`
  - `PHM.1:12` removed note-letter residue so `sending him back. a You` reads `sending him back. You`
- Realigned `JUD_footnote_markers.json` to include the source-backed scripture anchors now present in the extracted footnotes, including `JUD.1:1` and `JUD.1:13`.
- Realigned `PHM_footnote_markers.json` to the current ten-anchor extracted footnote set.
- Promoted both books into `canon/NT/` and refreshed the two dossiers plus the dashboard.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Treat `JUD` and `PHM` as a small standalone packet | The books were short, locally fixable, and did not require reopening the heavier NT queue | A missed note-letter residue could leave staged and canon text inconsistent | Reopen the exact staged anchors and re-promote the affected book |
| Repair marker sidecars instead of relaxing `verify_footnotes.py` | The footnote files were already source-derived, so the linkage metadata had to move toward them | A wrong anchor could hide a real extraction defect | Compare the sidecar anchor list against `*_footnotes.md` and regenerate if needed |
| Accept `JUD` with its existing `V8` warning | The warning is pre-existing heading-density debt, not a new structural failure | Heading curation debt remains visible | Revisit in a later heading-only pass without undoing promotion |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/JUD.md` | `warn` | `V8` only |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/PHM.md` | `pass` | structural validation clean |
| `python3 pipeline/cleanup/verify_footnotes.py --book JUD` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/verify_footnotes.py --book PHM` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/JUD.md` | `pass` | `0` candidates |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/PHM.md` | `pass` | `0` candidates |
| `python3 pipeline/promote/promote.py --book JUD --dry-run` | `pass` | canon preview clean; `V8` only |
| `python3 pipeline/promote/promote.py --book PHM --dry-run` | `pass` | canon preview clean |
| `python3 pipeline/promote/promote.py --book JUD` | `pass` | canon write complete |
| `python3 pipeline/promote/promote.py --book PHM` | `pass` | canon write complete |
| `python3 pipeline/tools/generate_book_status_dashboard.py` | `pass` | dashboard refreshed to `57` promoted |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | two staged books, two marker sidecars, two canon books, two dossiers, dashboard |
| `Verification run` | `done` | validators, footnote verifier, purity audit, dry-run promote, promote |
| `Artifacts refreshed` | `done` | `reports/JUD_promotion_dossier.json`, `reports/PHM_promotion_dossier.json`, `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | `JUD` retains its allowed `V8` heading-density warning; the remaining NT queue is `1TI`, `2PE`, `JAS`, and `TIT` |
| `Next owner` | `ezra` | refresh live dispatch so the queue truth reflects `57` promoted books and routes the next NT cleanup lane from current verifier output |

## Requested Next Action
- Close this packet on the live boards and rerank the remaining four NT books from current validator, footnote, and purity output rather than stale dossiers.

## Handoff
**To:** `ezra`  
**Ask:** `Route JUD and PHM as promoted, then dispatch the next NT cleanup lane from the remaining four staged books.`
