# 1 Kings Cleanup Report — 2026-03-09

## Summary
- Input: `staging/validated/OT/1KI.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 55

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 58 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 56 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L27:
  - `1KI.1:9 Adonijah sacrificed sheep, calves, and lambs by the stone of the Serpent, by the spring called Rogel, and he invited all his brothers, the king'ssons, and all the men of Judah, servants of the king.`
  + `1KI.1:9 Adonijah sacrificed sheep, calves, and lambs by the stone of the Serpent, by the spring called Rogel, and he invited all his brothers, the king's sons, and all the men of Judah, servants of the king.`

L43:
  - `1KI.1:25 For he went down today and sacrificed many calves, lambs, and sheep, and invited all the king'ssons, and the commanders of the army, and Abiathar the priest. Behold, they are eating and drinking before him, and they said, 'Long live King Adonijah.'`
  + `1KI.1:25 For he went down today and sacrificed many calves, lambs, and sheep, and invited all the king's sons, and the commanders of the army, and Abiathar the priest. Behold, they are eating and drinking before him, and they said, 'Long live King Adonijah.'`

L49:
  - `1KI.1:28 Then King David answered and said, 'Call Bathsheba to me.' So she came into the king'spresence and stood before him.`
  + `1KI.1:28 Then King David answered and said, 'Call Bathsheba to me.' So she came into the king's presence and stood before him.`

L55:
  - `1KI.1:34 There let Zadok the priest and Nathan the prophet anoint him as king over Israel, and blow the ram'shorn, and say, 'Long live King Solomon!'`
  + `1KI.1:34 There let Zadok the priest and Nathan the prophet anoint him as king over Israel, and blow the ram's horn, and say, 'Long live King Solomon!'`

L59:
  - `1KI.1:38 So Zadok the priest, Nathan the prophet, Benaiah the son of Jehoiada, the Cherethites, and the Pelethites mounted Solomon on King David'smule, and they led him to Gihon.`
  + `1KI.1:38 So Zadok the priest, Nathan the prophet, Benaiah the son of Jehoiada, the Cherethites, and the Pelethites mounted Solomon on King David's mule, and they led him to Gihon.`

L60:
  - `1KI.1:39 Then Zadok the priest took a horn of olive oil from the tabernacle and anointed Solomon. They blew the ram'shorn, and all the people said, 'Long live King Solomon!'`
  + `1KI.1:39 Then Zadok the priest took a horn of olive oil from the tabernacle and anointed Solomon. They blew the ram's horn, and all the people said, 'Long live King Solomon!'`

L65:
  - `1KI.1:44 The king sent with him Zadok the priest, Nathan the prophet, Benaiah the son of Jehoiada, the Cherethites, and the Pelethites, and they mounted him on the king'smule.`
  + `1KI.1:44 The king sent with him Zadok the priest, Nathan the prophet, Benaiah the son of Jehoiada, the Cherethites, and the Pelethites, and they mounted him on the king's mule.`

L68:
  - `1KI.1:47 The king'sservants also went to bless our lord, King David, saying, 'May God make the name of Solomon your son greater than your name, and may He make his throne greater than your throne.' Then the king worshiped upon his bed,`
  + `1KI.1:47 The king's servants also went to bless our lord, King David, saying, 'May God make the name of Solomon your son greater than your name, and may He make his throne greater than your throne.' Then the king worshiped upon his bed,`

L105:
  - `1KI.2:19 So Bathsheba went to King Solomon to speak to him for Adonijah. The king rose up to meet her and kissed her tenderly. He then sat down on his throne, and a throne was placed for the king'smother; and she was seated at his right hand.`
  + `1KI.2:19 So Bathsheba went to King Solomon to speak to him for Adonijah. The king rose up to meet her and kissed her tenderly. He then sat down on his throne, and a throne was placed for the king's mother; and she was seated at his right hand.`

L120:
  - `1KI.2:31 Then the king said to him, 'Go, and do as he said. Strike him down and bury him, and remove from me and from my father'shouse today the blood Joab shed for no reason.`
  + `1KI.2:31 Then the king said to him, 'Go, and do as he said. Strike him down and bury him, and remove from me and from my father's house today the blood Joab shed for no reason.`

L127:
  - `1KI.2:35 The king put Benaiah the son of Jehoiada in Joab'splace over the army, and the kingdom was established in Jerusalem. Then the king made Zadok the first priest in the place of Abiathar.`
  + `1KI.2:35 The king put Benaiah the son of Jehoiada in Joab's place over the army, and the kingdom was established in Jerusalem. Then the king made Zadok the first priest in the place of Abiathar.`

L129:
  - `1KI.2:37 Solomon'sdiscernment was multiplied exceedingly, beyond the discernment of all the sons of the ancient ones and all the wise men of Egypt.`
  + `1KI.2:37 Solomon's discernment was multiplied exceedingly, beyond the discernment of all the sons of the ancient ones and all the wise men of Egypt.`

L133:
  - `1KI.2:38 Then he took Pharaoh'sdaughter and brought her into the City of David until he should complete his house, and before all the house of the Lord, and the wall surrounding Jerusalem. In seven years he made and completed them.`
  + `1KI.2:38 Then he took Pharaoh's daughter and brought her into the City of David until he should complete his house, and before all the house of the Lord, and the wall surrounding Jerusalem. In seven years he made and completed them.`

L152:
  - `1KI.2:53 Now at the end of three years, two of Shimei'sslaves ran away to Achish the son of Maachah, king of Gath. They told Shimei, saying, 'Behold, your slaves are in Gath.'`
  + `1KI.2:53 Now at the end of three years, two of Shimei's slaves ran away to Achish the son of Maachah, king of Gath. They told Shimei, saying, 'Behold, your slaves are in Gath.'`

L167:
  - `1KI.2:65 Moreover, Solomon'sdaily provision was thirty measures of the finest wheat flour and sixty measures of ground meal, ten chosen calves and twenty pastured oxen and a hundred sheep, and, besides this, deer and gazelles and choice fed hens,`
  + `1KI.2:65 Moreover, Solomon's daily provision was thirty measures of the finest wheat flour and sixty measures of ground meal, ten chosen calves and twenty pastured oxen and a hundred sheep, and, besides this, deer and gazelles and choice fed hens,`

L170:
  - `1KI.2:68 Now Solomon'sofficials were Azariah, the son of Zadok, the priest, and Orniah, the son of Nathan, who was ruler of the standing guard, and Edram was over his house, and Zoba the scribe, and Baasha, the son of Achithalam, writing memoirs, and Abi, the son of Joab, the chief captain, and Achira, the son of Edrahi, over the labor force, and Benaiah the son of Jehoiada over the temple-court and over the brickworks, and Zechariah, the son of Nathan, the counselor.`
  + `1KI.2:68 Now Solomon's officials were Azariah, the son of Zadok, the priest, and Orniah, the son of Nathan, who was ruler of the standing guard, and Edram was over his house, and Zoba the scribe, and Baasha, the son of Achithalam, writing memoirs, and Abi, the son of Joab, the chief captain, and Achira, the son of Edrahi, over the labor force, and Benaiah the son of Jehoiada over the temple-court and over the brickworks, and Zechariah, the son of Nathan, the counselor.`

L204:
  - `1KI.3:18 But this woman'sson died that night, because she lay on him.`
  + `1KI.3:18 But this woman's son died that night, because she lay on him.`

L230:
  - `1KI.4:5 Azariah, the son of Nathan, over the administrators; Zabud the son of Nathan, the king'scompanion;`
  + `1KI.4:5 Azariah, the son of Nathan, over the administrators; Zabud the son of Nathan, the king's companion;`

L281:
  - `1KI.5:1 In this manner the governors provided everything King Solomon requested for the king'stable, each man in his month. They did not change athing; even the barley and the grain stalks for the horses and the chariots they brought to the place where the king was, each man according to his appointment.`
  + `1KI.5:1 In this manner the governors provided everything King Solomon requested for the king's table, each man in his month. They did not change athing; even the barley and the grain stalks for the horses and the chariots they brought to the place where the king was, each man according to his appointment.`

L305:
  - `1KI.5:10 So all the people came to hear Solomon'swisdom, and he received gifts from all the kings of the earth who heard his wisdom.`
  + `1KI.5:10 So all the people came to hear Solomon's wisdom, and he received gifts from all the kings of the earth who heard his wisdom.`

L1273:
  - `1KI.13:3 Then King Jeroboam said to the man of God, 'Entreat the favor of the Lord your God, that my hand may be restored to me.' So the man of God entreated the Lord, and the king'shand was restored new, as it was before.`
  + `1KI.13:3 Then King Jeroboam said to the man of God, 'Entreat the favor of the Lord your God, that my hand may be restored to me.' So the man of God entreated the Lord, and the king's hand was restored new, as it was before.`

L1290:
  - `1KI.13:8 Now an old prophet dwelt in Bethel, and his sons came and told him all the works the man of God did that day in Bethel. They also told their father the words he spoke to the king, and the father'scountenance changed.`
  + `1KI.13:8 Now an old prophet dwelt in Bethel, and his sons came and told him all the works the man of God did that day in Bethel. They also told their father the words he spoke to the king, and the father's countenance changed.`

L1371:
  - `1KI.13:32 Rehoboam the son of Solomon reigned over Judah, and he was forty-one years old when he became king. He reigned seventeen years in Jerusalem, the city the Lord chose out of all the tribes of Israel to place His name. His mother'sname was Naamah, an Ammonite woman.`
  + `1KI.13:32 Rehoboam the son of Solomon reigned over Judah, and he was forty-one years old when he became king. He reigned seventeen years in Jerusalem, the city the Lord chose out of all the tribes of Israel to place His name. His mother's name was Naamah, an Ammonite woman.`

L1385:
  - `1KI.14:4 He took all the treasures of the Lord'shouse, the treasures of the king'shouse, and the gold spears David received from the hand of the servants of Hadadezer, king of Syria, who brought them to Jerusalem. He took away all the gold weapons.`
  + `1KI.14:4 He took all the treasures of the Lord's house, the treasures of the king's house, and the gold spears David received from the hand of the servants of Hadadezer, king of Syria, who brought them to Jerusalem. He took away all the gold weapons.`

L1389:
  - `1KI.14:5 Then King Rehoboam made bronze weapons in their place, and committed them to the hands of the captains of the guard, who guarded the doorway of the king'shouse.`
  + `1KI.14:5 Then King Rehoboam made bronze weapons in their place, and committed them to the hands of the captains of the guard, who guarded the doorway of the king's house.`

L1407:
  - `1KI.14:11 He reigned for six years in Jerusalem. His mother'sname was Maachah the daughter of Abishalom.`
  + `1KI.14:11 He reigned for six years in Jerusalem. His mother's name was Maachah the daughter of Abishalom.`

L1415:
  - `1KI.15:2 Nevertheless for David'ssake, the Lord gave him aremnant, so as to establish his sons after him and to establish Jerusalem.`
  + `1KI.15:2 Nevertheless for David's sake, the Lord gave him aremnant, so as to establish his sons after him and to establish Jerusalem.`

L1426:
  - `1KI.15:7 He reigned forty-one years in Jerusalem. His mother'sname was Ana, the daughter of Abishalom.`
  + `1KI.15:7 He reigned forty-one years in Jerusalem. His mother's name was Ana, the daughter of Abishalom.`

L1442:
  - `1KI.15:11 But he did not remove the high places. Nevertheless, Asa'sheart was perfect with the Lord all his days.`
  + `1KI.15:11 But he did not remove the high places. Nevertheless, Asa's heart was perfect with the Lord all his days.`

L1455:
  - `1KI.15:15 Then Asa took all the silver and gold found in the treasuries of the king'shouse and delivered them into the hands of his servants. Asa then sent them to the son of Hadad the son of Tabrimmon, the son of Hezion, king of Syria, who dwelt in Damascus, saying,`
  + `1KI.15:15 Then Asa took all the silver and gold found in the treasuries of the king's house and delivered them into the hands of his servants. Asa then sent them to the son of Hadad the son of Tabrimmon, the son of Hezion, king of Syria, who dwelt in Damascus, saying,`

L1493:
  - `1KI.15:26 It came to pass that when he reigned, he struck every house of Jeroboam and left no one of Jeroboam'shouse breathing, until he utterly destroyed him, according to the word of the Lord spoken by His servant Ahijah the Shilonite,`
  + `1KI.15:26 It came to pass that when he reigned, he struck every house of Jeroboam and left no one of Jeroboam's house breathing, until he utterly destroyed him, according to the word of the Lord spoken by His servant Ahijah the Shilonite,`

L1554:
  - `1KI.16:14 When Zimri saw the city was taken, he went into the citadel of the king'shouse, and burned the king'shouse down upon himself, and died.`
  + `1KI.16:14 When Zimri saw the city was taken, he went into the citadel of the king's house, and burned the king's house down upon himself, and died.`

L1602:
  - `1KI.16:29 Now there was no king or king'sdeputy in Syria,`
  + `1KI.16:29 Now there was no king or king's deputy in Syria,`

L1735:
  - `1KI.18:3 Now Obadiah was alone on his way, and Elijah came alone to meet him. Obadiah quickly fell on his face in Elijah'spresence and said, 'My lord Elijah, is that you?'`
  + `1KI.18:3 Now Obadiah was alone on his way, and Elijah came alone to meet him. Obadiah quickly fell on his face in Elijah's presence and said, 'My lord Elijah, is that you?'`

L1756:
  - `1KI.18:9 Was it not reported to you, my lord, as to what I did when Jezebel killed the prophets of the Lord, how I hid one hundred men of the Lord'sprophets, fifty to acave, and fed them with bread and water?`
  + `1KI.18:9 Was it not reported to you, my lord, as to what I did when Jezebel killed the prophets of the Lord, how I hid one hundred men of the Lord's prophets, fifty to acave, and fed them with bread and water?`

L1777:
  - `1KI.18:15 Now therefore, send and gather all Israel to me on Mount Carmel, the four hundred and fifty prophets of shame, and the four hundred prophets of the sacred groves who eat at Jezebel'stable.'`
  + `1KI.18:15 Now therefore, send and gather all Israel to me on Mount Carmel, the four hundred and fifty prophets of shame, and the four hundred prophets of the sacred groves who eat at Jezebel's table.'`

L1875:
  - `1KI.18:46 But Elijah himself went aday'sjourney into the wilderness, and came and sat under ajuniper tree. He prayed concerning his life, that he might die, and said, 'I pray it be enough, O Lord. Now take my life, for I am no better than my fathers.'`
  + `1KI.18:46 But Elijah himself went aday's journey into the wilderness, and came and sat under ajuniper tree. He prayed concerning his life, that he might die, and said, 'I pray it be enough, O Lord. Now take my life, for I am no better than my fathers.'`

L1947:
  - `1KI.19:21 So Ahab'sspirit was disturbed; and he lay down on his bed and covered his face. He would not eat any food.`
  + `1KI.19:21 So Ahab's spirit was disturbed; and he lay down on his bed and covered his face. He would not eat any food.`

L1957:
  - `1KI.20:4 So she wrote aletter in Ahab'sname, sealed it with his seal, and sent the letter to the elders and the nobles dwelling in the city with Naboth.`
  + `1KI.20:4 So she wrote aletter in Ahab's name, sealed it with his seal, and sent the letter to the elders and the nobles dwelling in the city with Naboth.`

L2305:
  - `1KI.22:37 Jehoshaphat was thirty-five years old when he became king, and he reigned for twenty-five years in Jerusalem. His mother'sname was Azubah the daughter of Shilhi.`
  + `1KI.22:37 Jehoshaphat was thirty-five years old when he became king, and he reigned for twenty-five years in Jerusalem. His mother's name was Azubah the daughter of Shilhi.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 1KI.1:48 | `and the king said, 'Blessed be the Lord God of Isr...` |
| 1KI.2:4 | `that the Lord may confirm His word which He spoke,...` |
| 1KI.2:64 | `and he built Thermae in the desert....` |
| 1KI.2:66 | `because there was agovernor all along the opposite...` |
| 1KI.4:3 | `and Elihoreph and Ahijah, the sons of Shisha; and ...` |
| 1KI.4:4 | `and the priests, Zadok and Abiathar, the priests;...` |
| 1KI.4:9 | `the son of Rechab in Makaz and Bethlehem and Beth ...` |
| 1KI.4:10 | `the son of Hesed, in Arubboth; to him belonged Soc...` |
| 1KI.4:11 | `the son of Abinadab, in all the regions of Dor; he...` |
| 1KI.4:13 | `the son of Geber, in Ramoth Gilead; to him belonge...` |
| 1KI.5:3 | `ten chosen calves, twenty pastured oxen, a hundred...` |
| 1KI.5:4 | `because there was agovernor all along the opposite...` |
| 1KI.5:7 | `and he was made wise beyond every man. He was even...` |
| 1KI.5:28 | `with an additional three thousand six hundred from...` |
| 1KI.6:19 | `and he overlaid it with pure gold....` |
| 1KI.7:17 | `the reliefs were lions, oxen, and cherubim. Above ...` |
| 1KI.7:19 | `and axles of bronze; and the height of one wheel w...` |
| 1KI.7:28 | `the two pillars, the two bowl-shaped capitals on t...` |
| 1KI.7:29 | `four hundred pomegranates for the two lattice-work...` |
| 1KI.7:30 | `the ten bases, and ten washbasins on the bases;...` |
| 1KI.7:35 | `the lamp stands of pure gold, five on the right si...` |
| 1KI.7:36 | `the doorways, the nails, the bowls, the dishes, an...` |
| 1KI.7:47 | `where the foundation was laid with huge costly sto...` |
| 1KI.8:3 | `and the tabernacle of testimony and all the holy f...` |
| 1KI.8:10 | `so the priests could not stand there ministering b...` |
| 1KI.8:20 | `and he said, 'O Lord God of Israel, there is no Go...` |
| 1KI.8:26 | `that Your eyes may be open toward this temple day ...` |
| 1KI.8:31 | `then You will hear in heaven and be propitious to ...` |
| 1KI.8:39 | `when he comes and prays in this temple,...` |
| 1KI.8:42 | `then You will hear their prayer and supplication i...` |
| 1KI.8:44 | `yet when they turn their hearts in the land where ...` |
| 1KI.8:45 | `and they return to You with all their heart and wi...` |
| 1KI.8:46 | `then You will hear in heaven from Your dwelling pl...` |
| 1KI.8:47 | `and You will be propitious in their unrighteousnes...` |
| 1KI.8:48 | `for they are Your people and Your inheritance, who...` |
| 1KI.8:56 | `that He may incline our hearts to Himself, to walk...` |
| 1KI.8:58 | `that all the peoples of the earth may know the Lor...` |
| 1KI.9:3 | `then I will establish the throne of your kingdom o...` |
| 1KI.9:5 | `then I will cut off Israel from the land I gave th...` |
| 1KI.10:13 | `in addition to that from traveling merchants, from...` |
| 1KI.10:17 | `with six upward steps to the throne and busts of c...` |
| 1KI.10:20 | `for aship of Tarshish, amerchant ship of the king'...` |
| 1KI.10:22 | `the people left behind from the Cherethites, the A...` |
| 1KI.11:2 | `and for Ashtaroth, the abomination of the Sidonian...` |
| 1KI.11:6 | `and commanded him concerning this thing, that he s...` |
| 1KI.11:28 | `therefore I will surely set Myself against him all...` |
| 1KI.13:11 | `to seek after the man of God. He found him sitting...` |
| 1KI.13:18 | `and he said to the man of God who came from Judah,...` |
| 1KI.13:19 | `but indeed, did come back, and ate bread and drank...` |
| 1KI.15:27 | `for the sins of Jeroboam that Israel sinned, and i...` |
| 1KI.16:30 | `and King Jehoshaphat made aship in Tarshish to go ...` |
| 1KI.16:37 | `and also made a sacred grove. Ahab did yet more pr...` |
| 1KI.20:6 | `and seat two men before him, scoundrels, to bear w...` |
| 1KI.21:1 | `for I will send my servants to you at this time to...` |
| 1KI.21:14 | `because he did not believe the young men of the go...` |
| 1KI.22:22 | `and place him in prison. Feed him with bread of su...` |
