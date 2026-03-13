# Tobit Cleanup Report — 2026-03-09

## Summary
- Input: `staging/validated/OT/TOB.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 7

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 7 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 5 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L37:
  - `TOB.1:21 But not even fifty days passed before two of King Sennacherib'ssons had killed him and escaped into the mountains of Ararat. Thus Esarhaddon his son reigned in his place. He appointed Ahikar, the son of my brother Anael, to be over all the accounts of his kingdom and over the entire government.`
  + `TOB.1:21 But not even fifty days passed before two of King Sennacherib's sons had killed him and escaped into the mountains of Ararat. Thus Esarhaddon his son reigned in his place. He appointed Ahikar, the son of my brother Anael, to be over all the accounts of his kingdom and over the entire government.`

L69:
  - `TOB.3:7 On the same day, in Ecbatana of Media, Sarah, the daughter of Raguel, happened to be insulted by her father'smaids.`
  + `TOB.3:7 On the same day, in Ecbatana of Media, Sarah, the daughter of Raguel, happened to be insulted by her father's maids.`

L80:
  - `TOB.3:15 I have not defiled my name nor the name of my father in the land of my captivity. I am my father'sonly offspring. He has no other child who will be his heir. Neither does he have a brother close at hand, nor an adopted son that I might keep myself as a wife to him. Seven of my husbands have already perished. What should I live for? But if it does not seem good to You to kill me, command that I be looked upon with favor, and that mercy be shown to me, so I may no longer hear disgrace.'`
  + `TOB.3:15 I have not defiled my name nor the name of my father in the land of my captivity. I am my father's only offspring. He has no other child who will be his heir. Neither does he have a brother close at hand, nor an adopted son that I might keep myself as a wife to him. Seven of my husbands have already perished. What should I live for? But if it does not seem good to You to kill me, command that I be looked upon with favor, and that mercy be shown to me, so I may no longer hear disgrace.'`

L130:
  - `TOB.5:17 Thus they were well pleased. Then he said to Tobias, 'Prepare for the journey, and may it be prosperous.' So his son prepared the things for the journey. Then his father said to him, 'Go with this man, and may the God who dwells in heaven prosper your journey. May His angel journey with you.' They both departed, and the young man'sdog went with them.`
  + `TOB.5:17 Thus they were well pleased. Then he said to Tobias, 'Prepare for the journey, and may it be prosperous.' So his son prepared the things for the journey. Then his father said to him, 'Go with this man, and may the God who dwells in heaven prosper your journey. May His angel journey with you.' They both departed, and the young man's dog went with them.`

L239:
  - `TOB.10:12 To his daughter he said, 'Honor your husband'smother and father, for they are now your parents. Let me hear a good report of you,' and he kissed her.`
  + `TOB.10:12 To his daughter he said, 'Honor your husband's mother and father, for they are now your parents. Let me hear a good report of you,' and he kissed her.`

L276:
  - `TOB.12:6 Then Raphael secretly called the two of them, and said to them, 'Bless God and give Him thanks. Ascribe greatness to Him and give thanks in the presence of all the living for what He has done for you. It is good to bless God and to exalt His name. Make known the words of God'sworks honorably and do not delay to give thanks to Him.`
  + `TOB.12:6 Then Raphael secretly called the two of them, and said to them, 'Bless God and give Him thanks. Ascribe greatness to Him and give thanks in the presence of all the living for what He has done for you. It is good to bless God and to exalt His name. Make known the words of God's works honorably and do not delay to give thanks to Him.`

L321:
  - `TOB.14:3 He grew very old, and called his son and his son'ssons, and said, 'My son, take your sons. Behold, I have grown old, and I am departing from this life.`
  + `TOB.14:3 He grew very old, and called his son and his son's sons, and said, 'My son, take your sons. Behold, I have grown old, and I am departing from this life.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| TOB.3:17 | `and he was sent to heal the two of them: to remove...` |
| TOB.6:11 | `the angel said to the young man, 'Brother, we will...` |
| TOB.7:14 | `and summoned his wife Edna. She took a scroll and ...` |
| TOB.8:12 | `and said to his wife Edna, 'Send one of the maids ...` |
| TOB.10:2 | `he asked, 'Has he perhaps been dishonored? Or has ...` |
