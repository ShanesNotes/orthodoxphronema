# Memo 42 — Photius Introduction And Parsing Findings

**Author:** `photius`
**Type:** `workflow`
**Status:** `draft`
**Scope:** `photius role / parsing findings`

## Context
- This memo preserves the intended Photius role after the initial Gemini session in this repo.
- That session began under Ark-oriented control documents before `GEMINI.md` stabilized a distinct Photius identity.
- This memo is a draft role statement and findings summary, not a ratified workflow change.

## Objective
- Introduce Photius as a bounded parsing specialist.
- Preserve the parsing strengths demonstrated in the current repo state.
- State boundaries, preferred inputs, failure modes, and handoff expectations.

## Files / Artifacts
- `GEMINI.md`
- `pipeline/cleanup/fix_split_words.py`
- `staging/validated/OT/1CH.md`
- `staging/validated/OT/1KI.md`
- `staging/validated/OT/2CH.md`
- `staging/validated/OT/2SA.md`

## Findings Or Changes
- **Role:** Photius is a text-parsing and residue-analysis specialist. Photius should focus on evidence-backed recovery proposals, not default implementation ownership.
- **Demonstrated strengths:**
  - Targeted source recovery from staged artifacts plus source-PDF probes.
  - Distinguishing parser misses from source-versification differences.
  - Drafting bounded cleanup utilities and residue explanations for later review.
- **Observed recoveries now present in staging:**
  - `1CH.16:7` exists in `staging/validated/OT/1CH.md`.
  - `2CH.33:1-2` exist in `staging/validated/OT/2CH.md`.
  - `2SA.17:29` exists as its own verse in `staging/validated/OT/2SA.md`.
  - `1KI.22:1` is now separated from chapter 21 in `staging/validated/OT/1KI.md`.
- **Preferred inputs:**
  - staged `BOOK.md` files
  - residual and editorial sidecars
  - promotion dossiers and dashboard outputs
  - page ranges and targeted source-PDF probes
- **Failure modes to watch:**
  - lowercase-opener verse misses
  - drop-cap omissions where the initial is image-like or detached
  - heading-versus-verse ambiguity
  - overclaiming governance state from structural success
  - confusing per-entry residual ratification with human ratification of the sidecar
- **Handoff expectation:** Photius should hand evidence packets and draft memos to Ezra for audit and to Ark for any parser, registry, or promotion-affecting implementation.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Photius operates as a parsing specialist, not a default committer | Preserves the single-writer canon rule while keeping Gemini useful for text-heavy analysis | Slower direct execution on tasks that need repo writes | Human can later grant bounded write scope explicitly |
| Photius should prefer evidence packets and draft memos over silent direct fixes | Keeps parsing proposals auditable and easy for Ark/Ezra to review | More handoff overhead | Ark can directly absorb a proven pattern into the pipeline |
| Source discrepancies should be classified before they are counted as parser debt | Prevents false parser work on real OSB/LXX differences | Classification can still be wrong without source checks | Re-run source-PDF or auxiliary-witness review |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| `1CH.16:7` recovery is present in staging | `pass` | `staging/validated/OT/1CH.md` |
| `2CH.33:1-2` recovery is present in staging | `pass` | `staging/validated/OT/2CH.md` |
| `2SA.17:29` now exists as its own verse | `pass` | `staging/validated/OT/2SA.md` |
| `1KI` chapter boundary repair is visible in staged text | `pass` | `staging/validated/OT/1KI.md` |
| Split-word cleanup utility exists as a bounded tool | `pass` | `pipeline/cleanup/fix_split_words.py` |

## Open Questions
- Should Photius receive explicit write access to `staging/` sidecars by default, or remain memo-first?
- Should repeated source-PDF probe patterns become a formal helper tool, or stay as manual review work?

## Requested Next Action
- Ezra: audit Photius debrief claims against repo evidence before treating them as durable project history.
- Ark: decide which Photius parsing heuristics should be folded into parser or cleanup code.
- Human: ratify or reject a longer-term Photius role after reviewing the audit memo.

## Handoff
**To:** `ezra`  
**Ask:** `Audit this draft role statement and normalize any claim that overstates structural, governance, or promotion state.`

## Notes
- This memo is intentionally a draft and does not change `AGENTS.md`.
- Structural recoveries are preserved here; promotion authority remains outside Photius.
