# 1 Thessalonians Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/1TH.md`
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
| R6 | Drop-cap omissions detected (NO auto-fix) | 22 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L121:
  - `1TH.5:13 and to esteem them very highly in love for their work'ssake. Be at peace among yourselves.`
  + `1TH.5:13 and to esteem them very highly in love for their work's sake. Be at peace among yourselves.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 1TH.1:7 | `so that you became examples to all in Macedonia an...` |
| 1TH.1:10 | `and to wait for His Son from heaven, whom He raise...` |
| 1TH.2:1 | `or you yourselves know, brethren, that our coming ...` |
| 1TH.2:11 | `as you know how we exhorted, and comforted, and ch...` |
| 1TH.2:12 | `that you would walk worthy of God who calls you in...` |
| 1TH.2:15 | `who killed both the Lord Jesus and their own proph...` |
| 1TH.3:1 | `herefore, when we could no longer endure it, we th...` |
| 1TH.3:2 | `and sent Timothy, our brother and minister of God,...` |
| 1TH.3:3 | `that no one should be shaken by these afflictions;...` |
| 1TH.3:7 | `therefore, brethren, in all our affliction and dis...` |
| 1TH.3:13 | `so that He may establish your hearts blameless in ...` |
| 1TH.4:1 | `inally then, brethren, we urge and exhort in the L...` |
| 1TH.4:2 | `for you know what commandments we gave you through...` |
| 1TH.4:4 | `that each of you should know how to possess his ow...` |
| 1TH.4:5 | `not in passion of lust, like the Gentiles who do n...` |
| 1TH.4:6 | `that no one should take advantage of and defraud h...` |
| 1TH.4:10 | `and indeed you do so toward all the brethren who a...` |
| 1TH.4:11 | `that you also aspire to lead aquiet life, to mind ...` |
| 1TH.4:12 | `that you may walk properly toward those who are ou...` |
| 1TH.5:1 | `ut concerning the times and the seasons, brethren,...` |
| 1TH.5:10 | `who died for us, that whether we wake or sleep, we...` |
| 1TH.5:13 | `and to esteem them very highly in love for their w...` |
