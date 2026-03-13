# 1 John Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/1JN.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 3

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 3 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 7 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L52:
  - `1JN.2:12 I write to you, little children, Because your sins are forgiven you for His name'ssake.`
  + `1JN.2:12 I write to you, little children, Because your sins are forgiven you for His name's sake.`

L92:
  - `1JN.3:12 not as Cain who was of the wicked one and murdered his brother. And why did he murder him? Because his works were evil and his brother'srighteous.`
  + `1JN.3:12 not as Cain who was of the wicked one and murdered his brother. And why did he murder him? Because his works were evil and his brother's righteous.`

L97:
  - `1JN.3:17 But whoever has this world'sgoods, and sees his brother in need, and shuts up his heart from him, how does the love of God abide in him?`
  + `1JN.3:17 But whoever has this world's goods, and sees his brother in need, and shuts up his heart from him, how does the love of God abide in him?`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 1JN.1:3 | `that which we have seen and heard we declare to yo...` |
| 1JN.2:1 | `ylittle children, these things I write to you, so ...` |
| 1JN.3:1 | `ehold what manner of love the Father has bestowed ...` |
| 1JN.3:12 | `not as Cain who was of the wicked one and murdered...` |
| 1JN.4:1 | `eloved, do not believe every spirit, but test the ...` |
| 1JN.4:3 | `and every spirit that does not confess that a Jesu...` |
| 1JN.5:1 | `hoever believes that Jesus is the Christ is born o...` |
