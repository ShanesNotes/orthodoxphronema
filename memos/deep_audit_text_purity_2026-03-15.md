# Deep Audit: Text Purity, Duplication, and Tooling Gaps — 2026-03-15

**Author:** `ark`
**Type:** `implementation`
**Status:** `in_review`
**Scope:** `pipeline / canon / study / metadata`
**Workstream:** `canon-hygiene`
**Phase:** `3`
**Supersedes:** `none`
**Superseded by:** `none`

## Context
- The wikilinks sprint (13,288 wikilinks, bundle builder working) surfaced three systemic issues
- 82 mega-lines across 19 canon books (up to 16,457 chars) pass V1-V12 silently
- 152 companion files exist in both staging/ and study/ with 100% divergence
- R1 backlink pipeline reads both sources, producing ~50% duplicate edges (21,860 total, ~10,732 from staging)

## Objective
1. Add V13 mega-line detection to validation suite and promotion gate
2. Enhance V5 article-bleed detection with per-book headers
3. Fix R1 pipeline to read from one source per companion (study/ preferred)
4. Establish study/ as authoritative for promoted companions
5. Document the source-of-truth policy for companion files

## Files / Artifacts
- `pipeline/validate/checks.py` — V13 check_mega_lines + V5 check_article_bleed_enhanced
- `pipeline/validate/validate_canon.py` — wired V13, enhanced V5
- `pipeline/common/config.py` — MEGA_LINE_FAIL/WARN thresholds, ALLCAPS_EXEMPT
- `pipeline/promote/promote.py` — dossier range extended to V13
- `pipeline/graph/rebuild_all_backlinks.sh` — single-source companion selection

## Findings Or Changes

### Phase 4: V13 Mega-Line Check (implemented)
- FAIL threshold: >1,000 chars per verse line
- WARN threshold: 500-1,000 chars per verse line
- Classification: article_bleed (all-caps words), verse_fusing (embedded verse numbers or >3000 chars), oversized
- Corpus result: 55 PASS, 3 WARN, 19 FAIL

### Phase 5: V5 Enhancement (implemented)
- check_article_bleed_enhanced replaces check_article_bleed in validation pipeline
- Dynamically collects ### headers from study/articles/ for per-book matching
- Adds all-caps cluster heuristic (3+ consecutive all-caps words, excluding LORD/GOD/ISRAEL/AMEN/YHWH)
- Original 6 hardcoded patterns preserved for backward compatibility

### Phase 3: R1 Pipeline Fix (implemented)
- rebuild_all_backlinks.sh now prefers study/ over staging/ for each companion
- Only falls back to staging/ if study copy is missing
- Expected: R1 record count drops from ~21,860 to ~11,128 after regeneration

### Phase 2: Companion Source-of-Truth Decision
**Decision: study/ is authoritative for promoted companions.**

Rationale:
- study/ companions have already received quality improvements (OCR blank-line removal, corrections)
- Staging is 20-43% larger across all 76 footnote pairs (OCR blank lines)
- 21/76 article pairs also diverged (study has corrections staging lacks)
- Staging companions are pipeline working state, not final product

### Mega-Line Corpus Summary (19 books)
| Tier | Books | Issue | Count |
|---|---|---|---|
| P0 | LEV, EXO | Article bleed + verse fusing | 19 lines |
| P1 | JOS, 1CH, JDG, NEH, TOB, JER | Verse fusing | 34 lines |
| P2 | NUM, 2SA, 1KI, 2KI, 2CH, EZR, JDT, EST, JON, ZEP, ZEC | Oversized/fusing | 29 lines |

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Add V13 to validation suite | V1-V12 blind to line content; mega-lines invisible | Low — additive check only | Remove V13 from checks.py |
| Enhance V5 with per-book headers | 6 hardcoded Genesis patterns too narrow | Low — original patterns preserved | Revert to check_article_bleed |
| study/ authoritative for companions | study already cleaned; staging is working state | Medium — Photius staging fixes need back-porting | Revert rebuild_all_backlinks.sh |
| R1 single-source per companion | 50% duplicate edges inflate backlink counts | Low — study has same or better content | Revert rebuild_all_backlinks.sh |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| V13 on LEV | FAIL (13 mega-lines) | `python3 -c "from pipeline.validate.validate_canon import run_validation; ..."` |
| V13 corpus scan | 55 PASS / 3 WARN / 19 FAIL | Full corpus validation run |
| R1 companion selection | study/ preferred | Dry-run: GEN selects study/footnotes + study/articles |
| V5 enhanced on LEV | PASS (no false positives from dynamic headers) | Regression test |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| Files changed | done | checks.py, validate_canon.py, config.py, promote.py, rebuild_all_backlinks.sh |
| Verification run | done | V13 corpus scan: 55/3/19 matches plan prediction |
| Artifacts refreshed | deferred | stale dossiers for 19 V13-failing books; stale R1 output (not regenerated yet) |
| Remaining known drift | present | stale dossiers (19 books), stale R1/backlinks (needs rebuild), stale dashboard |
| Next owner | human | Ratify companion SOT decision, then proceed to Phase 6 mega-line remediation |

## Ezra Phase 1 Findings (memos/ezra_deep_audit_phase1_2026-03-15.md)

Key Ezra findings:
- **All 7 worst mega-lines are dual-track:** fused blob + correctly-split verses below
- Remediation for each = delete the fused mega-line, keep the split verses
- 4/7 worst cases contain article bleed (LEV ×3, EXO ×1 confirmed)
- Companion divergence is 100% whitespace (footnotes) and wikilink coverage (articles)
- Content line counts are identical between staging and study for all spot-checked pairs
- Study is strictly better in all cases — no staging-only fixes need back-porting

## Open Questions
- Phase 6 remediation order: P0 (LEV, EXO) first — confirm priority
- 3 WARN books (1SA, 3MA, 1CO) have lines 500-1000 chars — genuine long verses or parser issue?

## Requested Next Action
1. Human: ratify companion source-of-truth decision (study/ authoritative)
2. Ark: regenerate R1 + backlinks after ratification
3. Ark/Photius: begin Phase 6 mega-line remediation (LEV and EXO first)
4. Ark: update audit methodology (Phase 7) after remediation tooling is proven

## Handoff
**To:** `human`
**Ask:** Ratify companion SOT decision and Phase 6 priority order (P0→P1→P2)

## Notes
- V13 catches exactly what the plan predicted: 19 books, 82 mega-lines
- The 3 WARN books (1SA, 3MA, 1CO) have lines between 500-1000 chars — investigate whether these are genuine long verses
- CLAUDE.md lessons learned 16-20 should be added after human ratification
