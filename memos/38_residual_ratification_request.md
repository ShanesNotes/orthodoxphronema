# Memo 38 — Residual Ratification Request (Groups 2-3 Historical Books)

**Date:** 2026-03-09
**From:** Ark
**To:** Human
**Re:** 6 books need `ratified_by: "human"` on residuals sidecars before promotion

---

## Summary

The stabilization sprint (memos 37→38) created or updated residuals sidecars for 6 books. All are classified `docling_issue` (parser failure — text exists in OSB PDF but Docling didn't capture it). Per D5 gate, non-empty residuals require `ratified_by: "human"` before promotion.

**Action required:** For each book below, review the listed gaps and set `ratified_by: "human"` and `ratified_date` in the sidecar JSON if you accept the gaps as non-blocking parser issues.

---

## Books Awaiting Ratification

### 1. JDG — 1 residual (99.8% complete)
- **File:** `staging/validated/OT/JDG_residuals.json`
- `JDG.11:40` — final verse of chapter 11, not captured by Docling

### 2. 1SA — 19 residuals (97.9% complete)
- **File:** `staging/validated/OT/1SA_residuals.json`
- `1SA.17:34–17:52` — 19 tail-end verses of chapter 17 (David and Goliath narrative)
- This is the largest gap in any historical book; likely a page-boundary issue in Docling

### 3. 2SA — 2 residuals (99.9% complete)
- **File:** `staging/validated/OT/2SA_residuals.json`
- `2SA.17:29` — final verse of chapter 17
- `2SA.23:40` — final verse of chapter 23

### 4. 1KI — 5 residuals (99.4% complete)
- **File:** `staging/validated/OT/1KI_residuals.json`
- `1KI.22:46–22:50` — 5 tail-end verses of final chapter

### 5. 1CH — 1 residual (98.4% complete)
- **File:** `staging/validated/OT/1CH_residuals.json`
- `1CH.16:7` — verse absent from extraction (exists in OSB PDF)

### 6. 2CH — 1 residual (101.2% V7, 1 missing verse)
- **File:** `staging/validated/OT/2CH_residuals.json`
- `2CH.33:1` — dropcap + opening text not captured; verse 33:2 begins mid-sentence

---

## CVC Anomalies (informational, not blocking)

Some books have verses beyond CVC expectations (LXX versification differences):
- **1SA**: ch1 has 29 verses (CVC expects 28), ch18 has 19 (CVC expects 18) — net V7 gap = 17
- **2SA**: ch3 has 40 verses (CVC expects 39) — net V7 gap = 1

These extra verses are legitimate LXX content and do not require correction.

---

## How to Ratify

For each book, edit the `_residuals.json` file:
```json
"ratified_by": "human",
"ratified_date": "YYYY-MM-DD"
```

Once ratified, `promote.py --dry-run` will pass the D5 gate for that book.
