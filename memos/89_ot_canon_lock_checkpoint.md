# OT Canon Lock Checkpoint — 2026-03-11

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `ot canon lock`
**Workstream:** `canon-hygiene`  
**Phase:** `2`  
**Supersedes:** `84`  
**Superseded by:** `none`

## Context
- OT promotion is complete at `49/49`, but promoted OT canon still carried note-marker contamination and validator-warning debt.
- Human set the lock bar to block on text issues and required canon-wide removal of note/footnote markers from OT canon.
- Promoted OT staged files are not currently safe as a wholesale re-promotion base, so this pass had to treat canon as the lock surface.

## Objective
- Remove safe, corpus-wide OT canon contamination now.
- Refresh the OT canon audit surfaces from live canon truth.
- Reduce OT lock blockers to an explicit final queue instead of a broad warning cloud.

## Files / Artifacts
- `canon/OT/*.md`
- `reports/canon_ot_structural_audit.json`
- `reports/canon_ot_spell_audit.json`
- `memos/ezra_ops_board.md`
- `PROJECT_BOARD.md`
- `memos/INDEX.md`

## Findings Or Changes
- Removed canon-wide note/footnote markers (`†`, `ω`) from OT canon.
- Cleared the dense `###` heading layer in `1MA`, `2MA`, `HAB`, and `LJE`, which removed their `V8` heading-density warnings.
- Cleared the two colon-ended fragment headings in `JOB`, which removed the last OT canon error class.
- Refreshed the OT canon structural audit from canon truth:
  - `0` structural errors
  - `18` warning-bearing OT books
  - `17` of those books are `V7`-only
  - `EST` is the only remaining non-`V7` warning book
- Refreshed the OT canon spell audit:
  - `905` spelling suspects remain
  - this surface is still advisory and too noisy to use as a lock blocker without curated confirmation
- Important repo truth discovered during the pass:
  - several promoted OT staged files are not safe as a bulk re-promotion base
  - OT canon lock and promoted OT staged/canon resync must be tracked as separate lanes

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Treat OT canon as the lock surface | Promoted OT staged files are not uniformly stable enough for a safe all-books re-promotion pass | Dossier freshness and staged/canon sync remain separate work | Resync book-by-book from stable staged sources later |
| Block OT lock on non-`V7` text issues only | Human set the lock bar to block on text issues, not generic warning volume | `V7` drift could hide real corruption if misclassified | Keep `EST` and any future non-`V7` warning out of the ratification bucket |
| Keep spell audit advisory | Current suspect set still contains many proper names and acceptable compounds | Real OCR residue may remain in the advisory set | Curate allowlist / promote only corroborated spell findings later |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Canon marker purge | `pass` | `† []`, `ω []` across `canon/OT/*.md` |
| OT canon structural audit | `pass` | `python3 pipeline/tools/batch_validate.py --dir canon/OT --output-json reports/canon_ot_structural_audit.json` |
| `JOB` post-fix validation | `pass` | `python3 pipeline/validate/validate_canon.py canon/OT/JOB.md` |
| OT canon spell audit | `warn` | `python3 pipeline/tools/spell_audit.py --dir canon/OT --allowlist schemas/biblical_names.txt --output-json reports/canon_ot_spell_audit.json` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `canon/OT/*.md`, `reports/canon_ot_structural_audit.json`, `reports/canon_ot_spell_audit.json`, `memos/ezra_ops_board.md`, `PROJECT_BOARD.md`, `memos/INDEX.md` |
| `Verification run` | `done` | `validate_canon.py canon/OT/JOB.md`, `batch_validate.py --dir canon/OT`, `spell_audit.py --dir canon/OT` |
| `Artifacts refreshed` | `partial` | OT canon audit reports refreshed; dashboard and promotion dossiers intentionally not refreshed in this canon-first pass |
| `Remaining known drift` | `present` | Promoted OT staged files are not uniformly resynced to canon; dashboard remains a promotion-state surface, not the OT lock surface |
| `Next owner` | `human` | Ratify the OT `V7` drift set and decide `EST` disposition |

## Open Questions
- Should `EST.4:6` be treated as source-absent and ratified as-is, or should it get one more bounded source/image review before OT lock is declared?
- Should the `V7` warning set be ratified as versification drift now, or reviewed book-by-book in smaller packets?

## Requested Next Action
- Human reviews the OT lock packet:
  - `EST` as the only non-`V7` blocker
  - `GEN`, `EXO`, `NUM`, `DEU`, `JDG`, `2KI`, `1CH`, `2CH`, `EZR`, `JOB`, `EZK`, `TOB`, `JDT`, `SIR`, `BAR`, `1MA`, `3MA` as the `V7`-only ratification set
- After that decision, Ezra can either mark OT canon locked or continue with one bounded `EST` disposition pass.

## Handoff
**To:** `human`  
**Ask:** `Review Memo 89 as the OT lock checkpoint and decide the EST disposition plus the V7-only ratification set.`
