# Philemon Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/PHM.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 1

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 1 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 6 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L29:
  - `PHM.1:9 yet for love'ssake I rather appeal to you -being such aone as Paul, the aged, and now also aprisoner of Jesus Christ-`
  + `PHM.1:9 yet for love's sake I rather appeal to you -being such aone as Paul, the aged, and now also aprisoner of Jesus Christ-`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| PHM.1:2 | `to the beloved a Apphia, Archippus our fellow sold...` |
| PHM.1:9 | `yet for love'ssake I rather appeal to you -being s...` |
| PHM.1:11 | `who once was unprofitable to you, but now is profi...` |
| PHM.1:13 | `whom I wished to keep with me, that on your behalf...` |
| PHM.1:16 | `no longer as aslave but more than aslave-abeloved ...` |
| PHM.1:24 | `as do Mark, Aristarchus, Demas, Luke, my fellow la...` |
