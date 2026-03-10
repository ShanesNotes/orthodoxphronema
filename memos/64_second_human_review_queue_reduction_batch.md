# Memo 64 — Second Human Review Queue Reduction Batch

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `drop-cap sidecar refresh / purity queue reduction / dashboard truth`

## Context
- After Memo 63, the next large block of apparent human-review work looked suspiciously stale rather than truly unresolved.
- `2CH`, `1SA`, `1CH`, `2KI`, `JDG`, and `2SA` were the highest-value follow-up candidates because their staged chapter-open text already looked clean.
- `JOS.24:1` still had one real chapter-open ambiguity that could be checked directly against the OSB PDF.

## Objective
- Collapse stale drop-cap and purity sidecars where staged text was already clean.
- Repair `JOS.24:1` from the OSB PDF and remove its last chapter-open editorial blocker.
- Refresh dashboard-visible state so these books stop appearing to require manual review.

## Files / Artifacts
- [staging/validated/OT/JOS.md](/home/ark/orthodoxphronema/staging/validated/OT/JOS.md)
- [staging/validated/OT/2CH_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/2CH_dropcap_candidates.json)
- [staging/validated/OT/1SA_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/1SA_dropcap_candidates.json)
- [staging/validated/OT/1CH_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/1CH_dropcap_candidates.json)
- [staging/validated/OT/2KI_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/2KI_dropcap_candidates.json)
- [staging/validated/OT/JDG_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/JDG_dropcap_candidates.json)
- [staging/validated/OT/2SA_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/2SA_dropcap_candidates.json)
- [staging/validated/OT/JOS_dropcap_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/JOS_dropcap_candidates.json)
- [staging/validated/OT/2CH_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/2CH_editorial_candidates.json)
- [staging/validated/OT/1SA_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/1SA_editorial_candidates.json)
- [staging/validated/OT/1CH_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/1CH_editorial_candidates.json)
- [staging/validated/OT/2KI_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/2KI_editorial_candidates.json)
- [staging/validated/OT/JDG_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/JDG_editorial_candidates.json)
- [staging/validated/OT/2SA_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/2SA_editorial_candidates.json)
- [staging/validated/OT/JOS_editorial_candidates.json](/home/ark/orthodoxphronema/staging/validated/OT/JOS_editorial_candidates.json)
- [reports/1CH_promotion_dossier.json](/home/ark/orthodoxphronema/reports/1CH_promotion_dossier.json)
- [reports/2CH_promotion_dossier.json](/home/ark/orthodoxphronema/reports/2CH_promotion_dossier.json)
- [reports/1SA_promotion_dossier.json](/home/ark/orthodoxphronema/reports/1SA_promotion_dossier.json)
- [reports/JOS_promotion_dossier.json](/home/ark/orthodoxphronema/reports/JOS_promotion_dossier.json)
- [reports/book_status_dashboard.json](/home/ark/orthodoxphronema/reports/book_status_dashboard.json)

## Findings Or Changes
- Confirmed that `2CH`, `1SA`, `1CH`, `2KI`, `JDG`, and `2SA` were carrying stale drop-cap / purity queues.
  - Their refreshed `*_dropcap_candidates.json` files are now `0`.
  - Their refreshed `*_editorial_candidates.json` files are now `0`.
- Repaired the last chapter-open ambiguity in [JOS.md](/home/ark/orthodoxphronema/staging/validated/OT/JOS.md):
  - `JOS.24:1` now reads: `Then Joshua gathered together all the tribes of Israel to Shiloh, and summoned their elders, scribes, and judges; and he set them before God.`
  - This was confirmed directly from `pdftotext` on the OSB PDF page span for Joshua.
- Refreshed generated state:
  - `1CH`, `2CH`, `JOS`, `2KI`, `DAN`, and `EXO` now surface as `promotion_ready`.
  - `1SA`, `JDG`, and `2SA` no longer have editorial blockers; they remain held only by governance / residual policy.
  - `AMO` remains the only book touched in this lane with live chapter-open ambiguity (`2` items).

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Treat clean staged openings as stale-sidecar debt first | Cheapest way to shrink Human review without guessing | Could miss a subtle real defect | Re-run `dropcap_verify.py` after any text change |
| Repair `JOS.24:1` directly | PDF probe provided the missing opening phrase clearly | Structural context around `JOS` is historically noisy | Validation and refreshed sidecars keep the scope bounded to that line |
| Refresh only dossiers needed for queue truth | Avoid unnecessary churn while making status accurate | Some unaffected books still have older dossier timestamps | Re-run dossier refresh book-by-book when ownership lanes pick them up |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `JOS` validation | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/JOS.md` |
| `1CH` dossier refresh | `pass` | `python3 pipeline/promote/promote.py --book 1CH --dry-run --allow-incomplete` |
| `2CH` dossier refresh | `pass` | `python3 pipeline/promote/promote.py --book 2CH --dry-run --allow-incomplete` |
| `1SA` dossier refresh | `pass` | `python3 pipeline/promote/promote.py --book 1SA --dry-run --allow-incomplete` |
| `JOS` dossier refresh | `pass` | `python3 pipeline/promote/promote.py --book JOS --dry-run --allow-incomplete` |
| Dashboard refresh | `pass` | `python3 pipeline/tools/generate_book_status_dashboard.py` |
| Purity-audit regression tests | `pass` | `pytest tests/test_purity_audit.py tests/test_fix_articles.py -q` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `JOS.md`, refreshed OT drop-cap and editorial sidecars for `2CH`, `1SA`, `1CH`, `2KI`, `JDG`, `2SA`, `JOS`, refreshed dossiers for `1CH`, `2CH`, `1SA`, `JOS`, refreshed dashboard, this memo |
| `Verification run` | `done` | `dropcap_verify.py`, `purity_audit.py`, `validate_canon.py`, `promote.py --dry-run --allow-incomplete`, `generate_book_status_dashboard.py`, `pytest tests/test_purity_audit.py tests/test_fix_articles.py -q` |
| `Artifacts refreshed` | `done` | sidecars, dossiers, `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | `AMO` still has `2` unresolved chapter-open ambiguities; `1SA`, `JDG`, and `2SA` are governance-held despite editorial clearance |
| `Next owner` | `ark` | treat the remaining manual-review lane as small and explicit rather than broad and noisy |

## Requested Next Action
- Do not spend more Human time on `2CH`, `1SA`, `1CH`, `2KI`, `JDG`, `2SA`, or `JOS` chapter-open review.
- If another queue-reduction pass is needed, the remaining high-value target is `AMO` only, plus any yet-unverified poetry-book review debt Photius surfaces.

## Handoff
**To:** `ark`  
**Ask:** `Route work based on the new smaller queue: only `AMO` still has live chapter-open ambiguity from this lane; the rest are now editorially clear or blocked for non-editorial reasons.`
