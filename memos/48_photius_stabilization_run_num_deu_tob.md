# Memo 48 — Photius Stabilization Run: NUM, DEU, TOB

**Date:** 2026-03-10
**From:** Photius
**To:** Ezra, Ark, Human (Shane)
**Status:** Completed; 3 books moved to promotion_ready.

## Executive Summary
Per the priorities on the Ezra Ops Board, I have cleared the structural and editorial blockers for Numbers (NUM), Deuteronomy (DEU), and Tobit (TOB). These books are now in `dry-run` (Promotion Ready) status.

## Recoveries and Fixes

### 1. Numbers (NUM)
- **V12 Leakage:** Fixed inline verse-number leakage in `NUM.21:19` and `NUM.29:14`.
- **Residual Resolution:** Marked `NUM.6:27` as resolved (previously manually restored).
- **Status:** Moved from `blocked` to `promotion_ready`.

### 2. Deuteronomy (DEU)
- **V4/V10 Absorption:** Recovered `DEU.33:8` which was merged into `DEU.33:7`.
- **OCR Fix:** Fixed split-word artifact in "visit" (`DEU.33:7`).
- **Residual Resolution:** Marked `DEU.33:8` as resolved.
- **Status:** Moved from `blocked` to `promotion_ready`.

### 3. Tobit (TOB)
- **Truncation/Omission:** Recovered missing/truncated text for `TOB.13:1`, `TOB.13:2`, and `TOB.14:1` using `pdftotext` extraction from OSB PDF pages 1358-1361.
- **Residual Resolution:** Marked `TOB.13:2` and `TOB.14:1` as resolved.
- **Status:** Moved from `blocked` to `promotion_ready`.

## Evidence Pack
| Book | Change | OSB PDF Page(s) |
|---|---|---|
| NUM | V12 cleanup | n/a (editorial) |
| DEU | 33:8 recovery | 595 |
| TOB | 13:1-2, 14:1 recovery | 1358, 1361 |

## Dashboard Update
- **Promotion Ready:** Increased from 10 to 13.
- **Blocked:** Decreased accordingly.

## Next Steps
- Investigate `NEH` (Nehemiah) and `EST` (Esther) for `V8` fragment heading issues.
- Broaden `fix_split_words.py` to catch remaining editorial residue as proposed in Memo 44.
