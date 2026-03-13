# Wikilink Rollout Seed And REV Batch — 2026-03-13

**Author:** `ezra`  
**Type:** `implementation`  
**Status:** `implemented`  
**Scope:** `phase3 wikilink parsing / staged companion normalization / REV pilot batch`
**Workstream:** `phase3-impl`  
**Phase:** `3`  
**Supersedes:** `none`  
**Superseded by:** `none`

## Context
- Phase 3 architecture already froze the visible outbound link syntax as `[[BOOK.CH:V]]` everywhere outside `canon/`, but the live corpus still used almost entirely bare biblical references.
- Repo inspection showed the real migration surface was `staging/validated/*_{footnotes,articles}.md`, not a live `phronema/` corpus.
- A corpus census before the rewrite found roughly `5,361` bare biblical references and effectively `0` live wikilinks across staged companion files.

## Objective
- Add one shared parser/rewriter so wikilink extraction and wikilink migration use the same grammar.
- Convert a first real staged batch to prove the rollout path on repo-native artifacts, not only on tests.
- Keep canon untouched and leave unsupported chapter-only or chapter-range citations explicit rather than guessed.

## Files / Artifacts
- `pipeline/reference/wikilinks.py`
- `pipeline/reference/audit_wikilinks.py`
- `pipeline/reference/rewrite_wikilinks.py`
- `pipeline/extract/{models.py,r1_extractor.py}`
- `tests/test_wikilinks.py`
- `staging/validated/NT/{REV_articles.md,REV_footnotes.md}`
- `metadata/r1_output/REV.jsonl`
- `metadata/anchor_backlinks/study/*.json`
- `reports/{wikilink_audit.json,wikilink_rewrite_report.json,phase3_validation_report.json}`

## Findings Or Changes
- Added a shared biblical-reference parsing layer in `pipeline/reference/wikilinks.py`.
  - It detects existing wikilinks, same-chapter wikilink ranges, single bare references, and same-chapter comma-separated bare references.
  - It skips frontmatter, headings, code fences, and `*(anchor: ...)*` markers.
  - It refuses to guess unsupported chapter-only or chapter-range citations such as `Nm 22-24`; those remain bare and are reported.
- Updated `pipeline/extract/r1_extractor.py` to use the shared parser instead of a parallel regex implementation.
  - New emitted reference types are `wikilink`, `wikilink_range`, and `bare`.
  - Legacy `frozen` records remain tolerated for transition compatibility.
- Added two repo-native CLIs:
  - `audit_wikilinks.py` for conversion census and unresolved-citation reporting
  - `rewrite_wikilinks.py` for dry-run or in-place staged-companion rewrites
- Applied the first real in-place normalization batch to `REV_articles.md` and `REV_footnotes.md`.
  - `425` convertible bare references were rewritten into wikilinks.
  - Post-rewrite audit shows `457` linked references and `7` remaining unsupported chapter-range citations in `REV_footnotes.md`.
- Regenerated Phase 3 artifacts for the batch:
  - `metadata/r1_output/REV.jsonl`
  - study backlink shards under `metadata/anchor_backlinks/study/`
  - `reports/phase3_validation_report.json`

## Reasoning Summary
- The first design constraint was to avoid grammar drift between migration tooling and the Phase 3 extractor, so the parser and rewriter were implemented once and reused.
- The first rollout batch needed a dense real-world book, so `REV` was used because it produced a meaningful stress test while staying bounded to two companion files.
- Unsupported citation classes were kept explicit on purpose. The safer v1 move is to surface them for Ark review rather than infer chapter-range intent and contaminate future backlinks.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Share parser logic between rewrite and extraction | Prevents immediate grammar drift between migration and Phase 3 | Shared bug affects both lanes | Revert to prior extractor regex and disable rewrite CLI |
| Convert `REV` first | High-density batch gives strong proof with bounded blast radius | `REV` can expose many edge cases at once | Revert only `REV_articles.md` and `REV_footnotes.md` |
| Leave chapter-only/chapter-range refs unresolved in v1 | Safer than guessing unsupported semantics | Partial normalization remains visible | Extend parser later with explicit rules after Ark review |
| Keep backlinks generated from the batch even with zero-degree warnings | Zero-degree anchors are expected during incremental rollout | Warning volume may obscure harder failures | Remove generated shards and rerun after broader rollout |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Targeted wikilink + extractor tests | `pass` | `pytest tests/test_wikilinks.py tests/test_reference_aliases.py tests/test_future_seed.py tests/test_phase3_graph.py -q` |
| Full test suite | `pass` | `pytest -q` -> `338 passed in 1.07s` |
| Pre-rewrite REV audit | `pass` | `python3 -m pipeline.reference.audit_wikilinks staging/validated --book REV` -> `425` convertible refs |
| In-place REV rewrite | `pass` | `python3 -m pipeline.reference.rewrite_wikilinks staging/validated --book REV --in-place` |
| Post-rewrite REV audit | `pass` | `reports/wikilink_audit.json` -> `457` linked refs, `0` convertible refs, `7` unresolved |
| REV R1 regeneration | `pass` | `metadata/r1_output/REV.jsonl` |
| Phase 3 validation after batch | `warn` | `reports/phase3_validation_report.json` -> no errors; zero-degree `REV` anchors and one duplicate inbound-link warning at `1JN.2:18` |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | parser/CLI/test files plus `staging/validated/NT/{REV_articles.md,REV_footnotes.md}` |
| `Verification run` | `done` | targeted pytest, full pytest, REV audit/rewrite/audit, REV R1 + backlink + Phase 3 validation |
| `Artifacts refreshed` | `done` | `metadata/r1_output/REV.jsonl`, `metadata/anchor_backlinks/study/*.json`, `reports/wikilink_*.json`, `reports/phase3_validation_report.json` |
| `Remaining known drift` | `present` | unsupported chapter-range references remain bare; `reports/phase3_validation_report.json` is warning-only, not green |
| `Next owner` | `ark` | verify parser semantics, unresolved classes, and whether duplicate inbound-link warning needs graph-layer dedupe policy |

## Open Questions
- Should same-chapter list syntax such as `Acts 10:43, 47, 48` remain expanded to repeated wikilinks, or should a compressed house style be defined later?
- Should chapter-range citations such as `Nm 22-24` eventually become a supported non-verse link form, or remain intentionally non-wikilinked?
- Should the duplicate inbound-link warning at `1JN.2:18` be treated as expected repeated citation signal or as a graph-input cleanup target?

## Requested Next Action
- Ark:
  - inspect `pipeline/reference/wikilinks.py` and `pipeline/extract/r1_extractor.py` for semantic edge cases before batch 2
  - review the `REV` unresolved examples in `reports/wikilink_audit.json`
  - decide whether to keep batch 2 on the planned high-density books (`MAT`, `LUK`, `JOH`, `ACT`) or pause for chapter-range semantics
- Ezra:
  - hold off on wider in-place rewrites until Ark verifies the v1 grammar and warning profile

## Handoff
**To:** `ark`  
**Ask:** `Verify the shared wikilink grammar, the REV batch output, and the remaining unsupported citation classes before approving the next normalization batch.`
