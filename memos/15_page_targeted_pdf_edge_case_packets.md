# Page-Targeted PDF Edge-Case Packets — 2026-03-08

**Author:** `ezra`
**Type:** `workflow`
**Status:** `implemented`
**Scope:** `pipeline/validate/pdf_edge_case_check.py`

## Context
- Human requested movement toward LLM-assisted PDF spot checks for low-residual books instead of continued heuristic growth.
- The existing PDF edge-case helper already identified `V4` gaps and printed text windows, but it did not emit durable machine-readable output or page-targeted review packets.
- Memo 14 recommended a small enhancement rather than a larger new subsystem.

## Objective
- Make residual `V4` spot checks easier to hand off to Ark or an LLM reviewer.
- Keep the workflow source-backed and page-local.
- Avoid changing parser heuristics as part of this step.

## Files / Artifacts
- `pipeline/validate/pdf_edge_case_check.py`

## Findings Or Changes
- Added page-aware PDF matching:
  - the helper now splits the extracted OSB text into absolute PDF pages and book-local pages
  - a match can be reported against a single page or an adjacent page pair
- Added structured JSON output:
  - new `--json-out PATH` flag writes per-gap packets with
    - gap label
    - chapter / verse range
    - staged line numbers
    - adjacent staged verse text
    - matched PDF page span
    - matched PDF snippet
- Added optional page rendering for visual review:
  - new `--render-dir DIR` flag renders matched PDF pages with `pdftoppm`
  - rendered image paths are included in the JSON packet
- Preserved the current terminal report so the tool remains human-usable without downstream tooling.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Add JSON as an opt-in output, not default | Keeps existing workflow stable while enabling durable LLM packets | Users may forget to request JSON | Make it default later if the team adopts it |
| Match on page and adjacent page-pair scopes | Covers most low-residual edge cases without full coordinate extraction | Some true matches may still remain unresolved | Add richer PDF localization later |
| Render full matched pages, not cropped regions | Fast to implement and enough for manual / LLM visual confirmation | More visual noise than region crops | Add coordinate-aware crops later if needed |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Script syntax | pass | `python3 -m py_compile pipeline/validate/pdf_edge_case_check.py` |
| GEN JSON packet | pass | `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/GEN.md --limit 1 --json-out /tmp/gen_pdf_edge_cases_fixed.json` |
| GEN page rendering | pass | `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/GEN.md --limit 1 --json-out /tmp/gen_pdf_edge_cases_fixed.json --render-dir /tmp/gen_pdf_pages_fixed` |
| EXO packet coverage | warn | `python3 pipeline/validate/pdf_edge_case_check.py staging/validated/OT/EXO.md --limit 4 --json-out /tmp/exo_pdf_edge_cases_full.json` matched `2/4` current gap groups |

## Open Questions
- Should the tool default to writing JSON into `reports/` when `--json-out` is omitted?
- Should Ark add a thin reviewer wrapper that converts the JSON packet into a fixed LLM prompt template?
- Should unresolved `not found` cases like `EXO.21:24-25` and `EXO.25:4-7` trigger automatic escalation to page-image review or registry/witness comparison?

## Requested Next Action
- Ark: use the JSON/page packet mode for low-residual books before growing parser heuristics.
- Ark: decide whether to build a small prompt wrapper around the emitted JSON packets.
- Human: notify Ark to resume once this memo and the new helper output format are accepted.

## Handoff
**To:** `ark`
**Ask:** continue from page-targeted packet output, not from broader opener growth, on books with residual `V4` under the spot-check threshold.
