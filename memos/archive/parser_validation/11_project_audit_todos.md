# Project Audit — Current Loop and Forward Plan — 2026-03-07

**Author:** `ark`
**Type:** `workflow`
**Status:** `in_review`
**Scope:** Full project sequencing (pipeline, registry, staging, canon, tooling)

## Context
- Reframed after Ezra review to reduce oscillation between present-day execution and long-range planning.
- GEN and EXO are staged; zero books promoted to canon yet.
- The pipeline is functional, but the active bottleneck is still residual parser quality on the first two books.
- The previous version preserved inventory well, but mixed immediate blockers, ready parallel work, and Phase 2 ideas into one queue.

## Objective
- Keep one memo that preserves the project backlog.
- Separate `do now`, `ready next`, and `park for later`.
- Make gate ownership explicit so Ark can stay in the current loop without losing forward visibility.

## Working Rule
```text
Present-day execution and future planning must use different lanes.
```

Rules:
- Only `Now` items may compete for the next implementation session.
- `Ready Next` items may be prepared or documented, but should not displace unresolved `Now` gates.
- `Later` items remain visible for architecture continuity, but are not active work until their trigger is met.
- Revisit the `Later` lane only at milestones: first promotion, five promoted books, and pre-NT preparation.

## Gate Snapshot
| Gate | Current State | Owner | Next Evidence |
|---|---|---|---|
| G1. GEN/EXO residual boundary-shape recovery | **closed** | Ark | GEN 99.7%, EXO 98.0% — remaining gaps are non-regex issues (memo 13) |
| G2. First-promotion threshold | pending | Human | explicit acceptable `V4` / `V7` threshold |
| G3. Registry `chapter_verse_counts` completion for scale | pending | Ark | verified additions in `schemas/anchor_registry.json` |
| G4. Commit current workflow/tooling state | ready | Ark | clean commit boundary after current loop stabilizes |

## Now — Present-Day Execution Loop
These items should govern the next 1-3 work sessions.

### N1. Close residual GEN/EXO parser edge cases
| Field | Detail |
|---|---|
| Why now | This is the main structural blocker to confident first promotion and to meaningful scale-out |
| Evidence | `memos/10_lowercase_verse_split_strategy.md`, `memos/11_gen_exo_v4_edge_case_source_verification.md`, `memos/12_pdf_edge_case_spot_check_gate.md` |
| Constraint | Use `pipeline/validate/pdf_edge_case_check.py` before broadening allowlists or `_LC_OPENERS` |
| Special case | `GEN.49:2` is a separate poetic-block carryover issue, not a generic lc-opener miss |
| Exit | Updated `GEN.md` / `EXO.md`, rerun `validate_canon.py`, record before/after counts in memo |

### N2. Decide first-promotion threshold
| Field | Detail |
|---|---|
| Why now | Promotion readiness is undefined until Human states the acceptable residual defect level |
| Current counts | As of 2026-03-08 validation (registry corrected): GEN = 1 `V4` group / 3 `V7` gap / `99.8%`; EXO = 4 `V4` groups / 5 `V7` gap / `99.6%` |
| Owner | Human |
| Input | Ezra source verification + Ark rerun after parser patch |
| Exit | Explicit decision recorded in memo or audit log |

### N3. Bound GEN fused-compound cleanup to promotion-relevant cases only
| Field | Detail |
|---|---|
| Why now | Cleanup should not expand into a new open-ended lane while parser recovery is still active |
| Scope | Only compounds that materially affect first-promotion readability or source fidelity |
| Defer | Bulk allowlist strategy and threshold retuning belong in `Ready Next`, not current blocking flow |
| Exit | Short list of must-fix vs defer items |

## Ready Next — Start When `Now` Gates Clear
These items are useful and real, but should begin only after current GEN/EXO decisions stabilize or in parallel only if they do not interrupt `Now`.

| Item | Why It Matters | Trigger To Start | Owner |
|---|---|---|---|
| Complete 12 missing `chapter_verse_counts` entries | `V7` remains blind for key books without this | G1 stable or a dedicated registry session | Ark |
| LEV extraction prep and run | Next concrete book after GEN/EXO | G1 stable and LEV CVC verified | Ark |
| EXO allowlist creation | Cleanup hardening for book 2 | Post-parser rerun so cleanup is not compensating for parser misses | Ark |
| Cleanup residue disposition | Human review still needed | After promotion threshold is known | Human |
| Commit uncommitted workflow/tooling work | Reduces branch drift and handoff confusion | Natural checkpoint after current parser pass | Ark |
| 2TH page-range verification | Small integrity task | Any low-friction maintenance window | Ark |
| Brenton indexing strategy | Useful, but should be scoped by need | Decide per-book vs batch after LEV | Ark |

## Retained Detail From Prior Inventory
These details stay here so the horizon rewrite does not erase useful specifics.

### D1. Missing `chapter_verse_counts` books
- `1SA`, `2SA`, `TOB`, `JDT`, `1MA`, `2MA`, `PSA`, `JOB`, `SIR`, `EZK`, `1CO`, `EPH`
- Prior known risk: earlier plan arrays had bad values such as `PSA 163 vs 151` and `JOB 30 vs 42`

### D2. GEN fused-compound review pool
- `ashepherd`, `asmith`, `amanufacturer`, `acubit`, `acloud`, `ahusbandman`, `agarment`, `ahunter`, `aname`, `aremnant`, `alaw`, `apeople`, `amultitude`, `alawgiver`, `afarmer`, `araider`, `aspreading`, `agrown-up`, `adeep`, `acoffin`

### D3. Small integrity checks still worth preserving
- `2TH` page-range verification remains open: memory says `3278 -> 3728`, but registry confirmation is still required
- Brenton indexing is currently concentrated in `GEN` and `EXO`; batch indexing remains a scoped choice, not a default next move

## Later — Forward Plan, Visible But Non-Competing
These items stay documented so architecture does not get lost, but they should not pull attention from the current execution loop.

### L1. Pipeline Hardening
| Item | Trigger |
|---|---|
| Batch extraction script | After 3 consecutive OT books run cleanly enough to justify scale tooling |
| Dynamic V5 article bleed | After `_notes.md` structure is stable across more than 2 books |
| Brenton archaism suppression | After residue audit patterns repeat across multiple books |
| Checksum verification tool | After `canon/` contains promoted files worth auditing |
| Promotion rollback safety | Before repeated promotion use, not before first parser closure |
| Cleanup rule locking | After per-book allowlist workflow is stable |
| Brenton-backed word-split detection | After current parser and cleanup rules stop moving rapidly |

### L2. Validation Expansion
| Item | Trigger |
|---|---|
| Duplicate verse text similarity | After first promoted book, when regression checks become more valuable |
| Chapter header consistency | When heading behavior stabilizes across another 2-3 books |
| Notes back-reference validation | When notes pipeline is treated as production, not side output |
| Cross-book validation | Before larger-scale OT batch runs or Phase 2 |

### L3. Phase 2 / Pre-NT / Research
| Item | Trigger |
|---|---|
| OSB introductions extraction | After OT scripture pipeline is stable |
| Footnote text extraction | After marker indexing is stable across several books |
| Patristic quote linkage | After footnote text exists |
| Liturgical pericope mapping | After canon base is materially complete |
| Theological concordance | After broad canon coverage exists |
| NT footnote ordering probe | Before NT extraction begins |
| GPU OCR experiments | Only if parser quality plateaus with current extraction path |
| Multi-translation support | Only after canonical OSB baseline is stable |
| Obsidian integration | Only after core canon workflow is not moving |
| Sub-agent architecture | Only after roughly 20 books are stable and process invariants are proven |

## Watchlist — Technical Debt That Should Inform Decisions, Not Drive Them
| Item | Why It Matters | When To Pull Forward |
|---|---|---|
| Hardcoded parse heuristics in `osb_extract.py` | Current parser tuning can become book-fragile | If the same heuristic breaks across 2-3 more books |
| No structured logging | Hard to debug scale runs | Before batch extraction tooling |
| No test suite | Regression risk rises as parser rules expand | Before another major parser refactor |
| Partial `osb_name` coverage | Low current impact | Only when page-range/name coupling becomes necessary |

## Memo Queue
| Memo | Purpose | Trigger |
|---|---|---|
| `11_gen_exo_v4_edge_case_source_verification.md` | Current source-backed GEN/EXO parser evidence | active now |
| `registry_cvc_completion.md` | Durable evidence for missing registry counts | before scale |
| `promotion_ceremony_checklist.md` | First promotion protocol | before first promote |
| `leviticus_extraction_plan.md` | Next-book execution memo | before LEV |
| `08_gen_cleanup_report.md` update | Final fused-compound disposition | after human cleanup decision |
| `footnote_extraction_plan.md` | Phase 2 architecture | only when footnote work activates |
| `05_14day_execution_plan.md` update | Retrospective housekeeping | low-priority checkpoint |

## Cadence
| Moment | Rule |
|---|---|
| Start of session | Pick at most 3 active items, all from `Now` unless Human explicitly reprioritizes |
| End of session | Update gate state, evidence, and next unblocker; do not re-rank the full backlog |
| Milestone review | Revisit `Later` only at first promotion, five promoted books, or pre-NT |

## Open Questions
- What is the acceptable first-promotion threshold for residual `V4` and `V7` gaps?
- After the PDF edge-case checker, which remaining GEN/EXO gaps are parser-fixable now versus acceptable for deferment?
- Should registry `chapter_verse_counts` completion happen as one bounded sprint or incrementally per next-book sequence?
- Should Brenton indexing stay per-book until OT flow is stable, rather than batching everything now?

## Requested Next Action
- Ezra: finish the current `V4` classification / source-verification handoff in the form Ark can implement directly.
- Human: decide first-promotion tolerance after reviewing Ark's next parser rerun.
- Ark: stay in the `Now` lane until G1 and G2 are explicit, then pull the top `Ready Next` item.

## Handoff
**To:** `human`
**Ask:** review whether this horizon-based structure better matches how you want Ark to alternate between immediate execution and longer-range planning.
