# 2 Peter Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/2PE.md`
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
| R6 | Drop-cap omissions detected (NO auto-fix) | 17 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L64:
  - `2PE.2:16 but he was rebuked for his iniquity: adumb donkey speaking with aman'svoice restrained the madness of the prophet.`
  + `2PE.2:16 but he was rebuked for his iniquity: adumb donkey speaking with aman's voice restrained the madness of the prophet.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 2PE.1:3 | `as His divine power has given to us all things tha...` |
| 2PE.1:6 | `to knowledge self-control, to self-control perseve...` |
| 2PE.1:7 | `to godliness brotherly kindness, and to brotherly ...` |
| 2PE.1:11 | `for so an entrance will be supplied to you abundan...` |
| 2PE.2:1 | `ut there were also false prophets among the people...` |
| 2PE.2:5 | `and did not spare the ancient world, but saved Noa...` |
| 2PE.2:6 | `and turning the cities of Sodom and Gomorrah into ...` |
| 2PE.2:7 | `and delivered righteous Lot, who was oppressed by ...` |
| 2PE.2:9 | `then the Lord knows how to deliver the godly out o...` |
| 2PE.2:13 | `and will receive the wages of unrighteousness, as ...` |
| 2PE.2:14 | `having eyes full of adultery and that cannot cease...` |
| 2PE.2:16 | `but he was rebuked for his iniquity: adumb donkey ...` |
| 2PE.3:1 | `eloved, I now write to you this second epistle (in...` |
| 2PE.3:2 | `that you may be mindful of the words which were sp...` |
| 2PE.3:15 | `and consider that the longsuffering of our Lord is...` |
| 2PE.3:16 | `as also in all his epistles, speaking in them of t...` |
| 2PE.3:18 | `but grow in the grace and knowledge of our Lord an...` |
