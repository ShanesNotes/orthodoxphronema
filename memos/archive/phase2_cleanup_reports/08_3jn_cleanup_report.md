# 3 John Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/3JN.md`
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
| R6 | Drop-cap omissions detected (NO auto-fix) | 3 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L29:
  - `3JN.1:7 because they went forth for His name'ssake, taking nothing from the Gentiles.`
  + `3JN.1:7 because they went forth for His name's sake, taking nothing from the Gentiles.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 3JN.1:6 | `who have borne witness of your love before the chu...` |
| 3JN.1:7 | `because they went forth for His name'ssake, taking...` |
| 3JN.1:14 | `but I hope to see you shortly, and we shall speak ...` |
