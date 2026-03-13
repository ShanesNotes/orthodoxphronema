# Wikilink Full Rollout — All 76 Books — 2026-03-13

**Author:** `ark`
**Type:** `implementation`
**Status:** `implemented`
**Scope:** `phase3 wikilink normalization / all staged companions`
**Workstream:** `phase3-impl`
**Phase:** `3`
**Supersedes:** `none`
**Superseded by:** `none`

## Context
- Ezra built the shared wikilink parser, audit CLI, and rewrite CLI in Memo 120.
- REV was the pilot batch: 425 bare refs converted, 7 unresolved chapter-range citations, 0 bugs.
- Remaining corpus had ~3,595 convertible bare refs across 75 books.
- Ark verified Ezra's parser semantics and approved for full rollout.

## Objective
- Rewrite all remaining `*_footnotes.md` and `*_articles.md` files to use `[[BOOK.CH:V]]` wikilink syntax.
- Regenerate all Phase 3 artifacts (R1 JSONL, backlink shards, DuckDB graph).
- Leave chapter-range citations bare (deferred to future `[[BOOK.CH]]` form).

## Ark Verification of Ezra's v1 Grammar

Parser semantics reviewed and approved:
- Regex patterns correct (wikilinks, bare refs, ranges, comma lists)
- Overlap prevention works (occupied list tracking)
- Frontmatter/heading/anchor/code-fence skipping correct
- Reverse-order replacement preserves string indices
- Test coverage comprehensive (6 tests covering all major patterns)
- REV rewrite quality verified (425 conversions, no errors)

## Open Question Decisions

| Question | Decision | Rationale |
|---|---|---|
| Same-chapter comma lists (`Acts 10:43, 47, 48` → repeated wikilinks) | Keep as-is | Expanded wikilinks are machine-parseable and correct; house style compression is a later cosmetic pass |
| Chapter-range citations (`Nm 22-24`) | Leave bare in v1 | Genuinely chapter-level references without verse specificity; future `[[BOOK.CH]]` chapter-link form can be designed in Phase 3 |
| Duplicate inbound-link warning at `1JN.2:18` | Expected | Multiple companion files can cite the same verse; valid citation signal, not a cleanup target |

## Files / Artifacts
- `staging/validated/{OT,NT}/*_footnotes.md` — 95 files rewritten
- `staging/validated/{OT,NT}/*_articles.md` — included in rewrite pass
- `metadata/r1_output/*.jsonl` — 76 files regenerated
- `metadata/anchor_backlinks/study/*.json` — all shards regenerated
- `metadata/graph/phronema_graph.duckdb` — regenerated
- `reports/wikilink_audit_pre_rollout.json` — before-state baseline
- `reports/wikilink_audit.json` — post-rewrite audit
- `reports/wikilink_rewrite_report.json` — rewrite run report
- `reports/phase3_validation_report.json` — Phase 3 validation

## Findings Or Changes

### Before/After Audit Numbers

| Metric | Pre-Rollout | Post-Rollout |
|---|---|---|
| Total refs | 4,052 | 4,558 |
| Convertible bare refs | 3,595 | **0** |
| Already linked (wikilinks) | 457 | **4,558** |
| Unresolved (chapter-range) | 32 | 32 |
| Changed files | — | 95 |

Note: Total refs increased from 4,052 to 4,558 because the parser now detects comma-expanded wikilinks as individual linked refs (e.g., `Acts 10:43, 47, 48` → 3 wikilinks counted separately).

### Phase 3 Validation
- Status: `WARN` (no errors)
- 6 duplicate inbound-link warnings (expected: multiple companions can cite the same verse)
- 0 zero-degree anchors
- 6,094 backlink shard files validated

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Batch-rewrite all 76 books in one pass | Parser verified on REV; 338 tests pass; no reason to drip-feed | Bulk change to 95 files | `git revert` the commit |
| Leave 32 chapter-range citations bare | No verse-level target to link to; guessing semantics would contaminate backlinks | Partial normalization visible | Extend parser later with `[[BOOK.CH]]` form |
| Accept 6 duplicate-inbound-link warnings | Valid multi-source citation signal | Warning noise | Add graph-layer dedup if needed later |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| Pre-rollout audit | `pass` | `reports/wikilink_audit_pre_rollout.json` → 3,595 convertible |
| Batch rewrite (all books) | `pass` | `reports/wikilink_rewrite_report.json` → 3,595 converted, 95 files changed |
| Post-rewrite audit | `pass` | `reports/wikilink_audit.json` → 0 convertible, 4,558 linked |
| R1 regeneration (76 books) | `pass` | `metadata/r1_output/*.jsonl` |
| Backlink shard rebuild | `pass` | `metadata/anchor_backlinks/study/*.json` |
| DuckDB graph regeneration | `pass` | `metadata/graph/phronema_graph.duckdb` |
| Phase 3 validation | `warn` | `reports/phase3_validation_report.json` → 0 errors, 6 dup-inbound warnings |
| Full test suite | `pass` | `pytest tests/ -q` → 338 passed in 1.06s |
| Spot-check GEN | `pass` | Wikilinks correctly formed in footnotes |
| Spot-check MAT | `pass` | Wikilinks correctly formed; headings/anchors untouched |
| Spot-check PSA | `pass` | Wikilinks correctly formed in footnotes |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| `Files changed` | `done` | 95 companion files + 76 R1 JSONL + backlink shards + graph + 4 reports |
| `Verification run` | `done` | Pre/post audit, rewrite report, Phase 3 validation, pytest 338 pass, 3-book spot-check |
| `Artifacts refreshed` | `done` | R1, backlinks, graph, all 4 reports |
| `Remaining known drift` | `present` | 32 chapter-range citations remain bare (by design); `reports/book_status_dashboard.json` not refreshed (unrelated to wikilinks) |
| `Next owner` | `ezra` | Verify rollout numbers, confirm Phase 3 graph quality |

## Deferred Work
- Chapter-range link form (`[[BOOK.CH]]`) — design in Phase 3 if needed
- House style compression for comma-expanded wikilinks — cosmetic, not blocking
- Graph-layer dedup policy for duplicate inbound links — monitor, not blocking

## Handoff
**To:** `ezra`
**Ask:** `Verify the full-corpus rollout numbers and Phase 3 graph quality. Confirm 0 convertible bare refs remain and 32 unresolved chapter-range citations are expected.`
