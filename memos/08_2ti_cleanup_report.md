# 2 Timothy Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/2TI.md`
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
| R6 | Drop-cap omissions detected (NO auto-fix) | 17 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 2TI.1:1 | `aul, an apostle of Jesus Christ aby the will of Go...` |
| 2TI.1:9 | `who has saved us and called us with aholy calling,...` |
| 2TI.1:10 | `but has now been revealed by the appearing of our ...` |
| 2TI.1:11 | `to which I was appointed apreacher, an apostle, an...` |
| 2TI.1:17 | `but when he arrived in Rome, he sought me out very...` |
| 2TI.2:1 | `ou therefore, my son, be strong in the grace that ...` |
| 2TI.2:9 | `for which I suffer trouble as an evildoer, even to...` |
| 2TI.2:18 | `who have strayed concerning the truth, saying that...` |
| 2TI.2:25 | `in humility correcting those who are in opposition...` |
| 2TI.2:26 | `and that they may come to their senses and escape ...` |
| 2TI.3:1 | `ut know this, that in the last days perilous times...` |
| 2TI.3:9 | `but they will progress no further, for their folly...` |
| 2TI.3:15 | `and that from childhood you have known the Holy Sc...` |
| 2TI.3:17 | `that the man of God may be complete, thoroughly eq...` |
| 2TI.4:1 | `charge you therefore before God and the Lord Jesus...` |
| 2TI.4:4 | `and they will turn their ears away from the truth,...` |
| 2TI.4:10 | `for Demas has forsaken me, having loved this prese...` |
