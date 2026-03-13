# Revelation Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/REV.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 8

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 8 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 52 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L50:
  - `REV.2:3 and you have persevered and have patience, and have labored for My name'ssake and have not become weary.`
  + `REV.2:3 and you have persevered and have patience, and have labored for My name's sake and have not become weary.`

L66:
  - `REV.2:13 'I know your works, and where you dwell, where Satan'sthrone is. And you hold fast to My name, and did not deny My faith even in the days in which Antipas was My faithful martyr, who was killed among you, where Satan dwells.`
  + `REV.2:13 'I know your works, and where you dwell, where Satan's throne is. And you hold fast to My name, and did not deny My faith even in the days in which Antipas was My faithful martyr, who was killed among you, where Satan dwells.`

L83:
  - `REV.2:27 'He shall rule them with arod of iron; They shall be dashed to pieces like the potter'svessels' a - as I also have received from My Father;`
  + `REV.2:27 'He shall rule them with arod of iron; They shall be dashed to pieces like the potter's vessels' a - as I also have received from My Father;`

L223:
  - `REV.8:4 And the smoke of the incense, with the prayers of the saints, ascended before God from the angel'shand.`
  + `REV.8:4 And the smoke of the incense, with the prayers of the saints, ascended before God from the angel's hand.`

L257:
  - `REV.9:8 They had hair like women'shair, and their teeth were like lions' teeth.`
  + `REV.9:8 They had hair like women's hair, and their teeth were like lions' teeth.`

L288:
  - `REV.10:10 And he said to me, 'Take and eat it; and it will make your stomach bitter, but it will be as sweet as honey in your mouth.' Then I took the little book out of the angel'shand and ate it, and it was as sweet as honey in my mouth. But when I had eaten it, my stomach became bitter.`
  + `REV.10:10 And he said to me, 'Take and eat it; and it will make your stomach bitter, but it will be as sweet as honey in your mouth.' Then I took the little book out of the angel's hand and ate it, and it was as sweet as honey in my mouth. But when I had eaten it, my stomach became bitter.`

L379:
  - `REV.14:1 hen I looked, and behold, a a Lamb standing on Mount Zion, and with Him one hundred and forty-four thousand, having b His Father'sname written on their foreheads.`
  + `REV.14:1 hen I looked, and behold, a a Lamb standing on Mount Zion, and with Him one hundred and forty-four thousand, having b His Father's name written on their foreheads.`

L595:
  - `REV.21:9 Then one of the seven angels who had the seven bowls filled with the seven last plagues came to me aand talked with me, saying, 'Come, I will show you the bride, the Lamb'swife.' b`
  + `REV.21:9 Then one of the seven angels who had the seven bowls filled with the seven last plagues came to me aand talked with me, saying, 'Come, I will show you the bride, the Lamb's wife.' b`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| REV.1:1 | `he Revelation of Jesus Christ, which God gave Him ...` |
| REV.1:2 | `who bore witness to the word of God, and to the te...` |
| REV.1:5 | `and from Jesus Christ, the faithful witness, the f...` |
| REV.1:11 | `saying, 'I am the Alpha and the Omega, the First a...` |
| REV.1:13 | `and in the midst of the seven lampstands One like ...` |
| REV.2:3 | `and you have persevered and have patience, and hav...` |
| REV.2:28 | `and I will give him the morning star....` |
| REV.4:1 | `fter these things I looked, and behold, adoor stan...` |
| REV.4:10 | `the twenty-four elders fall down before Him who si...` |
| REV.5:1 | `nd I saw in the right hand of Him who sat on the t...` |
| REV.5:12 | `saying with aloud voice: To receive power and rich...` |
| REV.6:1 | `ow I saw when the Lamb opened one of the seals; aa...` |
| REV.6:16 | `and said to the mountains and rocks, 'Fall on us a...` |
| REV.7:1 | `fter these things I saw four angels standing at th...` |
| REV.7:3 | `saying, 'Do not harm the earth, the sea, or the tr...` |
| REV.7:6 | `of the tribe of Asher twelvethousand were sealed; ...` |
| REV.7:7 | `of the tribe of Simeon twelvethousand were sealed;...` |
| REV.7:8 | `of the tribe of Zebulun twelvethousand were sealed...` |
| REV.7:10 | `and crying out with aloud voice, saying, 'Salvatio...` |
| REV.7:12 | `saying: 'Amen! Blessing and glory and wisdom, Than...` |
| REV.7:17 | `for the Lamb who is in the midst of the throne wil...` |
| REV.8:1 | `hen He opened the seventh seal, there was silence ...` |
| REV.9:1 | `hen the fifth angel sounded: And I saw astar falle...` |
| REV.9:14 | `saying to the sixth angel who had the trumpet, 'Re...` |
| REV.10:1 | `saw still another mighty angel coming down from he...` |
| REV.10:3 | `and cried with aloud voice, as when alion roars. W...` |
| REV.10:6 | `and swore by Him who lives forever and ever, who c...` |
| REV.10:7 | `but in the days of the sounding of the seventh ang...` |
| REV.11:1 | `hen I was given areed like ameasuring rod. And the...` |
| REV.11:17 | `saying: 'We give You thanks, O Lord God Almighty, ...` |
| REV.12:1 | `ow agreat sign appeared in heaven: awoman clothed ...` |
| REV.12:8 | `but they did not prevail, nor was aplace found for...` |
| REV.13:1 | `hen I astood on the sand of the sea. And I saw abe...` |
| REV.13:17 | `and that no one may buy or sell except one who has...` |
| REV.14:1 | `hen I looked, and behold, a a Lamb standing on Mou...` |
| REV.14:10 | `he himself shall also drink of the wine of the wra...` |
| REV.15:1 | `hen I saw another sign in heaven, great and marvel...` |
| REV.16:1 | `hen I heard aloud voice from the temple saying to ...` |
| REV.17:1 | `hen the seventh angel poured out his bowl into the...` |
| REV.18:1 | `fter these things I saw another angel coming down ...` |
| REV.18:16 | `and saying, 'Alas, alas, that great city that was ...` |
| REV.18:18 | `and cried out when they saw the smoke of her burni...` |
| REV.19:1 | `fter these things I heard a aloud voice of agreat ...` |
| REV.20:1 | `hen I saw an angel coming down from heaven, having...` |
| REV.20:3 | `and he cast him into the bottomless pit, and shut ...` |
| REV.20:8 | `and will go out to deceive the nations which are i...` |
| REV.21:1 | `ow I saw anew heaven and anew earth, for the first...` |
| REV.21:11 | `having the glory of God. Her light was like amost ...` |
| REV.21:13 | `three gates on the east, three gates on the north,...` |
| REV.21:20 | `the fifth sardonyx, the sixth sardius, the seventh...` |
| REV.22:1 | `ut I saw no temple in it, for the Lord God Almight...` |
| REV.22:19 | `and if anyone takes away from the words of the boo...` |
