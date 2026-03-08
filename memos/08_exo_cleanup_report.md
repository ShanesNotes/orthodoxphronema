# Exodus Cleanup Report — 2026-03-07

## Summary
- Input: `staging/validated/OT/EXO.md`
- Mode: **in-place**
- Brenton reference: enabled (R7)
- Lines changed: 12

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 0 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 128 |
| R7 | Brenton-assisted fused compound splits | 19 |

## Before/After Examples (first 20 + last 20 changed lines)

L214:
  - `EXO.7:9 'When Pharaoh speaks to you, saying, 'Show us asign or awonder,' then you shall say to Aaron your brother, 'Take your rod and cast it on the ground before Pharaoh, and it shall become aserpent.' '`
  + `EXO.7:9 'When Pharaoh speaks to you, saying, 'Show us a sign or a wonder,' then you shall say to Aaron your brother, 'Take your rod and cast it on the ground before Pharaoh, and it shall become a serpent.' '`

L247:
  - `EXO.8:5 Moses replied to Pharaoh, 'Appoint me atime when I shall pray for you, for your servants, and for your people to make the frogs disappear from you, your people, and your houses. Only in the river will they remain.'`
  + `EXO.8:5 Moses replied to Pharaoh, 'Appoint me a time when I shall pray for you, for your servants, and for your people to make the frogs disappear from you, your people, and your houses. Only in the river will they remain.'`

L381:
  - `EXO.12:3 Speak to all the congregation of the children of Israel, saying, 'On the tenth day of this month every man shall take for himself alamb, according to the family households, alamb for each home.`
  + `EXO.12:3 Speak to all the congregation of the children of Israel, saying, 'On the tenth day of this month every man shall take for himself a lamb, according to the family households, a lamb for each home.`

L388:
  - `EXO.12:10 You shall let none of it remain until morning, nor shall you break abone of it; and what remains of it until morning you shall burn with fire.`
  + `EXO.12:10 You shall let none of it remain until morning, nor shall you break a bone of it; and what remains of it until morning you shall burn with fire.`

L663:
  - `EXO.19:16 So it was that on the third day in the morning, there were thunderings and lightnings and adark cloud on Mount Sinai; and the sound of the trumpet was very loud, and all the people in the camp trembled.`
  + `EXO.19:16 So it was that on the third day in the morning, there were thunderings and lightnings and a dark cloud on Mount Sinai; and the sound of the trumpet was very loud, and all the people in the camp trembled.`

L879:
  - `EXO.25:10 'Thus you shall make the ark of testimony from incorruptible wood; two and ahalf cubits shall be its length, acubit and ahalf its width, and acubit and ahalf its height.`
  + `EXO.25:10 'Thus you shall make the ark of testimony from incorruptible wood; two and a half cubits shall be its length, a cubit and a half its width, and a cubit and a half its height.`

L895:
  - `EXO.25:23 'You shall also make agolden table of pure gold; two cubits shall be its length, acubit its width, and acubit and ahalf its height.`
  + `EXO.25:23 'You shall also make a golden table of pure gold; two cubits shall be its length, a cubit its width, and a cubit and a half its height.`

L933:
  - `EXO.26:13 A cubit on one side and acubit on the other side of the remaining length of the tent's curtains shall hang over the sides of the tabernacle, on this side and on that side, to cover it.`
  + `EXO.26:13 A cubit on one side and a cubit on the other side of the remaining length of the tent's curtains shall hang over the sides of the tabernacle, on this side and on that side, to cover it.`

L1015:
  - `EXO.28:18 The second row shall be acarbuncle, asapphire, and ajasper;`
  + `EXO.28:18 The second row shall be a carbuncle, a sapphire, and a jasper;`

L1068:
  - `EXO.29:28 It shall be for Aaron and his sons an ordinance forever among the children of Israel. For it shall be aspecial offering from the children of Israel from their peace offerings, aspecial offering to the Lord.`
  + `EXO.29:28 It shall be for Aaron and his sons an ordinance forever among the children of Israel. For it shall be a special offering from the children of Israel from their peace offerings, a special offering to the Lord.`

L1220:
  - `EXO.33:5 For the Lord said to the children of Israel, 'You are astiff-necked people. Beware, lest I inflict another plague on you and consume you. Now therefore, take off your bright clothes and ornaments, and I will show you what I will do.'`
  + `EXO.33:5 For the Lord said to the children of Israel, 'You are a stiff-necked people. Beware, lest I inflict another plague on you and consume you. Now therefore, take off your bright clothes and ornaments, and I will show you what I will do.'`

L1353:
  - `EXO.36:16 They made the oracle square by doubling it; aspan was its length and aspan its width when doubled.`
  + `EXO.36:16 They made the oracle square by doubling it; a span was its length and a span its width when doubled.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| EXO.1:1 | `ow these are the names of the children of Israel w...` |
| EXO.1:10 | `come, let us outwit them, lest they multiply, and ...` |
| EXO.1:16 | `and he said, 'When you do the duties of amidwife f...` |
| EXO.2:1 | `ow aman of the house of Levi went and took as wife...` |
| EXO.3:1 | `ow Moses was tending the sheep of Jethro his fathe...` |
| EXO.3:17 | `and I will bring you up out of the affliction of E...` |
| EXO.4:1 | `hen Moses answered and said, 'But suppose they wil...` |
| EXO.5:1 | `ow after this Moses and Aaron went and spoke to Ph...` |
| EXO.6:1 | `hen the Lord said to Moses, 'Now you shall see wha...` |
| EXO.6:29 | `the Lord said to him, 'I am the Lord. Speak to Pha...` |
| EXO.7:1 | `ow the Lord said to Moses, 'See, I have made you a...` |
| EXO.8:1 | `gain the Lord spoke to Moses, 'Say to Aaron your b...` |
| EXO.9:1 | `ow the Lord said to Moses, 'Go to Pharaoh and you ...` |
| EXO.9:3 | `behold, the hand of the Lord will be on your cattl...` |
| EXO.9:9 | `and let it become dust in all the land of Egypt, a...` |
| EXO.9:14 | `for at this time I will send all My plagues into y...` |
| EXO.9:25 | `throughout the whole land of Egypt it struck both ...` |
| EXO.10:1 | `ow the Lord said to Moses, 'Go in to Pharaoh; for ...` |
| EXO.10:14 | `and the locusts went up over all the land of Egypt...` |
| EXO.11:1 | `ow the Lord said to Moses, 'I will bring yet one m...` |
| EXO.11:5 | `and all the firstborn in the land of Egypt shall d...` |
| EXO.12:1 | `ow the Lord spoke to Moses and Aaron in the land o...` |
| EXO.12:27 | `that you shall say, 'This is the Paschal sacrifice...` |
| EXO.13:1 | `ow the Lord spoke to Moses, saying,...` |
| EXO.13:12 | `that you shall set apart to the Lord all that open...` |
| EXO.14:1 | `ow the Lord spoke to Moses, saying,...` |
| EXO.15:1 | `ow Moses and the children of Israel sang this song...` |
| EXO.15:26 | `and said, 'If you diligently heed the voice of the...` |
| EXO.16:1 | `ow they journeyed from Elim, and all the congregat...` |
| EXO.17:1 | `ow all the congregation of the children of Israel ...` |
| EXO.17:16 | `for with asecret hand the Lord wars with Amalek fr...` |
| EXO.18:1 | `ow Jethro the priest of Midian, Moses' father-in-l...` |
| EXO.18:3 | `with her two sons, of whom the name of one was Ger...` |
| EXO.18:4 | `and the name of the other was Eliezer (for he said...` |
| EXO.18:5 | `and Jethro, Moses' father-in-law, came with his so...` |
| EXO.19:1 | `ow in the third month after the children of Israel...` |
| EXO.20:1 | `ow the Lord spoke all these words, saying:...` |
| EXO.20:6 | `but showing mercy to thousands, to those who love ...` |
| EXO.20:10 | `but the seventh day is the Sabbath of the Lord you...` |
| EXO.21:6 | `then his lord shall bring him to the judgment seat...` |
| EXO.21:34 | `the owner of the pit shall make it good; he shall ...` |
| EXO.22:10 | `then an oath of God shall be between them both, th...` |
| EXO.22:23 | `and My wrath will become hot, and I will kill you ...` |
| EXO.23:11 | `but in the seventh year you shall let it rest and ...` |
| EXO.23:16 | `and the Feast of Harvest, the first fruits of your...` |
| EXO.24:1 | `ow He said to Moses, 'Come up to the Lord, you and...` |
| EXO.24:10 | `and they saw the place where the God of Israel sto...` |
| EXO.25:1 | `ow the Lord spoke to Moses, saying,...` |
| EXO.25:25 | `and you shall make atwisted wreath of gold for the...` |
| EXO.25:30 | `and you shall set the bread on the table before Me...` |
| EXO.26:21 | `and their forty bases of silver: two bases for eac...` |
| EXO.26:27 | `five bars for the posts on the other side of the t...` |
| EXO.27:21 | `in the tabernacle of testimony, outside the veil b...` |
| EXO.28:6 | `and they shall make the ephod of fine spun linen, ...` |
| EXO.28:10 | `six of their names on one stone, and six names on ...` |
| EXO.28:14 | `and you shall make two fringes of pure gold interm...` |
| EXO.28:19 | `the third row, ajacinth, an agate, and an amethyst...` |
| EXO.28:20 | `and the fourth row, achrysolite, aberyl, and an on...` |
| EXO.29:2 | `and unleavened loaves kneaded with oil, and unleav...` |
| EXO.29:16 | `and you shall kill the ram and take its blood and ...` |
| EXO.29:23 | `and one loaf of bread, one unleavened cake from th...` |
| EXO.29:24 | `and you shall put all these things in the hands of...` |
| EXO.30:19 | `for Aaron and his sons shall wash their hands and ...` |
| EXO.30:24 | `and five hundred shekels of cassia, according to t...` |
| EXO.30:27 | `and the table and all its utensils, the lampstand ...` |
| EXO.30:28 | `and the altar of whole burnt offerings with all it...` |
| EXO.31:1 | `ow the Lord spoke to Moses, saying,...` |
| EXO.31:4 | `to design artistic works, to work in gold, silver,...` |
| EXO.31:5 | `in cutting jewels for setting, in carving wood, an...` |
| EXO.31:7 | `the tabernacle of testimony, the ark of the testim...` |
| EXO.31:8 | `the altars and the table and its utensils, the pur...` |
| EXO.31:9 | `and the laver and its base-...` |
| EXO.31:10 | `the liturgical garments for Aaron and the garments...` |
| EXO.31:11 | `and the anointing oil and the compound incense for...` |
| EXO.32:1 | `ow when the people saw that Moses delayed coming d...` |
| EXO.33:1 | `ow the Lord said to Moses, 'Depart, go up from her...` |
| EXO.34:1 | `ow the Lord said to Moses, 'Cut two tablets of sto...` |
| EXO.34:15 | `lest you make acovenant with the foreigners of the...` |
| EXO.34:16 | `and you take of their daughters for your sons and ...` |
| EXO.35:1 | `ow Moses gathered all the congregation of the chil...` |
| EXO.35:10 | `the tabernacle, its cords, coverings, rings, bars,...` |
| EXO.35:11 | `the ark of the testimony, its poles, mercy seat, a...` |
| EXO.35:12 | `and the curtains of the court and its posts;...` |
| EXO.35:13 | `and the emerald stones;...` |
| EXO.35:14 | `and the incense and the anointing oil;...` |
| EXO.35:15 | `and the table and all its utensils;...` |
| EXO.35:16 | `and the illuminating lampstand and all its utensil...` |
| EXO.35:17 | `and the altar and all its utensils;...` |
| EXO.35:18 | `and the holy vestments of Aaron the priest and the...` |
| EXO.35:19 | `and the priestly robes for the sons of Aaron and t...` |
| EXO.35:28 | `and the compounds for the anointing oil, and the c...` |
| EXO.35:31 | `and He has filled him with adivine Spirit of wisdo...` |
| EXO.35:32 | `to design artistic works, to work in gold and silv...` |
| EXO.35:33 | `in cutting jewels for setting, in carving wood, an...` |
| EXO.36:1 | `ow Bezalel and Aholiab, and every gifted artisan i...` |
| EXO.36:5 | `and they spoke to Moses, saying, 'The people bring...` |
| EXO.36:7 | `for the material was sufficient for all the work t...` |
| EXO.36:18 | `and the second row, acarbuncle, asapphire, and aja...` |
| EXO.36:19 | `and the third row, ajacinth, an agate, and an amet...` |
| EXO.36:20 | `and the fourth row, achrysolite, aberyl, and an on...` |
| EXO.36:37 | `and their sashes of fine woven linen, blue, purple...` |
| EXO.37:1 | `ow they made ten curtains for the tabernacle....` |
| EXO.37:6 | `and they made its five posts with their rings, and...` |
| EXO.37:12 | `with one curtain on one side of the court entrance...` |
| EXO.37:13 | `and one on the other side of the court entrance of...` |
| EXO.38:1 | `ow Bezalel made the ark....` |
| EXO.38:4 | `wide enough for the poles with which to carry it....` |
| EXO.38:6 | `and two cherubim of pure gold...` |
| EXO.38:8 | `spreading out their wings above the mercy seat....` |
| EXO.38:10 | `and cast for it four rings (two on one side and tw...` |
| EXO.38:14 | `both its solid stem and the branches on each side ...` |
| EXO.38:15 | `and the blossoms projecting from its branches, thr...` |
| EXO.39:1 | `ow all the gold used in all the production of the ...` |
| EXO.39:3 | `for everyone surveyed in the tally from twenty yea...` |
| EXO.39:7 | `and with it they made the bases for the doors of t...` |
| EXO.39:8 | `the bases for the court all around, the bases for ...` |
| EXO.39:9 | `the bronze appendage of the altar, all the vessels...` |
| EXO.39:14 | `the ark of the covenant and its poles,...` |
| EXO.39:15 | `the altar and all its vessels, the anointing oil, ...` |
| EXO.39:16 | `the pure lamp and its lamps (lamps for burning), t...` |
| EXO.39:17 | `the table of offertory and the bread set forth upo...` |
| EXO.39:18 | `the garments of the holy place, which belong to Aa...` |
| EXO.39:19 | `the curtains of the court and their posts, the vei...` |
| EXO.39:20 | `the rams' skins dyed red, the blue coverings and t...` |
| EXO.39:21 | `the pegs, and all the instruments for the work of ...` |
| EXO.40:1 | `ow the Lord spoke to Moses, saying,...` |
| EXO.40:23 | `and he placed its lamps before the Lord, as the Lo...` |
| EXO.40:25 | `and he burned the incense compound on it, as the L...` |

## Brenton-Assisted Repairs (R7)

Auto-applied: 19  |  Ambiguous (not applied): 173

### Auto-Applied Splits

| Anchor | Fused | Repair | Score Δ |
|--------|-------|--------|--------|
| EXO.7:9 | `asign` | `a sign` | +0.0356 |
| EXO.7:9 | `awonder` | `a wonder` | +0.0356 |
| EXO.7:9 | `aserpent` | `a serpent` | +0.0356 |
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
| EXO.28:18 | `asapphire` | `a sapphire` | +0.0292 |
| EXO.28:18 | `ajasper` | `a jasper` | +0.0292 |
| EXO.28:18 | `acarbuncle` | `a carbuncle` | +0.0292 |
| EXO.29:28 | `aspecial` | `a special` | +0.1226 |
| EXO.33:5 | `astiff` | `a stiff` | +0.029 |
| EXO.36:16 | `aspan` | `a span` | +0.0555 |

### Ambiguous — Not Applied (score did not improve)

| Anchor | Fused | Repair | Score Δ |
|--------|-------|--------|--------|
| EXO.1:9 | `agreat` | `a great` | +0.0047 |
| EXO.1:16 | `amale` | `a male` | +0.0074 |
| EXO.1:16 | `afemale` | `a female` | +0.0074 |
| EXO.2:4 | `adistance` | `a distance` | +0.0072 |
| EXO.2:7 | `anurse` | `a nurse` | +0.0049 |
| EXO.2:14 | `ajudge` | `a judge` | +0.0037 |
| EXO.2:18 | `today` | `to day` | -0.0041 |
| EXO.2:22 | `asojourner` | `a sojourner` | +0.0099 |
| EXO.2:22 | `ason` | `a son` | +0.0099 |
| EXO.3:8 | `aland` | `a land` | -0.0012 |
| EXO.3:8 | `agood` | `a good` | -0.0012 |
| EXO.3:17 | `aland` | `a land` | +0.0030 |
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
| EXO.9:3 | `avery` | `a very` | +0.0039 |
| EXO.9:18 | `tomorrow` | `to morrow` | -0.0025 |
| EXO.9:24 | `anation` | `a nation` | +0.0055 |
| EXO.10:4 | `tomorrow` | `to morrow` | -0.0026 |
| EXO.10:7 | `asnare` | `a snare` | +0.0038 |
| EXO.10:9 | `afeast` | `a feast` | +0.0043 |
| EXO.10:13 | `asouth` | `a south` | +0.0033 |
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
| EXO.12:30 | `agreat` | `a great` | +0.0061 |
| EXO.12:30 | `ahouse` | `a house` | +0.0061 |
| EXO.12:38 | `agreat` | `a great` | -0.0150 |
| EXO.13:5 | `aland` | `a land` | -0.0003 |
| EXO.13:6 | `afeast` | `a feast` | +0.0061 |
| EXO.13:9 | `astrong` | `a strong` | +0.0043 |
| EXO.13:9 | `amemorial` | `a memorial` | +0.0043 |
| EXO.13:9 | `asign` | `a sign` | +0.0043 |
| EXO.13:13 | `asheep` | `a sheep` | +0.0032 |
| EXO.13:14 | `astrong` | `a strong` | +0.0033 |
| EXO.13:16 | `astrong` | `a strong` | +0.0089 |
| EXO.13:16 | `asign` | `a sign` | +0.0089 |
| EXO.13:21 | `apillar` | `a pillar` | +0.0110 |
| EXO.14:8 | `ahigh` | `a high` | +0.0031 |
| EXO.14:13 | `today` | `to day` | -0.0017 |
| EXO.14:21 | `astrong` | `a strong` | +0.0032 |
| EXO.14:22 | `awall` | `a wall` | +0.0107 |
| EXO.14:29 | `awall` | `a wall` | -0.0029 |
| EXO.15:5 | `astone` | `a stone` | +0.0101 |
| EXO.15:25 | `atree` | `a tree` | +0.0032 |
| EXO.16:14 | `asmall` | `a small` | +0.0042 |
| EXO.16:23 | `aholy` | `a holy` | -0.0003 |
| EXO.16:25 | `today` | `to day` | -0.0019 |
| EXO.16:33 | `agolden` | `a golden` | +0.0040 |
| EXO.17:9 | `tomorrow` | `to morrow` | +0.0000 |
| EXO.17:12 | `astone` | `a stone` | +0.0034 |
| EXO.17:14 | `amemorial` | `a memorial` | +0.0065 |
| EXO.17:14 | `abook` | `a book` | +0.0065 |
| EXO.17:16 | `asecret` | `a secret` | +0.0084 |
| EXO.18:3 | `asojourner` | `a sojourner` | +0.0061 |
| EXO.18:16 | `adispute` | `a dispute` | +0.0048 |
| EXO.19:6 | `aroyal` | `a royal` | +0.0097 |
| EXO.19:6 | `aholy` | `a holy` | +0.0097 |
| EXO.19:10 | `today` | `to day` | -0.0066 |
| EXO.19:10 | `tomorrow` | `to morrow` | -0.0066 |
| EXO.19:13 | `ahand` | `a hand` | -0.0001 |
| EXO.19:18 | `afurnace` | `a furnace` | +0.0034 |
| EXO.20:5 | `ajealous` | `a jealous` | +0.0142 |
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
| EXO.21:33 | `apit` | `a pit` | +0.0136 |
| EXO.21:37 | `asheep` | `a sheep` | +0.0098 |
| EXO.22:5 | `afield` | `a field` | +0.0042 |
| EXO.22:8 | `asheep` | `a sheep` | -0.0001 |
| EXO.22:15 | `avirgin` | `a virgin` | +0.0053 |
| EXO.22:20 | `astranger` | `a stranger` | +0.0064 |
| EXO.22:25 | `apledge` | `a pledge` | +0.0062 |
| EXO.23:3 | `apoor` | `a poor` | +0.0132 |
| EXO.23:14 | `afeast` | `a feast` | +0.0120 |
| EXO.23:19 | `alamb` | `a lamb` | +0.0042 |
| EXO.23:22 | `aroyal` | `a royal` | -0.0001 |
| EXO.23:22 | `aholy` | `a holy` | -0.0001 |
| EXO.25:8 | `asanctuary` | `a sanctuary` | +0.0086 |
| EXO.25:17 | `ahalf` | `a half` | +0.0095 |
| EXO.25:17 | `acubit` | `a cubit` | +0.0095 |
| EXO.25:24 | `acrown` | `a crown` | +0.0055 |
| EXO.25:25 | `atwisted` | `a twisted` | +0.0092 |
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
| EXO.28:17 | `arow` | `a row` | +0.0127 |
| EXO.28:17 | `atopaz` | `a topaz` | +0.0127 |
| EXO.28:17 | `asardius` | `a sardius` | +0.0127 |
| EXO.28:20 | `aberyl` | `a beryl` | +0.0083 |
| EXO.28:20 | `achrysolite` | `a chrysolite` | +0.0083 |
| EXO.28:23 | `amemorial` | `a memorial` | -0.0030 |
| EXO.28:28 | `aflowering` | `a flowering` | -0.0001 |
| EXO.28:31 | `aplate` | `a plate` | +0.0059 |
| EXO.29:18 | `awhole` | `a whole` | +0.0079 |
| EXO.29:18 | `asweet` | `a sweet` | +0.0079 |
| EXO.29:24 | `aseparate` | `a separate` | -0.0028 |
| EXO.29:25 | `asweet` | `a sweet` | +0.0035 |
| EXO.29:40 | `ahin` | `a hin` | +0.0066 |
| EXO.29:40 | `adrink` | `a drink` | +0.0066 |
| EXO.30:2 | `acubit` | `a cubit` | +0.0081 |
| EXO.30:9 | `adrink` | `a drink` | +0.0081 |
| EXO.30:9 | `asacrifice` | `a sacrifice` | +0.0081 |
| EXO.30:12 | `aransom` | `a ransom` | -0.0001 |
| EXO.30:16 | `amemorial` | `a memorial` | -0.0001 |
| EXO.30:24 | `ahin` | `a hin` | +0.0073 |
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
| EXO.33:3 | `aland` | `a land` | +0.0081 |
| EXO.33:3 | `astiff` | `a stiff` | +0.0081 |
| EXO.33:11 | `ayoung` | `a young` | -0.0007 |
| EXO.33:21 | `aplace` | `a place` | +0.0076 |
| EXO.34:10 | `acovenant` | `a covenant` | -0.0002 |
| EXO.34:12 | `astumbling` | `a stumbling` | +0.0081 |
| EXO.34:12 | `acovenant` | `a covenant` | +0.0081 |
| EXO.34:14 | `ajealous` | `a jealous` | +0.0128 |
| EXO.34:15 | `acovenant` | `a covenant` | +0.0033 |
| EXO.34:20 | `aprice` | `a price` | -0.0003 |
| EXO.34:20 | `asheep` | `a sheep` | -0.0003 |
| EXO.34:26 | `alamb` | `a lamb` | +0.0046 |
| EXO.34:27 | `acovenant` | `a covenant` | +0.0041 |
| EXO.34:33 | `aveil` | `a veil` | +0.0094 |
| EXO.35:2 | `aholy` | `a holy` | +0.0044 |
| EXO.36:10 | `awoven` | `a woven` | -0.0019 |
| EXO.36:11 | `awork` | `a work` | +0.0058 |
| EXO.36:17 | `asardius` | `a sardius` | +0.0053 |
| EXO.36:18 | `acarbuncle` | `a carbuncle` | +0.0097 |
| EXO.36:20 | `achrysolite` | `a chrysolite` | +0.0055 |
| EXO.37:9 | `ahundred` | `a hundred` | +0.0096 |
