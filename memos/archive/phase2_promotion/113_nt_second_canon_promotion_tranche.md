# NT Second Canon Promotion Tranche (`1TH`, `2TH`, `2TI`, `1JN`) — 2026-03-13

**Author:** `ark`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `NT staged scripture + canon promotion + state refresh`
**Workstream:** `canon-hygiene`  
**Phase:** `4`  
**Supersedes:** `112`  
**Superseded by:** `none`

## Context
- Memo `112` closed marker purity for the next NT tranche and left fused-word scripture residue as the last blocker.
- The active lane was to clean `1TH`, `2TH`, `2TI`, and `1JN` enough to promote from the same staged files that were validated and audited.

## Objective
- Remove the remaining high-confidence fused-word and note-letter residue in the four fresh NT candidates.
- Re-verify structural state, footnote linkage, and purity before promotion.
- Promote every book in the tranche and refresh the generated state surfaces.

## Files / Artifacts
- `staging/validated/NT/1TH.md`
- `staging/validated/NT/2TH.md`
- `staging/validated/NT/2TI.md`
- `staging/validated/NT/1JN.md`
- `canon/NT/1TH.md`
- `canon/NT/2TH.md`
- `canon/NT/2TI.md`
- `canon/NT/1JN.md`
- `reports/1TH_promotion_dossier.json`
- `reports/2TH_promotion_dossier.json`
- `reports/2TI_promotion_dossier.json`
- `reports/1JN_promotion_dossier.json`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- Cleared the remaining tranche-blocking OCR residue in staged scripture:
  - `1TH`: fixed fused forms like `aafter`, `acloak`, `anursing`, `aburden`, `aquiet`, `ashout`, `athief`, `apregnant`, `aholy`, and `abrethren`.
  - `2TH`: fixed fused and note-letter residue like `arighteous`, `abecause`, `ahad`, `ais`, `ain`, `awho`, `bis`, `areceived`, `adisorderly`, `abrother`, and `asign`.
  - `2TI`: fixed fused and note-letter residue like `aby`, `abeloved`, `apure`, `aspirit`, `asound`, `aholy`, `apreacher`, `ateacher`, `aat`, `agood`, `asoldier`, `athe`, `livewith`, `aworker`, `adepart`, `agreat`, `avessel`, `aservant`, `aform`, and `adrink`.
  - `1JN`: fixed fused and note-letter residue like `ajoy`, `aliar`, `anew`, `haveknown`, `havewritten`, `alie`, `aabide`, `aabides`, `amurderer`, `athat`, `acommandment`, `abecause`, `ahe`, `afaith`, `athe`, `aand`, and `asin`.
- Re-ran structural validation, footnote verification, and purity audit on all four books.
- Promoted all four books into `canon/NT/`.
- Refreshed all four promotion dossiers and the book-status dashboard.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Repair residue directly in staged scripture | The remaining defects were local, source-evident, and already promotion-blocking | A missed ambiguous case could have forced a hold | Reopen the exact staged lines from git and re-verify against the OSB PDF |
| Promote `2TI` and `1JN` with existing `V8` warnings | The current gate already allows their heading-density warnings, and no new structural drift remained | Heading curation debt remains visible | Revisit as a later heading-only pass without undoing canon state |
| Refresh dossier and dashboard state in the same lane | Promotion changed readiness truth and stale generated state would be misleading | None | Re-run the generators |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/1TH.md` | `pass` | structural validation clean |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/2TH.md` | `pass` | structural validation clean |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/2TI.md` | `warn` | `V8` only |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/1JN.md` | `warn` | `V8` only |
| `python3 pipeline/cleanup/verify_footnotes.py --book 1TH` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/verify_footnotes.py --book 2TH` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/verify_footnotes.py --book 2TI` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/verify_footnotes.py --book 1JN` | `pass` | scripture markers and footnotes align |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/1TH.md` | `pass` | `0` candidates |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/2TH.md` | `pass` | `0` candidates |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/2TI.md` | `pass` | `0` candidates |
| `python3 pipeline/cleanup/purity_audit.py staging/validated/NT/1JN.md` | `pass` | `0` candidates |
| `python3 pipeline/promote/promote.py --book 1TH --dry-run` | `pass` | canon preview clean |
| `python3 pipeline/promote/promote.py --book 2TH --dry-run` | `pass` | canon preview clean |
| `python3 pipeline/promote/promote.py --book 2TI --dry-run` | `pass` | canon preview clean; `V8` only |
| `python3 pipeline/promote/promote.py --book 1JN --dry-run` | `pass` | canon preview clean; `V8` only |
| `python3 pipeline/promote/promote.py --book 1TH` | `pass` | canon write complete |
| `python3 pipeline/promote/promote.py --book 2TH` | `pass` | canon write complete |
| `python3 pipeline/promote/promote.py --book 2TI` | `pass` | canon write complete |
| `python3 pipeline/promote/promote.py --book 1JN` | `pass` | canon write complete |
| `python3 pipeline/tools/generate_book_status_dashboard.py` | `pass` | dashboard refreshed |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | four staged books, four canon books, four dossiers, dashboard |
| `Verification run` | `done` | validators, footnote verifier, purity audit, dry-run promote, promote |
| `Artifacts refreshed` | `done` | `reports/1TH_promotion_dossier.json`, `reports/2TH_promotion_dossier.json`, `reports/2TI_promotion_dossier.json`, `reports/1JN_promotion_dossier.json`, `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | `2TI` and `1JN` still carry allowed `V8` heading-density warnings; wider NT queue remains for later reranking |
| `Next owner` | `ezra` | refresh live dispatch so the second NT tranche routes as complete and the next NT lane is reranked from current truth |

## Requested Next Action
- Update the live boards so `1TH`, `2TH`, `2TI`, and `1JN` route as promoted, not merely gate-ready.
- Re-rank the remaining NT queue from the refreshed dashboard rather than from the former second-tranche blocker chain.

## Handoff
**To:** `ezra`  
**Ask:** `Treat the second NT canon tranche as complete, close the fused-word cleanup lane, and route the next NT lane from refreshed dashboard truth.`
