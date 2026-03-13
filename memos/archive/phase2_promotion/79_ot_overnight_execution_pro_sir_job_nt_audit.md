# Memo 79 — OT Overnight Execution: PRO, SIR, JOB, And NT Audit

**Author:** `ezra`  
**Type:** `implementation_audit`  
**Status:** `in_review`  
**Scope:** `ot closeout overnight execution`  
**Workstream:** `ot-closeout`  
**Phase:** `1`  
**Supersedes:** `memos/74_sir_polish_job_editorial_closure_and_ot_overnight_progress.md`, `memos/75_job_residual_triage_packet.md`  
**Superseded by:** `none`

## Context
- Memo 72 set the OT closeout sequence as `PRO + SIR`, then `JOB`, then `PSA`.
- The session dispatch expected only a light `SIR` polish pass, but live dry-run output showed a much worse problem: chapter 1 contained a leaked stream of headings that did not belong there.
- `JOB` still carried one bounded final PDF-backed recovery pass before converting fully to a human residual-risk decision.
- Ark's NT extraction has already landed in `memos/77_nt_extraction_results.md`, so the ops board also needed a same-session reset.

## Objective
- Remove the last easy formatting residue from `PRO`.
- Reconstruct `SIR` heading placement from the OSB `pdftotext` source layout instead of treating it as generic residue.
- Attempt one last bounded source-backed recovery pass on `JOB`.
- Spot-audit representative NT books so Ark starts NT stabilization from concrete evidence instead of vague severity labels.

## Files / Artifacts
- `staging/validated/OT/PRO.md`
- `staging/validated/OT/SIR.md`
- `staging/validated/OT/JOB.md`
- `reports/PRO_promotion_dossier.json`
- `reports/SIR_promotion_dossier.json`
- `reports/JOB_promotion_dossier.json`
- `reports/book_status_dashboard.json`
- `memos/ezra_ops_board.md`

## Findings Or Changes
### `PRO`
- Fixed the last easy visible residue:
  - `pray ers` -> `prayers` at `PRO.15:8`
  - `pray ers` -> `prayers` at `PRO.15:29`
- `PRO` remains structurally clean and dry-runs cleanly.
- Judgment: `PRO` is ready for human residual ratification, not further text recovery.

### `SIR`
- Confirmed by dry-run that chapter 1 was polluted by a leaked heading stream after nearly every verse.
- Used full-span `pdftotext` source verification across the Sirach PDF range to classify the headings:
  - kept at chapter 1 start: `### Wisdom Is from the Lord`
  - re-homed to chapter starts:
    - `### Put away Evil Acts` -> `SIR.7:1`
    - `### Kings and Commoners` -> `SIR.8:1`
    - `### The Reckless Soul` -> `SIR.19:1`
    - `### Honoring the Physician` -> `SIR.38:1`
    - `### Students of God's Word` -> `SIR.39:1`
    - `### Life's Afflictions` -> `SIR.40:1`
    - `### In Praise of Honored Men` -> `SIR.44:1`
  - removed from wrong locations:
    - the chapter 1 leaked heading stream
    - `### Hosea` before `SIR.3:30`
    - misplaced `### Honoring the Physician` before `SIR.4:31`
    - misplaced heading stream before `SIR.6:32-37`
- Also cleared a bounded set of obvious fused/split residues in the affected sections, including:
  - `give gladness`
  - `decisive influence`
  - `a hypocrite`
  - `strive anxiously`
  - `Cleave to`
  - `Believe in`
  - `everlasting`
  - `have lost`
  - `repays kindnesses`
  - `eye away`
  - `prayer`
  - `lays hold`
  - `serve her`
  - `obeys her`
  - `love to listen`
  - `lying`
  - `Love Him`
  - `destroyed`
  - `a talkative man`
  - `physician`
  - `give instruction`
  - `preserve`
  - `serve in`
  - `give his`
  - `heavy yoke`
  - `mother's womb`
  - `envy`
  - `verse`
  - `Living`
- Judgment: `SIR` is now source-layout correct enough for the same residual ratification packet as `PRO`.

### `JOB`
- Ran the final bounded PDF-backed pass against the live gap groups.
- Recovered one real absorbed chapter-open:
  - split `JOB.39:1` out of the text previously fused onto `JOB.38:41`
- Result after fix:
  - anchors: `1077` (up from `1076`)
  - residual missing-anchor count: `11` (down from `12`)
  - remaining live `V4` gap groups:
    - `17:2`
    - `18:2`
    - `19:4`
    - `23:7-9`
    - `23:13-15`
    - `24:2`
    - `36:30`
- PDF-backed judgment on the remaining groups:
  - `17:2`, `18:2`, `19:4`, `23:7-9`, `36:30`: not found in the PDF text layer
  - `23:13-15`, `24:2`: page-pair / cross-page noisy context, not safe for invented recovery
- Judgment: stop active text repair here and convert `JOB` to a human residual-risk decision.

### NT spot audit
- Representative NT checks:
  - `2JN`: fully clean and currently the best NT exemplar
  - `MAT`: chapter-zero drift, chapter-count mismatch, heavy `V3`, embedded verses
  - `HEB`: duplicate anchors, embedded verses, `44` missing verses
  - `EPH`: chapter-zero drift, duplicate anchors, `50` missing verses, severe `V3/V4/V9`
- OT regression check:
  - `PRO` validator still fully passes
  - `SIR` still passes structurally with the existing `V7` overcount warning only
  - `JOB` improved by one real anchor without structural regressions
- Judgment for Ark:
  - keep NT stabilization priorities as `V1` dedup, `EPH` recovery, then chapter-zero / chapter-count repair

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Keep `PRO` in Packet A with no further recovery work | It is now formatting-clean and structurally done | Human may still want residual review detail | Packet still waits on ratification |
| Reclassify `SIR` from “light polish” to “source-layout repaired” | The real defect was misplaced headings, not just kerning | Some removed headings may need later confirmation if source placement was ambiguous | Re-run page-span verification and reinsert only source-backed headings |
| Stop active `JOB` recovery after the `39:1` fix | Remaining groups are source-absent or page-pair ambiguous in the text layer | A later image/PDF review could still recover more | Keep the residual packet open for future ratification or spot review |
| Hand Ark concrete NT stabilization priorities | The current NT set is too unstable for generic “audit later” language | Ark may prefer a different sequencing once deep in NT | Adjust from live validator results, not memo narrative |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `PRO` validator | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/PRO.md` |
| `PRO` dry-run | `pass` | `python3 pipeline/promote/promote.py --book PRO --dry-run --allow-incomplete` |
| `SIR` validator | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/SIR.md` |
| `SIR` dry-run | `warn` | `python3 pipeline/promote/promote.py --book SIR --dry-run --allow-incomplete` |
| Sirach heading placement proof | `pass` | `python3 pipeline/tools/pdf_verify.py --book SIR --pages 2240-2397 --search ...` |
| `JOB` validator after final pass | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/JOB.md` |
| `JOB` dry-run after final pass | `warn` | `python3 pipeline/promote/promote.py --book JOB --dry-run --allow-incomplete` |
| `JOB` PDF edge-case pass | `warn` | `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/JOB.md` |
| NT sample audit | `mixed` | `validate_canon.py` on `2JN`, `MAT`, `HEB`, `EPH` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `PRO.md`, `SIR.md`, `JOB.md`, refreshed dossiers, ops board, this memo |
| `Verification run` | `done` | OT validators, OT dry-runs, `JOB` edge-case check, NT spot validators |
| `Artifacts refreshed` | `done` | `PRO_promotion_dossier.json`, `SIR_promotion_dossier.json`, `JOB_promotion_dossier.json`, `book_status_dashboard.json` |
| `Remaining known drift` | `present` | `PRO`/`SIR` await human residual ratification; `JOB` retains six live V4 groups plus three V10 warnings; NT books remain unstable |
| `Next owner` | `human / ark / photius` | Human for `PRO`/`SIR`/`JOB` residual posture, Ark for NT stabilization, Photius for `PSA` |

## Requested Next Action
- Human:
  - ratify `PRO` residual packet
  - ratify `SIR` residual packet
  - decide whether `JOB` residual posture is acceptable as-is or should wait for a later image-backed pass
- Ark:
  - start NT stabilization with `EPH`, then chapter-zero / chapter-count issues (`MAT`), then duplicate-anchor cleanup (`HEB`)
- Photius:
  - continue `PSA` only; do not absorb `PRO`, `SIR`, or `JOB`

## Handoff
**To:** `human / ark / photius`  
**Ask:** `Packet A is ready for human review on governance grounds. JOB is now a bounded residual-risk decision, not an active text-repair lane. Ark should stay on NT stabilization, and Photius should keep PSA isolated.`
