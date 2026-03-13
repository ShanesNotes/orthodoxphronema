# Memo 85 — Long-Horizon Repo Cleanup Program

**Author:** `ezra`  
**Type:** `workflow_implementation`  
**Status:** `in_review`  
**Scope:** `repo cleanup / artifact triage / long-horizon organization`  
**Workstream:** `workflow`  
**Phase:** `2`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- OT promotion is complete at `49/49`.
- The repo’s highest long-horizon debt is no longer missing OT books; it is accumulated artifact sprawl from the OT sprint, NT stabilization sprint, and memo-growth period.
- `git status` currently shows a large mixed tail of tracked changes plus untracked helpers, memos, staged variants, schema drafts, and audit outputs.

## Objective
- Turn repo sprawl into explicit cleanup lanes.
- Preserve useful work without letting temporary artifacts become permanent by accident.
- Keep cleanup non-destructive on the active branch: classify first, delete or archive later with explicit intent.

## Reviewed Artifact Classes
### Untracked memo tail
- Current count: `48`
- Includes:
  - NT cleanup reports in the `08_*_cleanup_report.md` family
  - OT closeout memos `66-85`
  - `INDEX.md`
- Judgment:
  - some are now clearly governing or historical record and should be adopted into the tracked memo archive
  - some are same-day or superseded operational notes and should be consolidated rather than left as standalone drift

### Untracked cleanup / helper scripts
- Current count: `17` under `pipeline/cleanup/` plus `1` under `pipeline/tools/`
- Families present:
  - book-specific recovery scripts: `job_*`, `sir_*`, `psa_recovery.py`
  - generic helpers worth retaining: `apply_purity_cleanup.py`, `repair_truncations.py`, `repair_verse_1.py`, `spell_audit.py`
  - NT one-off scripts: `nt_safe_purity.py`, `nt_surgical_fix.py`, `nt_verse_recovery.py`
- Judgment:
  - retain and track reusable helpers
  - archive or delete later the one-book sprint scripts once their logic is either absorbed or no longer needed

### Untracked staged variants
- Current count: `5`
- Files:
  - `staging/validated/OT/JOB_photius.md`
  - `staging/validated/OT/JOS_photius.md`
  - `staging/validated/OT/RUT_photius.md`
  - `staging/validated/OT/SIR_photius.md`
  - `staging/validated/OT/SIR_flash.md`
- Judgment:
  - these violate the one-staged-artifact steady-state rule
  - do not use them as live scripture sources
  - move them to archive or delete later after explicit human review

### Untracked schema and advisory files
- Current count: `4` schema drafts plus miscellaneous advisory files:
  - `schemas/anchor_backlinks.json`
  - `schemas/liturgical_reference.json`
  - `schemas/patristic_source_metadata.json`
  - `schemas/biblical_names.txt`
  - `reviews/OrthodoxPhronemaArchiveGithub.txt`
  - `structural-drift-report-2026-03-10.txt`
- Judgment:
  - keep schema drafts out of governing workflow until Phase 3 ratification
  - move advisory text outputs to `research/` or an archive location when they are deliberately retained

## Cleanup Program
### Lane 1: Canon-Hygiene First
- Keep the current execution priority:
  - `JOS`
  - `JDG`
  - `WIS`
- Do not let organizational cleanup block the live canon-quality lane.

### Lane 2: Adopt Reusable Helpers
- Candidate helpers to retain as tracked repo tools:
  - `pipeline/cleanup/apply_purity_cleanup.py`
  - historical `pipeline/archive/historical_cleanup/pdf_repairs/repair_truncations.py`
  - historical `pipeline/archive/historical_cleanup/pdf_repairs/repair_verse_1.py`
  - `pipeline/tools/spell_audit.py`
- Requirement before adoption:
  - brief tests or at least explicit scope documentation
  - one durable memo or board note confirming why they remain

### Lane 3: Quarantine Sprint Scripts
- Book-specific sprint scripts should be classified as:
  - `archive_keep`
  - `absorb_then_delete`
  - `delete_later`
- Default class for:
  - `job_absolute_*`
  - `job_final_*`
  - `sir_*_recovery.py`
  - `psa_recovery.py`
  - `find_psa_mismatch.py`
  - `psa_final_fix.py`
  is `delete_later` unless a live reusable seam is identified.

### Lane 4: Retire Parallel Staged Variants
- `*_photius.md` and `SIR_flash.md` should not survive as live artifacts in `staging/validated/OT/`.
- Do not delete them in the middle of active branch churn.
- Next safe action:
  - move to an archive location or remove in one explicit cleanup commit after human review

### Lane 5: Memo Archive Normalization
- Keep the current index/board model.
- Next memo cleanup rule:
  - adopt the memos that are now governing or historical record
  - stop spawning new standalone memos for same-day state pings
  - consolidate superseded operational memos into index status instead of proliferating more replacements

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Cleanup is classification-first, not delete-first | Current branch has too much mixed work for safe blind deletion | Artifact sprawl remains briefly visible | Run a dedicated cleanup commit later |
| Reusable helper adoption should be selective | Some new scripts are genuinely reusable, many are sprint residue | Could keep too many tools if not pruned later | Reclassify after canon-hygiene work |
| Parallel staged variants should be retired | They violate the one-artifact rule and create future ambiguity | Deleting too early could lose evidence | Archive them first if needed |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | project board, ops board, this memo |
| `Verification run` | `done` | repo artifact inventory via `git status`, file classification pass, dashboard truth read |
| `Artifacts refreshed` | `done` | coordination surfaces now carry repo cleanup as an active lane |
| `Remaining known drift` | `present` | untracked memo/helper/variant tail still exists physically |
| `Next owner` | `ezra / human / ark` | Ezra for triage execution, Human for archive/delete tolerance, Ark for any helper adoption that crosses into pipeline ownership |

## Requested Next Action
- Ezra:
  - continue canon hygiene first
  - then prepare one dedicated cleanup commit plan that separates reusable helper adoption from archive/delete work
- Human:
  - later approve whether staged variants and one-off sprint scripts should be archived or deleted
- Ark:
  - weigh in only where helper adoption touches long-lived pipeline ownership

## Handoff
**To:** `human / ark / ezra`  
**Ask:** `Treat long-horizon cleanup as an explicit project lane: canon hygiene first, then helper adoption, staged-variant retirement, and memo/script triage in a dedicated cleanup pass.`
