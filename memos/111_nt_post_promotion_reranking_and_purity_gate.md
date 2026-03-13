# NT Post-Promotion Reranking and Purity Gate — 2026-03-12

**Author:** `ezra`  
**Type:** `audit`  
**Status:** `implemented`  
**Scope:** `NT next tranche reranking after 2JN/3JN promotion`
**Workstream:** `canon-hygiene`  
**Phase:** `4`  
**Supersedes:** `110`  
**Superseded by:** `none`

## Context
- `2JN` and `3JN` were promoted into `canon/NT/` in Memo `110`.
- The next clean lane was to re-rank the remaining staged NT books from live validator and promote-gate truth instead of stale pre-promotion assumptions.
- Dry-runs were executed on the cleanest-looking candidates to determine whether a second bounded tranche already exists.

## Objective
- Refresh the live NT queue from actual promote-gate results.
- Distinguish `promotion_ready` by current gate logic from books that are still carrying visible purity defects or companion mismatch debt.

## Files / Artifacts
- `reports/1TH_promotion_dossier.json`
- `reports/2TH_promotion_dossier.json`
- `reports/2TI_promotion_dossier.json`
- `reports/1JN_promotion_dossier.json`
- `reports/book_status_dashboard.json`

## Findings Or Changes
- Dry-ran promotion for `1TH`, `2TH`, `2TI`, and `1JN`.
- Regenerated the dashboard after those dossier rewrites so live machine state stayed aligned.
- Post-rerank dashboard truth is now:
  - `51` promoted
  - `4` `promotion_ready` (`1TH`, `2TH`, `2TI`, `1JN`)
  - `6` `editorially_clean`
  - `15` `extracting`
- `2TH` validates fully clean.
- `2TI` and `1JN` validate with only `V8` heading-density warnings, which the current promotion gate allows.
- `1TH` validates cleanly, but still carries visible inline marker residue at `staging/validated/NT/1TH.md:19` (`a †`), which should not be treated as promotion-clean.
- Footnote verification remains warning-bearing for all four candidates, so the next lane should focus on scripture-side purity and marker bleed before the next NT canon tranche.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Regenerate the dashboard after dry-runs | Dry-runs rewrote dossiers and changed queue truth | None; this is a generated truth surface | Re-run the generator |
| Do not promote the new `promotion_ready` set yet | Gate readiness is broader than purity readiness | Slower NT promotion cadence | Promote later from the refreshed queue after purity checks |
| Route the next NT lane as a purity gate, not a promotion lane | `1TH` still shows literal marker bleed and the best candidates still have companion mismatch warnings | Requires one more bounded NT pass | Promote immediately later if purity lane closes cleanly |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `python3 pipeline/promote/promote.py --book 1TH --dry-run` | pass | dossier refreshed; current gate marks `promotion_ready` |
| `python3 pipeline/promote/promote.py --book 2TH --dry-run` | pass | dossier refreshed; current gate marks `promotion_ready` |
| `python3 pipeline/promote/promote.py --book 2TI --dry-run` | pass | dossier refreshed; current gate marks `promotion_ready` |
| `python3 pipeline/promote/promote.py --book 1JN --dry-run` | pass | dossier refreshed; current gate marks `promotion_ready` |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/1TH.md` | pass | structural validation clean |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/2TH.md` | pass | structural validation clean |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/2TI.md` | warn | `V8` only |
| `python3 pipeline/validate/validate_canon.py staging/validated/NT/1JN.md` | warn | `V8` only |
| `python3 pipeline/cleanup/verify_footnotes.py --book 1TH` | warn | marker/footnote mismatch remains |
| `python3 pipeline/cleanup/verify_footnotes.py --book 2TH` | warn | marker/footnote mismatch remains |
| `python3 pipeline/cleanup/verify_footnotes.py --book 2TI` | warn | marker/footnote mismatch remains |
| `python3 pipeline/cleanup/verify_footnotes.py --book 1JN` | warn | marker/footnote mismatch remains |
| `rg -n "†" staging/validated/NT/1TH.md staging/validated/NT/2TH.md staging/validated/NT/2TI.md staging/validated/NT/1JN.md` | warn | visible marker bleed remains in `1TH.1:1` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | refreshed dossiers for `1TH`, `2TH`, `2TI`, `1JN`; refreshed dashboard |
| `Verification run` | `done` | promote dry-runs, targeted validators, footnote verification, inline marker scan |
| `Artifacts refreshed` | `done` | `reports/book_status_dashboard.json` plus four dossiers |
| `Remaining known drift` | `present` | the current promote gate does not distinguish clean scripture from visible inline marker residue or companion mismatch debt |
| `Next owner` | `ezra` | route the next NT lane as a bounded purity pass on the four fresh candidates |

## Requested Next Action
- Open a bounded NT purity pass on `1TH`, `2TH`, `2TI`, and `1JN`, starting with literal inline marker residue and scripture-side note bleed before the next promotion tranche.

## Handoff
**To:** `ezra`  
**Ask:** `Refresh the live boards so the repo truth becomes: four NT books are gate-ready, but the next safe lane is purity, not immediate promotion.`
