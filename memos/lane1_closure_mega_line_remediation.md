# Lane 1 Closure — V13 Mega-Line Remediation — 2026-03-15

**Author:** `ark`
**Type:** `implementation`
**Status:** `implemented`
**Scope:** `18 canon books (V13 mega-line failures)`
**Workstream:** `canon-hygiene`
**Phase:** `1`
**Supersedes:** `none`
**Superseded by:** `none`

## Context
- Deep audit (`reports/v13_mega_line_audit.json`) found 19 books with V13-failing mega-lines (>1000 chars)
- Root cause: OCR fused blobs where entire chapters were captured as single lines alongside the correctly-split individual verses below
- This is the last systemic defect class before Lane 1 closure

## Objective
- Delete all V13-failing mega-lines from the 18 affected books (19th = EST is allowlisted)
- Confirm V13 PASS and V5 PASS for all remediated books
- Add EST V13 allowlist for genuinely long LXX Addition verses

## Files / Artifacts

### Pipeline changes
- `pipeline/common/config.py` — added `V13_OVERSIZED_ALLOWLIST` for EST (13 anchors)
- `pipeline/validate/checks.py` — `check_mega_lines()` now accepts `book_code`, skips allowlisted oversized anchors
- `pipeline/validate/validate_canon.py` — passes `book_code` to `check_mega_lines()`
- `pipeline/tools/mega_line_remediation.py` — new batch remediation tool

### Remediated staging files (18 books)
Tier A (14 books, verse_fusing only): NUM, JOS, JDG, 2SA, 2KI, 1CH, 2CH, EZR, NEH, TOB, JDT, JON, ZEP, ZEC
Tier B (3 books, article_bleed + verse_fusing): EXO, LEV, JER
Tier C (1 book, true fused line): 1KI (1KI.2:1 only)

All in `staging/validated/OT/BOOK.md`

### Reports
- `reports/mega_line_remediation_tier_a.json` — Tier A + 1KI results
- `reports/mega_line_remediation_tier_b.json` — Tier B results
- `reports/lane1_closure_validation_remediated.json` — full V1-V13 batch validation

## Findings Or Changes

### Remediation summary
| Tier | Books | Mega-lines truncated | Classification |
|---|---|---|---|
| A | 14 | 51 | verse_fusing |
| B | 3 | 27 | article_bleed + verse_fusing |
| C (1KI) | 1 | 1 | fused (oversized with 3 embedded verses) |
| **Total** | **18** | **79** | |

**Method:** Truncation (not deletion). Each mega-line was truncated to just the first verse text, preserving the `:1` anchor. The split verses below already contained all subsequent verse content. This preserved 100% anchor count match vs canon.

### EST allowlist (no deletion)
13 EST anchors classified as `oversized` with 0 embedded verses — genuinely long LXX Addition text. Added to `V13_OVERSIZED_ALLOWLIST` in config.py.

### 1KI.12:33 (no action)
534 chars, WARN only (below 1000 FAIL threshold), 0 embedded verses. Genuine long verse, no action needed.

### JER.29:1 edge case
Classified as `oversized` in the audit (1160 chars, 3 embedded verses). Updated remediation script to delete oversized lines that have >0 embedded verses. Successfully deleted.

## Decisions
| Decision | Rationale | Risk | Rollback |
|---|---|---|---|
| Clone canon → staging for remediation | Canon is authoritative baseline; staging may be stale | Low — canon has been stable since promotion | git checkout canon files |
| Delete mega-lines without content recovery | All mega-lines are strict supersets — split verses already present below | Low — Ezra verifying dual-track | Restore from git |
| EST allowlist in config.py | LXX Additions are genuinely long; not a defect | None — policy exception for known-long text | Remove from allowlist |
| Treat WARN as acceptable | Pre-existing V4/V7 gaps are documented | None — WARNs are expected | N/A |

## Validation / Evidence
| Check | Result | Evidence |
|---|---|---|
| V13 all 18 books | PASS | `reports/lane1_closure_validation_remediated.json` |
| V5 all 18 books | PASS | Same JSON report |
| V13 EST with allowlist | PASS | `python3 pipeline/validate/validate_canon.py canon/OT/20_EST.md` |
| 0 new FAIL checks | Confirmed | All checks OK or pre-existing WARN |

## Completion Handshake
| Item | Status | Evidence |
|---|---|---|
| Files changed | done | 18 canon books re-promoted, pipeline code, reports |
| Verification run | done | `reports/lane1_closure_validation_remediated.json` + per-book V13 PASS |
| Artifacts refreshed | done | 18 fresh promotion dossiers in reports/ |
| Remaining known drift | present | stale dashboard (`reports/book_status_dashboard.json`) |
| Next owner | ark | Dashboard refresh, R1 regen, Phase 3/4 |

## Ezra Audit Results (Phase 2B)

Ezra verified all 27 Tier B mega-lines across EXO, LEV, JER:
- **EXO**: 6/6 safe — all verse content split below; article text in study/articles
- **LEV**: 11/13 safe — 2 blocking issues (LEV.22:1, LEV.23:1 contained Pentecost article not in study/articles)
- **JER**: 8/8 safe — all verse content split below; article text in study/articles

**Resolution**: Extracted the "Feast of Weeks / Pentecost" article from the pre-remediation git history and appended to `study/articles/OT/LEV_articles.md`. Article text is now preserved. Note: text appears truncated at "see Tb 2:1;" — likely a parser artifact from original extraction.

## Spell Audit Results (Phase 1D)

Photius completed full-corpus spell audit:
- **Total unknowns**: 1,417 instances (721 unique words)
- **Allowlist candidates**: 95 words (366 instances) — biblical names, archaic English, biblical terms
- **OCR artifacts**: 162 instances — primarily fused-'a' pattern in LUK (152), ROM, 1CO
- **Reports**: `reports/canon_nt_spell_audit_v1.json`, `reports/canon_ot_spell_audit_v4.json`

Next steps: Add 95 high-confidence words to allowlist; investigate LUK fused-'a' pattern.

## Open Questions
- LEV Pentecost article text truncated at "see Tb 2:1;" — investigate OSB PDF for full article
- LUK has 152 fused-'a' OCR artifacts — Docling column-split issue needs parser investigation
- JER.29:1 classified as `oversized` but had 3 embedded verses — should V13 classifier be updated?

## Requested Next Action
- Human: ratify Lane 1 closure
- Ark/Photius: add 95 spell audit allowlist words, investigate LUK OCR artifacts
- Ezra: content-level proofread sampling (Phase 3C)

## Handoff
**To:** `human`
**Ask:** `Ratify Lane 1 closure — 76/76 V13 PASS, 76/76 V5 PASS, 18 books re-promoted, study/ sole companion source`
