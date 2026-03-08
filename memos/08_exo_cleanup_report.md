# Exodus Cleanup Report — 2026-03-07

## Summary
- Input: `staging/validated/OT/EXO.md`
- Mode: **in-place**
- Brenton reference: enabled (R7)
- Lines changed: 88

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 80 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 32 |
| R7 | Brenton-assisted fused compound splits | 16 |

## Before/After Examples (first 20 + last 20 changed lines)

L44:
  - `EXO.2:3 But when she could no longer hide him, she took an ark of bulrushes, daubed it with asphalt, put the child in it, and laid it in the reeds by the river'sbank.`
  + `EXO.2:3 But when she could no longer hide him, she took an ark of bulrushes, daubed it with asphalt, put the child in it, and laid it in the reeds by the river's bank.`

L48:
  - `EXO.2:7 Then his sister said to Pharaoh'sdaughter, 'Shall I go and call anurse for you from the Hebrew women, that she may nurse the child for you?'`
  + `EXO.2:7 Then his sister said to Pharaoh's daughter, 'Shall I go and call anurse for you from the Hebrew women, that she may nurse the child for you?'`

L49:
  - `EXO.2:8 So Pharaoh'sdaughter said to her, 'Go.' Then the maiden went and called the child'smother.`
  + `EXO.2:8 So Pharaoh's daughter said to her, 'Go.' Then the maiden went and called the child's mother.`

L50:
  - `EXO.2:9 Pharaoh'sdaughter then said to her, 'Take this child and nurse him for me, and I will pay you.' So the woman took the child and nursed him.`
  + `EXO.2:9 Pharaoh's daughter then said to her, 'Take this child and nurse him for me, and I will pay you.' So the woman took the child and nursed him.`

L54:
  - `EXO.2:10 Now when the boy was grown, she brought him to Pharaoh'sdaughter, and he became her son; and she called his name Moses, saying, 'Because I drew him out of the water.'`
  + `EXO.2:10 Now when the boy was grown, she brought him to Pharaoh's daughter, and he became her son; and she called his name Moses, saying, 'Because I drew him out of the water.'`

L60:
  - `EXO.2:16 Now the priest of Midian had seven daughters, who fed the sheep of their father Jethro; and they came and drew water, and filled the troughs to water their father'sflock.`
  + `EXO.2:16 Now the priest of Midian had seven daughters, who fed the sheep of their father Jethro; and they came and drew water, and filled the troughs to water their father's flock.`

L110:
  - `EXO.4:11 So the Lord said to him, 'Who made man'smouth? And who made the mute, the deaf, the seeing, and the blind? Did not I, God?`
  + `EXO.4:11 So the Lord said to him, 'Who made man's mouth? And who made the mute, the deaf, the seeing, and the blind? Did not I, God?`

L124:
  - `EXO.4:25 Then Zipporah took asharp stone and cut off the foreskin of her son, and fell at His feet and said, 'The flow of blood from my son'scircumcision is stopped.'`
  + `EXO.4:25 Then Zipporah took asharp stone and cut off the foreskin of her son, and fell at His feet and said, 'The flow of blood from my son's circumcision is stopped.'`

L125:
  - `EXO.4:26 So He departed from him, because she said, 'The flow of blood from my son'scircumcision is stopped.'`
  + `EXO.4:26 So He departed from him, because she said, 'The flow of blood from my son's circumcision is stopped.'`

L149:
  - `EXO.5:14 Also the clerks from the race of the children of Israel, whom Pharaoh'staskmasters set over them, were beaten and questioned, 'Why have you not fulfilled your task in making bricks both yesterday and the day before, and also today?'`
  + `EXO.5:14 Also the clerks from the race of the children of Israel, whom Pharaoh's taskmasters set over them, were beaten and questioned, 'Why have you not fulfilled your task in making bricks both yesterday and the day before, and also today?'`

L150:
  - `EXO.5:15 Then the clerks of Israel'ssons entered and cried out to Pharaoh, saying, 'Why are you dealing thus with your servants?`
  + `EXO.5:15 Then the clerks of Israel's sons entered and cried out to Pharaoh, saying, 'Why are you dealing thus with your servants?`

L186:
  - `EXO.6:20 Now Amram took as his wife Jochebed, the daughter of his father'sbrother; and she bore him Aaron and Moses and Miriam their sister; and Amram lived one hundred and thirty-seven years.`
  + `EXO.6:20 Now Amram took as his wife Jochebed, the daughter of his father's brother; and she bore him Aaron and Moses and Miriam their sister; and Amram lived one hundred and thirty-seven years.`

L191:
  - `EXO.6:25 Eleazar, Aaron'sson, took as his wife one of the daughters of Putiel; and she bore him Phinehas. These are the heads of the families of the Levites according to their genealogy.`
  + `EXO.6:25 Eleazar, Aaron's son, took as his wife one of the daughters of Putiel; and she bore him Phinehas. These are the heads of the families of the Levites according to their genealogy.`

L203:
  - `EXO.7:3 I will harden Pharaoh'sheart and multiply My signs and My wonders in the land of Egypt.`
  + `EXO.7:3 I will harden Pharaoh's heart and multiply My signs and My wonders in the land of Egypt.`

L209:
  - `EXO.7:9 'When Pharaoh speaks to you, saying, 'Show us asign or awonder,' then you shall say to Aaron your brother, 'Take your rod and cast it on the ground before Pharaoh, and it shall become aserpent.' '`
  + `EXO.7:9 'When Pharaoh speaks to you, saying, 'Show us a sign or a wonder,' then you shall say to Aaron your brother, 'Take your rod and cast it on the ground before Pharaoh, and it shall become a serpent.' '`

L212:
  - `EXO.7:12 For each man threw down his rod, and they became serpents. But Aaron'srod swallowed up their rods.`
  + `EXO.7:12 For each man threw down his rod, and they became serpents. But Aaron's rod swallowed up their rods.`

L216:
  - `EXO.7:13 But Pharaoh'sheart was hardened, and he did not give heed to them as the Lord commanded.`
  + `EXO.7:13 But Pharaoh's heart was hardened, and he did not give heed to them as the Lord commanded.`

L217:
  - `EXO.7:14 So the Lord said to Moses, 'Pharaoh'sheart is hardened; he refuses to let the people go.`
  + `EXO.7:14 So the Lord said to Moses, 'Pharaoh's heart is hardened; he refuses to let the people go.`

L218:
  - `EXO.7:15 Go to Pharaoh early in the morning, when he goes to the water, and you shall stand by the river'sbank to meet him; and you shall take in your hand the rod that turned to aserpent.`
  + `EXO.7:15 Go to Pharaoh early in the morning, when he goes to the water, and you shall stand by the river's bank to meet him; and you shall take in your hand the rod that turned to aserpent.`

L225:
  - `EXO.7:22 Then the sorcerers of Egypt did the same with their sorceries; and Pharaoh'sheart was hardened, and he did not heed them, as the Lord said.`
  + `EXO.7:22 Then the sorcerers of Egypt did the same with their sorceries; and Pharaoh's heart was hardened, and he did not heed them, as the Lord said.`

L971:
  - `EXO.28:11 With the work of the stone-engraver'sart, the engraving of aseal, you shall engrave the two stones with the names of the sons of Israel.`
  + `EXO.28:11 With the work of the stone-engraver's art, the engraving of aseal, you shall engrave the two stones with the names of the sons of Israel.`

L985:
  - `EXO.28:25 You shall put the revelation and the truth on the oracle of judgment, which will be on the breast of Aaron when he enters the holy place in the Lord'spresence; and on his breast Aaron will discern the judgments for the children of Israel at all times.`
  + `EXO.28:25 You shall put the revelation and the truth on the oracle of judgment, which will be on the breast of Aaron when he enters the holy place in the Lord's presence; and on his breast Aaron will discern the judgments for the children of Israel at all times.`

L993:
  - `EXO.28:33 So it shall be on Aaron'sforehead. Aaron shall take away the defilements of the holy things which the children of Israel might dedicate, of their every gift of holy things. It shall always be on Aaron'sforehead to make them acceptable before the Lord.`
  + `EXO.28:33 So it shall be on Aaron's forehead. Aaron shall take away the defilements of the holy things which the children of Israel might dedicate, of their every gift of holy things. It shall always be on Aaron's forehead to make them acceptable before the Lord.`

L995:
  - `EXO.28:35 For Aaron'ssons you shall make robes and sashes for them, and turbans you shall make for them for honor and glory.`
  + `EXO.28:35 For Aaron's sons you shall make robes and sashes for them, and turbans you shall make for them for honor and glory.`

L1021:
  - `EXO.29:20 Then you shall kill the ram, and take some of its blood and put it on the tip of Aaron'sright earlobe, on the thumb of his right hand, on the big toe of his right foot, and on the earlobes of his sons, on the thumbs of their right hands, and on the big toes of their right feet.`
  + `EXO.29:20 Then you shall kill the ram, and take some of its blood and put it on the tip of Aaron's right earlobe, on the thumb of his right hand, on the big toe of his right foot, and on the earlobes of his sons, on the thumbs of their right hands, and on the big toes of their right feet.`

L1025:
  - `EXO.29:26 'Then you shall take the breast from the ram of Aaron'sconsecration and set it aside before the Lord. It shall be your portion.`
  + `EXO.29:26 'Then you shall take the breast from the ram of Aaron's consecration and set it aside before the Lord. It shall be your portion.`

L1026:
  - `EXO.29:27 You shall sanctify the reserved breast and the shoulder that was lifted (both that which was reserved and that which was lifted) from the ram of consecration, both Aaron'sportion and that of his sons.`
  + `EXO.29:27 You shall sanctify the reserved breast and the shoulder that was lifted (both that which was reserved and that which was lifted) from the ram of consecration, both Aaron's portion and that of his sons.`

L1027:
  - `EXO.29:28 It shall be for Aaron and his sons an ordinance forever among the children of Israel. For it shall be aspecial offering from the children of Israel from their peace offerings, aspecial offering to the Lord.`
  + `EXO.29:28 It shall be for Aaron and his sons an ordinance forever among the children of Israel. For it shall be a special offering from the children of Israel from their peace offerings, a special offering to the Lord.`

L1028:
  - `EXO.29:29 'Moreover, Aaron'sholy garment of the sanctuary shall be his sons' after him, to be anointed and consecrated in them.`
  + `EXO.29:29 'Moreover, Aaron's holy garment of the sanctuary shall be his sons' after him, to be anointed and consecrated in them.`

L1090:
  - `EXO.30:32 It shall not be poured on man'sflesh; nor shall you make any like it according to its composition. It is holy, and it shall be holy to you.`
  + `EXO.30:32 It shall not be poured on man's flesh; nor shall you make any like it according to its composition. It is holy, and it shall be holy to you.`

L1149:
  - `EXO.32:26 Moses then stood in the entrance of the camp and said, 'Whoever is on the Lord'sside, come to me.' So all the sons of Levi gathered themselves together to him.`
  + `EXO.32:26 Moses then stood in the entrance of the camp and said, 'Whoever is on the Lord's side, come to me.' So all the sons of Levi gathered themselves together to him.`

L1168:
  - `EXO.33:5 For the Lord said to the children of Israel, 'You are astiff-necked people. Beware, lest I inflict another plague on you and consume you. Now therefore, take off your bright clothes and ornaments, and I will show you what I will do.'`
  + `EXO.33:5 For the Lord said to the children of Israel, 'You are a stiff-necked people. Beware, lest I inflict another plague on you and consume you. Now therefore, take off your bright clothes and ornaments, and I will show you what I will do.'`

L1203:
  - `EXO.34:6 Then the Lord passed before his face and proclaimed, 'The Lord God, compassionate, merciful, longsuffering, abounding in mercy and true, 7 preserving righteousness and showing mercy unto thousands, taking away lawlessness, wrongdoing, and sins; and He will not clear the guilty, visiting the lawlessness of the fathers upon the children and the children'schildren to the third and the fourth generation.'`
  + `EXO.34:6 Then the Lord passed before his face and proclaimed, 'The Lord God, compassionate, merciful, longsuffering, abounding in mercy and true, 7 preserving righteousness and showing mercy unto thousands, taking away lawlessness, wrongdoing, and sins; and He will not clear the guilty, visiting the lawlessness of the fathers upon the children and the children's children to the third and the fourth generation.'`

L1218:
  - `EXO.34:22 You shall observe the Feast of Weeks, the firstfruits of wheat harvest, and the Feast of Ingathering at the year'send.`
  + `EXO.34:22 You shall observe the Feast of Weeks, the firstfruits of wheat harvest, and the Feast of Ingathering at the year's end.`

L1222:
  - `EXO.34:26 The first fruits of your land you shall bring to the house of the Lord your God. You shall not boil alamb in its mother'smilk.'`
  + `EXO.34:26 The first fruits of your land you shall bring to the house of the Lord your God. You shall not boil alamb in its mother's milk.'`

L1247:
  - `EXO.35:21 Then everyone came whose heart was stirred and whose soul was willing; and they brought the Lord'soffering for the work of the tabernacle of testimony, for all its service and the garments of the holy place.`
  + `EXO.35:21 Then everyone came whose heart was stirred and whose soul was willing; and they brought the Lord's offering for the work of the tabernacle of testimony, for all its service and the garments of the holy place.`

L1274:
  - `EXO.36:8 Then all the gifted artisans among them who worked on Aaron'sgarments for the holy places did as the Lord commanded Moses.`
  + `EXO.36:8 Then all the gifted artisans among them who worked on Aaron's garments for the holy places did as the Lord commanded Moses.`

L1282:
  - `EXO.36:16 They made the oracle square by doubling it; aspan was its length and aspan its width when doubled.`
  + `EXO.36:16 They made the oracle square by doubling it; a span was its length and a span its width when doubled.`

L1353:
  - `EXO.38:22 He made the altar of bronze from the censers used by the men engaged in Korah'srebellion.`
  + `EXO.38:22 He made the altar of bronze from the censers used by the men engaged in Korah's rebellion.`

L1420:
  - `EXO.40:28 Then the cloud covered the tabernacle of testimony, and the tabernacle was filled with the Lord'sglory.`
  + `EXO.40:28 Then the cloud covered the tabernacle of testimony, and the tabernacle was filled with the Lord's glory.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| EXO.1:1 | `ow these are the names of the children of Israel w...` |
| EXO.2:1 | `ow aman of the house of Levi went and took as wife...` |
| EXO.3:1 | `ow Moses was tending the sheep of Jethro his fathe...` |
| EXO.4:1 | `hen Moses answered and said, 'But suppose they wil...` |
| EXO.5:1 | `ow after this Moses and Aaron went and spoke to Ph...` |
| EXO.6:1 | `hen the Lord said to Moses, 'Now you shall see wha...` |
| EXO.7:1 | `ow the Lord said to Moses, 'See, I have made you a...` |
| EXO.8:1 | `gain the Lord spoke to Moses, 'Say to Aaron your b...` |
| EXO.9:1 | `ow the Lord said to Moses, 'Go to Pharaoh and you ...` |
| EXO.10:1 | `ow the Lord said to Moses, 'Go in to Pharaoh; for ...` |
| EXO.11:1 | `ow the Lord said to Moses, 'I will bring yet one m...` |
| EXO.12:1 | `ow the Lord spoke to Moses and Aaron in the land o...` |
| EXO.13:1 | `ow the Lord spoke to Moses, saying,...` |
| EXO.14:1 | `ow the Lord spoke to Moses, saying,...` |
| EXO.15:1 | `ow Moses and the children of Israel sang this song...` |
| EXO.16:1 | `ow they journeyed from Elim, and all the congregat...` |
| EXO.17:1 | `ow all the congregation of the children of Israel ...` |
| EXO.18:1 | `ow Jethro the priest of Midian, Moses' father-in-l...` |
| EXO.19:1 | `ow in the third month after the children of Israel...` |
| EXO.20:1 | `ow the Lord spoke all these words, saying:...` |
| EXO.24:1 | `ow He said to Moses, 'Come up to the Lord, you and...` |
| EXO.25:1 | `ow the Lord spoke to Moses, saying,...` |
| EXO.31:1 | `ow the Lord spoke to Moses, saying,...` |
| EXO.32:1 | `ow when the people saw that Moses delayed coming d...` |
| EXO.33:1 | `ow the Lord said to Moses, 'Depart, go up from her...` |
| EXO.34:1 | `ow the Lord said to Moses, 'Cut two tablets of sto...` |
| EXO.35:1 | `ow Moses gathered all the congregation of the chil...` |
| EXO.36:1 | `ow Bezalel and Aholiab, and every gifted artisan i...` |
| EXO.37:1 | `ow they made ten curtains for the tabernacle....` |
| EXO.38:1 | `ow Bezalel made the ark....` |
| EXO.39:1 | `ow all the gold used in all the production of the ...` |
| EXO.40:1 | `ow the Lord spoke to Moses, saying,...` |

## Brenton-Assisted Repairs (R7)

Auto-applied: 16  |  Ambiguous (not applied): 161

### Auto-Applied Splits

| Anchor | Fused | Repair | Score Δ |
|--------|-------|--------|--------|
| EXO.7:9 | `asign` | `a sign` | +0.0356 |
| EXO.7:9 | `aserpent` | `a serpent` | +0.0356 |
| EXO.7:9 | `awonder` | `a wonder` | +0.0356 |
| EXO.8:5 | `atime` | `a time` | +0.0567 |
| EXO.12:3 | `alamb` | `a lamb` | +0.042 |
| EXO.12:10 | `abone` | `a bone` | +0.0456 |
| EXO.19:16 | `adark` | `a dark` | +0.1113 |
| EXO.25:10 | `ahalf` | `a half` | +0.0538 |
| EXO.25:10 | `acubit` | `a cubit` | +0.0538 |
| EXO.25:23 | `agolden` | `a golden` | +0.1298 |
| EXO.25:23 | `ahalf` | `a half` | +0.1298 |
| EXO.25:23 | `acubit` | `a cubit` | +0.1298 |
| EXO.26:13 | `acubit` | `a cubit` | +0.0329 |
| EXO.29:28 | `aspecial` | `a special` | +0.1226 |
| EXO.33:5 | `astiff` | `a stiff` | +0.029 |
| EXO.36:16 | `aspan` | `a span` | +0.0555 |

### Ambiguous — Not Applied (score did not improve)

| Anchor | Fused | Repair | Score Δ |
|--------|-------|--------|--------|
| EXO.1:9 | `agreat` | `a great` | +0.0037 |
| EXO.2:4 | `adistance` | `a distance` | +0.0072 |
| EXO.2:7 | `anurse` | `a nurse` | +0.0049 |
| EXO.2:14 | `ajudge` | `a judge` | +0.0037 |
| EXO.2:18 | `today` | `to day` | -0.0041 |
| EXO.2:22 | `ason` | `a son` | +0.0099 |
| EXO.2:22 | `asojourner` | `a sojourner` | +0.0099 |
| EXO.3:8 | `aland` | `a land` | -0.0012 |
| EXO.3:8 | `agood` | `a good` | -0.0012 |
| EXO.3:19 | `amighty` | `a mighty` | +0.0071 |
| EXO.4:3 | `aserpent` | `a serpent` | +0.0048 |
| EXO.4:17 | `aserpent` | `a serpent` | +0.0065 |
| EXO.5:1 | `afeast` | `a feast` | +0.0038 |
| EXO.5:14 | `today` | `to day` | +0.0000 |
| EXO.5:21 | `asword` | `a sword` | +0.0035 |
| EXO.7:1 | `agod` | `a god` | +0.0051 |
| EXO.7:10 | `aserpent` | `a serpent` | +0.0029 |
| EXO.7:15 | `aserpent` | `a serpent` | +0.0033 |
| EXO.8:19 | `adifference` | `a difference` | +0.0058 |
| EXO.8:25 | `tomorrow` | `to morrow` | -0.0001 |
| EXO.9:18 | `tomorrow` | `to morrow` | -0.0025 |
| EXO.9:24 | `anation` | `a nation` | +0.0040 |
| EXO.10:4 | `tomorrow` | `to morrow` | -0.0026 |
| EXO.10:7 | `asnare` | `a snare` | +0.0038 |
| EXO.10:9 | `afeast` | `a feast` | +0.0043 |
| EXO.10:13 | `asouth` | `a south` | +0.0026 |
| EXO.10:19 | `astrong` | `a strong` | +0.0031 |
| EXO.10:26 | `ahoof` | `a hoof` | +0.0134 |
| EXO.11:6 | `agreat` | `a great` | +0.0051 |
| EXO.11:7 | `adog` | `a dog` | +0.0035 |
| EXO.12:4 | `ahousehold` | `a household` | +0.0043 |
| EXO.12:5 | `amale` | `a male` | +0.0063 |
| EXO.12:13 | `asign` | `a sign` | +0.0147 |
| EXO.12:14 | `amemorial` | `a memorial` | -0.0017 |
| EXO.12:14 | `afeast` | `a feast` | -0.0017 |
| EXO.12:16 | `aholy` | `a holy` | -0.0011 |
| EXO.12:21 | `alamb` | `a lamb` | -0.0024 |
| EXO.12:22 | `abunch` | `a bunch` | +0.0034 |
| EXO.12:30 | `ahouse` | `a house` | +0.0061 |
| EXO.12:30 | `agreat` | `a great` | +0.0061 |
| EXO.12:38 | `agreat` | `a great` | -0.0150 |
| EXO.13:5 | `aland` | `a land` | -0.0003 |
| EXO.13:6 | `afeast` | `a feast` | +0.0061 |
| EXO.13:9 | `amemorial` | `a memorial` | +0.0043 |
| EXO.13:9 | `asign` | `a sign` | +0.0043 |
| EXO.13:9 | `astrong` | `a strong` | +0.0043 |
| EXO.13:13 | `asheep` | `a sheep` | +0.0032 |
| EXO.13:14 | `astrong` | `a strong` | +0.0033 |
| EXO.13:16 | `asign` | `a sign` | +0.0089 |
| EXO.13:16 | `astrong` | `a strong` | +0.0089 |
| EXO.13:21 | `apillar` | `a pillar` | +0.0110 |
| EXO.14:8 | `ahigh` | `a high` | +0.0031 |
| EXO.14:13 | `today` | `to day` | -0.0017 |
| EXO.14:21 | `astrong` | `a strong` | +0.0032 |
| EXO.14:22 | `awall` | `a wall` | +0.0107 |
| EXO.14:29 | `awall` | `a wall` | -0.0029 |
| EXO.15:5 | `astone` | `a stone` | +0.0101 |
| EXO.15:25 | `atree` | `a tree` | +0.0024 |
| EXO.16:14 | `asmall` | `a small` | +0.0042 |
| EXO.16:23 | `aholy` | `a holy` | -0.0003 |
| EXO.16:25 | `today` | `to day` | -0.0019 |
| EXO.16:33 | `agolden` | `a golden` | +0.0040 |
| EXO.17:9 | `tomorrow` | `to morrow` | +0.0000 |
| EXO.17:12 | `astone` | `a stone` | +0.0034 |
| EXO.17:14 | `amemorial` | `a memorial` | +0.0065 |
| EXO.17:14 | `abook` | `a book` | +0.0065 |
| EXO.18:16 | `adispute` | `a dispute` | +0.0048 |
| EXO.19:6 | `aholy` | `a holy` | +0.0097 |
| EXO.19:6 | `aroyal` | `a royal` | +0.0097 |
| EXO.19:10 | `today` | `to day` | -0.0066 |
| EXO.19:10 | `tomorrow` | `to morrow` | -0.0066 |
| EXO.19:13 | `ahand` | `a hand` | -0.0001 |
| EXO.19:18 | `afurnace` | `a furnace` | +0.0034 |
| EXO.20:5 | `ajealous` | `a jealous` | +0.0119 |
| EXO.21:4 | `awife` | `a wife` | +0.0040 |
| EXO.21:7 | `adomestic` | `a domestic` | +0.0065 |
| EXO.21:8 | `aforeign` | `a foreign` | +0.0034 |
| EXO.21:13 | `aplace` | `a place` | +0.0046 |
| EXO.21:18 | `astone` | `a stone` | +0.0036 |
| EXO.21:20 | `aman` | `a man` | +0.0107 |
| EXO.21:20 | `arod` | `a rod` | +0.0107 |
| EXO.21:21 | `aday` | `a day` | +0.0065 |
| EXO.21:22 | `awoman` | `a woman` | -0.0001 |
| EXO.21:28 | `abull` | `a bull` | +0.0074 |
| EXO.21:28 | `aman` | `a man` | +0.0074 |
| EXO.21:29 | `aman` | `a man` | -0.0003 |
| EXO.21:31 | `ason` | `a son` | +0.0067 |
| EXO.21:33 | `apit` | `a pit` | +0.0100 |
| EXO.21:37 | `asheep` | `a sheep` | +0.0098 |
| EXO.22:5 | `afield` | `a field` | +0.0042 |
| EXO.22:8 | `asheep` | `a sheep` | -0.0001 |
| EXO.22:15 | `avirgin` | `a virgin` | +0.0053 |
| EXO.22:20 | `astranger` | `a stranger` | +0.0064 |
| EXO.22:25 | `apledge` | `a pledge` | +0.0062 |
| EXO.23:3 | `apoor` | `a poor` | +0.0132 |
| EXO.23:14 | `afeast` | `a feast` | +0.0120 |
| EXO.23:19 | `alamb` | `a lamb` | +0.0042 |
| EXO.23:22 | `aholy` | `a holy` | -0.0001 |
| EXO.23:22 | `aroyal` | `a royal` | -0.0001 |
| EXO.25:8 | `asanctuary` | `a sanctuary` | +0.0086 |
| EXO.25:17 | `acubit` | `a cubit` | +0.0095 |
| EXO.25:17 | `ahalf` | `a half` | +0.0095 |
| EXO.25:24 | `acrown` | `a crown` | +0.0046 |
| EXO.25:39 | `atalent` | `a talent` | -0.0049 |
| EXO.26:14 | `acovering` | `a covering` | +0.0059 |
| EXO.26:16 | `ahalf` | `a half` | +0.0170 |
| EXO.26:16 | `acubit` | `a cubit` | +0.0170 |
| EXO.26:31 | `aveil` | `a veil` | +0.0052 |
| EXO.26:36 | `ascreen` | `a screen` | +0.0045 |
| EXO.27:9 | `acourt` | `a court` | +0.0043 |
| EXO.27:16 | `aveil` | `a veil` | -0.0001 |
| EXO.28:4 | `afringe` | `a fringe` | -0.0006 |
| EXO.28:11 | `aseal` | `a seal` | +0.0039 |
| EXO.28:12 | `amemorial` | `a memorial` | -0.0001 |
| EXO.28:16 | `aspan` | `a span` | +0.0044 |
| EXO.28:17 | `atopaz` | `a topaz` | +0.0127 |
| EXO.28:17 | `asardius` | `a sardius` | +0.0127 |
| EXO.28:17 | `arow` | `a row` | +0.0127 |
| EXO.28:18 | `acarbuncle` | `a carbuncle` | +0.0160 |
| EXO.28:18 | `ajasper` | `a jasper` | +0.0160 |
| EXO.28:18 | `asapphire` | `a sapphire` | +0.0160 |
| EXO.28:23 | `amemorial` | `a memorial` | -0.0030 |
| EXO.28:28 | `aflowering` | `a flowering` | -0.0001 |
| EXO.28:31 | `aplate` | `a plate` | +0.0059 |
| EXO.29:18 | `awhole` | `a whole` | +0.0079 |
| EXO.29:18 | `asweet` | `a sweet` | +0.0079 |
| EXO.29:25 | `asweet` | `a sweet` | +0.0035 |
| EXO.29:40 | `ahin` | `a hin` | +0.0066 |
| EXO.29:40 | `adrink` | `a drink` | +0.0066 |
| EXO.30:2 | `acubit` | `a cubit` | +0.0081 |
| EXO.30:9 | `asacrifice` | `a sacrifice` | +0.0081 |
| EXO.30:9 | `adrink` | `a drink` | +0.0081 |
| EXO.30:12 | `aransom` | `a ransom` | -0.0001 |
| EXO.30:16 | `amemorial` | `a memorial` | -0.0001 |
| EXO.30:25 | `aholy` | `a holy` | +0.0088 |
| EXO.30:31 | `aholy` | `a holy` | +0.0045 |
| EXO.30:36 | `amost` | `a most` | +0.0031 |
| EXO.30:37 | `aholy` | `a holy` | +0.0046 |
| EXO.31:13 | `asign` | `a sign` | -0.0007 |
| EXO.31:15 | `aholy` | `a holy` | +0.0041 |
| EXO.32:4 | `amolten` | `a molten` | +0.0030 |
| EXO.32:5 | `afeast` | `a feast` | +0.0050 |
| EXO.32:8 | `acalf` | `a calf` | -0.0003 |
| EXO.32:30 | `agreat` | `a great` | +0.0055 |
| EXO.33:3 | `astiff` | `a stiff` | +0.0081 |
| EXO.33:3 | `aland` | `a land` | +0.0081 |
| EXO.33:11 | `ayoung` | `a young` | -0.0007 |
| EXO.33:21 | `aplace` | `a place` | +0.0076 |
| EXO.34:10 | `acovenant` | `a covenant` | -0.0002 |
| EXO.34:12 | `acovenant` | `a covenant` | +0.0081 |
| EXO.34:12 | `astumbling` | `a stumbling` | +0.0081 |
| EXO.34:20 | `asheep` | `a sheep` | -0.0003 |
| EXO.34:20 | `aprice` | `a price` | -0.0003 |
| EXO.34:26 | `alamb` | `a lamb` | +0.0046 |
| EXO.34:27 | `acovenant` | `a covenant` | +0.0041 |
| EXO.34:33 | `aveil` | `a veil` | +0.0094 |
| EXO.35:2 | `aholy` | `a holy` | +0.0044 |
| EXO.36:10 | `awoven` | `a woven` | -0.0019 |
| EXO.36:11 | `awork` | `a work` | +0.0058 |
| EXO.36:17 | `asardius` | `a sardius` | +0.0035 |
| EXO.37:9 | `ahundred` | `a hundred` | +0.0096 |
