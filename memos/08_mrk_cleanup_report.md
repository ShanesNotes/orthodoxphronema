# Mark Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/MRK.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 16

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 17 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 56 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L32:
  - `MRK.1:6 Now John was clothed with camel'shair and with aleather belt around his waist, and he ate locusts and wild honey.`
  + `MRK.1:6 Now John was clothed with camel's hair and with aleather belt around his waist, and he ate locusts and wild honey.`

L65:
  - `MRK.1:30 But Simon'swife'smother lay sick with afever, and they told Him about her at once.`
  + `MRK.1:30 But Simon's wife's mother lay sick with afever, and they told Him about her at once.`

L110:
  - `MRK.2:15 Now it happened, as He was dining in Levi'shouse, that many tax collectors and sinners also sat together with Jesus and His disciples; for there were many, and they followed Him.`
  + `MRK.2:15 Now it happened, as He was dining in Levi's house, that many tax collectors and sinners also sat together with Jesus and His disciples; for there were many, and they followed Him.`

L167:
  - `MRK.3:27 No one can enter astrong man'shouse and plunder his goods, unless he first binds the strong man. And then he will plunder his house.`
  + `MRK.3:27 No one can enter astrong man's house and plunder his goods, unless he first binds the strong man. And then he will plunder his house.`

L207:
  - `MRK.4:17 and they have no root in themselves, and so endure only for atime. Afterward, when tribulation or persecution arises for the word'ssake, immediately they stumble.`
  + `MRK.4:17 and they have no root in themselves, and so endure only for atime. Afterward, when tribulation or persecution arises for the word's sake, immediately they stumble.`

L296:
  - `MRK.5:35 (Mt 9:23-26; Lk 8:49-56) While He was still speaking, some came from the ruler of the synagogue'shouse who said, 'Your daughter is dead. Why trouble the Teacher any further?'`
  + `MRK.5:35 (Mt 9:23-26; Lk 8:49-56) While He was still speaking, some came from the ruler of the synagogue's house who said, 'Your daughter is dead. Why trouble the Teacher any further?'`

L332:
  - `MRK.6:17 For Herod himself had sent and laid hold of John, and bound him in prison for the sake of Herodias, his brother Philip'swife; for he had married her.`
  + `MRK.6:17 For Herod himself had sent and laid hold of John, and bound him in prison for the sake of Herodias, his brother Philip's wife; for he had married her.`

L333:
  - `MRK.6:18 Because John had said to Herod, 'It is not lawful for you to have your brother'swife.'`
  + `MRK.6:18 Because John had said to Herod, 'It is not lawful for you to have your brother's wife.'`

L412:
  - `MRK.7:27 But Jesus said to her, 'Let the children be filled first, for it is not good to take the children'sbread and throw it to the little dogs.'`
  + `MRK.7:27 But Jesus said to her, 'Let the children be filled first, for it is not good to take the children's bread and throw it to the little dogs.'`

L413:
  - `MRK.7:28 And she answered and said to Him, 'Yes, Lord, yet even the little dogs under the table eat from the children'scrumbs.'`
  + `MRK.7:28 And she answered and said to Him, 'Yes, Lord, yet even the little dogs under the table eat from the children's crumbs.'`

L480:
  - `MRK.8:35 For whoever desires to save his life will lose it, but whoever loses his life for My sake and the gospel'swill save it.`
  + `MRK.8:35 For whoever desires to save his life will lose it, but whoever loses his life for My sake and the gospel's will save it.`

L688:
  - `MRK.12:11 This was the Lord'sdoing, And it is marvelous in our eyes'? ' a`
  + `MRK.12:11 This was the Lord's doing, And it is marvelous in our eyes'? ' a`

L702:
  - `MRK.12:19 (Mt 22:23-33; Lk 20:27-40) 'Teacher, Moses wrote to us that if aman'sbrother dies, and leaves his wife behind, and leaves no children, his brother should take his wife and raise up offspring for his brother.`
  + `MRK.12:19 (Mt 22:23-33; Lk 20:27-40) 'Teacher, Moses wrote to us that if aman's brother dies, and leaves his wife behind, and leaves no children, his brother should take his wife and raise up offspring for his brother.`

L719:
  - `MRK.12:33 And to love Him with all the heart, with all the understanding, with all the soul, aand with all the strength, and to love one'sneighbor as oneself, is more than all the whole burnt offerings and sacrifices.'`
  + `MRK.12:33 And to love Him with all the heart, with all the understanding, with all the soul, aand with all the strength, and to love one's neighbor as oneself, is more than all the whole burnt offerings and sacrifices.'`

L764:
  - `MRK.13:13 And you will be hated by all for My name'ssake. But he who endures to the end shall be saved.`
  + `MRK.13:13 And you will be hated by all for My name's sake. But he who endures to the end shall be saved.`

L771:
  - `MRK.13:20 And unless the Lord had shortened those days, no flesh would be saved; but for the elect'ssake, whom He chose, He shortened the days.`
  + `MRK.13:20 And unless the Lord had shortened those days, no flesh would be saved; but for the elect's sake, whom He chose, He shortened the days.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| MRK.1:1 | `he beginning of the gospel of Jesus Christ, the So...` |
| MRK.1:15 | `and saying, 'The time is fulfilled, and the kingdo...` |
| MRK.1:24 | `saying, 'Let us alone! What have we to do with You...` |
| MRK.1:44 | `and said to him, 'See that you say nothing to anyo...` |
| MRK.2:1 | `nd again He entered Capernaum after some days, and...` |
| MRK.2:26 | `how he went into the house of God in the days of A...` |
| MRK.3:1 | `nd He entered the synagogue again, and aman was th...` |
| MRK.3:8 | `and Jerusalem and Idumea and beyond the Jordan; an...` |
| MRK.3:15 | `and to have power to heal sicknesses and ato cast ...` |
| MRK.3:19 | `and Judas Iscariot, who also betrayed Him. And the...` |
| MRK.3:29 | `but he who blasphemes against the Holy Spirit neve...` |
| MRK.3:30 | `because they said, 'He has an unclean spirit.'...` |
| MRK.4:1 | `nd again He began to teach by the sea. And agreat ...` |
| MRK.4:12 | `so that 'Seeing they may see and not perceive, And...` |
| MRK.4:17 | `and they have no root in themselves, and so endure...` |
| MRK.4:19 | `and the cares of this world, the deceitfulness of ...` |
| MRK.4:27 | `and should sleep by night and rise by day, and the...` |
| MRK.4:32 | `but when it is sown, it grows up and becomes great...` |
| MRK.5:1 | `hen they came to the other side of the sea, to the...` |
| MRK.5:3 | `who had his dwelling among the tombs; and no one c...` |
| MRK.5:4 | `because he had often been bound with shackles and ...` |
| MRK.5:23 | `and begged Him earnestly, saying, 'My little daugh...` |
| MRK.5:26 | `and had suffered many things from many physicians....` |
| MRK.6:1 | `hen He went out from there and came to His own cou...` |
| MRK.6:9 | `but to wear sandals, and not to put on two tunics....` |
| MRK.6:20 | `for Herod feared John, knowing that he was ajust a...` |
| MRK.6:50 | `for they all saw Him and were troubled. But immedi...` |
| MRK.7:1 | `hen the Pharisees and some of the scribes came tog...` |
| MRK.7:12 | `then you no longer let him do anything for his fat...` |
| MRK.7:19 | `because it does not enter his heart but his stomac...` |
| MRK.8:1 | `nthose days, the multitude being very great and ha...` |
| MRK.9:1 | `nd He said to them, 'Assuredly, I say to you that ...` |
| MRK.9:6 | `because he did not know what to say, for they were...` |
| MRK.9:44 | `where 'Their worm does not die And the fire is not...` |
| MRK.9:46 | `where 'Their worm does not die And the fire is not...` |
| MRK.9:48 | `where...` |
| MRK.10:1 | `hen He arose from there and came to the region of ...` |
| MRK.10:8 | `and the two shall become one flesh'; aso then they...` |
| MRK.10:30 | `who shall not receive ahundredfold now in this tim...` |
| MRK.10:34 | `and they will mock Him, and scourge Him, and spit ...` |
| MRK.11:1 | `ow when they drew near Jerusalem, to Bethphage aan...` |
| MRK.11:2 | `and He said to them, 'Go into the village opposite...` |
| MRK.12:1 | `hen He began to speak to them in parables: 'A man ...` |
| MRK.12:40 | `who devour widows' houses, and for apretense make ...` |
| MRK.12:44 | `for they all put in out of their abundance, but sh...` |
| MRK.13:1 | `hen as He went out of the temple, one of His disci...` |
| MRK.13:25 | `the stars of heaven will fall, and the powers in t...` |
| MRK.13:36 | `lest, coming suddenly, he find you sleeping....` |
| MRK.14:1 | `fter two days it was the Passover and the Feast of...` |
| MRK.14:28 | `b 'But after I have been raised, I will go before ...` |
| MRK.14:52 | `and he left the linen cloth and fled from them nak...` |
| MRK.15:1 | `mmediately, in the morning, the chief priests held...` |
| MRK.15:18 | `and began to salute Him, 'Hail, King of the Jews!'...` |
| MRK.15:41 | `who also followed Him and ministered to Him when H...` |
| MRK.16:1 | `ow when the Sabbath was past, Mary Magdalene, Mary...` |
| MRK.16:18 | `they awill take up serpents; and if they drink any...` |
