# 2 Thessalonians Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/2TH.md`
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
| R6 | Drop-cap omissions detected (NO auto-fix) | 18 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L74:
  - `2TH.3:8 nor did we eat anyone'sbread free of charge, but worked with labor and toil night and day, that we might not be aburden to any of you,`
  + `2TH.3:8 nor did we eat anyone's bread free of charge, but worked with labor and toil night and day, that we might not be aburden to any of you,`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 2TH.1:1 | `aul, Silvanus, and Timothy, To the church of the T...` |
| 2TH.1:4 | `so that we ourselves boast of you among the church...` |
| 2TH.1:5 | `which is manifest evidence of the righteous judgme...` |
| 2TH.1:6 | `since it is arighteous thing with God to repay wit...` |
| 2TH.1:7 | `and to give you who are troubled rest with us when...` |
| 2TH.1:8 | `in flaming fire taking vengeance on those who do n...` |
| 2TH.1:10 | `when He comes, in that Day, to be glorified in His...` |
| 2TH.1:12 | `that the name of our Lord Jesus Christ may be glor...` |
| 2TH.2:1 | `ow, brethren, concerning the coming of our Lord Je...` |
| 2TH.2:2 | `not to be soon shaken in mind or troubled, either ...` |
| 2TH.2:4 | `who opposes and exalts himself above all that is c...` |
| 2TH.2:10 | `and with all unrighteous deception among those who...` |
| 2TH.2:12 | `that they all may be condemned who did not believe...` |
| 2TH.2:14 | `to which He called you by our gospel, for the obta...` |
| 2TH.3:1 | `inally, brethren, pray for us, that the word of th...` |
| 2TH.3:2 | `and that we may be delivered from unreasonable and...` |
| 2TH.3:8 | `nor did we eat anyone'sbread free of charge, but w...` |
| 2TH.3:9 | `not because we do not have authority, but to make ...` |
