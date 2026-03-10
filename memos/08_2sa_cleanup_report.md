# 2 Samuel Cleanup Report — 2026-03-09

## Summary
- Input: `staging/validated/OT/2SA.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 104

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 119 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 22 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L33:
  - `2SA.1:14 So David said to him, 'How was it you were not afraid to put forth your hand to destroy the Lord'sanointed?'`
  + `2SA.1:14 So David said to him, 'How was it you were not afraid to put forth your hand to destroy the Lord's anointed?'`

L38:
  - `2SA.1:16 And David said to him, 'Your blood is on your own head, for your own mouth spoke against you, saying, 'I killed the Lord'sanointed.' '`
  + `2SA.1:16 And David said to him, 'Your blood is on your own head, for your own mouth spoke against you, saying, 'I killed the Lord's anointed.' '`

L59:
  - `2SA.2:5 So David sent messengers to the rulers of Jabesh Gilead and said to them, 'You are blessed of the Lord, for you have shown this mercy to your lord, upon Saul, the Lord'sanointed, and you have buried him and his son Jonathan.`
  + `2SA.2:5 So David sent messengers to the rulers of Jabesh Gilead and said to them, 'You are blessed of the Lord, for you have shown this mercy to your lord, upon Saul, the Lord's anointed, and you have buried him and his son Jonathan.`

L65:
  - `2SA.2:8 But Abner the son of Ner, commander of Saul'sarmy, took Ishbosheth the son of Saul and brought him from the camp to Mahanaim.`
  + `2SA.2:8 But Abner the son of Ner, commander of Saul's army, took Ishbosheth the son of Saul and brought him from the camp to Mahanaim.`

L92:
  - `2SA.2:32 Then they took up Asahel and buried him in his father'stomb in Bethlehem. And Joab and his men traveled with him throughout the night and came to Hebron at daybreak.`
  + `2SA.2:32 Then they took up Asahel and buried him in his father's tomb in Bethlehem. And Joab and his men traveled with him throughout the night and came to Hebron at daybreak.`

L102:
  - `2SA.3:5 and the sixth, Ithream, by David'swife Eglah. These were born to David in Hebron.`
  + `2SA.3:5 and the sixth, Ithream, by David's wife Eglah. These were born to David in Hebron.`

L104:
  - `2SA.3:7 And Saul had a concubine, Rizpah, the daughter of Aiah; and Mephibosheth, son of Saul, said to Abner, 'Why did you go in to my father'sconcubine?'`
  + `2SA.3:7 And Saul had a concubine, Rizpah, the daughter of Aiah; and Mephibosheth, son of Saul, said to Abner, 'Why did you go in to my father's concubine?'`

L105:
  - `2SA.3:8 Then Abner became very angry at Mephibosheth'swords, and Abner said to him, 'Am I a dog'shead? Today I brought about mercy on the house of Saul your father, his brothers, and his friends, and have not shifted loyalties to the house of David. And you on this very day seek fault against me on behalf of an unrighteous wife.`
  + `2SA.3:8 Then Abner became very angry at Mephibosheth's words, and Abner said to him, 'Am I a dog's head? Today I brought about mercy on the house of Saul your father, his brothers, and his friends, and have not shifted loyalties to the house of David. And you on this very day seek fault against me on behalf of an unrighteous wife.`

L111:
  - `2SA.3:14 So David sent messengers to Mephibosheth, Saul'sson, saying, 'Give me my wife Michal, whom I received for a hundred foreskins of the Philistines.'`
  + `2SA.3:14 So David sent messengers to Mephibosheth, Saul's son, saying, 'Give me my wife Michal, whom I received for a hundred foreskins of the Philistines.'`

L126:
  - `2SA.3:26 And Joab went from David'spresence and sent messengers after Abner, who brought him back from the well of Sirah. But David did not know of this.`
  + `2SA.3:26 And Joab went from David's presence and sent messengers after Abner, who brought him back from the well of Sirah. But David did not know of this.`

L127:
  - `2SA.3:27 When Abner returned to Hebron, Joab turned him aside at the gate to speak with him privately. There an ambush awaited him. Joab stabbed him in the loins, and Abner died for the blood of Asahel, Joab'sbrother.`
  + `2SA.3:27 When Abner returned to Hebron, Joab turned him aside at the gate to speak with him privately. There an ambush awaited him. Joab stabbed him in the loins, and Abner died for the blood of Asahel, Joab's brother.`

L129:
  - `2SA.3:29 Let it rest on Joab'shead and on all his father'shouse. And let there never be a time in the house of Joab when it will be found free of one suffering from gonorrhea, or a leper, or one that leans on a staff, or falls by the sword, or lacks bread.'`
  + `2SA.3:29 Let it rest on Joab's head and on all his father's house. And let there never be a time in the house of Joab when it will be found free of one suffering from gonorrhea, or a leper, or one that leans on a staff, or falls by the sword, or lacks bread.'`

L150:
  - `2SA.4:2 Now Saul'sson, Mephibosheth, had two men who were captains over the troops. The name of one was Baanah and the name of the other Rechab, sons of Rimmon the Beerothite, of the sons of Benjamin; for Beeroth was considered as one of the sons of Benjamin.`
  + `2SA.4:2 Now Saul's son, Mephibosheth, had two men who were captains over the troops. The name of one was Baanah and the name of the other Rechab, sons of Rimmon the Beerothite, of the sons of Benjamin; for Beeroth was considered as one of the sons of Benjamin.`

L208:
  - `2SA.6:6 And when they came to Nachon'sthreshing-floor, Uzzah placed his hand on the ark of God to hold it steady when the oxen shook it out of its place.`
  + `2SA.6:6 And when they came to Nachon's threshing-floor, Uzzah placed his hand on the ark of God to hold it steady when the oxen shook it out of its place.`

L218:
  - `2SA.6:16 Now as the ark came into the City of David, Michal, Saul'sdaughter, looked through a window and saw King David dancing and playing instruments before the Lord, and she despised him in her heart.`
  + `2SA.6:16 Now as the ark came into the City of David, Michal, Saul's daughter, looked through a window and saw King David dancing and playing instruments before the Lord, and she despised him in her heart.`

L270:
  - `2SA.8:2 Then David defeated Moab, and after forcing them down to the ground, he measured them off with lines. With two lines he measured off those to be put to death, and with two lines those to be kept alive. So the Moabites became David'sservants and brought tribute.`
  + `2SA.8:2 Then David defeated Moab, and after forcing them down to the ground, he measured them off with lines. With two lines he measured off those to be put to death, and with two lines those to be kept alive. So the Moabites became David's servants and brought tribute.`

L274:
  - `2SA.8:6 Then David put garrisons in Syria of Damascus, and the Syrians became David'sservants and brought tribute. The Lord saved David wherever he went.`
  + `2SA.8:6 Then David put garrisons in Syria of Damascus, and the Syrians became David's servants and brought tribute. The Lord saved David wherever he went.`

L282:
  - `2SA.8:14 He also put garrisons in Idumea, throughout all Idumea, and all the Idumeans became the king'sservants. And the Lord preserved David wherever he went.`
  + `2SA.8:14 He also put garrisons in Idumea, throughout all Idumea, and all the Idumeans became the king's servants. And the Lord preserved David wherever he went.`

L289:
  - `2SA.8:18 Benaiah the son of Jehoiada was an advisor, as were the Cherethites and the Pelethites; and David'ssons were chief ministers.`
  + `2SA.8:18 Benaiah the son of Jehoiada was an advisor, as were the Cherethites and the Pelethites; and David's sons were chief ministers.`

L300:
  - `2SA.9:9 And the king called to Ziba, Saul'sservant, and said to him, 'I have given your master'sson everything that belonged to Saul and to all his house.`
  + `2SA.9:9 And the king called to Ziba, Saul's servant, and said to him, 'I have given your master's son everything that belonged to Saul and to all his house.`

L678:
  - `2SA.19:22 But Abishai the son of Zeruiah spoke up and said, 'Shall not Shimei be put to death for this, because he cursed the Lord'sanointed?'`
  + `2SA.19:22 But Abishai the son of Zeruiah spoke up and said, 'Shall not Shimei be put to death for this, because he cursed the Lord's anointed?'`

L688:
  - `2SA.19:29 For all my father'shouse were but dead men before my lord the king. Yet you set your servant among those who eat at your own table. Therefore what right do I still have to cry out any more to the king?'`
  + `2SA.19:29 For all my father's house were but dead men before my lord the king. Yet you set your servant among those who eat at your own table. Therefore what right do I still have to cry out any more to the king?'`

L707:
  - `2SA.19:42 And behold, all the men of Israel came to the king and said to him, 'Why did our brethren, the men of Judah, steal you away and bring the king, his household, and all David'smen with him across the Jordan?'`
  + `2SA.19:42 And behold, all the men of Israel came to the king and said to him, 'Why did our brethren, the men of Judah, steal you away and bring the king, his household, and all David's men with him across the Jordan?'`

L708:
  - `2SA.19:43 So all the men of Judah answered the men of Israel, 'Because the king is aclose relative of ours. Why then are you angry over this matter? Have we ever eaten at the king'sexpense? Or has he given us any gift?'`
  + `2SA.19:43 So all the men of Judah answered the men of Israel, 'Because the king is aclose relative of ours. Why then are you angry over this matter? Have we ever eaten at the king's expense? Or has he given us any gift?'`

L720:
  - `2SA.20:6 And David said to Abishai, 'Now Sheba the son of Bichri will do us more harm than Absalom. Take your lord'sservants with you and pursue him so that he does not fortify cities for himself and escape from our sight.'`
  + `2SA.20:6 And David said to Abishai, 'Now Sheba the son of Bichri will do us more harm than Absalom. Take your lord's servants with you and pursue him so that he does not fortify cities for himself and escape from our sight.'`

L721:
  - `2SA.20:7 So Joab'smen with the Cherethites, the Pelethites, and all the mighty men went out after him. They went out of Jerusalem to pursue Sheba the son of Bichri.`
  + `2SA.20:7 So Joab's men with the Cherethites, the Pelethites, and all the mighty men went out after him. They went out of Jerusalem to pursue Sheba the son of Bichri.`

L724:
  - `2SA.20:10 But Amasa did not notice the sword that was in Joab'shand. And he struck him with it in the stomach, and his entrails poured out on the ground. He did not strike him again, and he died.`
  + `2SA.20:10 But Amasa did not notice the sword that was in Joab's hand. And he struck him with it in the stomach, and his entrails poured out on the ground. He did not strike him again, and he died.`

L725:
  - `2SA.20:11 Then Joab and Abishai his brother pursued Sheba the son of Bichri. Meanwhile one of Joab'sservants stood near him and said, 'Whoever favors Joab and whoever is for Davidfollow Joab!'`
  + `2SA.20:11 Then Joab and Abishai his brother pursued Sheba the son of Bichri. Meanwhile one of Joab's servants stood near him and said, 'Whoever favors Joab and whoever is for Davidfollow Joab!'`

L755:
  - `2SA.21:7 And the king said, 'I will give them.' But the king spared Mephibosheth, the son of Jonathan, the son of Saul, because of the Lord'soath between David and Jonathan the son of Saul.`
  + `2SA.21:7 And the king said, 'I will give them.' But the king spared Mephibosheth, the son of Jonathan, the son of Saul, because of the Lord's oath between David and Jonathan the son of Saul.`

L760:
  - `2SA.21:12 Then David went and took Saul'sbones and the bones of Jonathan his son. He took them from the men of Jabesh Gilead, who stole them from the square of Beth Shan where the Philistines put them, on the day the Philistines struck down Saul in Gilboa.`
  + `2SA.21:12 Then David went and took Saul's bones and the bones of Jonathan his son. He took them from the men of Jabesh Gilead, who stole them from the square of Beth Shan where the Philistines put them, on the day the Philistines struck down Saul in Gilboa.`

L765:
  - `2SA.21:14 And they buried Saul'sbones and the bones of Jonathan his son and the bones of those who were hanged in the country of Benjamin, in Zelah beside the tomb of Kish his father. So they did everything the king commanded. And after that God heeded the prayer for the land.`
  + `2SA.21:14 And they buried Saul's bones and the bones of Jonathan his son and the bones of those who were hanged in the country of Benjamin, in Zelah beside the tomb of Kish his father. So they did everything the king commanded. And after that God heeded the prayer for the land.`

L768:
  - `2SA.21:17 But Abishai the son of Zeruiah came to his aid and struck the Philistine and killed him. Then David'smen swore to him, saying, 'You shall no longer go out with us to battle, that you do not quench the lamp of Israel.'`
  + `2SA.21:17 But Abishai the son of Zeruiah came to his aid and struck the Philistine and killed him. Then David's men swore to him, saying, 'You shall no longer go out with us to battle, that you do not quench the lamp of Israel.'`

L770:
  - `2SA.21:19 And there was war at Gob with the Philistines, where Elhanan the son of Jaare-Oregim the Bethlehemite killed Goliath the Gittite, whose spear had ashaft like a weaver'sbeam.`
  + `2SA.21:19 And there was war at Gob with the Philistines, where Elhanan the son of Jaare-Oregim the Bethlehemite killed Goliath the Gittite, whose spear had ashaft like a weaver's beam.`

L858:
  - `2SA.23:8 The names of David'smighty men were, first, Jebosheth the Canaanite, chief among the three. The second was called Adino the Eznite. He drew his sword against eight hundred men at one time and killed them.`
  + `2SA.23:8 The names of David's mighty men were, first, Jebosheth the Canaanite, chief among the three. The second was called Adino the Eznite. He drew his sword against eight hundred men at one time and killed them.`

L877:
  - `2SA.23:21 And he killed an Egyptian man, ahandsome man. The Egyptian had a spear in his hand like the wood of a ladder, so he went down to him with a staff, snatched the spear from the Egyptian'shand, and killed him with his own spear.`
  + `2SA.23:21 And he killed an Egyptian man, ahandsome man. The Egyptian had a spear in his hand like the wood of a ladder, so he went down to him with a staff, snatched the spear from the Egyptian's hand, and killed him with his own spear.`

L880:
  - `2SA.23:24 And the names of King David'smighty men were Asahel the brother of Joab, one of the thirty; Elhanan the son of Dodo, David'suncle, of Bethlehem;`
  + `2SA.23:24 And the names of King David's mighty men were Asahel the brother of Joab, one of the thirty; Elhanan the son of Dodo, David's uncle, of Bethlehem;`

L905:
  - `2SA.24:4 Nevertheless, the king'sword prevailed against Joab and against the captains of the army. Therefore Joab and the captains of the army went out before the king to inspect the people of Israel.`
  + `2SA.24:4 Nevertheless, the king's word prevailed against Joab and against the captains of the army. Therefore Joab and the captains of the army went out before the king to inspect the people of Israel.`

L917:
  - `2SA.24:10 And David'sheart condemned him after he had numbered the people. So David said to the Lord, 'I sinned greatly in what I did. But now, I pray, O Lord, take away the iniquity of Your servant, for I have done very foolishly.'`
  + `2SA.24:10 And David's heart condemned him after he had numbered the people. So David said to the Lord, 'I sinned greatly in what I did. But now, I pray, O Lord, take away the iniquity of Your servant, for I have done very foolishly.'`

L918:
  - `2SA.24:11 Now when David arose in the morning, the word of the Lord came to the prophet Gad, David'sseer, saying,`
  + `2SA.24:11 Now when David arose in the morning, the word of the Lord came to the prophet Gad, David's seer, saying,`

L927:
  - `2SA.24:17 Then David spoke to the Lord when he saw the angel who was striking the people, and he said, 'I am the shepherd and I have done wickedly, but these sheep-what have they done? Let Your hand, I pray, be against me and against my father'shouse.'`
  + `2SA.24:17 Then David spoke to the Lord when he saw the angel who was striking the people, and he said, 'I am the shepherd and I have done wickedly, but these sheep-what have they done? Let Your hand, I pray, be against me and against my father's house.'`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 2SA.1:18 | `and he told them to teach the children of Judah; i...` |
| 2SA.2:13 | `and Joab the son of Zeruiah and the servants of Da...` |
| 2SA.3:3 | `his second, Chileab, by Abigail the widow of Nabal...` |
| 2SA.3:4 | `the fourth, Adonijah the son of Haggith; the fifth...` |
| 2SA.3:5 | `and the sixth, Ithream, by David'swife Eglah. Thes...` |
| 2SA.3:10 | `to transfer the kingdom from the house of Saul, an...` |
| 2SA.4:10 | `when someone told me, 'Look, Saul is dead,' believ...` |
| 2SA.6:4 | `with the ark, and his brothers went before the ark...` |
| 2SA.7:2 | `the king said to Nathan the prophet, 'See now, I n...` |
| 2SA.7:7 | `wherever I went with all of Israel. In that time, ...` |
| 2SA.7:11 | `since the days I appointed judges over My people I...` |
| 2SA.7:22 | `to magnify You. O Lord, my Lord, according to all ...` |
| 2SA.8:12 | `from Idumea, from Moab, from the sons of Ammon, fr...` |
| 2SA.11:19 | `and charged the messenger, saying, 'When you have ...` |
| 2SA.11:20 | `if the king'swrath rises and he says to you, 'Why ...` |
| 2SA.12:25 | `and He sent word by the hand of Nathan the prophet...` |
| 2SA.16:6 | `casting stones at David and all the servants of Da...` |
| 2SA.19:7 | `because you love those who hate you and hate those...` |
| 2SA.20:26 | `and Ira the Jairite was a priest of David....` |
| 2SA.21:9 | `and he delivered them into the hands of the Gibeon...` |
| 2SA.23:39 | `and Uriah the Hittite. These were thirty-seven in ...` |
| 2SA.24:7 | `and they came to Mapsar of Tyre and all the cities...` |
