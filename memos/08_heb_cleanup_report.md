# Hebrews Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/HEB.md`
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
| R6 | Drop-cap omissions detected (NO auto-fix) | 55 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L25:
  - `HEB.1:6 The power given at ordination is strong and effective. The power of Christ'spriesthood is perfect and draws us near to God. His sacrifice is offered once for all. The Father Himself ordains the Son.`
  + `HEB.1:6 The power given at ordination is strong and effective. The power of Christ's priesthood is perfect and draws us near to God. His sacrifice is offered once for all. The Father Himself ordains the Son.`

L222:
  - `HEB.9:4 which had the golden censer and the ark of the covenant overlaid on all sides with gold, in which were the golden pot that had the manna, Aaron'srod that budded, and the tablets of the covenant;`
  + `HEB.9:4 which had the golden censer and the ark of the covenant overlaid on all sides with gold, in which were the golden pot that had the manna, Aaron's rod that budded, and the tablets of the covenant;`

L225:
  - `HEB.9:7 But into the second part the high priest went alone once ayear, not without blood, which he offered for himself and for the people'ssins committed in ignorance;`
  + `HEB.9:7 But into the second part the high priest went alone once ayear, not without blood, which he offered for himself and for the people's sins committed in ignorance;`

L340:
  - `HEB.11:23 By faith Moses, when he was born, was hidden three months by his parents, because they saw he was abeautiful child; and they were not afraid of the king'scommand.`
  + `HEB.11:23 By faith Moses, when he was born, was hidden three months by his parents, because they saw he was abeautiful child; and they were not afraid of the king's command.`

L341:
  - `HEB.11:24 By faith Moses, when he became of age, refused to be called the son of Pharaoh'sdaughter, 25 choosing rather to suffer affliction with the people of God than to enjoy the passing pleasures of sin, 26 esteeming the reproach of Christ greater riches than the treasures in a Egypt; for he looked to the reward.`
  + `HEB.11:24 By faith Moses, when he became of age, refused to be called the son of Pharaoh's daughter, 25 choosing rather to suffer affliction with the people of God than to enjoy the passing pleasures of sin, 26 esteeming the reproach of Christ greater riches than the treasures in a Egypt; for he looked to the reward.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| HEB.2:1 | `herefore we must give the more earnest heed to the...` |
| HEB.2:3 | `how shall we escape if we neglect so great asalvat...` |
| HEB.2:12 | `saying: 'I will declare Your name to My brethren; ...` |
| HEB.2:15 | `and release those who through fear of death were a...` |
| HEB.3:1 | `herefore, holy brethren, partakers of the heavenly...` |
| HEB.3:2 | `who was faithful to Him who appointed Him, as Mose...` |
| HEB.3:6 | `but Christ as a Son over His own house, whose hous...` |
| HEB.3:13 | `but exhort one another daily, while it is called '...` |
| HEB.4:1 | `herefore, since apromise remains of entering His r...` |
| HEB.5:1 | `or every high priest taken from among men is appoi...` |
| HEB.5:11 | `of whom we have much to say, and hard to explain, ...` |
| HEB.6:1 | `herefore, leaving the discussion of the elementary...` |
| HEB.6:2 | `of the doctrine of baptisms, of laying on of hands...` |
| HEB.6:5 | `and have tasted the good word of God and the power...` |
| HEB.6:6 | `if they fall away, ato renew them again to repenta...` |
| HEB.6:8 | `but if it bears thorns and briers, it is rejected ...` |
| HEB.6:12 | `that you do not become sluggish, but imitate those...` |
| HEB.6:14 | `saying, 'Surely blessing I will bless you, and mul...` |
| HEB.6:18 | `that by two immutable things, in which it is impos...` |
| HEB.6:20 | `where the forerunner has entered for us, even Jesu...` |
| HEB.7:1 | `or this Melchizedek, king of Salem, priest of the ...` |
| HEB.7:2 | `to whom also Abraham gave atenth part of all, firs...` |
| HEB.7:6 | `but he whose genealogy is not derived from them re...` |
| HEB.7:10 | `for he was still in the loins of his father when M...` |
| HEB.7:16 | `who has come, not according to the law of afleshly...` |
| HEB.7:19 | `for the law made nothing perfect; on the other han...` |
| HEB.7:27 | `who does not need daily, as those high priests, to...` |
| HEB.8:1 | `ow this is the main point of the things we are say...` |
| HEB.8:5 | `who serve the copy and shadow of the heavenly thin...` |
| HEB.9:1 | `hen indeed, even the first covenant had ordinances...` |
| HEB.9:3 | `and behind the second veil, the part of the tabern...` |
| HEB.9:4 | `which had the golden censer and the ark of the cov...` |
| HEB.9:5 | `and above it were the cherubim of glory overshadow...` |
| HEB.9:8 | `the Holy Spirit indicating this, that the way into...` |
| HEB.9:14 | `how much more shall the blood of Christ, who throu...` |
| HEB.9:20 | `saying, 'This is the blood of the covenant which G...` |
| HEB.9:25 | `not that He should offer Himself often, as the hig...` |
| HEB.9:28 | `so Christ was offered once to bear the sins of man...` |
| HEB.10:1 | `or the law, having ashadow of the good things to c...` |
| HEB.10:9 | `then He said, 'Behold, I have come to do Your will...` |
| HEB.10:13 | `from that time waiting till His enemies are made H...` |
| HEB.10:25 | `not forsaking the assembling of ourselves together...` |
| HEB.10:27 | `but acertain fearful expectation of judgment, and ...` |
| HEB.11:1 | `ow faith is the substance of things hoped for, the...` |
| HEB.11:10 | `for he waited for the city which has foundations, ...` |
| HEB.11:18 | `of whom it was said, 'In Isaac your seed shall be ...` |
| HEB.11:33 | `who through faith subdued kingdoms, worked righteo...` |
| HEB.11:38 | `of whom the world was not worthy. They wandered in...` |
| HEB.12:1 | `herefore we also, since we are surrounded by so gr...` |
| HEB.12:13 | `and make straight paths for your feet, so that wha...` |
| HEB.12:19 | `and the sound of atrumpet and the voice of words, ...` |
| HEB.12:23 | `to the general assembly and church of the firstbor...` |
| HEB.12:24 | `to Jesus the Mediator of the new covenant, and to ...` |
| HEB.12:26 | `whose voice then shook the earth; but now He has p...` |
| HEB.13:1 | `et brotherly love continue....` |
