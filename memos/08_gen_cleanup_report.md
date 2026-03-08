# Genesis Cleanup Report — 2026-03-07

## Summary
- Input: `staging/validated/OT/GEN.md`
- Mode: **in-place**
- Brenton reference: enabled (R7)
- Lines changed: 1

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 0 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 94 |
| R7 | Brenton-assisted fused compound splits | 1 |

## Before/After Examples (first 20 + last 20 changed lines)

L656:
  - `GEN.21:14 So Abraham rose early in the morning, and took bread and askin of water; and putting it on her shoulder, he gave it and the boy to Hagar, and sent her away. Then she departed and wandered in the wilderness, near the Well of Oath.`
  + `GEN.21:14 So Abraham rose early in the morning, and took bread and a skin of water; and putting it on her shoulder, he gave it and the boy to Hagar, and sent her away. Then she departed and wandered in the wilderness, near the Well of Oath.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| GEN.1:1 | `nthe beginning God made heaven and earth....` |
| GEN.1:18 | `and to rule over the day and over the night, and t...` |
| GEN.2:1 | `hus heaven and earth and all their adornment were ...` |
| GEN.2:5 | `before any plant of the field was on earth and bef...` |
| GEN.2:6 | `but a fountain came up from the ground and watered...` |
| GEN.2:17 | `but from the tree of the knowledge of good and evi...` |
| GEN.3:1 | `ow the serpent was more cunning than all the wild ...` |
| GEN.3:3 | `but from the fruit of the tree in the middle of th...` |
| GEN.3:23 | `therefore the Lord God sent him out of the garden ...` |
| GEN.4:1 | `ow Adam knew Eve his wife, and she conceived and b...` |
| GEN.4:5 | `but He did not respect Cain and his sacrifices. So...` |
| GEN.5:1 | `his is the book of the genesis of mankind in the d...` |
| GEN.6:1 | `ow it came to pass that men began to exist in grea...` |
| GEN.7:1 | `hen the Lord God said to Noah, 'Enter the ark, you...` |
| GEN.7:3 | `and the clean birds of heaven by twos, male and fe...` |
| GEN.8:1 | `hen God remembered Noah, and whatever was with him...` |
| GEN.9:1 | `hus God blessed Noah and his sons, and said to the...` |
| GEN.9:10 | `and every living creature with you: the birds, the...` |
| GEN.9:15 | `and I will remember My covenant between Me and you...` |
| GEN.10:1 | `ow this is the genealogy of Noah's sons: Shem, Ham...` |
| GEN.10:12 | `and Resen between Nineveh and Calah (the principal...` |
| GEN.11:1 | `ow the whole earth was one language and one speech...` |
| GEN.12:1 | `ow the Lord said to Abram, 'Get out of your countr...` |
| GEN.13:1 | `ow Abram went up from Egypt to the South, he and h...` |
| GEN.13:15 | `for all the land you see I give to you and your se...` |
| GEN.14:1 | `ow it came to pass in the reign of Amraphel king o...` |
| GEN.14:6 | `and the Horites in the mountains of Seir, as far a...` |
| GEN.14:20 | `and blessed be God Most High, who delivered your e...` |
| GEN.15:1 | `fter these things the Word of the Lord came to Abr...` |
| GEN.16:1 | `ow Sarai, Abram's wife, bore him no children, but ...` |
| GEN.17:1 | `hen Abram was ninety-nine years old, the Lord appe...` |
| GEN.17:11 | `and you shall be circumcised in the flesh of your ...` |
| GEN.18:1 | `hen God appeared to him at the oak of Mamre, as he...` |
| GEN.18:3 | `and said, 'O Lord, if I have now found grace in Yo...` |
| GEN.19:1 | `ow the two angels came to Sodom in the evening, an...` |
| GEN.19:7 | `and said, 'By no means, my brethren, do not act wi...` |
| GEN.20:1 | `ow Abraham journeyed from there to the South, and ...` |
| GEN.20:18 | `for the Lord closed up all the wombs of the house ...` |
| GEN.21:1 | `ow the Lord visited Sarah as He said, and the Lord...` |
| GEN.22:1 | `ow it came to pass after these things that God tes...` |
| GEN.22:16 | `and said, 'By Myself I have sworn, says the Lord, ...` |
| GEN.23:1 | `ow Sarah lived one hundred and twenty-seven years....` |
| GEN.23:13 | `and he spoke to Ephron in the hearing of the peopl...` |
| GEN.24:1 | `ow Abraham was old, well advanced in age; and the ...` |
| GEN.24:3 | `and I will make you swear by the Lord, the God of ...` |
| GEN.24:4 | `but you shall go to my land where I was born, and ...` |
| GEN.24:23 | `and said, 'Whose daughter are you? Tell me, is the...` |
| GEN.24:38 | `but you shall go to my father's house and to my tr...` |
| GEN.24:44 | `and she says to me, 'Drink, and I will draw for yo...` |
| GEN.24:65 | `for she had said to the servant, 'Who is that man ...` |
| GEN.25:1 | `ow Abraham again took a wife, and her name was Ket...` |
| GEN.26:1 | `ow there was a famine in the land, besides the fir...` |
| GEN.26:5 | `because Abraham your father obeyed My voice and ke...` |
| GEN.26:14 | `for he had herds of sheep and oxen and many fields...` |
| GEN.27:1 | `ow it came to pass, when Isaac was old and his eye...` |
| GEN.27:45 | `and wrath turn away from you, and he forgets what ...` |
| GEN.28:1 | `ow Isaac called Jacob and blessed him, and charged...` |
| GEN.28:4 | `and give you the blessing of Abraham, to you and y...` |
| GEN.28:7 | `and Jacob had obeyed his father and mother and had...` |
| GEN.28:21 | `and bring me back in safety to my father's house, ...` |
| GEN.29:1 | `ow Jacob went on his journey and came to the land ...` |
| GEN.30:1 | `ow when Rachel saw that she bore Jacob no children...` |
| GEN.31:1 | `ow Jacob heard the words of Laban's sons, saying, ...` |
| GEN.31:49 | `and also The Vision, because he said, 'May God wat...` |
| GEN.32:1 | `oearly in the morning, Laban arose, and kissed his...` |
| GEN.32:20 | `and also say, 'Behold, your servant Jacob is comin...` |
| GEN.33:1 | `ow Jacob lifted his eyes and looked, and behold, E...` |
| GEN.34:1 | `ow Dinah the daughter of Leah, whom she bore to Ja...` |
| GEN.34:16 | `then we will give our daughters to you, and we wil...` |
| GEN.34:29 | `and took captive all their wives, their children, ...` |
| GEN.35:1 | `ow God said to Jacob, 'Arise, go up to Bethel and ...` |
| GEN.36:1 | `ow this is the genealogy of Esau, who is Edom....` |
| GEN.36:3 | `and Basemath, Ishmael's daughter, sister of Nebajo...` |
| GEN.36:5 | `and Aholibamah bore Jeush, Jaalam, and Korah. Thes...` |
| GEN.37:1 | `ow Jacob dwelt in the land where his father had so...` |
| GEN.38:1 | `tcame to pass at that time that Judah departed fro...` |
| GEN.39:1 | `ow Joseph had been taken down to Egypt, and Potiph...` |
| GEN.39:18 | `so it happened, as I lifted my voice and cried out...` |
| GEN.40:1 | `ow it came to pass after these things, that the ki...` |
| GEN.40:10 | `and in the vine were three branches; it was as tho...` |
| GEN.41:1 | `hen it came to pass, at the end of two full years,...` |
| GEN.41:30 | `but after them seven years of famine will arise, a...` |
| GEN.41:54 | `and the seven years of famine began to come, as Jo...` |
| GEN.42:1 | `hen Jacob found out there was grain for sale in Eg...` |
| GEN.43:1 | `ow the famine was severe in the land....` |
| GEN.44:1 | `ow Joseph commanded the steward of his house, sayi...` |
| GEN.45:1 | `ow Joseph could not restrain himself before all th...` |
| GEN.46:1 | `ow Israel took his journey with all he had, and ca...` |
| GEN.47:1 | `ow Joseph went and told Pharaoh, and said, 'My fat...` |
| GEN.47:30 | `but let me lie with my fathers; you shall carry me...` |
| GEN.48:1 | `ow it came to pass after these things that Joseph ...` |
| GEN.48:4 | `and said to me, 'Behold, I will increase and multi...` |
| GEN.49:1 | `ow Jacob called his sons and said, 'Gather togethe...` |
| GEN.50:1 | `ow Joseph fell on his father's face and wept over ...` |

## Brenton-Assisted Repairs (R7)

Auto-applied: 1  |  Ambiguous (not applied): 31

### Auto-Applied Splits

| Anchor | Fused | Repair | Score Δ |
|--------|-------|--------|--------|
| GEN.21:14 | `askin` | `a skin` | +0.0298 |

### Ambiguous — Not Applied (score did not improve)

| Anchor | Fused | Repair | Score Δ |
|--------|-------|--------|--------|
| GEN.8:7 | `araven` | `a raven` | +0.0067 |
| GEN.8:8 | `adove` | `a dove` | +0.0077 |
| GEN.11:2 | `aplain` | `a plain` | +0.0049 |
| GEN.15:17 | `asmoking` | `a smoking` | -0.0025 |
| GEN.19:14 | `inlaw` | `in law` | -0.0008 |
| GEN.19:28 | `afurnace` | `a furnace` | +0.0038 |
| GEN.19:30 | `acave` | `a cave` | +0.0040 |
| GEN.20:7 | `aprophet` | `a prophet` | +0.0038 |
| GEN.21:16 | `adistance` | `a distance` | +0.0033 |
| GEN.21:26 | `today` | `to day` | -0.0025 |
| GEN.22:13 | `aram` | `a ram` | -0.0004 |
| GEN.23:6 | `aking` | `a king` | +0.0000 |
| GEN.26:8 | `along` | `a long` | +0.0042 |
| GEN.27:11 | `asmooth` | `a smooth` | -0.0043 |
| GEN.27:12 | `acurse` | `a curse` | +0.0050 |
| GEN.28:12 | `aladder` | `a ladder` | +0.0041 |
| GEN.30:15 | `tonight` | `to night` | -0.0018 |
| GEN.30:17 | `afifth` | `a fifth` | +0.0080 |
| GEN.30:19 | `asixth` | `a sixth` | +0.0105 |
| GEN.30:32 | `today` | `to day` | -0.0014 |
| GEN.30:40 | `aspeckled` | `a speckled` | +0.0133 |
| GEN.31:43 | `today` | `to day` | -0.0004 |
| GEN.31:46 | `aheap` | `a heap` | +0.0008 |
| GEN.31:46 | `today` | `to day` | +0.0008 |
| GEN.33:18 | `aposition` | `a position` | +0.0035 |
| GEN.33:19 | `ahundred` | `a hundred` | +0.0055 |
| GEN.37:31 | `akid` | `a kid` | +0.0069 |
| GEN.38:28 | `ascarlet` | `a scarlet` | +0.0038 |
| GEN.40:7 | `today` | `to day` | -0.0026 |
| GEN.42:13 | `today` | `to day` | -0.0023 |
| GEN.44:33 | `aservant` | `a servant` | +0.0134 |
