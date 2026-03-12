# Memo 73 — PRO And SIR Residual Ratification Packet

**Author:** `ezra`  
**Type:** `audit`  
**Status:** `in_review`  
**Scope:** `PRO / SIR residual ratification`
**Workstream:** `ot-closeout`  
**Phase:** `1`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- Memo 72 reset OT closeout around four holdouts: `PRO`, `SIR`, `JOB`, `PSA`.
- `PRO` and `SIR` are the next promotion packet, but both still carry unratified residual sidecars.
- Current validator and dry-run truth shows these residuals are provenance / governance debt, not live structural failure.

## Objective
- Package `PRO` and `SIR` into one human-readable ratification ask.
- Distinguish residual provenance from current staged-text readiness.
- Preserve one explicit caution: `SIR` still shows visible kerning residue in dry-run preview and should receive one bounded polish pass before actual promotion.

## Files / Artifacts
- `staging/validated/OT/PRO_residuals.json`
- `staging/validated/OT/SIR_residuals.json`
- `reports/PRO_promotion_dossier.json`
- `reports/SIR_promotion_dossier.json`

## Findings Or Changes
- `PRO`
  - Current staged text is structurally complete and dry-runs cleanly.
  - Residual count: `130`, all currently marked `docling_issue`, all unratified.
  - Residual concentration is late-book and clustered, not random:
    - ch.31 = `31`
    - ch.30 = `27`
    - ch.25 = `19`
    - ch.20 = `7`
  - Representative source evidence confirms these chapters are present in the OSB PDF text layer:
    - `PRO.25:1` search hit: “These are the miscellaneous instructions of Solomon...”
    - `PRO.30:7` search hit: “Two things I ask from You...”
    - `PRO.31:10` direct anchor verification found the “A Virtuous Wife” section with verse `10`.
  - Judgment: residuals record extraction exceptions that have already been recovered in staged text. They should be ratified as accepted provenance debt unless Human wants per-entry recovery history preserved elsewhere.
- `SIR`
  - Current staged text is structurally complete and dry-runs with only a `V7` overcount warning (`1377/1371`, gap `-6`).
  - Residual count: `63`, all currently marked `docling_issue`, all unratified.
  - Residual concentration is light overall but heaviest in late-book chapters:
    - ch.48 = `7`
    - ch.49 = `6`
    - ch.2 / ch.33 / ch.34 = `2` each
  - Representative source evidence confirms the late-book residual clusters are present in the OSB PDF text layer:
    - ch.48 search hit: “Then Elijah the prophet rose up like fire...”
    - ch.49 search hit: “The remembrance of Josiah is like the composition of incense...”
  - Caution: dry-run preview still shows visible residue such as `day s`, `aby ss`, `lam p`, and `rem ov es`. This is not a structural blocker, but it is still a canon-purity concern.
  - Judgment: residual posture is ratifiable now, but promotion should wait for one bounded visible-text polish pass.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Ask for `PRO` residual ratification now | Staged text is complete, clean, and source-backed at representative residual clusters | Human may want deeper per-entry evidence | Expand packet with additional PDF spot checks |
| Ask for `SIR` residual ratification now, but hold promotion until polish | Residuals appear to be provenance debt, but visible text still needs a bounded cleanup pass | Human may prefer ratification and polish together | Re-issue `SIR` in a second packet after the polish pass |
| Keep `PRO` and `SIR` together as Packet A | Both are governance-closeout books, not active parser lanes | `SIR` could delay `PRO` if coupled too tightly | Split promotion execution while keeping one ratification memo |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `PRO` validation | `pass` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/PRO.md` |
| `PRO` dry-run | `pass` | `python3 pipeline/promote/promote.py --book PRO --dry-run --allow-incomplete` |
| `PRO` ch.25 source spot-check | `pass` | `python3 pipeline/tools/pdf_verify.py --book PRO --chapter 25 --search "miscellaneous instructions of Solomon"` |
| `PRO` ch.30 source spot-check | `pass` | `python3 pipeline/tools/pdf_verify.py --book PRO --chapter 30 --search "Two things I ask from You"` |
| `PRO.31:10` source spot-check | `pass` | `python3 pipeline/tools/pdf_verify.py --book PRO --anchor PRO.31:10` |
| `SIR` validation | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/SIR.md` (`V7` overcount only) |
| `SIR` dry-run | `warn` | `python3 pipeline/promote/promote.py --book SIR --dry-run --allow-incomplete` (preview exposes visible residue) |
| `SIR` ch.48 source spot-check | `pass` | `python3 pipeline/tools/pdf_verify.py --book SIR --chapter 48 --search "rose up like fire"` |
| `SIR` ch.49 source spot-check | `pass` | `python3 pipeline/tools/pdf_verify.py --book SIR --chapter 49 --search "remembrance of Josiah"` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `memos/73_pro_sir_residual_ratification_packet.md`, `memos/ezra_ops_board.md`, `PROJECT_BOARD.md`, `memos/INDEX.md` |
| `Verification run` | `done` | Validator, dry-run, and `pdf_verify.py` spot checks for `PRO` / `SIR` |
| `Artifacts refreshed` | `partial` | `reports/SIR_promotion_dossier.json` refreshed by dry-run; no book-state dashboard change yet |
| `Remaining known drift` | `present` | `SIR` still needs one bounded visible-text polish pass before promotion |
| `Next owner` | `human` | Ratify `PRO` residual posture; optionally ratify `SIR` residual posture in advance of polish |

## Requested Next Action
- Human:
  - `PRO`: approve residual ratification so promotion can proceed at the next canon checkpoint.
  - `SIR`: approve residual ratification posture, with promotion held until one bounded polish pass lands.
- Ezra:
  - perform the `SIR` polish pass next if no higher-priority `JOB` repair interrupts it.

## Handoff
**To:** `human`  
**Ask:** `Approve PRO residual ratification now. Approve SIR residual ratification posture, with promotion still held until the visible-residue polish pass is complete.`
