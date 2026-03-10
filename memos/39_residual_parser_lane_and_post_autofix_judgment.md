# Memo 39 — Residual/Parser Lane + Post-Auto-Fix Judgment

**Date:** 2026-03-10
**Author:** Ark
**Status:** COMPLETE — awaiting Human ratification

---

## Summary

Executed memo 39 plan: V11 split-word fixes, 1SA versification correction, 2KI.1 bounded review, dossier/dashboard refresh, and residual governance consolidation.

---

## Phase 1 — V11 Split-Word Fixes (DONE)

### JOS (4 fixes, lines 301-303)
| Location | Before | After |
|----------|--------|-------|
| JOS.10:12 | `ov er Gibeon` | `over Gibeon` |
| JOS.10:12 | `v alley of Ajalon` | `valley of Ajalon` |
| JOS.10:13 | `v engeance` | `vengeance` |
| JOS.10:14 | `heav en` | `heaven` |

### 2SA (1 fix, line 41)
| Location | Before | After |
|----------|--------|-------|
| 2SA.1:19 | `ov er the dead` | `over the dead` |

**Validation:** Both books now V11 PASS. JOS 99.8% (660/661), 2SA 99.9% (696/697).

---

## Phase 2 — 1SA Versification Correction (DONE)

**Key discovery:** 1SA.17:34-52 (19 verses) is a versification difference, not a parser gap. OSB follows LXX shorter text for 1 Samuel 17 (33 verses vs MT's 52).

**Actions taken:**
1. Reclassified all 19 residuals from `docling_issue` → `osb_source_absent` in `1SA_residuals.json`
2. Updated descriptions to document LXX shorter text versification
3. Corrected CVC in `anchor_registry.json`:
   - ch1: 28 → 29
   - ch17: 52 → 33
   - ch18: 18 → 19
4. Registry bumped to v1.2.4

**Result:** 1SA V7 now **775/775 (100.0%)** — up from 97.9%.

---

## Phase 3 — 2KI.1:7 Bounded Review (DONE)

**Finding:** 2KI.1:7 contains a Docling column-split artifact. The tail of v6 text (`"return to the king who sent you, and say to him, 'Thus says the Lord: 'Is it because there is'"`) was merged into v7, displacing v7's opening. Garbled quotation marks result.

**Brenton reference** confirms the OSB should read something like: "So they returned and reported to the king...What was the manner of the man..."

**Decision:** Per OSB immutability policy, we cannot reconstruct from Brenton. Classified as `docling_issue` residual (non-blocking, ratified=true since it's a known parser limitation). Created `2KI_residuals.json`.

---

## Phase 4 — Dossier & Dashboard Refresh (DONE)

Dossiers regenerated: JOS, 2SA, 1SA, EXO. Dashboard regenerated.
All 64 tests pass.

---

## Phase 5 — Ratification Request for Human

### Category A — File-level ratification only
These books have all per-entry `ratified: true`. Human needs to set `ratified_by: "human"` in sidecar header:

| Book | Residuals | Notes |
|------|-----------|-------|
| NUM | 1 | absorbed content (NUM.6:27) |
| DEU | 1 | absorbed content (DEU.33:8) |
| NEH | 7 | various docling_issue |
| TOB | 2 | docling_issue |
| 1MA | 2 | docling_issue |
| 2MA | 3 | docling_issue |
| 3MA | 1 | docling_issue |
| EST | 1 | docling_issue |
| 2KI | 1 | docling_issue (2KI.1:7 column-split) |

### Category B — Per-entry + file-level ratification needed
These have `ratified: false` entries requiring Human review:

| Book | Count | Entries |
|------|-------|---------|
| 1SA | 19 | 1SA.17:34-52 (osb_source_absent — LXX shorter text) |
| 1KI | 5 | 1KI.22:46-50 (tail-end final chapter) |
| 2SA | 2 | 2SA.17:29, 2SA.23:40 |
| JDG | 1 | JDG.11:40 |
| 1CH | 1 | 1CH.16:7 |
| 2CH | 1 | 2CH.33:1 |

### Category C — Promotion decisions
| Book | Status | Blocker |
|------|--------|---------|
| RUT | Dry-run passes, no residuals | Ezra audit + Human confirmation |
| 2KI | Dry-run passes, 1 residual (ratified) | Human ratification of sidecar |
| EXO | Previously promotion-ready | Ezra audit + Human confirmation |

---

## Updated Promotion Readiness Matrix

| Book | V7 | V11 | Editorial | Residuals | Gate Status |
|------|-----|-----|-----------|-----------|-------------|
| GEN | 99.9% | PASS | 0 | 1 (ratified) | **PROMOTED** |
| EXO | 100.4% | PASS | 0 | 0 | Ezra audit needed |
| LEV | 100.0% | PASS | 0 | 0 | **PROMOTED** |
| NUM | 99.9% | PASS | 0 | 1 (ratified) | D5: human ratification |
| DEU | 100.1% | PASS | 0 | 1 (ratified) | D5: human ratification |
| JOS | 99.8% | PASS | 0 | 0 | V7 gap (1 verse) |
| JDG | — | — | 0 | 1 (unratified) | D5: human ratification |
| RUT | — | — | 0 | 0 | Ezra audit needed |
| 1SA | 100.0% | PASS | 0 | 19 (osb_source_absent) | D5: human ratification |
| 2SA | 99.9% | PASS | 0 | 2 (unratified) | D5: human ratification |
| 1KI | — | — | 0 | 5 (unratified) | D5: human ratification |
| 2KI | — | — | 0 | 1 (ratified) | Human sidecar ratification |
| 1CH | — | — | 0 | 1 (unratified) | D5: human ratification |
| 2CH | — | — | 0 | 1 (unratified) | D5: human ratification |
