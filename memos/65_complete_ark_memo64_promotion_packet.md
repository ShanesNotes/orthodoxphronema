# Memo 65 — Complete Ark Memo 64 Promotion Packet

**Author:** `ezra`
**Type:** `implementation`
**Status:** `implemented`
**Scope:** `memo64 packet completion / canon checkpoint / dashboard reconciliation`

## Context
- Ark's Memo 64 handed off a partially completed session with pending promotions for `ECC`, `EZK`, and `JER`.
- By implementation time, repo truth had moved past parts of the memo:
  - [canon/OT/EZK.md](/home/ark/orthodoxphronema/canon/OT/EZK.md) already existed locally as an untracked canon artifact.
  - [reports/book_status_dashboard.json](/home/ark/orthodoxphronema/reports/book_status_dashboard.json) classified `EZK` as `promoted` because the canon artifact existed.
- Leaving `EZK` out of the checkpoint would have preserved an inconsistent local state: canon artifact present, dashboard promoted, but no commit boundary recording it.

## Objective
- Close Ark's stopped promotion packet as a coherent checkpoint.
- Refresh canon, dossiers, and dashboard so they all describe the same local state.
- Avoid mixing this packet with the still-open cleanup lanes for `JOB`, `SIR`, `PRO`, `PSA`, and `WIS`.

## Findings Or Changes
- Re-promoted `ECC` from [staging/validated/OT/ECC.md](/home/ark/orthodoxphronema/staging/validated/OT/ECC.md) into [canon/OT/ECC.md](/home/ark/orthodoxphronema/canon/OT/ECC.md).
- Re-promoted `JER` from [staging/validated/OT/JER.md](/home/ark/orthodoxphronema/staging/validated/OT/JER.md) into [canon/OT/JER.md](/home/ark/orthodoxphronema/canon/OT/JER.md).
- Included `EZK` in the checkpoint because the canon artifact already existed locally and the dashboard already counted it as promoted.
- Refreshed:
  - [reports/ECC_promotion_dossier.json](/home/ark/orthodoxphronema/reports/ECC_promotion_dossier.json)
  - [reports/EZK_promotion_dossier.json](/home/ark/orthodoxphronema/reports/EZK_promotion_dossier.json)
  - [reports/JER_promotion_dossier.json](/home/ark/orthodoxphronema/reports/JER_promotion_dossier.json)
  - [reports/book_status_dashboard.json](/home/ark/orthodoxphronema/reports/book_status_dashboard.json)
- Preserved Ark's staged packet files for `ECC`, `EZK`, and `JER` in the same checkpoint instead of cherry-picking only canon outputs.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Include `EZK` in the packet | Existing local canon artifact plus dashboard truth made exclusion inconsistent | `EZK` still carries nonzero structural warning debt | Re-open `EZK` in a follow-up cleanup memo and re-promote after source verification |
| Keep `SIR`, `PRO`, `WIS`, `JOB`, and `PSA` out of this checkpoint | They need cleanup or further review and would blur the promotion checkpoint | Leaves meaningful work still open | Handle in separate lane-specific commits |
| Commit only the Memo 64 packet files plus this memo | Produces a clean recovery boundary after Ark's session limit interruption | Other local work remains dirty | Land later packets separately |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `ECC` validation | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/ECC.md` |
| `JER` validation | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/JER.md` |
| `EZK` validation | `pass with warnings` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/EZK.md` |
| `ECC` promotion | `pass` | `python3 pipeline/promote/promote.py --book ECC --allow-incomplete` |
| `JER` promotion | `pass` | `python3 pipeline/promote/promote.py --book JER --allow-incomplete` |
| Dashboard refresh | `pass` | `python3 pipeline/tools/generate_book_status_dashboard.py` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `ECC`, `EZK`, `JER` canon/report/staging packet plus this memo |
| `Verification run` | `done` | `validate_canon.py`, `promote.py`, `generate_book_status_dashboard.py` |
| `Artifacts refreshed` | `done` | canon files, promotion dossiers, dashboard |
| `Remaining known drift` | `present` | `JOB`, `SIR`, `PRO`, `PSA`, `WIS` still require cleanup or review; unrelated local dirt remains outside this checkpoint |
| `Next owner` | `ezra` | continue with cleanup lanes after the packet checkpoint is committed |

## Rescue Addendum — Photius Containment After Revised Memo 65

### Situation
- Photius continued broad experimentation after this packet checkpoint and expanded into:
  - `pipeline/common/poetry.py`
  - `pipeline/tools/restructure_pro.py`
  - `schemas/anchor_registry.json`
  - multiple unrelated staged books and reports
  - new ad hoc helper scripts and tests
- That exceeded the intended `PSA` / `PRO` recovery lane and made the dirty experiment state unsafe to continue directly on `main`.

### Containment Action Taken
- The full experimental worktree was preserved on:
  - branch: `photius-rescue-snapshot-20260310`
  - commit: `cb4dc6b`
  - message: `Snapshot Photius PSA/PRO experiments before containment`
- `main` was then restored to the clean committed baseline so the active rescue lane could be narrowed safely.

### Corrected Repo Truth On Clean `main`
- `PSA`
  - still has `151` chapters
  - still reads as a `raw` intermediate artifact with `source: "OSB-v1"`
  - still has `61` live `V4` gap groups / `62` missing verses on clean `main`
  - therefore it is not yet in a simple normalize-and-promote lane on `main`
- `PRO`
  - clean `main` is safer than the experimental branch
  - the current baseline no longer has the raw fragment-heading explosion from the snapshot branch
  - but it still fails promotion-readiness at `V2 expected 31, got 30` and `V7 gap 66`
  - visible kerning and split-word residue remains throughout the early chapters

### Active Rescue Lane On `main`
- Only these artifacts are in scope during rescue:
  - [staging/validated/OT/PSA.md](/home/ark/orthodoxphronema/staging/validated/OT/PSA.md)
  - [staging/validated/OT/PRO.md](/home/ark/orthodoxphronema/staging/validated/OT/PRO.md)
  - [reports/PSA_promotion_dossier.json](/home/ark/orthodoxphronema/reports/PSA_promotion_dossier.json)
  - [reports/PRO_promotion_dossier.json](/home/ark/orthodoxphronema/reports/PRO_promotion_dossier.json)
  - this memo
- Everything else from the experiment branch is archive material and must not be reintroduced into `main` during this rescue.

### Rescue Rules
- Photius is not to make further code, schema, or multi-book workflow changes on `main` during this pass.
- If a proposed change touches anything outside the five in-scope artifacts above, stop and hand back to Ezra/Ark.
- `PRO` work must continue from the clean `main` baseline, not from the dirtier snapshot version.
- `PSA` work on `main` must prove validator improvement from the clean baseline; if a change worsens the current `PSA` state, revert to the clean `main` version and continue analysis off-branch.

### Immediate Handoff
**To:** `photius`
**Ask:** `Use the snapshot branch as archive only. On main, touch only PSA.md, PRO.md, their dry-run dossiers, and Memo 65. Do not resume the broader code churn. Continue PRO from clean main, and treat PSA as still structurally unresolved on main until dry-run evidence improves from that baseline.`
