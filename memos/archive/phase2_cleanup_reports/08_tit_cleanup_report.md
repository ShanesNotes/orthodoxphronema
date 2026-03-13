# Titus Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/TIT.md`
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
| R6 | Drop-cap omissions detected (NO auto-fix) | 19 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L17:
  - `TIT.1:1 aul, abondservant of God and an apostle of Jesus Christ, according to the faith of God'select and the acknowledgment of the truth which accords with godliness,`
  + `TIT.1:1 aul, abondservant of God and an apostle of Jesus Christ, according to the faith of God's elect and the acknowledgment of the truth which accords with godliness,`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| TIT.1:1 | `aul, abondservant of God and an apostle of Jesus C...` |
| TIT.1:2 | `in hope of eternal life which God, who cannot lie,...` |
| TIT.1:3 | `but has in due time manifested His word through pr...` |
| TIT.1:6 | `if aman is blameless, the husband of one wife, hav...` |
| TIT.1:8 | `but hospitable, alover of what is good, sober-mind...` |
| TIT.1:11 | `whose mouths must be stopped, who subvert whole ho...` |
| TIT.1:14 | `not giving heed to Jewish fables and commandments ...` |
| TIT.2:1 | `ut as for you, speak the things which are proper f...` |
| TIT.2:2 | `that the older men be sober, reverent, temperate, ...` |
| TIT.2:3 | `the older women likewise, that they be reverent in...` |
| TIT.2:4 | `that they admonish the young women to love their h...` |
| TIT.2:5 | `to be discreet, chaste, homemakers, good, obedient...` |
| TIT.2:7 | `in all things showing yourself to be apattern of g...` |
| TIT.2:10 | `not pilfering, but showing all good fidelity, that...` |
| TIT.3:1 | `emind them to be subject to rulers and authorities...` |
| TIT.3:2 | `to speak evil of no one, to be peaceable, gentle, ...` |
| TIT.3:5 | `not by works of righteousness which we have done, ...` |
| TIT.3:6 | `whom He poured out on us abundantly through Jesus ...` |
| TIT.3:7 | `that having been justified by His grace we should ...` |
