# Dossier Schema Drift Packet (2026-03-12)

This packet summarizes the exact dossier-schema delta required for the `promote.py` repair lane. It establishes the current baseline from real dossiers and the target state required by `tests/test_promote_gate.py`.

## 1. Dossier Field Matrix

| Field Name | Current Source in `promote.py` | Required by Tests | Present in Real Dossiers | Recommended Status |
| :--- | :--- | :--- | :--- | :--- |
| `book_code` | `book_code` (arg) | Yes | Yes (all) | Keep |
| `testament` | `testament` (arg) | Yes | Yes (all) | Keep |
| `timestamp` | `datetime.now()` | Yes | Yes (all) | Keep |
| `registry_version`| `registry_version` (arg) | Yes | Yes (all) | Keep |
| `body_checksum` | `body_checksum` (arg) | Yes | Yes (all) | Keep |
| `validation` | `generate_dossier` logic | Yes | Yes (all) | Reshape (add V10, INFO, SKIP) |
| `residuals_sidecar`| `sidecar` (arg) | Yes | Yes (`EST`) | Keep |
| `decision` | `decision` (arg) | Yes | Yes (all) | Keep |
| `allow_incomplete` | **Missing** | Yes (L510) | No | **Add** (boolean) |
| `staged_path` | **Missing** | Yes (L578) | No | **Add** (string/path) |
| `residuals_path` | **Missing** | Yes (L595) | No | **Add** (string/path) |
| `editorial_candidates_path` | **Missing** | Yes (L596) | No | **Add** (string/path) |

## 2. Validation Status Matrix (V1-V10)

Current `promote.py` logic (`L111-L125`) only maps `V1-V9` and uses a binary `WARN` -> `FAIL` or `PASS` mapping. It lacks the granularity required by the new validation contract.

| Check | Current Dossier Support | Test Expectations (`L542-L568`) | Current Misclassification Path |
| :--- | :--- | :--- | :--- |
| **V1-V6** | Binary (PASS/FAIL) | PASS, WARN, FAIL | Warnings always map to `FAIL` if strict, or `WARN` otherwise. |
| **V7** | PASS/WARN | **INFO** (informational gap) | Maps to `PASS` or `WARN` in `promote.py:121`. |
| **V8-V9** | PASS/WARN | PASS, WARN, FAIL | Same as V1-V6. |
| **V10** | **None** | **SKIP**, **WARN** | Totally omitted; warnings might leak into other checks if matched loosely. |

**Recommended Status Logic:**
- `V7`: Should support `INFO` for non-blocking completeness issues.
- `V10`: Must be added for "Absorbed content" detection.
- `SKIP`: Should be used when a check is explicitly bypassed.

## 3. Exit-Path Matrix

| Exit Path | `promote.py` Line | Dossier Written? | Shape Status |
| :--- | :--- | :--- | :--- |
| **Validation Error (V1-V9)** | `L181` | Yes | **Incomplete** (Missing `staged_path`, etc.) |
| **Editorial Block (D1)** | **None** | No | **Gap** (Gate not implemented in `promote.py`) |
| **Freshness Block (D2)** | **None** | No | **Gap** (Gate not implemented in `promote.py`) |
| **Ratification Block (D5)** | `L215`, `L225` | Yes | **Incomplete** (Missing paths) |
| **Completeness Block (V7)** | `L235` | Yes | **Incomplete** (Missing `allow_incomplete` flag) |
| **Dry-Run Success** | `L256` | Yes | **Incomplete** (Missing paths/flags) |
| **Promote Success** | `L264` | Yes | **Incomplete** (Missing paths/flags) |

## Evidence References

- **Real Dossier Sample:** `reports/EST_promotion_dossier.json` (Shows `residuals_sidecar` inclusion but missing paths).
- **Test Failures:** `tests/test_promote_gate.py`
  - `KeyError: 'allow_incomplete'` (L510)
  - `AssertionError: assert 'PASS' == 'INFO'` (L542 - V7 mapping drift)
  - `KeyError: 'staged_path'` (L578)
  - `KeyError: 'residuals_path'` (L595)

---

## Completion Handshake

- **Files read:**
  - `pipeline/promote/promote.py`
  - `pipeline/promote/gates.py`
  - `tests/test_promote_gate.py`
  - `reports/2JN_promotion_dossier.json`
  - `reports/EST_promotion_dossier.json`
  - `reports/WIS_promotion_dossier.json`
  - `reports/MAT_promotion_dossier.json`
- **Verification run:**
  - `pytest tests/test_promote_gate.py -q`
  - **Result:** 13 failed, 9 passed. (Dossier schema and gate drift confirmed).
- **Artifacts refreshed:**
  - `memos/100_dossier_schema_drift_packet.md` (Created)
- **Remaining known drift:**
  - `promote.py` is not utilizing `gates.py`.
  - `generate_dossier` schema is stale.
  - Validation status mapping is insufficient.
- **Next owner:** Ark (for `promote.py` repair lane)
