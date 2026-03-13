# 3 Maccabees Cleanup Report — 2026-03-09

## Summary
- Input: `staging/validated/OT/3MA.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 14

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 15 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 10 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L18:
  - `3MA.1:2 Now a certain Theodotus, intending to carry out a plan he had developed, took the finest of the Ptolemaic weapons issued earlier to him and crossed by night to Ptolemy'stent with the intention of killing him by himself, and in that way ending the war.`
  + `3MA.1:2 Now a certain Theodotus, intending to carry out a plan he had developed, took the finest of the Ptolemaic weapons issued earlier to him and crossed by night to Ptolemy's tent with the intention of killing him by himself, and in that way ending the war.`

L79:
  - `3MA.2:26 He was not content with his countless acts of indecency, but audaciously proceeded to spread many evil reports throughout the region. Many of his friends observed the king'sintentions and adjusted themselves to conform to his will.`
  + `3MA.2:26 He was not content with his countless acts of indecency, but audaciously proceeded to spread many evil reports throughout the region. Many of his friends observed the king's intentions and adjusted themselves to conform to his will.`

L133:
  - `3MA.4:11 When they were brought to the place called Schedia and their voyage was completed according to the king'sdecree, he directed that they be confined outside the city in the hippodrome, which had an immense outside perimeter. He also commanded that at the appointed time, they be made a public example for those returning to the city and those going from the city to the country. Thus they could not communicate with the king'sforces, or in any way claim to be within the boundaries of the city.`
  + `3MA.4:11 When they were brought to the place called Schedia and their voyage was completed according to the king's decree, he directed that they be confined outside the city in the hippodrome, which had an immense outside perimeter. He also commanded that at the appointed time, they be made a public example for those returning to the city and those going from the city to the country. Thus they could not communicate with the king's forces, or in any way claim to be within the boundaries of the city.`

L143:
  - `3MA.4:21 This was the activity of God'sinvincible providence helping the Jews from heaven.`
  + `3MA.4:21 This was the activity of God's invincible providence helping the Jews from heaven.`

L165:
  - `3MA.5:19 But when Hermon declared that while it was still night he had done what was ordered, the king'sfriends confirmed this.`
  + `3MA.5:19 But when Hermon declared that while it was still night he had done what was ordered, the king's friends confirmed this.`

L166:
  - `3MA.5:20 Then overcome with a savagery worse than that of Phalaris, the king said that because of the day'ssleep they received favor; but without delay on the coming day, Hermon must ready the elephants for the extermination of the godless Jews.`
  + `3MA.5:20 Then overcome with a savagery worse than that of Phalaris, the king said that because of the day's sleep they received favor; but without delay on the coming day, Hermon must ready the elephants for the extermination of the godless Jews.`

L174:
  - `3MA.5:28 This was an act of God, Master over all things, who placed a forgetfulness in the king'smind about what had been plotted before.`
  + `3MA.5:28 This was an act of God, Master over all things, who placed a forgetfulness in the king's mind about what had been plotted before.`

L175:
  - `3MA.5:29 But Hermon and all the king'sfriends told him, 'The beasts and the troops are ready, O king, according to your eager purpose.'`
  + `3MA.5:29 But Hermon and all the king's friends told him, 'The beasts and the troops are ready, O king, according to your eager purpose.'`

L176:
  - `3MA.5:30 But at these words, he was filled with deep anger, because his whole plot had been scattered from his mind by God'sprovidence. Then he glared at them and threatened,`
  + `3MA.5:30 But at these words, he was filled with deep anger, because his whole plot had been scattered from his mind by God's providence. Then he glared at them and threatened,`

L180:
  - `3MA.5:34 Then one by one the king'sfriends slunk away sullenly, and each one returned to his own business.`
  + `3MA.5:34 Then one by one the king's friends slunk away sullenly, and each one returned to his own business.`

L220:
  - `3MA.6:20 The king'sbody was seized with a tremor, and he even forgot his contemptible vocabulary.`
  + `3MA.6:20 The king's body was seized with a tremor, and he even forgot his contemptible vocabulary.`

L222:
  - `3MA.6:22 The king'swrath was turned to compassion and tears because of the plot he devised earlier,`
  + `3MA.6:22 The king's wrath was turned to compassion and tears because of the plot he devised earlier,`

L231:
  - `3MA.6:31 Then those who had been treated disgracefully and were close to death, or rather stood at death'sdoor, were given a special invitation. They organized a feast of deliverance from the bitter and mournful fate of death. Filled with joy, their celebration took the place of desolation and grave clothes.`
  + `3MA.6:31 Then those who had been treated disgracefully and were close to death, or rather stood at death's door, were given a special invitation. They organized a feast of deliverance from the bitter and mournful fate of death. Filled with joy, their celebration took the place of desolation and grave clothes.`

L255:
  - `3MA.7:11 They proclaimed that those who transgressed the divine commands on account of their appetites would never again be favorable toward the king'sgovernment.`
  + `3MA.7:11 They proclaimed that those who transgressed the divine commands on account of their appetites would never again be favorable toward the king's government.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 3MA.1:10 | `and he admired the good order of the temple and co...` |
| 3MA.2:18 | `that they trampled the house of holiness as the ho...` |
| 3MA.3:15 | `we thought it fit not by force of the spear, but b...` |
| 3MA.3:18 | `we were carried away by arrogant old men who preve...` |
| 3MA.4:20 | `when they proved what they said, for they showed h...` |
| 3MA.5:7 | `called out to the Lord Almighty, Sovereign of all ...` |
| 3MA.5:8 | `that He divert the unholy plot against them with a...` |
| 3MA.5:51 | `and they cried out in aloud voice, beseeching the ...` |
| 3MA.6:3 | `look upon the seed of Abraham and the descendants ...` |
| 3MA.6:23 | `for he heard the wailing and saw all the people wh...` |
