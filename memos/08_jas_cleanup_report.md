# James Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/JAS.md`
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
| R6 | Drop-cap omissions detected (NO auto-fix) | 12 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L49:
  - `JAS.1:26 If anyone among you athinks he is religious, and does not bridle his tongue but deceives his own heart, this one'sreligion is useless.`
  + `JAS.1:26 If anyone among you athinks he is religious, and does not bridle his tongue but deceives his own heart, this one's religion is useless.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| JAS.1:8 | `he is adouble-minded man, unstable in all his ways...` |
| JAS.1:10 | `but the rich in his humiliation, because as aflowe...` |
| JAS.1:20 | `for the wrath of man does not produce the righteou...` |
| JAS.1:24 | `for he observes himself, goes away, and immediatel...` |
| JAS.2:1 | `ybrethren, do not hold the faith of our Lord Jesus...` |
| JAS.2:3 | `and you pay attention to the one wearing the fine ...` |
| JAS.2:9 | `but if you show partiality, you commit sin, and ar...` |
| JAS.2:16 | `and one of you says to them, 'Depart in peace, be ...` |
| JAS.3:1 | `ybrethren, let not many of you become teachers, kn...` |
| JAS.4:1 | `here do wars and fights come from among you? Do th...` |
| JAS.5:1 | `ome now, you rich, weep and howl for your miseries...` |
| JAS.5:20 | `let him know that he who turns asinner from the er...` |
