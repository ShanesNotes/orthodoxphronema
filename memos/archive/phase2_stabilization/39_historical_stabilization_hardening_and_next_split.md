# Memo 39 — Historical Stabilization Hardening And Next Split

**Date:** 2026-03-09
**From:** Ezra
**To:** Ark
**Status:** detector/evidence hardening implemented; historical books re-baselined below promotion

## What Changed

I implemented the workflow hardening from the stabilization plan in code and regenerated the affected evidence artifacts.

### 1. Editorial sidecar generation now reflects unresolved work
- `pipeline/cleanup/fix_articles.py` no longer treats high-confidence candidates as effectively resolved during dry-run/report mode.
- This was the core cause of the false `0`-candidate sidecars on books that still visibly contained `acertain`, `atreaty`, `aprophet`, `as aresult`, etc.
- High-confidence article fusions now remain pending in `BOOK_editorial_candidates.json` until an in-place cleanup actually resolves them.

### 2. Historical fused-article coverage widened
- Expanded `_KNOWN_BIBLICAL_TARGETS` in `pipeline/cleanup/fix_articles.py` for the live historical-book residue classes we kept re-spending tokens on:
  - `certain`, `treaty`, `prophet`, `lion`, `monument`, `widow`, `drinking`, `vessel`, `handbreadth`, `eunuch`, `demand`, `response`, `bandage`, `wound`, `horse`, `cavalryman`, `forked`, `pile`, `small`, `little`, `jar`, `bin`, `cup`, `morsel`, `cave`, `ship`, `fire`, `calf`, `furrow`, `severe`, and others.

### 3. V11 now catches the split-word shapes still present in live books
- `pipeline/validate/validate_canon.py` still keeps the old narrow Docling split check, but now also catches joined-fragment cases like:
  - `ov er`
  - `v alley`
- This now surfaces the real split-word residue still present in `JOS` and `2SA`.

### 4. V8 was tightened only where signal remained clean
- I kept the useful new `V8` failure for a heading with no following verse content.
- I removed the one-verse-span heading warning because it produced broad noise across otherwise legitimate pericopes and was not a good blocker.

### 5. Dashboard status now respects editorial validation better
- `pipeline/tools/generate_book_status_dashboard.py` now includes `V11` and `V12` in the displayed validation map.
- It also treats non-pass `V11`/`V12` as editorial blockers before a book can be considered `editorially_clean` or `promotion_ready`.

## Re-Baselined Historical State

I regenerated:
- historical `*_editorial_candidates.json` sidecars
- historical dry-run promotion dossiers
- `reports/book_status_dashboard.json`

Current historical-book editorial candidate counts:

| Book | Candidates | Notes |
|---|---:|---|
| `JOS` | 26 | plus `V11` split-word residue (`ov er`, `v alley`) |
| `JDG` | 38 | fused-article debt still broad |
| `RUT` | 1 | almost clean |
| `1SA` | 68 | large fused-article backlog |
| `2SA` | 45 | plus `V11` split-word residue |
| `1CH` | 23 | editorial cleanup still needed |
| `2CH` | 0 | still blocked by residual governance / `V4`+`V7` issues |
| `1KI` | 127 | largest live editorial backlog |
| `2KI` | 48 | fused-article backlog remains |

Dashboard outcome after regeneration:
- `JOS`, `JDG`, `RUT`, `1SA`, `2SA`, `1CH`, `1KI`, `2KI` => `structurally_passable`
- `2CH` => `editorially_clean` but still blocked by residual ratification / live `V4`

This is the correct reset. Group 2 and Group 3 are not promotion-lane books yet.

## Lessons Confirmed

These token sinks were avoidable once formalized:

1. **Dry-run/report semantics drift**
   - A detector that says “auto-fixable” is not the same as “already fixed in the file.”
   - Sidecars must reflect file state, not hypothetical fixability.

2. **Known OCR residue classes should be codified quickly**
   - Once we see `acertain`, `atreaty`, `aprophet`, `ov er`, or `v alley` in multiple books, they should move into shared detection immediately.

3. **Promotion evidence must be regenerated after detector hardening**
   - Old dossiers and dashboards were carrying cleaner conclusions than the live text warranted.

4. **Human ratification before stabilization is wasted effort**
   - Ratifying residuals while editorial sidecars are still under-detecting only creates a second review loop later.

## Next Split Of Work

### Ark
1. Run the actual in-place cleanup pass on the historical books using the refreshed editorial sidecars as the queue.
2. Prioritize in this order:
   - `1KI`
   - `1SA`
   - `2KI`
   - `2SA`
   - `JDG`
   - `1CH`
   - `JOS`
   - `RUT`
   - `2CH`
3. After each cleanup pass:
   - rerun `fix_articles.py --editorial-report`
   - rerun `promote.py --dry-run --allow-incomplete`
   - regenerate the dashboard
4. Do not ask for human ratification on Group 2/3 residuals until the editorial candidate counts are near zero and the live text looks visibly clean.

### Ezra
1. Re-audit the cleaned books after Ark reruns them.
2. Spot-check that `V11` remains useful and does not create new false positives as cleanup proceeds.
3. Verify which residuals remain genuinely parser/source issues after the editorial backlog is reduced.
4. Prepare the next ratification packet only for books that are already editorially clean.

## Exit Criteria For Returning To Ratification

Do not return Group 2/3 books for residual ratification until all are true for the candidate book:
- editorial candidates are `0` or explicitly explained
- no obvious spellcheck-level fused words remain on spot check
- current dry-run dossier is regenerated from the present staged file
- any `V11`/`V12` warnings are resolved or explicitly understood
- residual sidecar reflects only the post-cleanup remainder

## Verification

- `python3 -m pytest tests/ -q` → `63 passed`
- historical editorial sidecars regenerated
- historical dossiers regenerated
- dashboard regenerated
