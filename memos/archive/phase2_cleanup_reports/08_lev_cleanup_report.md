# Leviticus Cleanup Report — 2026-03-08

## Summary
- Input: `staging/validated/OT/LEV.md`
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
| R6 | Drop-cap omissions detected (NO auto-fix) | 110 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| LEV.1:9 | `but he shall wash its entrails and its legs with w...` |
| LEV.1:13 | `but he shall wash the entrails and the legs with w...` |
| LEV.3:4 | `the two kidneys and the fat on them by the flanks,...` |
| LEV.3:5 | `and Aaron's sons, the priests, shall offer these u...` |
| LEV.3:10 | `the two kidneys and the fat on them by the flanks,...` |
| LEV.3:11 | `and the priest shall offer these on the altar as a...` |
| LEV.3:15 | `the two kidneys and the fat on them by the flanks,...` |
| LEV.3:16 | `and the priest shall offer these on the altar as a...` |
| LEV.4:3 | `even if he should be the anointed priest, and shou...` |
| LEV.4:9 | `the two kidneys and the fat on them by the flanks,...` |
| LEV.4:10 | `as it was taken from the young bull of the sacrifi...` |
| LEV.4:12 | `the whole young bull he shall carry outside the ca...` |
| LEV.4:14 | `when the sin they committed becomes known, then th...` |
| LEV.4:23 | `and the sin he committed comes to his knowledge, h...` |
| LEV.4:28 | `and the sin he committed comes to his knowledge, t...` |
| LEV.5:3 | `or should touch human uncleanness-even by any uncl...` |
| LEV.5:5 | `then he shall confess his sin in that thing;...` |
| LEV.5:6 | `and he shall bring for his trespass against the Lo...` |
| LEV.5:22 | `or if he found what was lost and should lie about ...` |
| LEV.5:23 | `then it shall be, whenever he should trespass and ...` |
| LEV.5:24 | `or everything about which he swore falsely. He sha...` |
| LEV.7:4 | `the two kidneys and the fat on them by the flanks,...` |
| LEV.7:17 | `but the remainder of the flesh of the sacrifice on...` |
| LEV.7:38 | `in the manner the Lord commanded Moses on Mount Si...` |
| LEV.8:3 | `and gather all the congregation together at the do...` |
| LEV.8:11 | `and he sprinkled some of it on the altar seven tim...` |
| LEV.8:15 | `and Moses killed it. Then he took the blood, and p...` |
| LEV.8:23 | `and Moses killed it. Also he took some of its bloo...` |
| LEV.8:26 | `and from the basket of consecration before the Lor...` |
| LEV.8:27 | `and he put all these in Aaron's hands and in his s...` |
| LEV.9:4 | `also a young bull and a ram as peace offerings bef...` |
| LEV.9:20 | `they put on the breasts. Then he offered the fat o...` |
| LEV.9:21 | `but the breasts and the right thigh Aaron removed ...` |
| LEV.9:24 | `and fire came out from the Lord, and consumed the ...` |
| LEV.10:10 | `that you may distinguish between holy and unholy, ...` |
| LEV.10:11 | `and that you may teach the children of Israel all ...` |
| LEV.11:5 | `the rock hyrax, because it chews the cud but does ...` |
| LEV.11:6 | `the hare, because it chews the cud but does not ha...` |
| LEV.11:7 | `and the swine, though it divides the hoof, having ...` |
| LEV.11:14 | `the kite, and the falcon after its kind;...` |
| LEV.11:15 | `every raven after its kind,...` |
| LEV.11:16 | `the ostrich, the short-eared owl, the sea gull, an...` |
| LEV.11:17 | `the little owl, the fisher owl, and the screech ow...` |
| LEV.11:18 | `the white owl, the jackdaw, and the carrion vultur...` |
| LEV.11:19 | `the stork, the heron after its kind, the hoopoe, a...` |
| LEV.11:25 | `whoever carries part of the carcass of any of them...` |
| LEV.11:26 | `any animal which divides the foot, but is not clov...` |
| LEV.11:30 | `the gecko, the monitor lizard, the sand reptile, t...` |
| LEV.11:34 | `in such a vessel, any edible food upon which water...` |
| LEV.11:47 | `to distinguish between the unclean and the clean, ...` |
| LEV.13:11 | `it is an old leprosy on the surface of his skin. T...` |
| LEV.13:13 | `then the priest shall consider; and indeed, if the...` |
| LEV.13:19 | `and in the place of the ulcer there comes a white ...` |
| LEV.13:25 | `the priest shall examine it; and indeed, if the ha...` |
| LEV.13:30 | `the priest shall examine the infection; and indeed...` |
| LEV.13:33 | `he shall shave himself, but he shall not shave the...` |
| LEV.13:36 | `the priest shall examine him; and indeed, if the l...` |
| LEV.13:39 | `the priest shall look; and indeed, if the bright s...` |
| LEV.13:44 | `he is a leprous man. The priest shall surely prono...` |
| LEV.13:48 | `whether it is in the warp or woof of linen or wool...` |
| LEV.13:49 | `and if the infection is greenish or reddish in the...` |
| LEV.13:54 | `then the priest shall order that the object with t...` |
| LEV.14:4 | `the priest shall give orders to take, for the one ...` |
| LEV.14:22 | `two turtledoves or two young pigeons, such as he i...` |
| LEV.14:27 | `and sprinkle with his right finger some of the oil...` |
| LEV.14:31 | `one as a sin offering and the other as a whole bur...` |
| LEV.14:35 | `and he who owns the house comes and tells the prie...` |
| LEV.14:36 | `then before the priest goes into the house to exam...` |
| LEV.14:38 | `then the priest shall go outside the house to the ...` |
| LEV.14:40 | `then the priest shall give orders to take away the...` |
| LEV.14:44 | `then the priest shall enter the house to examine i...` |
| LEV.14:51 | `and he shall take the cedar wood, the hyssop, the ...` |
| LEV.14:55 | `and for a leprous garment, a house, 56 a scar, a m...` |
| LEV.15:33 | `and for her who is indisposed because of her menst...` |
| LEV.16:2 | `and the Lord said to Moses, 'Tell Aaron your broth...` |
| LEV.17:4 | `and does not bring it to the door of the tabernacl...` |
| LEV.17:5 | `that the children of Israel may bring their sacrif...` |
| LEV.17:9 | `and does not bring it to the door of the tabernacl...` |
| LEV.17:14 | `for the life of all flesh is its blood. Therefore,...` |
| LEV.18:28 | `that the land not be vexed with you in your defile...` |
| LEV.20:5 | `then I will set My face against that man and those...` |
| LEV.21:11 | `nor shall he go near any soul who died, nor defile...` |
| LEV.21:12 | `nor shall he go out of the holy places, nor defile...` |
| LEV.21:19 | `a man who has a broken hand or foot,...` |
| LEV.21:20 | `or is a hunchback or has a defect in his eye, or a...` |
| LEV.21:23 | `but he shall not go near the veil or approach the ...` |
| LEV.22:5 | `or whoever touches any unclean creeping thing by w...` |
| LEV.22:6 | `the soul who has touched any such thing shall be u...` |
| LEV.22:16 | `or allow them to bear the guilt of trespass when t...` |
| LEV.22:19 | `to be acceptable on your behalf, they must be male...` |
| LEV.23:38 | `besides the Sabbaths of the Lord, and besides your...` |
| LEV.23:43 | `that your generations may know that I made the chi...` |
| LEV.24:20 | `fracture for fracture, eye for eye, tooth for toot...` |
| LEV.25:4 | `but in the seventh year there shall be a Sabbath r...` |
| LEV.25:7 | `and for your cattle and the wild animals in your l...` |
| LEV.25:27 | `then let him compute the years since its sale and ...` |
| LEV.25:48 | `after he is sold he may be redeemed again. One of ...` |
| LEV.25:49 | `or his uncle or his uncle's son may redeem him; or...` |
| LEV.26:4 | `then I will give you rain in its season, the land ...` |
| LEV.26:15 | `but your soul disobeys them and despises My judgme...` |
| LEV.26:24 | `then I also will walk in hostility to you, and I w...` |
| LEV.26:28 | `then I also will walk in hostility to you; and I, ...` |
| LEV.26:41 | `and that I also have walked in hostility to them a...` |
| LEV.27:3 | `and if your valuation is of a male from twenty yea...` |
| LEV.27:5 | `and if from five years old up to twenty years old,...` |
| LEV.27:6 | `and if from a month old up to five years old, your...` |
| LEV.27:7 | `and if from sixty years old and above, if it is a ...` |
| LEV.27:12 | `and the priest shall set a value for it, whether g...` |
| LEV.27:21 | `but the field, when it is released in the Remissio...` |
| LEV.27:23 | `then the priest shall reckon to him its full asses...` |

## Brenton-Assisted Repairs (R7)

Auto-applied: 0  |  Ambiguous (not applied): 6


### Ambiguous — Not Applied (score did not improve)

| Anchor | Fused | Repair | Score Δ |
|--------|-------|--------|--------|
| LEV.7:16 | `avow` | `a vow` | -0.0010 |
| LEV.9:4 | `today` | `to day` | -0.0030 |
| LEV.10:19 | `today` | `to day` | -0.0011 |
| LEV.19:27 | `around` | `a round` | +0.0069 |
| LEV.22:29 | `avow` | `a vow` | +0.0049 |
| LEV.27:2 | `avow` | `a vow` | +0.0052 |
