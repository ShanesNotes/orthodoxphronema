# Jude Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/JUD.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 0

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 0 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 3 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| JUD.1:7 | `as Sodom and Gomorrah, and the cities around them ...` |
| JUD.1:15 | `to execute judgment on all, to convict all who are...` |
| JUD.1:18 | `how they told you that there would be mockers in t...` |
