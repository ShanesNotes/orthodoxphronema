# 1 Samuel Cleanup Report — 2026-03-09

## Summary
- Input: `staging/validated/OT/1SA.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 50

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 54 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 20 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L41:
  - `1SA.1:19 Then they rose early in the morning and worshiped the Lord and went on their way back to Elkanah'shouse at Ramathaim. And he knew Hannah his wife, and the Lord remembered her.`
  + `1SA.1:19 Then they rose early in the morning and worshiped the Lord and went on their way back to Elkanah's house at Ramathaim. And he knew Hannah his wife, and the Lord remembered her.`

L84:
  - `1SA.2:25 If one man sins against another, they will pray to the Lord for him. But if a man sins against the Lord, who will pray for him?' Nevertheless they did not heed their father'svoice, so the Lord desired to destroy them.`
  + `1SA.2:25 If one man sins against another, they will pray to the Lord for him. But if a man sins against the Lord, who will pray for him?' Nevertheless they did not heed their father's voice, so the Lord desired to destroy them.`

L86:
  - `1SA.2:27 Then a man of God came to Eli and said to him, 'Thus says the Lord, 'I clearly revealed Myself to the house of your father when they were slaves in Egypt in Pharaoh'shouse.`
  + `1SA.2:27 Then a man of God came to Eli and said to him, 'Thus says the Lord, 'I clearly revealed Myself to the house of your father when they were slaves in Egypt in Pharaoh's house.`

L89:
  - `1SA.2:30 Therefore the Lord God of Israel says, 'I said indeed that your house and your father'shouse would walk before Me forever.' But now the Lord says, 'Far be it from Me, for I will honor those who honor Me, and the one who despises Me shall be dishonored.`
  + `1SA.2:30 Therefore the Lord God of Israel says, 'I said indeed that your house and your father's house would walk before Me forever.' But now the Lord says, 'Far be it from Me, for I will honor those who honor Me, and the one who despises Me shall be dishonored.`

L92:
  - `1SA.2:33 But for you-I will not destroy a man from My altar even though his eyes have failed and his life has drained away. But all the descendants of your house shall fall by men'sswords.`
  + `1SA.2:33 But for you-I will not destroy a man from My altar even though his eyes have failed and his life has drained away. But all the descendants of your house shall fall by men's swords.`

L115:
  - `1SA.3:15 So Samuel fell asleep and rose early in the morning. He opened the doors of the Lord'shouse. But Samuel was afraid to tell Eli the vision.`
  + `1SA.3:15 So Samuel fell asleep and rose early in the morning. He opened the doors of the Lord's house. But Samuel was afraid to tell Eli the vision.`

L151:
  - `1SA.4:19 Now Eli'sdaughter-in-law, Phinehas' wife, was pregnant, about to give birth. When she heard the news that the ark of God was captured, and her father-in-law and her husband were dead, she crouched down and gave birth, for her labor pains came upon her.`
  + `1SA.4:19 Now Eli's daughter-in-law, Phinehas' wife, was pregnant, about to give birth. When she heard the news that the ark of God was captured, and her father-in-law and her husband were dead, she crouched down and gave birth, for her labor pains came upon her.`

L254:
  - `1SA.9:3 Now the donkeys of Kish, Saul'sfather, were lost. And Kish said to his son Saul, 'Take one of the servants with you, and arise, go and look for the donkeys.'`
  + `1SA.9:3 Now the donkeys of Kish, Saul's father, were lost. And Kish said to his son Saul, 'Take one of the servants with you, and arise, go and look for the donkeys.'`

L269:
  - `1SA.9:18 Then Saul approached Samuel in the midst of the city, and said, 'Please tell me, where is the seer'shouse?'`
  + `1SA.9:18 Then Saul approached Samuel in the midst of the city, and said, 'Please tell me, where is the seer's house?'`

L271:
  - `1SA.9:20 But as for your donkeys lost three days ago, do not let your heart be anxious about them, for they have been found. And to whom is the beauty of Israel? Is it not on you and on your father'shouse?'`
  + `1SA.9:20 But as for your donkeys lost three days ago, do not let your heart be anxious about them, for they have been found. And to whom is the beauty of Israel? Is it not on you and on your father's house?'`

L285:
  - `1SA.10:2 As you depart from me today, you shall come to find two men by Rachel'stomb in the territory of Benjamin who are jumping about ecstatically, and they will say to you, 'The donkeys you searched for are found, but take notice, your father stopped worrying about news concerning the donkeys and is anxious about you, saying, 'What shall I do about my son?' '`
  + `1SA.10:2 As you depart from me today, you shall come to find two men by Rachel's tomb in the territory of Benjamin who are jumping about ecstatically, and they will say to you, 'The donkeys you searched for are found, but take notice, your father stopped worrying about news concerning the donkeys and is anxious about you, saying, 'What shall I do about my son?' '`

L342:
  - `1SA.12:4 And they said to Samuel, 'You have not wronged us or oppressed us or crushed us, nor taken anything from anyone'shand.'`
  + `1SA.12:4 And they said to Samuel, 'You have not wronged us or oppressed us or crushed us, nor taken anything from anyone's hand.'`

L390:
  - `1SA.13:19 Thus all Israel went down to the land of the Philistines to forge each man'sploughshare into his light armor, his tool, his ax, and his sickle.`
  + `1SA.13:19 Thus all Israel went down to the land of the Philistines to forge each man's ploughshare into his light armor, his tool, his ax, and his sickle.`

L418:
  - `1SA.14:20 Then Saul and all the people with him cried aloud, and they went into battle. Indeed, every man'ssword was against the enemy next to him. There was great confusion.`
  + `1SA.14:20 Then Saul and all the people with him cried aloud, and they went into battle. Indeed, every man's sword was against the enemy next to him. There was great confusion.`

L519:
  - `1SA.16:15 And Saul'sservants said to him, 'Behold, an evil spirit from the Lord is tormenting you.`
  + `1SA.16:15 And Saul's servants said to him, 'Behold, an evil spirit from the Lord is tormenting you.`

L552:
  - `1SA.17:20 Then David took his staff in his hand, and chose for himself five smooth stones from the brook. He put them in ashepherd'sbag to store away, and in his hand was his sling. He then approached the Philistine.`
  + `1SA.17:20 Then David took his staff in his hand, and chose for himself five smooth stones from the brook. He put them in ashepherd's bag to store away, and in his hand was his sling. He then approached the Philistine.`

L586:
  - `1SA.18:13 So Saul'sservants spoke these words in the ear of David. And David said, 'Is it trivial in your eyes if one becomes the son-inlaw of the king when he is lowly and without honor?'`
  + `1SA.18:13 So Saul's servants spoke these words in the ear of David. And David said, 'Is it trivial in your eyes if one becomes the son-inlaw of the king when he is lowly and without honor?'`

L651:
  - `1SA.20:25 As usual, the king sat on his seat by the wall and arrived before Jonathan. Abner sat by Saul'sside, but David'splace was seen as empty.`
  + `1SA.20:25 As usual, the king sat on his seat by the wall and arrived before Jonathan. Abner sat by Saul's side, but David's place was seen as empty.`

L653:
  - `1SA.20:27 And the next day, the second day of the month, David'splace was noticed as being empty. And Saul said to Jonathan his son, 'Why has the son of Jesse not come to the table yesterday or today?'`
  + `1SA.20:27 And the next day, the second day of the month, David's place was noticed as being empty. And Saul said to Jonathan his son, 'Why has the son of Jesse not come to the table yesterday or today?'`

L655:
  - `1SA.20:29 And he said, 'Please let me go, for our tribe has a sacrifice in the city, and my brothers commanded me to be there. And now, if I have found favor in your eyes, please let me go away safely and see my brothers.' Therefore he has not come to the king'stable.'`
  + `1SA.20:29 And he said, 'Please let me go, for our tribe has a sacrifice in the city, and my brothers commanded me to be there. And now, if I have found favor in your eyes, please let me go away safely and see my brothers.' Therefore he has not come to the king's table.'`

L763:
  - `1SA.24:6 Then it happened that David'sheart afflicted him afterward, because he cut the corner of his robe.`
  + `1SA.24:6 Then it happened that David's heart afflicted him afterward, because he cut the corner of his robe.`

L768:
  - `1SA.24:11 Take notice! This day your eyes have seen that the Lord delivered you into my hand in the cave; but I would not kill you. I spared you and said, 'I will not put my hand against my lord, for he is the Lord'sanointed.'`
  + `1SA.24:11 Take notice! This day your eyes have seen that the Lord delivered you into my hand in the cave; but I would not kill you. I spared you and said, 'I will not put my hand against my lord, for he is the Lord's anointed.'`

L779:
  - `1SA.24:22 Therefore by the Lord, swear now to me that you will not cut off my seed after me, and that you will not destroy my name from my father'shouse.'`
  + `1SA.24:22 Therefore by the Lord, swear now to me that you will not cut off my seed after me, and that you will not destroy my name from my father's house.'`

L791:
  - `1SA.25:3 The man'sname was Nabal, and his wife'sname was Abigail. She was a woman of good understanding and very beautiful in appearance; but the man was harsh and wicked in his doings, like adog.`
  + `1SA.25:3 The man's name was Nabal, and his wife's name was Abigail. She was a woman of good understanding and very beautiful in appearance; but the man was harsh and wicked in his doings, like adog.`

L797:
  - `1SA.25:9 So when David'syoung men came, they told Nabal all these words in the name of David, and he leapt up.`
  + `1SA.25:9 So when David's young men came, they told Nabal all these words in the name of David, and he leapt up.`

L798:
  - `1SA.25:10 Then Nabal replied to David'sservants and said, 'Who is David, and who is the son of Jesse? There are many servants nowadays who break away, each one from his master.`
  + `1SA.25:10 Then Nabal replied to David's servants and said, 'Who is David, and who is the son of Jesse? There are many servants nowadays who break away, each one from his master.`

L800:
  - `1SA.25:12 So David'syoung men turned back and returned. They came and told him these words.`
  + `1SA.25:12 So David's young men turned back and returned. They came and told him these words.`

L802:
  - `1SA.25:14 Now one of the young men told Abigail, Nabal'swife, saying, 'Look, David sent messengers from the desert to bless our master, but Nabal turned away from them.`
  + `1SA.25:14 Now one of the young men told Abigail, Nabal's wife, saying, 'Look, David sent messengers from the desert to bless our master, but Nabal turned away from them.`

L824:
  - `1SA.25:36 Now Abigail returned to Nabal, and behold, he was holding a feast in his house like the feast of a king. And Nabal'sheart was merry within him, for he was very drunk. Thus, she decided to say not aword to him, not even one, until morning light.`
  + `1SA.25:36 Now Abigail returned to Nabal, and behold, he was holding a feast in his house like the feast of a king. And Nabal's heart was merry within him, for he was very drunk. Thus, she decided to say not aword to him, not even one, until morning light.`

L835:
  - `1SA.25:44 But Saul gave Michal his daughter, David'swife, to Palti the son of Laish, from Gallim.`
  + `1SA.25:44 But Saul gave Michal his daughter, David's wife, to Palti the son of Laish, from Gallim.`

L849:
  - `1SA.26:12 So David took the spear by Saul'shead and the container of water, and they went away. No one noticed or knew what happened or even awoke. All were sleeping, because adeep sleep from the Lord fell upon them.`
  + `1SA.26:12 So David took the spear by Saul's head and the container of water, and they went away. No one noticed or knew what happened or even awoke. All were sleeping, because adeep sleep from the Lord fell upon them.`

L853:
  - `1SA.26:16 And this thing which you allowed to happen is not good. As the Lord lives, you are sons of death-you guarding the lord your king, the anointed of the Lord. Now look and tell me, where is the king'sspear that was by his head, and the jug of water?'`
  + `1SA.26:16 And this thing which you allowed to happen is not good. As the Lord lives, you are sons of death-you guarding the lord your king, the anointed of the Lord. Now look and tell me, where is the king's spear that was by his head, and the jug of water?'`

L854:
  - `1SA.26:17 Then Saul recognized David'svoice and said, 'Is that truly your voice, my son David?' And David said, 'It is your servant, my lord, O King.'`
  + `1SA.26:17 Then Saul recognized David's voice and said, 'Is that truly your voice, my son David?' And David said, 'It is your servant, my lord, O King.'`

L856:
  - `1SA.26:19 Now let my lord the king hear his servant'swords: If God incites you against me, let Him accept the scent of your offering. If the sons of men incite you against me, let these men be cursed before the Lord. For today by their saying, 'Go, serve other gods,' they show their desire to cast me out in order to prevent me from being established in the inheritance of the Lord.`
  + `1SA.26:19 Now let my lord the king hear his servant's words: If God incites you against me, let Him accept the scent of your offering. If the sons of men incite you against me, let these men be cursed before the Lord. For today by their saying, 'Go, serve other gods,' they show their desire to cast me out in order to prevent me from being established in the inheritance of the Lord.`

L860:
  - `1SA.26:23 And the Lord shall repay each man for his righteousness and his faithfulness, as the Lord delivered you into my hands today, though I did not lift my hand against the Lord'sanointed.`
  + `1SA.26:23 And the Lord shall repay each man for his righteousness and his faithfulness, as the Lord delivered you into my hands today, though I did not lift my hand against the Lord's anointed.`

L878:
  - `1SA.27:11 And David did not leave man or woman alive to bring news to Gath, saying, 'Let them not inform on us to those in Gath by saying, 'Thus David did.' ' This was David'sbehavior as long as he dwelt in the country of the Philistines.`
  + `1SA.27:11 And David did not leave man or woman alive to bring news to Gath, saying, 'Let them not inform on us to those in Gath by saying, 'Thus David did.' ' This was David's behavior as long as he dwelt in the country of the Philistines.`

L904:
  - `1SA.28:20 Saul fell prostrate on the ground, for he was very afraid because of Samuel'swords. He was also weak since he had not eaten any food all that day and night.`
  + `1SA.28:20 Saul fell prostrate on the ground, for he was very afraid because of Samuel's words. He was also weak since he had not eaten any food all that day and night.`

L935:
  - `1SA.30:5 And both David'swives, Ahinoam the Jezreelite woman and Abigail the widow of Nabal the Carmelite, were taken captive.`
  + `1SA.30:5 And both David's wives, Ahinoam the Jezreelite woman and Abigail the widow of Nabal the Carmelite, were taken captive.`

L937:
  - `1SA.30:7 And David said to Abiathar the priest, Ahimelech'sson, 'Bring the ephod.'`
  + `1SA.30:7 And David said to Abiathar the priest, Ahimelech's son, 'Bring the ephod.'`

L950:
  - `1SA.30:20 And David took all the flocks and herds and put them ahead of the plunder. Concerning the plunder, it was said, 'This is David'splunder.'`
  + `1SA.30:20 And David took all the flocks and herds and put them ahead of the plunder. Concerning the plunder, it was said, 'This is David's plunder.'`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 1SA.3:4 | `the Lord called, 'Samuel, Samuel.' Samuel answered...` |
| 1SA.8:5 | `and said to him, 'Look, you have become old, and y...` |
| 1SA.8:12 | `and for himself, he will appoint them as captains ...` |
| 1SA.10:18 | `and to the sons of Israel he said, 'Thus says the ...` |
| 1SA.13:11 | `then I said, 'The Philistines will now come down a...` |
| 1SA.14:29 | `and Jonathan knew it, and said, 'See indeed, my fa...` |
| 1SA.17:19 | `and he girded David with his sword over his armor....` |
| 1SA.18:5 | `as Saul was apprehensive of the mere presence of D...` |
| 1SA.18:6 | `and he removed David from himself. He made David h...` |
| 1SA.20:13 | `may the Lord do this to Jonathan and add to this e...` |
| 1SA.20:15 | `you shall not cut off your mercy from my house for...` |
| 1SA.20:16 | `or removes the name of Jonathan from the house of ...` |
| 1SA.25:24 | `about his feet and said, 'O my lord, let this unri...` |
| 1SA.25:31 | `will this not be an abomination to my lord and an ...` |
| 1SA.30:27 | `to those who were in Beth Shur, to those who were ...` |
| 1SA.30:28 | `to those who were in Aroer, to those who were in A...` |
| 1SA.30:29 | `to those who were in Gath and in Kinan, and to tho...` |
| 1SA.30:30 | `to those who were in Carmel, to those who were in ...` |
| 1SA.30:31 | `to those who were in Jerimouth, to those who were ...` |
| 1SA.30:32 | `to those who were in Hebron, and to all the places...` |
