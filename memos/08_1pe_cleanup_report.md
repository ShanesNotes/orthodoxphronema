# 1 Peter Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/1PE.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 4

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 4 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 27 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L39:
  - `1PE.1:17 And if you call on the Father, who without partiality judges according to each one'swork, conduct yourselves throughout the time of your stay here in fear; 18 knowing that you were not redeemed with corruptible things, like silver or gold, from your aimless conduct received by tradition from your fathers, 19 but with the precious blood of Christ, as of alamb without blemish and without spot.`
  + `1PE.1:17 And if you call on the Father, who without partiality judges according to each one's work, conduct yourselves throughout the time of your stay here in fear; 18 knowing that you were not redeemed with corruptible things, like silver or gold, from your aimless conduct received by tradition from your fathers, 19 but with the precious blood of Christ, as of alamb without blemish and without spot.`

L70:
  - `1PE.2:13 Therefore submit yourselves to every ordinance of man for the Lord'ssake, whether to the king as supreme,`
  + `1PE.2:13 Therefore submit yourselves to every ordinance of man for the Lord's sake, whether to the king as supreme,`

L140:
  - `1PE.4:13 but rejoice to the extent that you partake of Christ'ssufferings, that when His glory is revealed, you may also be glad with exceeding joy.`
  + `1PE.4:13 but rejoice to the extent that you partake of Christ's sufferings, that when His glory is revealed, you may also be glad with exceeding joy.`

L142:
  - `1PE.4:15 But let none of you suffer as amurderer, athief, an evildoer, or as abusybody in other people'smatters.`
  + `1PE.4:15 But let none of you suffer as amurderer, athief, an evildoer, or as abusybody in other people's matters.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 1PE.1:4 | `to an inheritance incorruptible and undefiled and ...` |
| 1PE.1:5 | `who are kept by the power of God through faith for...` |
| 1PE.1:7 | `that the genuineness of your faith, being much mor...` |
| 1PE.1:8 | `whom having not seen ayou love. Though now you do ...` |
| 1PE.1:14 | `as obedient children, not conforming yourselves to...` |
| 1PE.1:15 | `but as He who called you is holy, you also be holy...` |
| 1PE.1:16 | `because it is written, 'Be holy, for I am holy.' a...` |
| 1PE.1:21 | `who through Him believe in God, who raised Him fro...` |
| 1PE.1:23 | `having been born again, not of corruptible seed bu...` |
| 1PE.2:1 | `herefore, laying aside all malice, all deceit, hyp...` |
| 1PE.2:2 | `as newborn babes, desire the pure milk of the word...` |
| 1PE.2:5 | `you also, as living stones, are being built up asp...` |
| 1PE.2:10 | `who once were not apeople but are now the people o...` |
| 1PE.2:12 | `having your conduct honorable among the Gentiles, ...` |
| 1PE.2:14 | `or to governors, as to those who are sent by him f...` |
| 1PE.2:24 | `who Himself bore our sins in His own body on the t...` |
| 1PE.3:1 | `ives, likewise, be submissive to your own husbands...` |
| 1PE.3:2 | `when they observe your chaste conduct accompanied ...` |
| 1PE.3:6 | `as Sarah obeyed Abraham, calling him lord, whose d...` |
| 1PE.3:16 | `having agood conscience, that when they defame you...` |
| 1PE.3:22 | `who has gone into heaven and is at the right hand ...` |
| 1PE.4:1 | `herefore, since Christ suffered for us ain the fle...` |
| 1PE.4:2 | `that he no longer should live the rest of his time...` |
| 1PE.4:13 | `but rejoice to the extent that you partake of Chri...` |
| 1PE.5:1 | `he elders who are among you I exhort, I who am afe...` |
| 1PE.5:3 | `nor as being lords over those entrusted to you, bu...` |
| 1PE.5:4 | `and when the Chief Shepherd appears, you will rece...` |
