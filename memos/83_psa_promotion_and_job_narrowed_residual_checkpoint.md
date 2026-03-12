# Memo 83 — PSA Promotion And JOB Narrowed Residual Checkpoint

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `in_review`  
**Scope:** `ot closeout / psa promotion / job residual narrowing`  
**Workstream:** `ot-closeout`  
**Phase:** `1`  
**Supersedes:** `memos/82_job_retriage_recovery_pass_and_est_disposition.md`  
**Superseded by:** `memos/84_ot_closeout_complete_and_canon_hygiene_handoff.md`

## Context
- OT closeout had been stalled on two remaining holdouts: `JOB` and `PSA`.
- Human reassigned `PSA` away from Photius.
- Live validation showed `PSA` was no longer a structural recovery book; it already passed `V1-V9` and only remained blocked by raw-text quality and stale promotion posture.

## Objective
- Normalize and promote `PSA` from the current staged artifact.
- Use the newly opened OT capacity on one more bounded `JOB` pass.
- Refresh the OT control surfaces so the repo stops routing from stale assumptions.

## Files / Artifacts
- `pipeline/common/poetry.py`
- `pipeline/parse/psa_extract.py`
- `tests/test_poetry_extraction.py`
- `staging/validated/OT/PSA.md`
- `canon/OT/PSA.md`
- `staging/validated/OT/JOB.md`
- `reports/PSA_promotion_dossier.json`
- `reports/JOB_promotion_dossier.json`
- `reports/book_status_dashboard.json`
- `memos/ezra_ops_board.md`

## Findings Or Changes
### `PSA` reclassification and promotion
- Reclassified `PSA` from “systematic verse-2 recovery” to “normalization + promotion.”
- Expanded the shared poetry cleanup seam in `pipeline/common/poetry.py` with safe Psalms-specific kerning repairs and punctuation normalization.
- Fixed a fallback bug in `pipeline/parse/psa_extract.py` for unknown-book defaults.
- Applied the shared poetry cleanup to `staging/validated/OT/PSA.md`.
- Normalized staged `PSA` frontmatter from raw-extraction shape into normal staged shape.
- Promoted `PSA` into `canon/OT/PSA.md`.

### `PSA` result
- `PSA` now validates cleanly with:
  - `V1` through `V9` all `PASS`
- Dry-run and live promotion both write the same checksum:
  - `efb6ccced37135ead3c5eab8ce0c0c2f2386ef14a79977f92c5736fa610cd681`
- Judgment:
  - `PSA` is no longer an OT holdout
  - remaining Psalms marker / Selah policy is part of later canon-hygiene work, not a promotion blocker in this pass

### `JOB` bounded recovery pass
- Used `pdf_verify.py` chapter probes to isolate chapter-open omissions rather than continuing broad recovery.
- Recovered the following source-backed chapter-open verses:
  - `JOB.17:1-2`
  - `JOB.18:1-2`
  - `JOB.20:1`
  - `JOB.21:1`
  - `JOB.22:1`
  - `JOB.24:1-2`
  - `JOB.25:1`
  - `JOB.26:1`
  - `JOB.39:1`

### `JOB` result
- Validator improved from:
  - `20` residual missing anchors
  - `V7` gap `19`
- To:
  - `8` residual missing anchors
  - `V7` gap `7`
- Remaining live warnings are now confined to `JOB.23`:
  - `23:6-9`
  - `23:12-15`
  - `V10` hint at `JOB.23:14`
- Judgment:
  - `JOB` is no longer a broad OT repair lane
  - `JOB` is now a narrow residual-risk / final source-check book

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Promote `PSA` now | Staged text became validator-clean and canon-readable after normalization | Psalms still carries broader marker-policy debt shared by the canon | Re-promote from later staged cleanup if marker policy changes |
| Stop treating `PSA` as a Photius recovery lane | Live repo truth no longer supports that routing | Old memos and board state can mislead tomorrow’s work | Refresh all control surfaces now |
| Narrow `JOB` to the chapter 23 residual cluster | All other remaining chapter-open gaps were source-backed and recoverable | Chapter 23 may still require human ratification or stronger page evidence | Resume only on that cluster if further recovery is justified |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| poetry cleaner tests | `pass` | `pytest tests/test_poetry_extraction.py -q` |
| `PSA` staged validation | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/PSA.md` |
| `PSA` promotion | `pass` | `python3 pipeline/promote/promote.py --book PSA --allow-incomplete` |
| `JOB` staged validation after pass | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/JOB.md` |
| `JOB` dry-run after pass | `warn` | `python3 pipeline/promote/promote.py --book JOB --dry-run --allow-incomplete` |
| `JOB` source proof | `pass` | `python3 pipeline/tools/pdf_verify.py --book JOB --chapter 20/21/22/23/24/25/26/39` |
| dashboard refresh | `pass` | `python3 pipeline/tools/generate_book_status_dashboard.py` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | shared poetry cleaner, PSA staged/canon, JOB staged, refreshed reports, ops board, this memo |
| `Verification run` | `done` | poetry tests, `PSA` validation + promotion, `JOB` validation + dry-run, chapter PDF probes |
| `Artifacts refreshed` | `done` | `reports/PSA_promotion_dossier.json`, `reports/JOB_promotion_dossier.json`, `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | `JOB` still has a bounded chapter 23 residual cluster; promoted-canon hygiene still remains after OT closeout |
| `Next owner` | `ezra / human / ark` | Ezra for final `JOB` disposition, Human for residual acceptance if needed, Ark stays on NT |

## Requested Next Action
- Ezra:
  - treat `JOB` as the only remaining OT holdout
  - decide whether to do one last chapter 23 source pass or convert it directly into the final residual-ratification ask
- Human:
  - be ready for a narrow `JOB` residual packet rather than a broad OT repair decision
- Ark:
  - stay on NT stabilization unless `JOB` exposes a real parser/schema issue

## Handoff
**To:** `human / ark / ezra`  
**Ask:** `PSA is promoted. JOB is down to one real residual cluster in chapter 23. OT closeout is now a single-book finish.`
