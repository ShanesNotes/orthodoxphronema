# Ruth Cleanup Report — 2026-03-09

## Summary
- Input: `staging/validated/OT/RUT.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 5

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 5 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 1 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L19:
  - `RUT.1:3 Then Elimelech, Naomi'shusband, died; and she was left with her two sons.`
  + `RUT.1:3 Then Elimelech, Naomi's husband, died; and she was left with her two sons.`

L27:
  - `RUT.1:8 And Naomi said to her two daughters-in-law, 'Go, return each to her mother'shouse. May the Lord have mercy on you, as you have dealt with the dead and with me.`
  + `RUT.1:8 And Naomi said to her two daughters-in-law, 'Go, return each to her mother's house. May the Lord have mercy on you, as you have dealt with the dead and with me.`

L47:
  - `RUT.2:1 There was arelative of Naomi'shusband, a man of great wealth,`
  + `RUT.2:1 There was arelative of Naomi's husband, a man of great wealth,`

L65:
  - `RUT.2:19 And her mother-in-law said to her, 'Where have you gleaned today? And where did you work? Blessed be the one who took notice of you.' So Ruth told her mother-in-law where she had worked and said, 'The man'sname with whom I worked today is Boaz.'`
  + `RUT.2:19 And her mother-in-law said to her, 'Where have you gleaned today? And where did you work? Blessed be the one who took notice of you.' So Ruth told her mother-in-law where she had worked and said, 'The man's name with whom I worked today is Boaz.'`

L106:
  - `RUT.4:9 And Boaz said to the elders and all the people, 'You are witnesses today that I have bought all that was Elimelech's, and all that was Chilion'sand Mahlon's, from the hand of Naomi.`
  + `RUT.4:9 And Boaz said to the elders and all the people, 'You are witnesses today that I have bought all that was Elimelech's, and all that was Chilion's and Mahlon's, from the hand of Naomi.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| RUT.1:13 | `would you wait for them till they were grown? Woul...` |
