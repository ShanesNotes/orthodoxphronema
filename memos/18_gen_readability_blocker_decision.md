# Genesis Readability Blocker Decision — 2026-03-08

**Author:** `ezra`
**Type:** `audit`
**Status:** `in_review`
**Scope:** `staging/validated/OT/GEN.md / promotion readiness`

## Context
- Human reviewed `staging/validated/OT/GEN.md` and flagged visible spelling / word-conjunction defects.
- Human requested an Ezra executive decision rather than treating GEN as merely a threshold question.
- The current question is whether `GEN.md` is clean enough to proceed toward promotion work.

## Objective
- Decide whether `GEN.md` is promotion-ready from a text-quality standpoint.
- Determine whether the defects are just a stale artifact or the current script/output reality.
- Hand Ark a concrete next step.

## Files / Artifacts
- `staging/validated/OT/GEN.md`
- `staging/validated/OT/GEN_dropcap_candidates.json`
- `staging/validated/OT/GEN_residue_audit.json`
- `memos/08_gen_cleanup_report.md`
- `reports/GEN_promotion_dossier.json`

## Findings Or Changes
- High: `GEN.md` is not clean text and should not be treated as promotion-ready.
  - Visible examples in the staged file:
    - `afirmament` at `GEN.1:6`
    - `heaven'sfirmament` at `GEN.1:20`
    - `afountain` at `GEN.2:6`
    - `ahelper` at `GEN.2:18`
    - `ashepherd` / `asacrifice` at `GEN.4:2-4`
    - `wiv es`, `av enged`, `sev enfold` at `GEN.4:23-24`
  - These are readability defects, not acceptable cosmetic noise.
- High: this is not just a memo-16 staleness problem.
  - The file frontmatter still shows `parse_date: 2026-03-07`, so the staged text itself predates the foundation pass.
  - But the current dossier and sidecars were generated against this same staged artifact, which means the project is knowingly carrying this text forward in its present state.
  - Memo 16 work improved governance, reports, and tests; it did not make `GEN.md` text clean.
- Medium: the repo already has quantitative evidence that GEN text cleanup remains unfinished.
  - `GEN_dropcap_candidates.json` reports `50` candidates (`29` confirmed_auto, `21` ambiguous_human).
  - `GEN_residue_audit.json` reports `52` findings (`31` fused_article, `21` fused_compound).
  - This confirms the defects are systematic, not a few isolated lines.
- Medium: current validation does not capture this class of defect.
  - `GEN` currently passes `V9` and only warns on `V4`/`V7`.
  - Therefore structural validation alone is not enough to declare the file clean.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| GEN is blocked on readability cleanup | Human explicitly wants a clean `GEN.md`; visible OCR/fusion defects remain widespread | Slows first promotion | Revisit after a targeted cleanup pass and rerun |
| Treat current GEN defects as present-state output, not stale bookkeeping | Sidecars and dossier confirm the project is still carrying these defects now | May obscure which fixes are parser vs cleanup | Separate in Ark’s next memo |
| Promotion-threshold discussion should pause for GEN until readability is acceptable | Prevents structural success from waiving obvious text defects | Delays threshold decision | Resume once GEN cleanup pass lands |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Visible text audit | fail | multiple obvious fused/split words in `GEN.md` |
| Drop-cap candidate sidecar | warn | `50` total candidates, `29` auto-confirmed |
| Residue audit sidecar | warn | `52` total findings |
| Promotion dossier | warn | structure-focused; does not clear readability concerns |

## Open Questions
- Should Ark define a temporary readability gate for first-promotion books, using residue/drop-cap counts plus human scan?
- Should confirmed-auto drop-cap repairs be applied deterministically before asking Human to review again?
- Should ambiguous drop-cap candidates be reviewed in one bounded GEN session rather than incrementally?

## Requested Next Action
- Ark: move GEN back into a readability-cleanup lane before promotion-threshold discussion proceeds.
- Ark: distinguish three buckets in the next pass:
  - deterministic auto-fixable drop-cap / fused-space repairs
  - bounded human-ratify ambiguities
  - acceptable historical spellings or genuine OSB wording that should not be normalized away
- Human: defer GEN promotion review until Ark presents a visibly cleaner staged file.

## Handoff
**To:** `ark`
**Ask:** treat GEN as text-quality blocked; deliver a visibly clean `staging/validated/OT/GEN.md` before asking Human to decide promotion readiness.
