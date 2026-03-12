# Memo 82 — JOB Re-Triage Recovery Pass And EST Disposition

**Author:** `ezra`  
**Type:** `implementation_audit`  
**Status:** `in_review`  
**Scope:** `job retriage / est promoted-canon disposition`  
**Workstream:** `ot-closeout`  
**Phase:** `1`  
**Supersedes:** `memos/81_ot_packet_a_promotion_and_ezk_cleanup_checkpoint.md`  
**Superseded by:** `none`

## Context
- After Packet A promotion, `JOB` remained the primary OT holdout and no longer matched the older bounded Memo 79 state.
- The immediate goal was to rebuild a trustworthy `JOB` floor from current staged truth without inventing text.
- In parallel, `EST` was the next promoted-canon warning target after `EZK`.

## Objective
- Recover only the `JOB` verses and chapter-open fragments that are clearly supported by the OSB PDF text layer.
- Stop before ambiguous or article-contaminated segments start forcing speculative text.
- Determine whether `EST.4:6` is fixable or should be treated as source-absent / ratify-as-is.

## Files / Artifacts
- `staging/validated/OT/JOB.md`
- `reports/JOB_promotion_dossier.json`
- `reports/book_status_dashboard.json`
- `memos/ezra_ops_board.md`

## Findings Or Changes
### `JOB` source-backed recoveries
- Repaired chapter-open drop-cap loss:
  - `JOB.1:1` -> `There was ...`
  - `JOB.2:1` -> `Then again ...`
  - `JOB.3:1` -> `After this ...`
- Recovered clean missing verses from the OSB text layer:
  - `JOB.9:16`
  - `JOB.27:22`
  - `JOB.36:29`
  - `JOB.36:30`
  - `JOB.37:12`
  - `JOB.40:3`
- Recovered chapter-open / early-block text where the PDF layer was explicit:
  - `JOB.8:1-3`
  - `JOB.19:3-4`
- Repaired the chapter 19 numbering seam so the inserted verses do not leave a shifted duplicate block behind.

### `JOB` result after the pass
- Validator moved from the broken post-regression state to a bounded warning state:
  - residual missing-anchor count: `29 -> 20`
  - completeness gap: `25 -> 19`
  - current live remaining gap clusters:
    - `17:0->3`
    - `18:0->3`
    - `20:0->2`
    - `21:0->2`
    - `22:0->2`
    - `23:5->10`
    - `23:11->16`
    - `24:0->3`
    - `25:0->2`
    - `26:0->2`
    - `39:0->2`
- Remaining live `V10` hints are now narrowed to:
  - `JOB.17:2`
  - `JOB.23:14`
- Judgment:
  - `JOB` is no longer in catastrophic regression shape
  - `JOB` is still not ready for promotion
  - the next pass should continue from the chapter-open `0 -> n` cases, starting with chapters `17`, `18`, `20`, `21`, `22`, `24`, `25`, `26`, and `39`

### `EST` disposition
- `pdf_edge_case_check.py` on `EST` still does not find `EST.4:6` in the OSB text layer.
- Current judgment:
  - do not invent `EST.4:6`
  - keep `EST` in the promoted-canon warning packet as a likely source-absent / ratify-as-is case until stronger evidence appears

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Keep the `JOB` pass source-backed and narrow | The book is too noisy now for broad heuristic repair | Some recoverable verses remain deferred | Continue later from the narrowed gap list |
| Stop before forcing `JOB.23` from ambiguous PDF context | The text layer around chapter 23 is still mixed and noisy | Leaves a large visible residual cluster | Resume only with cleaner page evidence |
| Hold `EST` as a disposition case, not an edit case | The current PDF text layer does not support the missing verse | Could leave a true omission unresolved | Re-open if stronger page or image evidence appears |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `JOB` validator after recovery pass | `warn` | `python3 pipeline/validate/validate_canon.py staging/validated/OT/JOB.md` |
| `JOB` dry-run after recovery pass | `warn` | `python3 pipeline/promote/promote.py --book JOB --dry-run --allow-incomplete` |
| `JOB` page probes | `pass` | raw `pdftotext` extraction via `pipeline.common.pdf_source.extract_pdf_text()` on pages `1969-1972`, `1986-1989`, `2001-2002`, `2016-2018`, `2024` |
| `EST` edge-case check | `warn` | `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/EST.md` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | `JOB.md`, refreshed `JOB` dossier/dashboard, ops board, this memo |
| `Verification run` | `done` | `JOB` validator + dry-run, targeted PDF page probes, `EST` edge-case check |
| `Artifacts refreshed` | `done` | `reports/JOB_promotion_dossier.json`, `reports/book_status_dashboard.json` |
| `Remaining known drift` | `present` | `JOB` still has `20` missing anchors and `2` live V10 hints; `EST` remains a promoted warning book |
| `Next owner` | `ezra / photius / ark` | Ezra for the next `JOB` or promoted-canon pass, Photius for `PSA`, Ark stays on NT |

## Requested Next Action
- Ezra:
  - either continue `JOB` from the narrowed chapter-open gaps
  - or switch to the next promoted-canon warning case (`JOS` / `JDG`) if OT holdout pressure is intentionally paused
- Human:
  - treat `EST` as likely source-absent unless stronger evidence appears

## Handoff
**To:** `human / ark / photius / ezra`  
**Ask:** `JOB is materially better and back to a bounded warning lane, but it still needs another source-backed pass. EST is not an edit target yet; it is a disposition target.`
