# 2 Ezra Cleanup Report — 2026-03-09

## Summary
- Input: `staging/validated/OT/EZR.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 11

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 12 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 112 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L94:
  - `EZR.2:59 And these came up from Tel Melah, Tel Harsha, Cherub, Addan, and Immer; but they could not identify their father'shouse or their seed, whether it was of Israel:`
  + `EZR.2:59 And these came up from Tel Melah, Tel Harsha, Cherub, Addan, and Immer; but they could not identify their father's house or their seed, whether it was of Israel:`

L125:
  - `EZR.3:12 But many of the priests and the Levites and the elders and the heads of the father'shouses, who had seen the first temple on its foundation and with their own eyes saw this house, wept with aloud voice. But the multitude, shouting with joy and gladness, lifted up their voices in song,`
  + `EZR.3:12 But many of the priests and the Levites and the elders and the heads of the father's houses, who had seen the first temple on its foundation and with their own eyes saw this house, wept with aloud voice. But the multitude, shouting with joy and gladness, lifted up their voices in song,`

L133:
  - `EZR.4:2 they approached Zerubbabel and the heads of the father'shouses and said to them, 'We will rebuild with you, for we seek as you do, and we have sacrificed to Him since the days of Esarhaddon king of Assyria, who brought us here.'`
  + `EZR.4:2 they approached Zerubbabel and the heads of the father's houses and said to them, 'We will rebuild with you, for we seek as you do, and we have sacrificed to Him since the days of Esarhaddon king of Assyria, who brought us here.'`

L134:
  - `EZR.4:3 But Zerubbabel and Jeshua and the rest of the heads of the father'shouses of Israel said to them, 'It is not for us and you to rebuild a house to our God, for we ourselves will rebuild it to the Lord our God, as King Cyrus the king of the Persians commanded us.'`
  + `EZR.4:3 But Zerubbabel and Jeshua and the rest of the heads of the father's houses of Israel said to them, 'It is not for us and you to rebuild a house to our God, for we ourselves will rebuild it to the Lord our God, as King Cyrus the king of the Persians commanded us.'`

L183:
  - `EZR.5:17 Now therefore, if it seems good to the king, let a search be made in the king'streasure house, which is there in Babylon, whether it is so that a decree was issued by King Cyrus to build this house of God at Jerusalem, and let the king send us his pleasure concerning this matter.`
  + `EZR.5:17 Now therefore, if it seems good to the king, let a search be made in the king's treasure house, which is there in Babylon, whether it is so that a decree was issued by King Cyrus to build this house of God at Jerusalem, and let the king send us his pleasure concerning this matter.`

L189:
  - `EZR.6:4 with three rows of heavy stones and one row of new timber. Let the expenses be paid from the king'streasury.`
  + `EZR.6:4 with three rows of heavy stones and one row of new timber. Let the expenses be paid from the king's treasury.`

L193:
  - `EZR.6:8 Moreover I issue a decree as to what you shall do for the elders of these Jews, for the building of this house of God: Let the cost be paid at the king'sexpense from taxes on the region beyond the River; this is to be given immediately to these men, so that they are not hindered.`
  + `EZR.6:8 Moreover I issue a decree as to what you shall do for the elders of these Jews, for the building of this house of God: Let the cost be paid at the king's expense from taxes on the region beyond the River; this is to be given immediately to these men, so that they are not hindered.`

L238:
  - `EZR.7:20 And whatever more may be needed for the house of your God, which you may have occasion to provide, pay for it from the king'streasury.`
  + `EZR.7:20 And whatever more may be needed for the house of your God, which you may have occasion to provide, pay for it from the king's treasury.`

L245:
  - `EZR.7:27 Blessed be the Lord God of our fathers, who has put such a thing as this in the king'sheart, to beautify the house of the Lord which is in Jerusalem,`
  + `EZR.7:27 Blessed be the Lord God of our fathers, who has put such a thing as this in the king's heart, to beautify the house of the Lord which is in Jerusalem,`

L246:
  - `EZR.7:28 and has extended mercy to me before the king and his counselors, and before all the king'smighty princes.`
  + `EZR.7:28 and has extended mercy to me before the king and his counselors, and before all the king's mighty princes.`

L303:
  - `EZR.8:36 And they delivered the king'sorders to the king'ssatraps and the governors in the region beyond the River. So they gave support to the people and the house of God.`
  + `EZR.8:36 And they delivered the king's orders to the king's satraps and the governors in the region beyond the River. So they gave support to the people and the house of God.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| EZR.1:8 | `and Cyrus king of the Persians brought them out by...` |
| EZR.1:10 | `thirty gold bowls, two hundred silver bowls, and o...` |
| EZR.2:4 | `the sons of Shephatiah were three hundred seventy-...` |
| EZR.2:5 | `the sons of A rah were seven hundred seventy-five;...` |
| EZR.2:6 | `the sons of Pahath-Moab belonging to the sons of J...` |
| EZR.2:7 | `the sons of Elam were one thousand two hundred fif...` |
| EZR.2:8 | `the sons of Zattu were nine hundred forty-five;...` |
| EZR.2:9 | `the sons of Zaccai were seven hundred sixty;...` |
| EZR.2:10 | `the sons of Bani were six hundred forty-two;...` |
| EZR.2:11 | `the sons of Bebai were six hundred twenty-three;...` |
| EZR.2:12 | `the sons of Azgad were three thousand two hundred ...` |
| EZR.2:13 | `the sons of Adonikam were six hundred sixty-six;...` |
| EZR.2:14 | `the sons of Bigvai were two thousand fifty-six;...` |
| EZR.2:15 | `the sons of A din were four hundred fifty-four;...` |
| EZR.2:16 | `the sons of Ater belonging to Hezekiah were ninety...` |
| EZR.2:17 | `the sons of Bezai were three hundred twenty-three;...` |
| EZR.2:18 | `the sons of Jorah were one hundred twelve;...` |
| EZR.2:19 | `the sons of Hashum were two hundred twenty-three;...` |
| EZR.2:20 | `the sons of Gibbar were ninety-five;...` |
| EZR.2:21 | `the sons of Bethlehem were one hundred twenty-thre...` |
| EZR.2:22 | `the sons of Netophah were fifty-six;...` |
| EZR.2:23 | `the sons of Anathoth were one hundred twenty-eight...` |
| EZR.2:24 | `the sons of Azmaveth were forty-two;...` |
| EZR.2:25 | `the sons of Kirjath A rim, Chephirah, and Beeroth ...` |
| EZR.2:26 | `the sons of Ramah and Geba were six hundred twenty...` |
| EZR.2:27 | `the men of Michmas were one hundred twentytwo;...` |
| EZR.2:28 | `the men of Bethel and Ai were four hundred twenty-...` |
| EZR.2:29 | `the sons of Nebo were fifty-two;...` |
| EZR.2:30 | `the sons of Magbish were one hundred fifty-six;...` |
| EZR.2:31 | `the sons of Elam were one thousand two hundred fif...` |
| EZR.2:32 | `the sons of Harim were three hundred twenty;...` |
| EZR.2:33 | `the sons of Lod, Aroth, and Ono were seven hundred...` |
| EZR.2:34 | `the sons of Jericho were three hundred forty-five;...` |
| EZR.2:35 | `the sons of Senaah were three thousand six hundred...` |
| EZR.2:36 | `the priests: the sons of Jedaiah belonging to the ...` |
| EZR.2:37 | `the sons of Immer were one thousand fifty-two;...` |
| EZR.2:38 | `the sons of Pashhur were one thousand two hundred ...` |
| EZR.2:39 | `the sons of Harim were one thousand seven;...` |
| EZR.2:40 | `the Levites, the sons of Jesus and Kadmiel, belong...` |
| EZR.2:41 | `the singers: the sons of Asaph were one hundred tw...` |
| EZR.2:42 | `the sons of the gatekeepers: the sons of Shallum, ...` |
| EZR.2:43 | `the Nethinim: the sons of Ziha, the sons of Hasuph...` |
| EZR.2:44 | `the sons of Keros, the sons of Siaha, the sons of ...` |
| EZR.2:45 | `the sons of Lebanah, the sons of Hagabah, the sons...` |
| EZR.2:46 | `the sons of Hagab, the sons of Shalmai, the sons o...` |
| EZR.2:47 | `the sons of Giddel, the sons of Gahar, the sons of...` |
| EZR.2:48 | `the sons of Rezin, the sons of Nekoda, the sons of...` |
| EZR.2:49 | `the sons of Uzza, the sons of Paseah, the sons of ...` |
| EZR.2:50 | `the sons of Asnah, the sons of Meunim, the sons of...` |
| EZR.2:51 | `the sons of Bakbuk, the sons of Hakupha, the sons ...` |
| EZR.2:52 | `the sons of Bazluth, the sons of Mehida, the sons ...` |
| EZR.2:53 | `the sons of Barkos, the sons of Sisera, the sons o...` |
| EZR.2:54 | `the sons of Neziah, and the sons of Hatipha;...` |
| EZR.2:55 | `the sons of Abdeselma: the sons of Sotai, the sons...` |
| EZR.2:56 | `the sons of Jaala, the sons of Darkon, the sons of...` |
| EZR.2:57 | `the sons of Shephatiah, the sons of Hattil, the so...` |
| EZR.2:58 | `all the Nethinim and the sons of Abdeselma were th...` |
| EZR.2:60 | `the sons of Delaiah, the sons of Bua, the sons of ...` |
| EZR.2:61 | `and of the sons of the priests: the sons of Habaia...` |
| EZR.2:65 | `besides their male and female servants, of whom th...` |
| EZR.2:67 | `four hundred thirty-five camels, and six thousand ...` |
| EZR.3:13 | `and the people could not distinguish the shouting ...` |
| EZR.4:2 | `they approached Zerubbabel and the heads of the fa...` |
| EZR.4:5 | `and hiring people to work against them to frustrat...` |
| EZR.4:10 | `and the rest of the nations whom the great and nob...` |
| EZR.4:15 | `that a search may be made in the book of the recor...` |
| EZR.4:19 | `and a command was given by me, and we examined for...` |
| EZR.6:4 | `with three rows of heavy stones and one row of new...` |
| EZR.6:10 | `that they may offer sacrifices of sweet aroma to t...` |
| EZR.7:2 | `the son of Shallum, the son of Zadok, the son of A...` |
| EZR.7:3 | `the son of Amariah, the son of Azariah, the son of...` |
| EZR.7:4 | `the son of Zerahiah, the son of Uzzi, the son of B...` |
| EZR.7:5 | `the son of Abishua, the son of Phinehas, the son o...` |
| EZR.7:6 | `this Ezra came up from Babylon, and he was a skill...` |
| EZR.7:15 | `and whereas you are to carry the silver and gold w...` |
| EZR.7:16 | `and whereas all the silver and gold that you may f...` |
| EZR.7:17 | `now therefore, be careful to buy with this money b...` |
| EZR.7:22 | `up to one hundred talents of silver, one hundred k...` |
| EZR.7:28 | `and has extended mercy to me before the king and h...` |
| EZR.8:2 | `of the sons of Phinehas, Gershom; of the sons of I...` |
| EZR.8:3 | `of the sons of Shecaniah, of the sons of Parosh, Z...` |
| EZR.8:4 | `of the sons of PahathMoab, Eliehoenai the son of Z...` |
| EZR.8:5 | `of the sons of Zathoe, Shechaniah, the son of Jaha...` |
| EZR.8:6 | `of the sons of A din, Ebed the son of Jonathan, an...` |
| EZR.8:7 | `of the sons of Elam, Jeshaiah the son of Athaliah,...` |
| EZR.8:8 | `of the sons of Shephatiah, Zebadiah the son of Mic...` |
| EZR.8:9 | `of the sons of Joab, Obadiah the son of Jehiel, an...` |
| EZR.8:10 | `of the sons of Shelomith, the son of Josiphiah, an...` |
| EZR.8:11 | `of the sons of Bebai, Zechariah the son of Bebai, ...` |
| EZR.8:12 | `of the sons of Azgad, Johanan the son of Hakkatan,...` |
| EZR.8:13 | `of the last sons of Adonikam, whose names are thes...` |
| EZR.8:14 | `also of the sons of Bigvai and Uthai, and with him...` |
| EZR.8:19 | `and Hashabiah, and Jeshaiah of the sons of Merari,...` |
| EZR.8:20 | `and from the temple servants of the Levites, whom ...` |
| EZR.8:25 | `and weighed out to them the silver, gold, and the ...` |
| EZR.8:27 | `twenty gold basins worth a thousand drachmas, and ...` |
| EZR.8:34 | `with the number and weight of everything. All the ...` |
| EZR.9:6 | `and I said, 'O Lord, I am too ashamed and embarras...` |
| EZR.9:11 | `which You gave us by Your servants the prophets, s...` |
| EZR.9:14 | `even though we kept breaking Your commandments and...` |
| EZR.10:8 | `and that whoever would not come within three days,...` |
| EZR.10:21 | `of the sons of Harim: Maaseiah, Elijah, Shemaiah, ...` |
| EZR.10:22 | `of the sons of Pashhur: Elioenai, Maaseiah, Ishmae...` |
| EZR.10:26 | `of the sons of Elam: Mattaniah, Zechariah, Jehiel,...` |
| EZR.10:27 | `of the sons of Zattu: Elioenai, Eliashib, Mattania...` |
| EZR.10:28 | `of the sons of Bebai: Jehohanan, Hananiah, Zabbai,...` |
| EZR.10:29 | `of the sons of Bani: Meshullam, Malluch, Adaiah, J...` |
| EZR.10:30 | `of the sons of PahathMoab: Adna, Chelal, Benaiah, ...` |
| EZR.10:31 | `of the sons of Harim: Eliezer, Ishijah, Malchijah,...` |
| EZR.10:33 | `of the sons of Hashum: Mattenai, Mattattah, Zabad,...` |
| EZR.10:34 | `of the sons of Bani: Maadai, Amram, Uel,...` |
| EZR.10:43 | `of the sons of Nebo: Jeiel, Mattithiah, Zebed, Zeb...` |
