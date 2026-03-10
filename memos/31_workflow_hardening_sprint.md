# Memo 31 — Workflow Hardening Sprint

**Author:** `ark`
**Type:** `implementation`
**Status:** `complete`
**Date:** 2026-03-09
**Scope:** Promotion gate hardening, sidecar normalization, validator additions
**Directive source:** Ezra (Day 13 session review)

---

## Context

Ezra reviewed Pentateuch extraction results and identified six systemic weaknesses that will compound across the next 9+ books if not fixed now. This memo documents each fix and its implementation.

## Directives (from Ezra)

### D1: Editorial candidates as real gate (not advisory)
- **Problem:** `promote.py` ignores `BOOK_editorial_candidates.json` entirely
- **Fix:** If sidecar exists with `total_candidates > 0`, block promotion (exit 3)
- **File:** `pipeline/promote/promote.py`

### D2: Dossier freshness enforcement
- **Problem:** Dry-run dossier recorded once; if staged text changes afterward, evidence is stale
- **Fix:** On promote (non-dry-run), compare staged file body checksum against existing dossier's `body_checksum`. If mismatch, warn and require `--force-refresh` or re-run dry-run
- **File:** `pipeline/promote/promote.py`

### D3: Normalize residual sidecar field names
- **Problem:** NUM and DEU sidecars use `"class"` instead of `"classification"`. promote.py reads `"classification"` — so the per-entry ratification gate silently passes
- **Fix:** (a) Fix NUM/DEU sidecars to use `"classification"`. (b) Add validation in promote.py that rejects sidecars containing `"class"` field (explicit error, not silent pass)
- **Files:** `staging/validated/OT/NUM_residuals.json`, `DEU_residuals.json`, `pipeline/promote/promote.py`

### D4: Absorbed/fused content = non-promotable
- **Problem:** NUM.6:27 description says "absorbed parenthetically into NUM.6:23" but is classified as `docling_issue` (non-blocking). Absorbed content means the text exists but is misplaced — recoverable in principle.
- **Fix:** Any residual whose description contains "absorbed", "fused into", or "embedded in" is auto-flagged as blocking. promote.py scans description text.
- **File:** `pipeline/promote/promote.py`

### D5: Require `ratified_by: human` for non-empty residuals
- **Problem:** NUM and DEU sidecars have `ratified_by: "ark"`. Ark is the architecture agent, not the human.
- **Fix:** promote.py requires `ratified_by` to be `"human"` (case-insensitive) for any sidecar with non-empty `residuals` array. Set NUM/DEU to `ratified_by: null` until human ratifies.
- **Files:** `pipeline/promote/promote.py`, NUM/DEU sidecars

### D6: V10 absorbed-content detection
- **Problem:** V9 detects embedded verses by digit pattern in preceding verse text. DEU.33:8 was absorbed without a digit signal — V9 can't detect it.
- **Fix:** New V10 check: for each V4 gap, load Brenton text for the missing verse and fuzzy-match against adjacent OSB verses. If match score > threshold, flag as "absorbed content likely present in adjacent verse".
- **File:** `pipeline/validate/validate_canon.py`

---

## Execution Sequence

1. Fix NUM/DEU sidecars (D3 data fix)
2. Implement promote.py gates (D1, D2, D3 validation, D4, D5)
3. Implement V10 validator (D6)
4. Add tests for all new gates
5. Run full test suite
6. Promote LEV (Ezra says: if satisfied)
7. Regenerate EXO/NUM/DEU dossiers with hardened gate

---

## Execution Results

All 6 directives implemented, tested, and verified:

| Directive | Status | Evidence |
|-----------|--------|----------|
| D1 Editorial candidates gate | DONE | `TestEditorialCandidatesGate` (2 tests pass) |
| D2 Dossier freshness | DONE | `TestDossierFreshness` (2 tests pass) |
| D3 Field normalization | DONE | NUM/DEU sidecars fixed + `TestSidecarFieldNormalization` (1 test) |
| D4 Absorbed content auto-block | DONE | NUM.6:27 now blocks (exit 3) + `TestAbsorbedContentGate` (3 tests) |
| D5 Human ratification required | DONE | NUM/DEU set to null + `TestHumanRatificationGate` (4 tests) |
| D6 V10 absorbed-content detector | DONE | DEU.33:8 detected in DEU.33:7 (47% word match) |

**Additional fix:** V10 prefix collision with V1 in dossier generator resolved (exact prefix regex matching).

**Test suite:** 37 tests, all pass (was 25 → +12 new gate tests).

**LEV promoted:** canon/OT/LEV.md written with checksum e8ff6895...

## Post-Hardening Dashboard

| Book | Status | Gate blockers |
|------|--------|---------------|
| GEN | promoted | — |
| EXO | promotion_ready | Awaiting Ezra audit + Human confirmation |
| LEV | promoted | — |
| NUM | editorially_clean | D4: absorbed content (NUM.6:27), D5: needs human ratification |
| DEU | editorially_clean | D5: needs human ratification, V10: absorbed content warning |

## Post-Hardening Gate Summary

The promotion gate now enforces:
- V1-V9 validation clean (existing)
- V7 completeness (existing, --allow-incomplete)
- V10 absorbed-content cross-reference (NEW)
- Residual sidecar ratified by human (NEW)
- Residual field normalization (NEW)
- Absorbed/fused description auto-block (NEW)
- Editorial candidates gate (NEW)
- Dossier freshness verification (NEW)
