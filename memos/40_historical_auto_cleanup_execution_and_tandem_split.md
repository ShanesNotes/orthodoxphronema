# Memo 40 — Historical Auto-Cleanup Execution And Tandem Split

**Date:** 2026-03-10
**From:** Ezra
**To:** Ark
**Status:** high-confidence fused-article cleanup executed; residual/V11 lane remains

## What Ezra Executed

I used the hardened `fix_articles.py` pass to clear the high-confidence fused-article backlog in the historical books, then regenerated:
- `*_editorial_candidates.json`
- dry-run promotion dossiers
- `reports/book_status_dashboard.json`

### Safety fix before applying cleanup
- Suppressed titlecase proper-name false positives in `fix_articles.py` so tokens like `Arad` / `Anab` are no longer treated as `A rad` / `A nab` unless there is stronger evidence.
- Preserved lowercase OCR-fusion detection like `acertain`, `atreaty`, `aprophet`, `aresult`, etc.

## In-Place Cleanup Applied

High-confidence auto-fixes applied:

| Book | Applied |
|---|---:|
| `JOS` | 20 |
| `JDG` | 36 |
| `RUT` | 1 |
| `1SA` | 60 |
| `2SA` | 45 |
| `1CH` | 15 |
| `1KI` | 127 |
| `2KI` | 47 |

After regeneration, all nine current historical editorial sidecars are now at `0` high-confidence candidates.

## Current Post-Cleanup State

### Promotion-ready now
- `RUT`
- `2KI`

### Structurally passable but not promotion-ready
- `JOS`
  - still has live `V11` split-word residue (`ov er`, `v alley`)

### Editorially clean but blocked by residual governance / completeness issues
- `JDG`
- `1SA`
- `2SA`
- `1CH`
- `2CH`
- `1KI`

## Important Remaining Risks

1. `JOS` still has live `V11` split-word residue after article cleanup.
2. `2SA` still has live `V11` split-word residue after article cleanup.
3. Residual sidecars still block several books because `ratified_by` is not yet `human`.
4. `1CH` and `2CH` still carry live `V4` / `V7` concerns.
5. `2KI` now dry-runs cleanly through the current gate, but chapter 1 still deserves a quick human skim before actual promotion because the opening dialogue remains stylistically messy even though it is no longer blocked by the current detectors.

## Tandem Split

### Ark
1. Take the residual/governance lane:
   - `JDG`
   - `1SA`
   - `2SA`
   - `1CH`
   - `2CH`
   - `1KI`
2. Fix the remaining `V11` split-word cases in:
   - `JOS`
   - `2SA`
3. Re-run dossiers/dashboard after each targeted fix.
4. Do a bounded review of `2KI.1` before actual promotion.

### Ezra
1. Ready to audit the post-fix `JOS` / `2SA` split-word cleanup.
2. Ready to review any residual packet once Ark has the sidecars in final promotion shape.
3. Ready to do final promotion audit on `RUT` and `2KI` if Human wants that next.

## Verification

- `python3 -m pytest tests/ -q` → `64 passed`
- dashboard regenerated
- dossiers regenerated
