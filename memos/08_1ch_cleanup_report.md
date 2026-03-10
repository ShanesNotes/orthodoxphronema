# 1 Chronicles Cleanup Report — 2026-03-09

## Summary
- Input: `staging/validated/OT/1CH.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 43

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 47 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 122 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L39:
  - `1CH.1:20 And the sons of Keturah, Abraham'sconcubine: she bore him Zembram, Jexan, Madiam, Madam, Sobac, Soe; and the sons of Jexan: Daedan and Sabai;`
  + `1CH.1:20 And the sons of Keturah, Abraham's concubine: she bore him Zembram, Jexan, Madiam, Madam, Sobac, Soe; and the sons of Jexan: Daedan and Sabai;`

L108:
  - `1CH.2:24 After Hezron died in Caleb-Ephrathah, Hezron'swife Abijah bore him Ashhur the father of Tekoa.`
  + `1CH.2:24 After Hezron died in Caleb-Ephrathah, Hezron's wife Abijah bore him Ashhur the father of Tekoa.`

L115:
  - `1CH.2:31 The son of Appaim was Ishi, the son of Ishi was Sheshan, and Sheshan'sson was Ahlai.`
  + `1CH.2:31 The son of Appaim was Ishi, the son of Ishi was Sheshan, and Sheshan's son was Ahlai.`

L133:
  - `1CH.2:46 Ephah, Caleb'sconcubine, bore Haran, Moza, and Gazez; and Haran begot Gazez.`
  + `1CH.2:46 Ephah, Caleb's concubine, bore Haran, Moza, and Gazez; and Haran begot Gazez.`

L135:
  - `1CH.2:48 Maachah, Caleb'sconcubine, bore Sheber and Tirhanah.`
  + `1CH.2:48 Maachah, Caleb's concubine, bore Sheber and Tirhanah.`

L199:
  - `1CH.4:17 The sons of Ezrah were Jether, Mered, Epher, and Jalon. Mered'swife bore Miriam, Shammai, and Ishbah the father of Eshtemoa.`
  + `1CH.4:17 The sons of Ezrah were Jether, Mered, Epher, and Jalon. Mered's wife bore Miriam, Shammai, and Ishbah the father of Eshtemoa.`

L201:
  - `1CH.4:19 The sons of Hodiah'swife, the sister of Naham, were the fathers of Keilah the Garmite and of Eshtemoa the Maachathite.`
  + `1CH.4:19 The sons of Hodiah's wife, the sister of Naham, were the fathers of Keilah the Garmite and of Eshtemoa the Maachathite.`

L389:
  - `1CH.7:15 Machir took as his wife the sister of Huppim and Shuppim, whose name was Maachah. The name of Gilead'sgrandson was Zelophehad, but Zelophehad begot only daughters.`
  + `1CH.7:15 Machir took as his wife the sister of Huppim and Shuppim, whose name was Maachah. The name of Gilead's grandson was Zelophehad, but Zelophehad begot only daughters.`

L454:
  - `1CH.8:29 Now the father of Gibeon, whose wife'sname was Maacah, dwelt at Gibeon.`
  + `1CH.8:29 Now the father of Gibeon, whose wife's name was Maacah, dwelt at Gibeon.`

L501:
  - `1CH.9:19 Shallum the son of Kore, the son of Ebiasaph, the son of Korah, and his brethren from his father'shouse, the Korahites, were in charge of the work of the service, gatekeepers of the tabernacle. Their fathers had been keepers of the entrance to the camp of the Lord.`
  + `1CH.9:19 Shallum the son of Kore, the son of Ebiasaph, the son of Korah, and his brethren from his father's house, the Korahites, were in charge of the work of the service, gatekeepers of the tabernacle. Their fathers had been keepers of the entrance to the camp of the Lord.`

L516:
  - `1CH.9:31 Mattithiah of the Levites, the firstborn of Shallum the Korahite, was entrusted over the items of the sacrificial offering from the chief priest'sfrying pan.`
  + `1CH.9:31 Mattithiah of the Levites, the firstborn of Shallum the Korahite, was entrusted over the items of the sacrificial offering from the chief priest's frying pan.`

L523:
  - `1CH.9:35 Jeiel the father of Gibeon, whose wife'sname was Maacah, dwelt at Gibeon.`
  + `1CH.9:35 Jeiel the father of Gibeon, whose wife's name was Maacah, dwelt at Gibeon.`

L581:
  - `1CH.11:23 And he killed an Egyptian, a man of great height, five cubits tall. In the hand of the Egyptian there was a spear like a weaver'sbeam, and he went down to him with a staff, snatched the spear out of the Egyptian'shand, and killed him with his own spear.`
  + `1CH.11:23 And he killed an Egyptian, a man of great height, five cubits tall. In the hand of the Egyptian there was a spear like a weaver's beam, and he went down to him with a staff, snatched the spear out of the Egyptian's hand, and killed him with his own spear.`

L612:
  - `1CH.12:2 being armed with bows for shooting arrows and using either the right hand or the left for slinging stones. They were of Benjamin, Saul'sbrethren.`
  + `1CH.12:2 being armed with bows for shooting arrows and using either the right hand or the left for slinging stones. They were of Benjamin, Saul's brethren.`

L642:
  - `1CH.12:29 Zadok, a young man, avaliant warrior, and from his father'shouse, twenty-two captains;`
  + `1CH.12:29 Zadok, a young man, avaliant warrior, and from his father's house, twenty-two captains;`

L670:
  - `1CH.13:11 And David became disheartened regarding the Lord'saction against Uzza, and called that place PerezUzza until this day.`
  + `1CH.13:11 And David became disheartened regarding the Lord's action against Uzza, and called that place PerezUzza until this day.`

L735:
  - `1CH.15:29 And it happened, as the ark of the covenant of the Lord came to the City of David, that Michal, Saul'sdaughter, looked out through a window and saw King David dancing and playing music; and she despised him in her heart.`
  + `1CH.15:29 And it happened, as the ark of the covenant of the Lord came to the City of David, that Michal, Saul's daughter, looked out through a window and saw King David dancing and playing music; and she despised him in her heart.`

L830:
  - `1CH.18:6 Then David put a garrison in Damascus of Syria; and the Syrians became David'sservants and brought tribute. So the Lord preserved David wherever he went.`
  + `1CH.18:6 Then David put a garrison in Damascus of Syria; and the Syrians became David's servants and brought tribute. So the Lord preserved David wherever he went.`

L837:
  - `1CH.18:13 He also put garrisons in Edom, and all the Edomites became David'sservants. And the Lord preserved David wherever he went.`
  + `1CH.18:13 He also put garrisons in Edom, and all the Edomites became David's servants. And the Lord preserved David wherever he went.`

L844:
  - `1CH.18:17 Benaiah the son of Jehoiada was over the Cherethites and the Pelethites; and David'ssons were the king'sfirst successors.`
  + `1CH.18:17 Benaiah the son of Jehoiada was over the Cherethites and the Pelethites; and David's sons were the king's first successors.`

L862:
  - `1CH.19:16 Now when the Syrians saw that they had been defeated by Israel, they sent messengers and brought the Syrians who were beyond the river, and Shophach the commander of Hadadezer'sarmy went before them.`
  + `1CH.19:16 Now when the Syrians saw that they had been defeated by Israel, they sent messengers and brought the Syrians who were beyond the river, and Shophach the commander of Hadadezer's army went before them.`

L872:
  - `1CH.20:2 Then David took the crown of Molchol their king from his head, and found it to weigh a talent of gold, and there were precious stones in it. And it was set on David'shead. Also he brought out the spoil of the city in great abundance.`
  + `1CH.20:2 Then David took the crown of Molchol their king from his head, and found it to weigh a talent of gold, and there were precious stones in it. And it was set on David's head. Also he brought out the spoil of the city in great abundance.`

L878:
  - `1CH.20:5 Again there was war with the Philistines, and Elhanan the son of Jair killed Lahmi the brother of Goliath the Gittite, the shaft of whose spear was like a weaver'sbeam.`
  + `1CH.20:5 Again there was war with the Philistines, and Elhanan the son of Jair killed Lahmi the brother of Goliath the Gittite, the shaft of whose spear was like a weaver's beam.`

L880:
  - `1CH.20:7 So when he defied Israel, Jonathan the son of Shimea, David'sbrother, killed him.`
  + `1CH.20:7 So when he defied Israel, Jonathan the son of Shimea, David's brother, killed him.`

L890:
  - `1CH.21:4 Nevertheless the king'sword prevailed against Joab. Therefore Joab departed and went throughout all Israel and came to Jerusalem.`
  + `1CH.21:4 Nevertheless the king's word prevailed against Joab. Therefore Joab departed and went throughout all Israel and came to Jerusalem.`

L892:
  - `1CH.21:6 But he did not count Levi and Benjamin among them, for the king'sword was painful to Joab.`
  + `1CH.21:6 But he did not count Levi and Benjamin among them, for the king's word was painful to Joab.`

L895:
  - `1CH.21:9 Then the Lord spoke to Gad, David'sseer, saying,`
  + `1CH.21:9 Then the Lord spoke to Gad, David's seer, saying,`

L903:
  - `1CH.21:17 And David said to God, 'Was it not I who commanded the people to be numbered? I am the one who has sinned and done evil indeed; but these sheep, what have they done? Let Your hand, I pray, O Lord my God, be against me and my father'shouse, but not against Your people that they should be plagued.'`
  + `1CH.21:17 And David said to God, 'Was it not I who commanded the people to be numbered? I am the one who has sinned and done evil indeed; but these sheep, what have they done? Let Your hand, I pray, O Lord my God, be against me and my father's house, but not against Your people that they should be plagued.'`

L956:
  - `1CH.23:11 Jahath was the first, and Zizah the second. As for Jeush and Beriah, they did not multiply sons, and they became but one reckoning, according to their father'shouse.`
  + `1CH.23:11 Jahath was the first, and Zizah the second. As for Jeush and Beriah, they did not multiply sons, and they became but one reckoning, according to their father's house.`

L988:
  - `1CH.24:6 And the scribe, Shemaiah the son of Nethanel, one of the Levites, wrote them down before the king, the leaders, Zadok the priest, Ahimelech the son of Abiathar, and the heads of the fathers' houses of the priests and Levites, one father'shouse taken for Eleazar and one for Ithamar.`
  + `1CH.24:6 And the scribe, Shemaiah the son of Nethanel, one of the Levites, wrote them down before the king, the leaders, Zadok the priest, Ahimelech the son of Abiathar, and the heads of the fathers' houses of the priests and Levites, one father's house taken for Eleazar and one for Ithamar.`

L1026:
  - `1CH.25:5 All these were the sons of Heman the king'schief musician in the words of God, to lift up the horn. And God gave to Heman fourteen sons and three daughters.`
  + `1CH.25:5 All these were the sons of Heman the king's chief musician in the words of God, to lift up the horn. And God gave to Heman fourteen sons and three daughters.`

L1063:
  - `1CH.26:6 Also to Shemaiah his son were sons born from the firstborn Roshai in his father'shouse, because they were men of great ability.`
  + `1CH.26:6 Also to Shemaiah his son were sons born from the firstborn Roshai in his father's house, because they were men of great ability.`

L1070:
  - `1CH.26:13 And they cast lots for each gate, the small as well as the great, according to their father'shouse.`
  + `1CH.26:13 And they cast lots for each gate, the small as well as the great, according to their father's house.`

L1118:
  - `1CH.27:18 over Judah, Elihu, one of David'sbrothers; over Issachar, Omri the son of Michael;`
  + `1CH.27:18 over Judah, Elihu, one of David's brothers; over Issachar, Omri the son of Michael;`

L1128:
  - `1CH.27:25 And Azmaveth the son of Adiel was over the king'streasuries; and Jehonathan the son of Uzziah was over the storehouses in the field, in the cities, in the villages, and in the fortresses.`
  + `1CH.27:25 And Azmaveth the son of Adiel was over the king's treasuries; and Jehonathan the son of Uzziah was over the storehouses in the field, in the cities, in the villages, and in the fortresses.`

L1134:
  - `1CH.27:31 and Jaziz the Hagrite was over the flocks. All these were the officials over King David'sproperty.`
  + `1CH.27:31 and Jaziz the Hagrite was over the flocks. All these were the officials over King David's property.`

L1135:
  - `1CH.27:32 Also Jehonathan, David'suncle, was acounselor, a wise man and ascribe; and Jehiel the son of Hachmoni was with the king'ssons.`
  + `1CH.27:32 Also Jehonathan, David's uncle, was acounselor, a wise man and ascribe; and Jehiel the son of Hachmoni was with the king's sons.`

L1136:
  - `1CH.27:33 Ahithophel was the king'scounselor, and Hushai was the king'sbest friend.`
  + `1CH.27:33 Ahithophel was the king's counselor, and Hushai was the king's best friend.`

L1140:
  - `1CH.27:34 After Ahithophel was Jehoiada the son of Benaiah, then Abiathar. And the general of the king'sarmy was Joab.`
  + `1CH.27:34 After Ahithophel was Jehoiada the son of Benaiah, then Abiathar. And the general of the king's army was Joab.`

L1174:
  - `1CH.29:6 Then the heads of the families, the princes of the sons of Israel, and the captains of thousands and of hundreds, with the officers over the king'swork, offered willingly.`
  + `1CH.29:6 Then the heads of the families, the princes of the sons of Israel, and the captains of thousands and of hundreds, with the officers over the king's work, offered willingly.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 1CH.1:21 | `and the sons of Madiam: Gephar, and Opher, and Eno...` |
| 1CH.3:2 | `the third, Absalom the son of Maacah, the daughter...` |
| 1CH.3:3 | `the fifth, Shephatiah, by Abital; the sixth, Ithre...` |
| 1CH.3:18 | `and Malchiram, Pedaiah, Shenazzar, Jecamiah, Hosha...` |
| 1CH.3:20 | `and Hashubah, Ohel, Berechiah, Hasadiah, and Jusha...` |
| 1CH.4:4 | `and Penuel was the father of Gedor, and Ezer was t...` |
| 1CH.4:14 | `and Meonothai who begot Ophrah. Seraiah begot Joab...` |
| 1CH.4:22 | `also Jokim, and the men of Chozeba and Joash and S...` |
| 1CH.4:33 | `and all their villages were round about these citi...` |
| 1CH.4:38 | `these mentioned by name were leaders in their fami...` |
| 1CH.5:2 | `for Judah was able to prevail over his brothers, a...` |
| 1CH.5:6 | `and Beerah his son, whom Tiglath-Pileser, king of ...` |
| 1CH.5:8 | `and Bela the son of Azaz, the son of Shema, the so...` |
| 1CH.5:13 | `and their brethren according to the house of their...` |
| 1CH.5:22 | `for many fell dead, because the war was of God. An...` |
| 1CH.6:5 | `of Gershon were Libni his son, Jahath his son, Zim...` |
| 1CH.6:19 | `the son of Elkanah, the son of Jeroham, the son of...` |
| 1CH.6:20 | `the son of Zuph, the son of Elkanah, the son of Ma...` |
| 1CH.6:21 | `the son of Elkanah, the son of Joel, the son of Az...` |
| 1CH.6:22 | `the son of Tahath, the son of Assir, the son of Eb...` |
| 1CH.6:23 | `the son of Izhar, the son of Kohath, the son of Le...` |
| 1CH.6:25 | `the son of Michael, the son of Baaseiah, the son o...` |
| 1CH.6:26 | `the son of Ethni, the son of Zerah, the son of Ada...` |
| 1CH.6:27 | `the son of Ethan, the son of Zimmah, the son of Sh...` |
| 1CH.6:28 | `the son of Jahath, the son of Gershon, the son of ...` |
| 1CH.6:30 | `the son of Hashabiah, the son of Amaziah, the son ...` |
| 1CH.6:31 | `the son of Amzi, the son of Bani, the son of Shame...` |
| 1CH.6:32 | `the son of Mahli, the son of Mushi, the son of Mer...` |
| 1CH.7:25 | `and Rephah was his son, as well as Resheph, and Te...` |
| 1CH.7:29 | `and by the borders of the children of Manasseh wer...` |
| 1CH.8:13 | `and Beriah and Shema, who were heads of their fath...` |
| 1CH.8:32 | `and Mikloth, who begot Shimeah. They also dwelt al...` |
| 1CH.9:2 | `and those who dwelled formerly with their possessi...` |
| 1CH.9:9 | `and their brethren, according to their generations...` |
| 1CH.9:13 | `and their brethren, heads of the houses of their f...` |
| 1CH.10:12 | `all the valiant men arose from Gilead and took the...` |
| 1CH.11:34 | `the sons of Hashem the Gizonite, Jonathan the son ...` |
| 1CH.12:2 | `being armed with bows for shooting arrows and usin...` |
| 1CH.12:8 | `and Joelah and Zebadiah, the sons of Jeroham of Ge...` |
| 1CH.12:25 | `of the sons of Judah bearing shield and spear, six...` |
| 1CH.12:26 | `of the sons of Simeon, mighty men of valor fit for...` |
| 1CH.12:27 | `of the sons of Levi, four thousand six hundred;...` |
| 1CH.12:30 | `of the sons of Benjamin, relatives of Saul, three ...` |
| 1CH.12:31 | `of the sons of Ephraim, twenty thousand eight hund...` |
| 1CH.12:32 | `of the half-tribe of Manasseh, eighteen thousand w...` |
| 1CH.12:33 | `of the sons of Issachar who had understanding of t...` |
| 1CH.12:34 | `of Zebulun, there were fifty thousand who went out...` |
| 1CH.12:35 | `of Naphtali, one thousand captains, and with them ...` |
| 1CH.12:36 | `of the Danites who could keep battle formation, tw...` |
| 1CH.12:37 | `of Asher, those who could go out to war, able to k...` |
| 1CH.12:38 | `of the Reubenites and the Gadites and the half-tri...` |
| 1CH.15:5 | `of the sons of Kohath, Uriel the chief, and one hu...` |
| 1CH.15:6 | `of the sons of Merari, Asaiah the chief, and two h...` |
| 1CH.15:7 | `of the sons of Gershom, Joel the chief, and one hu...` |
| 1CH.15:8 | `of the sons of Elizaphan, Shemaiah the chief, and ...` |
| 1CH.15:9 | `of the sons of Hebron, Eliel the chief, and eighty...` |
| 1CH.15:10 | `of the sons of Uzziel, Amminadab the chief, and on...` |
| 1CH.15:18 | `and with them their brethren of the second rank: Z...` |
| 1CH.15:19 | `the singers, Heman, Asaph, and Ethan, were to soun...` |
| 1CH.16:39 | `to offer whole burnt offerings to the Lord on the ...` |
| 1CH.16:41 | `and with them Heman and Jeduthun, to sound aloud w...` |
| 1CH.17:5 | `for I have not dwelt in a house from the day I bro...` |
| 1CH.17:6 | `in all the places through which I went with all Is...` |
| 1CH.17:10 | `and from the days when I appointed judges to be ov...` |
| 1CH.17:24 | `saying, 'O Lord, O Lord, the Almighty is the God o...` |
| 1CH.18:10 | `he sent Hadoram his son, to King David to ask him ...` |
| 1CH.21:12 | `either three years of famine, or that you flee for...` |
| 1CH.22:4 | `and cedar trees in abundance; for the Sidonians an...` |
| 1CH.23:5 | `four thousand were gatekeepers, and four thousand ...` |
| 1CH.23:29 | `for the showbread and fine flour for the meat offe...` |
| 1CH.23:30 | `to stand every morning to thank and praise the Lor...` |
| 1CH.23:31 | `and regularly before the Lord-at every presentatio...` |
| 1CH.24:8 | `the third to Harim, the fourth to Seorim,...` |
| 1CH.24:9 | `the fifth to Malchijah, the sixth to Mijamin,...` |
| 1CH.24:10 | `the seventh to Hakkoz, the eighth to Abijah,...` |
| 1CH.24:11 | `the ninth to Jeshua, the tenth to Shecaniah,...` |
| 1CH.24:12 | `the eleventh to Eliashib, the twelfth to Jakim,...` |
| 1CH.24:13 | `the thirteenth to Huppah, the fourteenth to Jesheb...` |
| 1CH.24:14 | `the fifteenth to Bilgah, the sixteenth to Immer,...` |
| 1CH.24:15 | `the seventeenth to Hezir, the eighteenth to Happiz...` |
| 1CH.24:16 | `the nineteenth to Pethahiah, the twentieth to Jehe...` |
| 1CH.24:17 | `the twenty-first to Jachin, the twenty-second to G...` |
| 1CH.24:18 | `the twenty-third to Delaiah, the twenty-fourth to ...` |
| 1CH.25:2 | `of the sons of Asaph: Zaccur, Joseph, Nethaniah, a...` |
| 1CH.25:10 | `the third for Zaccur, his sons and his brethren, t...` |
| 1CH.25:11 | `the fourth for Jizri, his sons and his brethren, t...` |
| 1CH.25:12 | `the fifth for Nethaniah, his sons and his brethren...` |
| 1CH.25:13 | `the sixth for Bukkiah, his sons and his brethren, ...` |
| 1CH.25:14 | `the seventh for Jesharelah, his sons and his breth...` |
| 1CH.25:15 | `the eighth for Jeshaiah, his sons and his brethren...` |
| 1CH.25:16 | `the ninth for Mattaniah, his sons and his brethren...` |
| 1CH.25:17 | `the tenth for Shimei, his sons and his brethren, t...` |
| 1CH.25:18 | `the eleventh for Azarel, his sons and his brethren...` |
| 1CH.25:19 | `the twelfth for Hashabiah, his sons and his brethr...` |
| 1CH.25:20 | `the thirteenth for Shubael, his sons and his breth...` |
| 1CH.25:21 | `the fourteenth for Mattithiah, his sons and his br...` |
| 1CH.25:22 | `the fifteenth for Jeremoth, his sons and his breth...` |
| 1CH.25:23 | `the sixteenth for Hananiah, his sons and his breth...` |
| 1CH.25:24 | `the seventeenth for Joshbekashah, his sons and his...` |
| 1CH.25:25 | `the eighteenth for Hanani, his sons and his brethr...` |
| 1CH.25:26 | `the nineteenth for Mallothi, his sons and his bret...` |
| 1CH.25:27 | `the twentieth for Eliathah, his sons and his breth...` |
| 1CH.25:28 | `the twenty-first for Hothir, his sons and his bret...` |
| 1CH.25:29 | `the twenty-second for Giddalti, his sons and his b...` |
| 1CH.25:30 | `the twenty-third for Mahazioth, his sons and his b...` |
| 1CH.25:31 | `the twenty-fourth for Romamti-Ezer, his sons and h...` |
| 1CH.26:15 | `to Obed-Edom the South Gate opposite the storehous...` |
| 1CH.27:3 | `he was of the children of Perez and the chief of a...` |
| 1CH.27:17 | `over the Levites, Hashabiah the son of Kemuel; ove...` |
| 1CH.27:18 | `over Judah, Elihu, one of David'sbrothers; over Is...` |
| 1CH.27:19 | `over Zebulun, Ishmaiah the son of Obadiah; over Na...` |
| 1CH.27:20 | `over the children of Ephraim, Hoshea the son of Az...` |
| 1CH.27:21 | `over the halftribe of Manasseh in Gilead, Iddo the...` |
| 1CH.27:22 | `over Dan, Azarel the son of Jeroham. These were th...` |
| 1CH.27:31 | `and Jaziz the Hagrite was over the flocks. All the...` |
| 1CH.28:12 | `and the plans that he had in his mind concerning t...` |
| 1CH.28:13 | `also for the quarters for the daily priests and th...` |
| 1CH.28:15 | `he gave to him the weight of the lamps and of the ...` |
| 1CH.28:17 | `also for the forks, the basins, the pitchers of go...` |
| 1CH.28:18 | `and the weight of the altar for burning incense ma...` |
| 1CH.29:5 | `by the hands of craftsmen. And who this day zealou...` |
| 1CH.29:27 | `forty years, in Hebron for seven years and in Jeru...` |
