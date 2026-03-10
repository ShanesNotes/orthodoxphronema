# Genesis Cleanup Report — 2026-03-08

## Summary
- Input: `staging/validated/OT/GEN.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 1

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 0 |
| R3 | Rejoin word-split artifacts (allowlist) | 1 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 81 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L1499:
  - `GEN.41:14 Then Pharaoh sent and called Joseph, and they brought him quickly out of the dungeon; and he shaved, changed his clothing, and came to Pharaoh.`
  + `GEN.41:14 Then Pharaoh sent and called Joseph, and they brought him quicklyout of the dungeon; and he shaved, changed his clothing, and came to Pharaoh.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| GEN.1:18 | `and to rule over the day and over the night, and t...` |
| GEN.2:5 | `before any plant of the field was on earth and bef...` |
| GEN.2:6 | `but a fountain came up from the ground and watered...` |
| GEN.2:17 | `but from the tree of the knowledge of good and evi...` |
| GEN.3:3 | `but from the fruit of the tree in the middle of th...` |
| GEN.3:23 | `therefore the Lord God sent him out of the garden ...` |
| GEN.4:5 | `but He did not respect Cain and his sacrifices. So...` |
| GEN.7:3 | `and the clean birds of heaven by twos, male and fe...` |
| GEN.7:9 | `entered with Noah into the ark, two by two, male a...` |
| GEN.7:15 | `entered the ark with Noah, two by two, of all fles...` |
| GEN.9:10 | `and every living creature with you: the birds, the...` |
| GEN.9:15 | `and I will remember My covenant between Me and you...` |
| GEN.9:25 | `he said: 'Cursed be Canaan; A servant of servants ...` |
| GEN.10:12 | `and Resen between Nineveh and Calah (the principal...` |
| GEN.10:16 | `the Jebusite, the Amorite, and the Girgashite;...` |
| GEN.10:17 | `the Hivite, the Arkite, and the Sinite;...` |
| GEN.10:18 | `the Arvadite, the Zemarite, and the Hamathite. Aft...` |
| GEN.13:4 | `to the place of the altar he made there at the beg...` |
| GEN.13:15 | `for all the land you see I give to you and your se...` |
| GEN.14:2 | `that they made war with Bera king of Sodom, Birsha...` |
| GEN.14:6 | `and the Horites in the mountains of Seir, as far a...` |
| GEN.14:9 | `against Chedorlaomer king of Elam, Tidal king of n...` |
| GEN.14:20 | `and blessed be God Most High, who delivered your e...` |
| GEN.14:23 | `that I will take nothing of yours, from a thread t...` |
| GEN.14:24 | `except only what the young men have eaten, and the...` |
| GEN.15:19 | `the Kenites, the Kenezzites, the Kadmonites,...` |
| GEN.15:20 | `the Hittites, the Perizzites, the Rephaim,...` |
| GEN.15:21 | `the Amorites, the Canaanites, the Euaites, the Gir...` |
| GEN.17:11 | `and you shall be circumcised in the flesh of your ...` |
| GEN.18:3 | `and said, 'O Lord, if I have now found grace in Yo...` |
| GEN.19:7 | `and said, 'By no means, my brethren, do not act wi...` |
| GEN.19:19 | `since Your servant found mercy in Your sight, and ...` |
| GEN.20:18 | `for the Lord closed up all the wombs of the house ...` |
| GEN.22:16 | `and said, 'By Myself I have sworn, says the Lord, ...` |
| GEN.23:9 | `that he may give me the cave of Machpelah, which h...` |
| GEN.23:13 | `and he spoke to Ephron in the hearing of the peopl...` |
| GEN.23:18 | `to Abraham as his possession in the presence of th...` |
| GEN.24:3 | `and I will make you swear by the Lord, the God of ...` |
| GEN.24:4 | `but you shall go to my land where I was born, and ...` |
| GEN.24:23 | `and said, 'Whose daughter are you? Tell me, is the...` |
| GEN.24:38 | `but you shall go to my father's house and to my tr...` |
| GEN.24:43 | `behold, I stand by the well of water; and it shall...` |
| GEN.24:44 | `and she says to me, 'Drink, and I will draw for yo...` |
| GEN.24:65 | `for she had said to the servant, 'Who is that man ...` |
| GEN.25:10 | `the field and the cave Abraham purchased from the ...` |
| GEN.26:5 | `because Abraham your father obeyed My voice and ke...` |
| GEN.26:14 | `for he had herds of sheep and oxen and many fields...` |
| GEN.26:29 | `that you will do us no harm, since we have not tou...` |
| GEN.27:45 | `and wrath turn away from you, and he forgets what ...` |
| GEN.28:4 | `and give you the blessing of Abraham, to you and y...` |
| GEN.28:7 | `and Jacob had obeyed his father and mother and had...` |
| GEN.28:21 | `and bring me back in safety to my father's house, ...` |
| GEN.31:5 | `and said to them, 'I see your father's countenance...` |
| GEN.31:49 | `and also The Vision, because he said, 'May God wat...` |
| GEN.32:10 | `let me be satisfied with all the righteousness and...` |
| GEN.32:14 | `two hundred female goats and twenty male goats, tw...` |
| GEN.32:15 | `thirty milk camels with their offspring, forty cow...` |
| GEN.32:20 | `and also say, 'Behold, your servant Jacob is comin...` |
| GEN.34:16 | `then we will give our daughters to you, and we wil...` |
| GEN.34:29 | `and took captive all their wives, their children, ...` |
| GEN.35:24 | `the sons of Rachel were Joseph and Benjamin;...` |
| GEN.35:25 | `the sons of Bilhah, Rachel's maidservant, were Dan...` |
| GEN.35:26 | `and the sons of Zilpah, Leah's maidservant, were G...` |
| GEN.36:3 | `and Basemath, Ishmael's daughter, sister of Nebajo...` |
| GEN.36:5 | `and Aholibamah bore Jeush, Jaalam, and Korah. Thes...` |
| GEN.39:12 | `she caught him by his garment, saying, 'Lie with m...` |
| GEN.39:14 | `she called to the men of her house and spoke to th...` |
| GEN.39:18 | `so it happened, as I lifted my voice and cried out...` |
| GEN.40:10 | `and in the vine were three branches; it was as tho...` |
| GEN.41:11 | `we each had a dream in one night, both he and I. E...` |
| GEN.41:30 | `but after them seven years of famine will arise, a...` |
| GEN.41:54 | `and the seven years of famine began to come, as Jo...` |
| GEN.43:20 | `saying, 'We entreat you, my lord, we indeed came d...` |
| GEN.43:21 | `but it happened, when we came to the encampment, t...` |
| GEN.44:28 | `and the one went out from me, and I said, 'Surely ...` |
| GEN.44:31 | `it will happen, when he sees the lad is not with u...` |
| GEN.46:34 | `that you shall say, 'Your servants are pastoral me...` |
| GEN.47:30 | `but let me lie with my fathers; you shall carry me...` |
| GEN.48:4 | `and said to me, 'Behold, I will increase and multi...` |
| GEN.49:30 | `opposite Mamre in the land of Canaan, which Abraha...` |
| GEN.50:8 | `as well as all the house of Joseph, his brothers, ...` |
