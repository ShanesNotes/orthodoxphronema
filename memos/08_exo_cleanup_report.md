# Exodus Cleanup Report — 2026-03-08

## Summary
- Input: `staging/validated/OT/EXO.md`
- Mode: **in-place**
- Brenton reference: enabled (R7)
- Lines changed: 0

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 0 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 121 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| EXO.1:10 | `come, let us outwit them, lest they multiply, and ...` |
| EXO.1:16 | `and he said, 'When you do the duties of a midwife ...` |
| EXO.2:1 | `ow a man of the house of Levi went and took as wif...` |
| EXO.3:17 | `and I will bring you up out of the affliction of E...` |
| EXO.4:1 | `hen Moses answered and said, 'But suppose they wil...` |
| EXO.5:1 | `ow after this Moses and Aaron went and spoke to Ph...` |
| EXO.6:1 | `hen the Lord said to Moses, 'Now you shall see wha...` |
| EXO.6:29 | `the Lord said to him, 'I am the Lord. Speak to Pha...` |
| EXO.7:1 | `ow the Lord said to Moses, 'See, I have made you a...` |
| EXO.8:1 | `gain the Lord spoke to Moses, 'Say to Aaron your b...` |
| EXO.9:3 | `behold, the hand of the Lord will be on your cattl...` |
| EXO.9:9 | `and let it become dust in all the land of Egypt, a...` |
| EXO.9:14 | `for at this time I will send all My plagues into y...` |
| EXO.9:25 | `throughout the whole land of Egypt it struck both ...` |
| EXO.10:1 | `ow the Lord said to Moses, 'Go in to Pharaoh; for ...` |
| EXO.10:2 | `and that you may tell in the hearing of your child...` |
| EXO.10:14 | `and the locusts went up over all the land of Egypt...` |
| EXO.11:5 | `and all the firstborn in the land of Egypt shall d...` |
| EXO.12:27 | `that you shall say, 'This is the Paschal sacrifice...` |
| EXO.13:12 | `that you shall set apart to the Lord all that open...` |
| EXO.15:26 | `and said, 'If you diligently heed the voice of the...` |
| EXO.16:1 | `ow they journeyed from Elim, and all the congregat...` |
| EXO.17:16 | `for with a secret hand the Lord wars with Amalek f...` |
| EXO.18:3 | `with her two sons, of whom the name of one was Ger...` |
| EXO.18:4 | `and the name of the other was Eliezer (for he said...` |
| EXO.18:5 | `and Jethro, Moses' father-in-law, came with his so...` |
| EXO.19:1 | `ow in the third month after the children of Israel...` |
| EXO.20:6 | `but showing mercy to thousands, to those who love ...` |
| EXO.20:10 | `but the seventh day is the Sabbath of the Lord you...` |
| EXO.21:6 | `then his lord shall bring him to the judgment seat...` |
| EXO.21:19 | `if the man rises again and walks about outside wit...` |
| EXO.21:24 | `eye for eye, tooth for tooth, hand for hand, foot ...` |
| EXO.21:25 | `burn for burn, wound for wound, stripe for stripe....` |
| EXO.21:34 | `the owner of the pit shall make it good; he shall ...` |
| EXO.22:10 | `then an oath of God shall be between them both, th...` |
| EXO.22:23 | `and My wrath will become hot, and I will kill you ...` |
| EXO.23:11 | `but in the seventh year you shall let it rest and ...` |
| EXO.23:16 | `and the Feast of Harvest, the first fruits of your...` |
| EXO.24:1 | `ow He said to Moses, 'Come up to the Lord, you and...` |
| EXO.24:10 | `and they saw the place where the God of Israel sto...` |
| EXO.25:4 | `blue, purple, and scarlet cloth, fine spun linen; ...` |
| EXO.25:5 | `ram skins dyed red and skins dyed blue, and incorr...` |
| EXO.25:6 | `oil for the light, and incense for anointing oil a...` |
| EXO.25:7 | `sardius stones, and stones for the carved work of ...` |
| EXO.25:25 | `and you shall make a twisted wreath of gold for th...` |
| EXO.25:30 | `and you shall set the bread on the table before Me...` |
| EXO.26:21 | `and their forty bases of silver: two bases for eac...` |
| EXO.26:27 | `five bars for the posts on the other side of the t...` |
| EXO.27:21 | `in the tabernacle of testimony, outside the veil b...` |
| EXO.28:6 | `and they shall make the ephod of fine spun linen, ...` |
| EXO.28:10 | `six of their names on one stone, and six names on ...` |
| EXO.28:14 | `and you shall make two fringes of pure gold interm...` |
| EXO.28:19 | `the third row, ajacinth, an agate, and an amethyst...` |
| EXO.28:20 | `and the fourth row, a chrysolite, a beryl, and an ...` |
| EXO.29:2 | `and unleavened loaves kneaded with oil, and unleav...` |
| EXO.29:16 | `and you shall kill the ram and take its blood and ...` |
| EXO.29:23 | `and one loaf of bread, one unleavened cake from th...` |
| EXO.29:24 | `and you shall put all these things in the hands of...` |
| EXO.30:19 | `for Aaron and his sons shall wash their hands and ...` |
| EXO.30:24 | `and five hundred shekels of cassia, according to t...` |
| EXO.30:27 | `and the table and all its utensils, the lampstand ...` |
| EXO.30:28 | `and the altar of whole burnt offerings with all it...` |
| EXO.31:4 | `to design artistic works, to work in gold, silver,...` |
| EXO.31:5 | `in cutting jewels for setting, in carving wood, an...` |
| EXO.31:7 | `the tabernacle of testimony, the ark of the testim...` |
| EXO.31:8 | `the altars and the table and its utensils, the pur...` |
| EXO.31:9 | `and the laver and its base-...` |
| EXO.31:10 | `the liturgical garments for Aaron and the garments...` |
| EXO.31:11 | `and the anointing oil and the compound incense for...` |
| EXO.32:1 | `ow when the people saw that Moses delayed coming d...` |
| EXO.34:7 | `preserving righteousness and showing mercy unto th...` |
| EXO.34:15 | `lest you make a covenant with the foreigners of th...` |
| EXO.34:16 | `and you take of their daughters for your sons and ...` |
| EXO.35:6 | `blue, purple, and scarlet fabric, fine linen, and ...` |
| EXO.35:7 | `ram skins dyed red, skins dyed blue, and incorrupt...` |
| EXO.35:8 | `sardius stones and stones to be set in the ephod a...` |
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
| EXO.36:18 | `and the second row, a carbuncle, a sapphire, and a...` |
| EXO.36:19 | `and the third row, ajacinth, an agate, and an amet...` |
| EXO.36:20 | `and the fourth row, a chrysolite, a beryl, and an ...` |
| EXO.36:37 | `and their sashes of fine woven linen, blue, purple...` |
| EXO.37:6 | `and they made its five posts with their rings, and...` |
| EXO.37:12 | `with one curtain on one side of the court entrance...` |
| EXO.37:13 | `and one on the other side of the court entrance of...` |
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
| EXO.40:23 | `and he placed its lamps before the Lord, as the Lo...` |
| EXO.40:25 | `and he burned the incense compound on it, as the L...` |

## Brenton-Assisted Repairs (R7)

Auto-applied: 0  |  Ambiguous (not applied): 10


### Ambiguous — Not Applied (score did not improve)

| Anchor | Fused | Repair | Score Δ |
|--------|-------|--------|--------|
| EXO.2:18 | `today` | `to day` | -0.0041 |
| EXO.5:14 | `today` | `to day` | +0.0000 |
| EXO.8:25 | `tomorrow` | `to morrow` | -0.0001 |
| EXO.9:18 | `tomorrow` | `to morrow` | -0.0025 |
| EXO.10:4 | `tomorrow` | `to morrow` | -0.0026 |
| EXO.14:13 | `today` | `to day` | -0.0017 |
| EXO.16:25 | `today` | `to day` | -0.0019 |
| EXO.17:9 | `tomorrow` | `to morrow` | +0.0000 |
| EXO.19:10 | `today` | `to day` | -0.0066 |
| EXO.19:10 | `tomorrow` | `to morrow` | -0.0066 |
