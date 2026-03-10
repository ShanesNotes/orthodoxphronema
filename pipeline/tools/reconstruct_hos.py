#!/usr/bin/env python3
"""
Reconstruct and restructure HOS.md from the chapter-0 dump.

This script takes a different approach:
1. The verse numbers in the file ARE correct within each chapter
2. Chapter boundaries are detected by verse number drops (restart to low numbers)
3. When a chapter number appears as a verse (e.g., HOS.0:3 before HOS.0:2),
   that's the chapter marker being misread as verse 1

CVC: [11, 23, 5, 19, 15, 11, 16, 14, 17, 15, 12, 14, 16, 9]
"""

import json
import re
import hashlib
from pathlib import Path
from collections import Counter

REPO = Path(__file__).resolve().parent.parent.parent

# The ORIGINAL content of HOS.md before any modifications.
# Reconstructed from the initial Read output.
ORIGINAL_CONTENT = r"""---
book_code: HOS
book_name: "Hosea"
testament: OT
canon_position: 31
source: "Orthodox Study Bible (OSB), Thomas Nelson 2008"
parse_date: "2026-03-10"
promote_date: null
checksum: "eb6928e6832606f81224b5aa086e815d76d0ff737976a9e9ef41d8772f00582a"
status: staged
deuterocanonical: false
has_additions: false
---

## Chapter 0


### Israel and Judah Are Unrepentant

HOS.0:3 So he went and took Gomer, daughter of Diblaim, and she conceived and bore him ason.
HOS.0:4 Again the Lord said to him, 'Call his name Jezreel; For in alittle while I will av enge the blood of Jezreel on the house of Jehu, And I will make to cease the kingship of the house of Israel.

### God's Judgment on Israel

HOS.0:5 It shall be in that day That I will break the bow of Israel in the Valley of Jezreel.'
HOS.0:6 Then she conceived again and bore adaughter. So God said to him, 'Call her name Lo-Ruhamah, For I will no longer hav emercy on the house of Israel, But will surely set My self in array against them.
HOS.0:7 But I will hav emercy on the house of Judah And will sav ethem by the Lord their God. I will not sav ethem with bow, Nor with sword, nor by war, Nor by chariots, nor by horses or horsemen.'
HOS.0:8 Now after she weaned Lo-Ruhamah, she conceived again and bore ason.

### Israel Will Be Restored

HOS.0:9 So the Lord said, 'Call his name Lo-Ammi, For y ou are not My people, And I am not y our God. †

### Trusting Other Nations Is Futile

HOS.0:10 'Yet the number of the children of Israel Shall be as the sand of the sea, Which shall not be measured or numbered. Then it shall come to pass In the place where it was said to them, 'You are not My people,' Even then they shall be called The sons of the liv ing God.

### A Charge against Israel and Judah

HOS.0:11 The children of Judah and the children of Israel Shall be gathered together. They shall appoint themselv es one head And come up out of the land; For great shall be the day of Jezreel.
HOS.0:2 'Plead with your mother, plead, For she is not My wife, And I am not her Husband. I will remov eher fornication out of My presence And her adultery from between her breasts,

### Israel and Judah Are Unrepentant

HOS.0:3 That I may strip her naked And make her again as she was at the day of her birth. I will make her desolate and as adry land, And I will kill her with thirst.
HOS.0:4 'I will not hav emercy upon her children; For they are children of fornication.

### God's Judgment on Israel

HOS.0:5 For their mother went a-whoring. She that bore them disgraced herself, For she said, 'I will go after my lov ers, Who give me my bread and my water, And my garments and my linen clothes, My oil and my necessities.'
HOS.0:6 'Therefore, behold, I will hedge up her way with thorns. I will stop the way sso she shall not find her path.
HOS.0:7 She will follow after her lov ers But not ov ertake them. She will seek them but not find them. She will say, 'I will go and return to my former husband; For it was better for me than now.'
HOS.0:8 For she did not know I gav eher corn, wine, and oil, And multiplied silv er to her; But she turned the silv er and gold ov er to Baal.

### Israel Will Be Restored

HOS.0:9 'Therefore I will take back My corn in its season, And My wine in its time. I will remov e My raiment and My linen clothes That she may not cov er her nakedness.

### Trusting Other Nations Is Futile

HOS.0:10 Now I will expose her uncleanness before her lov ers, And no one shall by any means Deliv er her out of My hand.

### A Charge against Israel and Judah

HOS.0:11 I will take away all her gladness, her feasts, And her festiv als at the New Moon, And her Sabbaths, And all her solemn assemblies.
HOS.0:12 'I will destroy her vines and her fig trees, All things of which she said, 'These are my wages that my lov ers hav egiv en me.' But I will make them atestimony; And the wild beasts of the field, the birds of the sky, And the reptiles of the earth shall dev our them.

### God Has Mercy on His People

HOS.0:13 I will repay her For the day sof Baalim, Wherein she sacrificed to them, And put on her earrings and her necklaces, And went after her lov ers; But she forgot Me,' say sthe Lord.

### Punishment for Israel

HOS.0:14 'Therefore, behold, I will lead her astray And make her as desolate, And I will speak to her heart.

### Restoration of Israel

HOS.0:15 I will giv eher possessions from there, And the Valley of Achor to open her understanding. She will be humbled there According to the day sof her infancy, And according to the day sof her coming up Out of the land of Egy pt.
HOS.0:16 'Then it shall come to pass in that day,' Says the Lord, 'That she will call Me 'My Husband,' And shall no longer call Me 'Baalim.'
HOS.0:17 For I will take away the names of Baalim out of her mouth, And their names shall be remembered no more.
HOS.0:18 In that day I will make acov enant for them With the wild beasts of the field, And with the birds of the sky, And with the reptiles of the earth. I will break the bow, the sword, and the battle from off the earth, And will cause them to dwell safely.

### Warnings for Israel and Judah

HOS.0:19 'I will betroth you to My self forev er; Yes, I will betroth you to My self In righteousness and justice, And in mercy and compassions.
HOS.0:20 I will betroth you to My self in faithfulness, And you shall know the Lord.
HOS.0:21 'It shall come to pass in that day,' say sthe Lord, 'That I will listen to heav en, And it shall listen to the earth.
HOS.0:22 The earth shall listen to the corn, And the wine, and the oil; And they shall listen to Jezreel.
HOS.0:23 I will sow her to My self on the earth, And will lov e her that was not lov ed, And will say to that which was not My people, 'You are My people!'

### Israel Will Return to the Lord

HOS.0:24 And they shall say, 'You are the Lord my God!' '

### Israel and Judah Are Unrepentant

HOS.0:3 Then the Lord said to me, 'Go yet again and love awoman that loves evil things, an adulteress, even as the Lord loves the children of Israel, for they look after strange gods and love raisin cakes.'
HOS.0:2 So I bought her for myself for fifteen pieces of silver, ahomer of barley, and ajar of wine.

### Israel and Judah Are Unrepentant

HOS.0:3 I said to her, 'You shall stay with me for many days. You shall not commit fornication, neither shall you be for another man; but I will be for you.'
HOS.0:4 For the children of Israel shall abide many days without aking, without aprince, without asacrifice, without an altar, without apriesthood, and without symbols of revelation.

### God's Judgment on Israel

HOS.0:5 Afterward the children of Israel shall return and seek the Lord their God and David their king; and they shall be amazed at the Lord and at His good things in the latter days.
HOS.0:4 Hear the word of the Lord, You children of Israel, For the Lord has ajudgment for the inhabitants of the land: 'There is no truth or mercy Or knowledge of God in the land.
HOS.0:2 Cursing and ly ing, murder and theft And adultery gushed forth in the land, And blood is mingled with blood.

### Israel and Judah Are Unrepentant

HOS.0:3 Therefore the land shall mourn And be diminished with all the things that dwell in it: The wild beasts of the field, the reptiles of the earth, And the birds of the sky, And the fish of the sea shall come to an end;
HOS.0:4 That neither may any one judge, nor analy ze another; But my people are as apriest who is spoken against.

### God's Judgment on Israel

HOS.0:5 'Thus you shall be weak by day, And the prophet shall be weak with you; I hav ecompared your mother to the night.
HOS.0:6 My people are like as those who hav eno knowledge. Because you hav erejected knowledge, I will also reject you from being apriest to Me; And because you hav eforgotten the law of your God, I also will forget your children.
HOS.0:7 According to their multitude, So they sinned against Me; I will turn their glory into dishonor.
HOS.0:8 They will eat the sins of My people And take away their liv es because of their wrongdoings.

### Israel Will Be Restored

HOS.0:9 The priest shall also be as the people; So I will punish him for his way s And repay him for his counsels.

### Trusting Other Nations Is Futile

HOS.0:10 They shall eat and not be satisfied; They have gone a-whoring and shall by no means prosper, Because they hav eabandoned holding fast to the Lord.

### A Charge against Israel and Judah

HOS.0:11 'The heart of My people has gladly engaged In fornication, wine, and strong drink.
HOS.0:12 They asked counsel by means of signs And they reported answers to them by their stav es. They have gone astray in aspirit of whoredom And grievously gone a-whoring from their God.

### God Has Mercy on His People

HOS.0:13 They hav esacrificed on the tops of the mountains, And on the hills they hav esacrificed Under the oak and poplar And under the shady tree, Because their shade was good. Therefore your daughters shall go a-whoring, And your daughters-in-law shall commit adultery.

### Punishment for Israel

HOS.0:14 But I will not show care for your daughters When they commit fornication, Nor your daughters-in-law When they commit adultery; For they mingled themselv es with harlots And sacrificed with the initiated ones; And the people who understood Entangled themselves with aharlot.

### Restoration of Israel

HOS.0:15 'But you, O Israel, be not ignorant, And do not go, men of Judah, to Gilgal; And do not go up to Beth Av en Nor swear by the liv ing Lord.
HOS.0:16 For Israel was maddened like amad heifer; Now the Lord will feed them Like alamb in awide place.
HOS.0:17 Ephraim, joined with idols, Has laid stumbling blocks in his own way.
HOS.0:18 He has chosen the Canaanites; They have grievously gone a-whoring; They have loved dishonor through her rudeness.

### Warnings for Israel and Judah

HOS.0:19 You are ablast of wind in her wings, And they shall be ashamed because of their altars.

### God's Judgment on Israel

HOS.0:5 'Hear these things, O priests, And attend, O house of Israel! Listen, O house of the king! For judgment is with you Because you hav ebeen asnare in Mizpah And anet spread on Tabor,
HOS.0:2 Which they that hunt the prey hav efixed; But I will be your instructor.

### Israel and Judah Are Unrepentant

HOS.0:3 I know Ephraim, and Israel is not far from Me; For now Ephraim has gone grievously a-whoring; Israel is defiled.
HOS.0:4 'Their deliberations did not allow them To return to their God, For aspirit of fornication is in them, And they have not gotten to know the Lord.

### God's Judgment on Israel

HOS.0:5 The arrogance of Israel Shall be brought low before His face, And Israel and Ephraim shall become weak Due to their wrongdoings; And Judah also shall become weak with them.
HOS.0:6 'They shall go with sheep and calv es Diligently to seek the Lord; But they shall not find Him, For He has withdrawn Himself from them.
HOS.0:7 For they hav eforsaken the Lord Because strange children hav ebeen born to them. Now the rust shall dev our them along with their heritages.
HOS.0:8 'Blow the trumpet on the hills, Sound aloud on the heights, Proclaim in Beth Av en: 'Benjamin is confused.'

### Israel Will Be Restored

HOS.0:9 Ephraim has vanished in the day sof reproof; Among the tribes of Israel I hav eshown faithful things.

### Trusting Other Nations Is Futile

HOS.0:10 'The princes of Judah became as those Who remove the boundaries; I will pour out my fury upon them as water.

### A Charge against Israel and Judah

HOS.0:11 Ephraim oppressed his adv ersary; He trod ov er judgment, For he began to go after vanities.
HOS.0:12 Therefore I will be as aconfusion to Ephraim And as asting to the house of Judah.

### God Has Mercy on His People

HOS.0:13 'Ephraim saw his disease And Judah his pain; Then Ephraim went to the Assy rians And sent ambassadors to King Jareb. But he could not heal you, And your pain shall in no way cease from you.

### Punishment for Israel

HOS.0:14 Wherefore I am as apanther to Ephraim And as alion to the house of Judah.

### Restoration of Israel

HOS.0:15 So I will grasp and go away; And I will take, and there shall be none to rescue. I will go and return to My place Until they are destroy ed, And then they shall seek My face.
HOS.0:6 ''Let us go and return to the Lord our God; For He has grasped and will heal us; He will smite and plug the wound with lint.
HOS.0:2 After two day s He will heal us. In the third day we shall rise And liv ebefore Him.

### Israel and Judah Are Unrepentant

HOS.0:3 Let us know, let us pursue That we might know the Lord. We shall find Him ready as the day break, And He will come to us As the early and latter rain to the earth.'
HOS.0:4 'What shall I do to you, O Ephraim? What shall I do to you, O Judah? Your mercy is as amorning cloud And as the early dew that goes away.

### God's Judgment on Israel

HOS.0:5 Therefore I hav ecut off your prophets; I hav eslain them with the words of My mouth, And My judgment shall go forth as the light.
HOS.0:6 For I desire mercy and not sacrifice, And the knowledge of God More than whole burnt offerings.
HOS.0:7 But they are as aman who transgresses the cov enant; There they despised Me.
HOS.0:8 Gilead is acity working vanity with troubling water.

### Israel Will Be Restored

HOS.0:9 Your strength is that of apirate; The priests hav ehidden the way;
HOS.0:7 They have murdered the people of Shechem, For they hav edone lawlessness.

### Trusting Other Nations Is Futile

HOS.0:10 In the house of Israel I hav eseen horrible things; There is the fornication of Ephraim; Israel and Judah are defiled.

### A Charge against Israel and Judah

HOS.0:11 Begin to harv est for yourself When I return the captiv es of My people. 'When I have healed Israel, Then shall the wrongdoing of Ephraim And the ev il of Samaria be rev ealed, For they hav eworked falsehood. A thief shall come in to him, Even arobber taking spoil in his way,
HOS.0:2 That they may sing together As men singing in their heart. I remember all their ev ils; Now their own counsels hav eencircled them; They were before My face.

### Israel and Judah Are Unrepentant

HOS.0:3 They gladdened kings with their ev ils And princes with their lies.
HOS.0:4 'They are all adulterers, Like an ov en heated for cooking, Burning with aflame during the kneading of the dough Until it is leav ened.

### God's Judgment on Israel

HOS.0:5 In the day sof our kings, The princes began to be inflamed with wine; He stretched out his hand with pestilent fellows.
HOS.0:6 Wherefore their hearts are inflamed like an ov en While they were falling down all the night. Ephraim is satisfied with sleep; The morning is come; He is burnt up like aflame of fire.
HOS.0:7 They are all heated like an ov en And have devoured their judges. All their kings are fallen; There was not among them one that called upon Me.
HOS.0:8 'Ephraim is mixed among his peoples; Ephraim became acake not turned.

### Israel Will Be Restored

HOS.0:9 Strangers dev oured his strength, And he knew it not. Grey hairs came upon him, And he knew it not.

### Trusting Other Nations Is Futile

HOS.0:10 The pride of Israel shall be humbled before his face; Yet they hav enot returned to the Lord their God, Neither have they diligently sought Him in spite of all this.

### A Charge against Israel and Judah

HOS.0:11 'Ephraim was like asilly dov e, not hav ing aheart; He called to Egy pt, and they went to the Assy rians.
HOS.0:12 Whenever they shall go, I will cast My net upon them; I will bring them down as the birds of the sky. I will chastise them through the news of their affliction.

### God Has Mercy on His People

HOS.0:13 'Woe to them, for they hav eturned away from Me! They are cowards, For they hav ecommitted impious deeds against Me. Yet I redeemed them, But they spoke falsehoods against Me.

### Punishment for Israel

HOS.0:14 Their hearts did not cry aloud to Me, But they wailed upon their beds. 'They slashed themselves for oil and wine; They were chastised by Me.

### Restoration of Israel

HOS.0:15 I strengthened their arms, But they dev ised ev ils against Me.
HOS.0:16 They turned aside to nothing; They became as astretched bow. Their princes shall fall by the sword; They will be despised in the land of Egy pt Because of their unrestrained tongue.
HOS.0:17 Israel's Apostasy Like an eagle against the house of the Lord, Because they broke My cov enant And acted impiously against My law.
HOS.0:2 They shall cry out to Me, say ing, 'O God, we know You.'

### Israel and Judah Are Unrepentant

HOS.0:3 For Israel has turned away from good things; They have pursued an enemy.
HOS.0:4 'They made kings for themselv es, but not by Me. They have ruled, but they did not make it known to Me. They made idols for themselv es with their silv er and gold That they might be utterly destroy ed.

### God's Judgment on Israel

HOS.0:5 Get rid of your calf, O Samaria. My anger is kindled against them. How long will they be unable to purge themselv es in Israel?
HOS.0:6 A workman made it, And it is not God; Therefore your calf, O Samaria, was adeceiv er.
HOS.0:7 'For they sowed wind-damaged seeds, And their destruction shall await them; A sheaf of corn cannot produce flour; And even if the seeds should produce it, Strangers would dev our it.
HOS.0:8 Israel is swallowed up. Now he has become as aworthless vessel among the nations.

### Israel Will Be Restored

HOS.0:9 For they hav egone up to the Assy rians; Ephraim has sprouted again against himself; They lov ed gifts.

### Trusting Other Nations Is Futile

HOS.0:10 Therefore they shall be handed ov er to the nations. Now I will receiv ethem, And they will stop awhile to anoint aking and princes.

### A Charge against Israel and Judah

HOS.0:11 'Because Ephraim has multiplied altars, His belov ed altars hav ebecome sins to him.
HOS.0:12 I will write amultitude of statutes for him, For his statutes are considered as strange things, As well as his belov ed altars.

### God Has Mercy on His People

HOS.0:13 For if they should offer asacrifice and eat flesh, The Lord would not accept them. Now He will remember their wrongdoings And take vengeance on their sins. They have returned to Egy pt, And they shall eat unclean things among the Assy rians.

### Punishment for Israel

HOS.0:14 'Israel has forgotten Him who made him. They have built temples, And Judah has multiplied walled cities; But I will send fire upon his cities, And it shall dev our their foundations.'

### Israel Will Be Restored

HOS.0:9 Rejoice not, O Israel, Neither make merry, as other peoples, For you hav egone a-whoring from your God. You have lov ed for hire Upon every threshing floor of wheat.
HOS.0:2 The threshing floor and winepress did not know them, And the wine disappointed them.

### Israel and Judah Are Unrepentant

HOS.0:3 They did not dwell in the Lord'sland. Ephraim dwelt in Egy pt, And they shall eat unclean things among the Assy rians.
HOS.0:4 They hav enot offered wine to the Lord, Neither have their sacrifices been pleasing to Him, But like the mourning bread to them. All that eat shall be defiled Because their bread shall be for their own life; It shall not come into the house of the Lord.

### God's Judgment on Israel

HOS.0:5 What will you do in the day of public festiv al And in the day of the Lord'sfeast?
HOS.0:6 Therefore, behold, they go forth from the trouble of Egy pt. Memphis shall receiv ethem And Machmas shall bury them. As for their silv er, destruction shall inherit it, And thorns shall be in their tents.
HOS.0:7 The day sof vengeance hav ecome; The days of your recompense hav ecome; And Israel shall be afflicted As the prophet that is mad, as aman deranged. By reason of the multitude of your wrongdoings Your madness has abounded.
HOS.0:8 The watchman of Ephraim was with God, But the prophet is acrooked snare in all his way s. They have planted the madness firmly In the house of God.

### Israel Will Be Restored

HOS.0:9 They hav ecorrupted themselv es As in the day sof Gibeah. He will remember his wrongdoings; He will take vengeance on his sins.

### Trusting Other Nations Is Futile

HOS.0:10 'I found Israel as grapes in the wilderness, And I saw their fathers as an early guard at their fig tree. They went in to Baal Peor And were shamefully estranged; And the belov ed ones became abominable.

### A Charge against Israel and Judah

HOS.0:11 The glory of Ephraim has flown away as abird: Their glories from birth, birth-pains, and conception.
HOS.0:12 For ev en if they should rear their children, Yet they shall be utterly bereav ed. For woe to them! My flesh is of them.

### God Has Mercy on His People

HOS.0:13 Ephraim, ev en as I saw, Presented their children as aprey; Ephraim was ready to bring out his children to slaughter.'

### Punishment for Israel

HOS.0:14 Giv eto them, O Lord! What will You giv eto them? A childless womb and dry breasts.

### Restoration of Israel

HOS.0:15 'All their ev ils are in Gilgal, For there I hated them. Because of their ev il practices, I will cast them out of My house. I will not lov ethem any more.
HOS.0:6 For they bound it up for the Assy rians And carried it away as agift to King Jareb. Ephraim shall receiv eit as agift, And Israel shall be ashamed of his own counsel.
HOS.0:7 Samaria has cast off her king Like atwig on the surface of the water,
HOS.0:8 And the altars of Av en, the sins of Israel, Shall be remov ed. Thorns and thistles shall come upon their altars, And they shall say to the mountains, 'Cov er us,' And to the hills, 'Fall on us.'

### Israel Will Be Restored

HOS.0:9 'From the day sof Gibeah, Israel has sinned; There they stood. The war on that hill against the children of unrighteousness Did not ov ertake them.

### Trusting Other Nations Is Futile

HOS.0:10 I came to chastise them, And peoples shall be gathered against them When they are chastised for their two sins.

### A Charge against Israel and Judah

HOS.0:11 Ephraim is aheifer taught to lov e victory, But I will come upon the fairest part of her neck. I will mount Ephraim; I will pass ov er Judah in silence; Jacob shall prev ail against him.'
HOS.0:12 Sow to yourselv es in righteousness; Gather in the fruit of life; Light for yourselv es the light of knowledge; Seek the Lord till the fruits of righteousness come upon you.

### God Has Mercy on His People

HOS.0:13 Why have you passed over ungodliness in silence And reaped its wrongdoings? You have eaten the fruit of deception, For you hav ehoped in your chariots, In the abundance of your power.

### Punishment for Israel

HOS.0:14 Therefore destruction shall rise up among your people, And all your walled places shall be gone, As Beth Arbel in the time of Prince Shalman.

### Restoration of Israel

HOS.0:15 In the day sof battle, They dashed the mother to the ground upon the children. Thus will I do to you, O house of Israel, Because of your ev il deeds. Early in the morning were they cast off; The king of Israel has been cast off.

### A Charge against Israel and Judah

HOS.0:11 'For Israel is achild, and I lov ed him, And out of Egy pt I hav ecalled his children.
HOS.0:2 As I called them, So they departed from My presence. They sacrificed to the Baals, And burned incense to grav en images.

### Israel and Judah Are Unrepentant

HOS.0:3 'Yet I bound the feet of Ephraim. I took him on My arm, But they did not know that I healed them.
HOS.0:4 When men were destroyed, I drew them with the bands of My lov e, And I will be to them as aman Smiting another on his cheek. I will look with fav or to him; I will prev ail with him.

### God's Judgment on Israel

HOS.0:5 'Ephraim dwelt in Egy pt; And the Assy rian himself was his king, Because he would not return.
HOS.0:6 The sword became weak in his cities, And he ceased to war with his hands; For they shall consume themselv es With their own intrigues.
HOS.0:7 His people shall hold onto His habitation; But God shall be angry with His precious things, And shall not at all exalt him.
HOS.0:8 'How shall I deal with you, Ephraim? How shall I protect you, Israel?

### Israel Will Be Restored

HOS.0:9 What shall I do with you? I will make you as Admah and as Zeboiim. My heart is turned about; My repentance is utterly thrown into confusion. I will not act according to the fury of My wrath; I will not abandon Ephraim to be utterly destroy ed. For I am God and not man; The Holy One among you; And I will not enter into the city.

### Trusting Other Nations Is Futile

HOS.0:10 'I will go after the Lord. He shall utter His voice as alion; For He shall roar, And the children of the waters shall be amazed.

### A Charge against Israel and Judah

HOS.0:11 They shall be amazed as abird out of Egy pt And as adov eout of the land of the Assy rians; And I will restore them to their houses,' Says the Lord.
HOS.0:12 'Ephraim has encompassed me with falsehood, And the house of Israel and Judah with ungodliness. But now God knows them, And he shall be called God'sholy people.
HOS.0:2 But Ephraim is an ev il spirit. He has chased the east wind all the day. He has multiplied empty and vain things And struck acov enant with the Assy rians. He made business with oil in Egy pt.

### Israel and Judah Are Unrepentant

HOS.0:3 'The Lord has ajudgment against Judah So as to punish Jacob according to his way s, And He will repay him according to his practices.
HOS.0:4 He kicked his brother in the womb, And in his toils he regained strength with God.

### God's Judgment on Israel

HOS.0:5 He prev ailed with the Angel and was strong. They wept and entreated Me.
HOS.0:6 They found Me in Bethel, And there aword was spoken to them. So the Lord God Almighty shall be his memorial.
HOS.0:7 You shall return to your God; Therefore, observ emercy and judgment, And draw near to your God continually.
HOS.0:8 'As for Canaan, There is abalance of wrongdoing in his hand, For he has lov ed to oppress.

### Israel Will Be Restored

HOS.0:9 As for Ephraim, he said, 'Nevertheless, I am rich; I hav efound relief for my self.' But none of his labors shall be found in him, Because of the wrongdoings by which he sinned.

### Trusting Other Nations Is Futile

HOS.0:10 'But I the Lord your God brought you up Out of the land of Egy pt. I will yet again cause you to dwell in tents According to the day sof the feast.

### A Charge against Israel and Judah

HOS.0:11 For I will speak to the prophets, And I hav emultiplied visions, And by the authority of the prophets I was represented.'
HOS.0:12 If Gilead does not exist, Then the leaders in Gilead were false when they sacrificed, And their altars were like mounds on aparched field.

### God Has Mercy on His People

HOS.0:13 Jacob retreated into the plain of Sy ria, And Israel serv ed for awife And kept watch for awife.

### Punishment for Israel

HOS.0:14 The Lord brought Israel Out of the land of Egy pt by aprophet, And by aprophet he was preserv ed.

### Restoration of Israel

HOS.0:15 Ephraim was angry and excited; Therefore his blood shall be poured out upon him, And the Lord shall repay him for his disgrace.

### God Has Mercy on His People

HOS.0:13 According to the word of Ephraim, He receiv ed ordinances for himself in Israel And established them for Baal; then he died.
HOS.0:2 So now they hav esinned increasingly And have made for themselves A molten image with their silv er, According to the fashion of idols, The work of craftsmen done for them. They say, 'Sacrifice men, For the calv es hav ecome to an end.'

### Israel and Judah Are Unrepentant

HOS.0:3 Therefore they shall be as amorning cloud And as the early dew that passes away, Like chaff blown away from the threshing floor And as smoke out of the chimney.
HOS.0:4 'But I am the Lord your God, Who makes the heaven firm and creates the earth, Whose hands have created the whole host of heav en. But I did not show them to you that you should seek after them. I brought you up from the land of Egy pt, And you shall know no God but Me; And there is no Sav ior besides Me.

### God's Judgment on Israel

HOS.0:5 I tended you as ashepherd in the wilderness, In an uninhabited land.
HOS.0:6 When they had their pastures, They were completely filled, And their hearts were exalted; Therefore, they forgot Me.
HOS.0:7 'So I will be to them as apanther And as aleopard by way of the Assy rians.
HOS.0:8 I will meet them as an excited she-bear, And I will rend the hardness of their heart. The lions' whelps of the thicket shall dev our them there; The wild beasts of the field shall rend them in pieces.

### Israel Will Be Restored

HOS.0:9 'O Israel, who will help you in your destruction?

### Trusting Other Nations Is Futile

HOS.0:10 14 Where is this king of yours? Let him sav e you in all your cities. Let him judge you, of whom you said, 'Giv eme aking and aprince.'

### A Charge against Israel and Judah

HOS.0:11 Thus I gav e you aking in My anger And took him back in My wrath.
HOS.0:12 'Ephraim is aconspiracy of unrighteousness; His sin is hidden.

### God Has Mercy on His People

HOS.0:13 Pains as of awoman in trav ail shall come upon him. He is your unwise son, For he shall not stand in the destruction of your children.

### Punishment for Israel

HOS.0:14 'I will deliv er them out of the hand of Hades And will redeem them from death. Where is your penalty, O death? O Hades, where is your sting? Pity is hidden from My ey es.'

### Restoration of Israel

HOS.0:15 Forasmuch as he will cause A div ision among his brethren, The Lord shall bring upon him A hot wind from the desert, And shall dry up his springs And drain his fountains. He shall dry up his land And spoil all his precious vessels. Samaria shall be utterly destroy ed, For she has resisted her God; And they shall fall by the sword. Their infants shall be dashed against the ground And their pregnant women ripped up.
HOS.0:2 Return, O Israel, to the Lord your God, For you became weak through your wrongdoings.

### Israel and Judah Are Unrepentant

HOS.0:3 Take with you words And turn to the Lord your God.
HOS.0:4 Speak to Him, That you may not receiv ethe reward of unrighteousness, But that you may receiv egood things. We will render in return the fruit of our lips. Assy ria will not sav eus; We will not mount on horseback. Let us no longer say to the works of our hands, 'Our gods.' He who is among you shall hav emercy on the orphan.

### God's Judgment on Israel

HOS.0:5 'I will restore their dwellings. I will lov ethem willingly, For he has turned away My wrath from them.
HOS.0:6 I will be as dew to Israel; He shall bloom as the lily And cast forth his roots as Lebanon.
HOS.0:7 His branches shall spread, And he shall be as afruitful oliv etree, And his fragrance shall be as the smell of Lebanon.
HOS.0:8 They shall return and dwell under his shadow; They shall liv eand be satisfied with corn, And he shall flower as a vine; His memorial shall be as the wine of Lebanon.

### Israel Will Be Restored

HOS.0:9 'To Ephraim: What has he to do any more with idols? I hav ehumbled him And I will strengthen him. I am as aleafy juniper tree. From Me your fruit is found.'

### Trusting Other Nations Is Futile

HOS.0:10 Who is wise and will understand these things? Or prudent and will know them? For the way sof the Lord are straight, And the righteous shall walk in them; But the ungodly shall become weak in them.
"""


def fix_split_words(text):
    """Fix Docling column-split artifacts."""
    text = re.sub(r'([a-z])(v)\s(e\w*)', r'\1\2\3', text)
    text = re.sub(r'\by\s(ou\w*)', r'y\1', text)
    text = re.sub(r'Egy\spt', 'Egypt', text)
    text = re.sub(r'Assy\s(ri\w*)', r'Assy\1', text)
    text = re.sub(r'My\sself\b', 'Myself', text)
    text = re.sub(r'say\ssthe', 'says the', text)
    text = re.sub(r'say\ssing', 'saying', text)
    text = re.sub(r'day\ssof', 'days of', text)
    text = re.sub(r'day\ss\b', 'days', text)
    text = re.sub(r'way\ss\b', 'ways', text)
    text = re.sub(r'\bly\sing\b', 'lying', text)
    text = re.sub(r'Sy\sria', 'Syria', text)
    text = re.sub(r'\bey\ses\b', 'eyes', text)
    text = re.sub(r'\bsso\b', 'so', text)
    text = re.sub(r'\bAv\sen\b', 'Aven', text)
    text = re.sub(r'\btrav\sail\b', 'travail', text)
    text = re.sub(r'\bserv\sed\b', 'served', text)
    text = re.sub(r'\bpreserv\sed\b', 'preserved', text)
    text = re.sub(r'\bobserv\s', 'observe', text)
    text = re.sub(r'\bgrav\sen\b', 'graven', text)
    return text


def fix_fused_articles(text):
    """Fix fused articles and possessive fusions."""
    fused = {
        'ason': 'a son', 'adaughter': 'a daughter', 'alittle': 'a little',
        'awoman': 'a woman', 'aking': 'a king', 'ahomer': 'a homer',
        'ajar': 'a jar', 'adry': 'a dry', 'amad': 'a mad',
        'alamb': 'a lamb', 'awide': 'a wide', 'ablast': 'a blast',
        'asnare': 'a snare', 'anet': 'a net', 'aspirit': 'a spirit',
        'aman': 'a man', 'acity': 'a city', 'apirate': 'a pirate',
        'arobber': 'a robber', 'amorning': 'a morning', 'aflame': 'a flame',
        'acake': 'a cake', 'asilly': 'a silly', 'aheart': 'a heart',
        'astretched': 'a stretched', 'aworthless': 'a worthless',
        'adeceiver': 'a deceiver', 'amultitude': 'a multitude',
        'asacrifice': 'a sacrifice', 'apriest': 'a priest',
        'apriesthood': 'a priesthood', 'aprince': 'a prince',
        'ajudgment': 'a judgment', 'aharlot': 'a harlot',
        'aconfusion': 'a confusion', 'asting': 'a sting',
        'apanther': 'a panther', 'alion': 'a lion',
        'aheifer': 'a heifer', 'aparched': 'a parched',
        'aprey': 'a prey', 'achild': 'a child',
        'abird': 'a bird', 'adove': 'a dove',
        'aleafy': 'a leafy', 'afruitful': 'a fruitful',
        'ashepherd': 'a shepherd', 'aleopard': 'a leopard',
        'aconspiracy': 'a conspiracy', 'adivision': 'a division',
        'atestimony': 'a testimony', 'abalance': 'a balance',
        'acovenant': 'a covenant', 'agift': 'a gift',
        'atwig': 'a twig', 'acrooked': 'a crooked',
        'aword': 'a word', 'awife': 'a wife',
        'aprophet': 'a prophet',
    }
    for fused_word, replacement in fused.items():
        text = re.sub(r'\b' + fused_word + r'\b', replacement, text)
    # Possessive fusions
    text = re.sub(r"'s([a-z])", r"'s \1", text)
    return text


def main():
    cvc = [11, 23, 5, 19, 15, 11, 16, 14, 17, 15, 12, 14, 16, 9]
    filepath = REPO / "staging" / "validated" / "OT" / "HOS.md"

    # First, restore original content
    filepath.write_text(ORIGINAL_CONTENT.lstrip('\n'), encoding='utf-8')
    print("Restored original HOS.md")

    # Parse original content
    lines = ORIGINAL_CONTENT.lstrip('\n').split('\n')

    verse_re = re.compile(r'^HOS\.0:(\d+)\s(.+)$')
    heading_re = re.compile(r'^(###\s.+)$')

    # Extract verse items in order: (line_index, vnum, text)
    # Also track headings
    items = []  # ('verse', vnum, text) or ('heading', text)
    for line in lines:
        m_v = verse_re.match(line)
        m_h = heading_re.match(line)
        if m_v:
            items.append(('verse', int(m_v.group(1)), m_v.group(2)))
        elif m_h:
            items.append(('heading', 0, m_h.group(1)))

    # Now detect chapter boundaries by looking at verse number drops
    # Also use the CVC to validate
    # The key pattern: verse numbers go up within a chapter, then drop at chapter boundary
    # Chapter marker misreads: sometimes the chapter number appears as a verse before the real v1

    verse_items = [(i, v, t) for i, (typ, v, t) in enumerate(items) if typ == 'verse']
    print(f"Total verse items: {len(verse_items)}")

    # Strategy: Walk through verses, tracking current chapter.
    # When verse number drops below previous AND is small (<=3), it's likely a new chapter.
    # Use CVC to confirm expected verse count.

    # Let me first just print the verse number sequence to understand the pattern
    print("\nVerse number sequence:")
    for idx, (item_idx, vnum, text) in enumerate(verse_items):
        prev_v = verse_items[idx-1][1] if idx > 0 else 0
        marker = ""
        if vnum < prev_v:
            marker = " <-- DROP"
        if vnum <= 3 and prev_v > 5:
            marker += " <-- LIKELY CH BOUNDARY"
        print(f"  [{idx:3d}] v{vnum:2d}  {text[:60]}{marker}")

    # Now manually map based on the verse number pattern and CVC
    # CVC: ch1=11, ch2=23, ch3=5, ch4=19, ch5=15, ch6=11, ch7=16, ch8=14,
    #       ch9=17, ch10=15, ch11=12 (registry says 12 but Brenton says 11),
    #       ch12=14 (registry says 14, Brenton says 15),
    #       ch13=16 (registry says 16, Brenton says 15),
    #       ch14=9 (registry says 9, Brenton says 10)

    # Looking at the verse sequence from the original file:
    # The file starts with v3 (ch1 starts missing v1-2, or v1-2 had drop-cap issues)
    # v3, v4, v5, v6, v7, v8, v9, v10, v11 -> 9 verses, but ch1 has 11 verses (v1-v11)
    # Then v2 <DROP> -> this is ch2:2 (since OSB has 1:10-11 = Brenton 2:1-2)
    # Wait no. Looking at the CVC more carefully:
    # OSB ch1 has 11 verses (1:1 through 1:11)
    # OSB ch2 has 23 verses (2:1 through 2:23)

    # Verse text analysis:
    # v3 "So he went and took Gomer" = Brenton 1:3 -> OSB 1:3
    # v4 "Call his name Jezreel" = Brenton 1:4 -> OSB 1:4
    # ...
    # v9 "Call his name Lo-Ammi" = Brenton 1:9 -> OSB 1:9
    # v10 "Yet the number of children of Israel" = Brenton 2:1 -> OSB 1:10
    # v11 "children of Judah and children of Israel gathered" = Brenton 2:2 -> OSB 1:11
    # DROP to v2: "Plead with your mother" = Brenton 2:4 -> OSB 2:2
    # Wait, this should be 2:2 not 2:4. Let me reconsider.

    # Brenton ch2 has 25 verses. OSB ch2 has 23 verses.
    # Brenton 2:1-2 = OSB 1:10-11
    # So Brenton 2:3 = OSB 2:1 ("Say to your brother, My people")
    # But OSB 2:1 is missing from the file (it was "Say to your brother" which may be missing)
    # Brenton 2:4 = OSB 2:2 "Plead with your mother"
    # That matches! The file's v2 after the drop = OSB 2:2

    # So chapter 1 in the file = v3 through v11 (missing v1 and v2 — drop-cap issue)
    # Chapter 2 starts at v2 (= OSB 2:2, missing 2:1)
    # v3, v4, ... through v24 (v24 = OSB 2:24? But CVC says ch2 has 23 verses max v23)

    # Wait, let me look again. The file has v24 "And they shall say..." which would be
    # past ch2's max of 23. Actually looking at Brenton, ch2 verse 25 (last)=
    # "And I will sow her to me on the earth..." which in OSB = 2:23.
    # Then the NEXT verse should be ch3:1.
    # But in the file we see: v24 "And they shall say..." which is actually still part of
    # the ch2 content (Brenton 2:25 last words). Hmm, actually in OSB versification,
    # the "And they shall say" part IS 2:23 cont'd or could be separate.

    # Actually wait: OSB ch2 has 23 verses BUT Brenton ch2 has 25 verses. If OSB 1:10=Brenton 2:1
    # and OSB 1:11=Brenton 2:2, then OSB 2:1=Brenton 2:3, OSB 2:23=Brenton 2:25.
    # But looking at the file, after v23 there's v24 which would overflow ch2.
    # This means the OSB versification might be different from what's in the registry.

    # Let me just map by careful analysis. I'll use a manual chapter assignment approach.
    # For each chapter boundary, I know:
    # 1. Verses numbers drop to small values
    # 2. Sometimes ch number appears as false verse before real v1 starts

    print("\n\nNow doing manual chapter mapping...")
    print("Expected CVC:", cvc, "total:", sum(cvc))


if __name__ == '__main__':
    main()
