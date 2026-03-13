# 1 Corinthians Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/1CO.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 18

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 22 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 49 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L42:
  - `1CO.1:11 For it has been declared to me concerning you, my brethren, by those of Chloe'shousehold, that there are contentions among you.`
  + `1CO.1:11 For it has been declared to me concerning you, my brethren, by those of Chloe's household, that there are contentions among you.`

L85:
  - `1CO.2:13 These things we also speak, not in words which man'swisdom teaches but which the Holy a Spirit teaches, comparing spiritual things with spiritual.`
  + `1CO.2:13 These things we also speak, not in words which man's wisdom teaches but which the Holy a Spirit teaches, comparing spiritual things with spiritual.`

L102:
  - `1CO.3:9 For we are God'sfellow workers; you are God'sfield, you are God'sbuilding.`
  + `1CO.3:9 For we are God's fellow workers; you are God's field, you are God's building.`

L105:
  - `1CO.3:12 Now if anyone builds on this foundation with gold, silver, precious stones, wood, hay, straw, 13 each one'swork will become clear; for the Day will declare it, because it will be revealed by fire; and the fire will test each one'swork, of what sort it is.`
  + `1CO.3:12 Now if anyone builds on this foundation with gold, silver, precious stones, wood, hay, straw, 13 each one's work will become clear; for the Day will declare it, because it will be revealed by fire; and the fire will test each one's work, of what sort it is.`

L106:
  - `1CO.3:14 If anyone'swork which he has built on it endures, he will receive areward.`
  + `1CO.3:14 If anyone's work which he has built on it endures, he will receive areward.`

L107:
  - `1CO.3:15 If anyone'swork is burned, he will suffer loss; but he himself will be saved, yet so as through fire.`
  + `1CO.3:15 If anyone's work is burned, he will suffer loss; but he himself will be saved, yet so as through fire.`

L126:
  - `1CO.4:5 Therefore judge nothing before the time, until the Lord comes, who will both bring to light the hidden things of darkness and reveal the counsels of the hearts. Then each one'spraise will come from God.`
  + `1CO.4:5 Therefore judge nothing before the time, until the Lord comes, who will both bring to light the hidden things of darkness and reveal the counsels of the hearts. Then each one's praise will come from God.`

L131:
  - `1CO.4:10 We are fools for Christ'ssake, but you are wise in Christ! We are weak, but you are strong! You are distinguished, but we are dishonored!`
  + `1CO.4:10 We are fools for Christ's sake, but you are wise in Christ! We are weak, but you are strong! You are distinguished, but we are dishonored!`

L151:
  - `1CO.5:1 tis actually reported that there is sexual immorality among you, and such sexual immorality as is not even named aamong the Gentiles-that aman has his father'swife!`
  + `1CO.5:1 tis actually reported that there is sexual immorality among you, and such sexual immorality as is not even named aamong the Gentiles-that aman has his father's wife!`

L186:
  - `1CO.6:16 Or do you not know that he who is joined to aharlot is one body with her? For 'the two,' He says,'shall become one flesh.' a`
  + `1CO.6:16 Or do you not know that he who is joined to aharlot is one body with her? For 'the two,' He says,'s hall become one flesh.' a`

L217:
  - `1CO.7:22 For he who is called in the Lord while aslave is the Lord'sfreedman. Likewise he who is called while free is Christ'sslave.`
  + `1CO.7:22 For he who is called in the Lord while aslave is the Lord's freedman. Likewise he who is called while free is Christ's slave.`

L254:
  - `1CO.8:10 For if anyone sees you who have knowledge eating in an idol'stemple, will not the conscience of him who is weak be emboldened to eat those things offered to idols?`
  + `1CO.8:10 For if anyone sees you who have knowledge eating in an idol's temple, will not the conscience of him who is weak be emboldened to eat those things offered to idols?`

L291:
  - `1CO.9:23 Now this I do for the gospel'ssake, that I may be partaker of it with you.`
  + `1CO.9:23 Now this I do for the gospel's sake, that I may be partaker of it with you.`

L321:
  - `1CO.10:21 You cannot drink the cup of the Lord and the cup of demons; you cannot partake of the Lord'stable and of the table of demons.`
  + `1CO.10:21 You cannot drink the cup of the Lord and the cup of demons; you cannot partake of the Lord's table and of the table of demons.`

L327:
  - `1CO.10:24 Let no one seek his own, but each one the other'swell-being.`
  + `1CO.10:24 Let no one seek his own, but each one the other's well-being.`

L332:
  - `1CO.10:29 'Conscience,' I say, not your own, but that of the other. For why is my liberty judged by another man'sconscience?`
  + `1CO.10:29 'Conscience,' I say, not your own, but that of the other. For why is my liberty judged by another man's conscience?`

L370:
  - `1CO.11:26 For as often as you eat this bread and drink this cup, you proclaim the Lord'sdeath till He comes.`
  + `1CO.11:26 For as often as you eat this bread and drink this cup, you proclaim the Lord's death till He comes.`

L513:
  - `1CO.15:23 But each one in his own order: Christ the firstfruits, afterward those who are Christ'sat His coming.`
  + `1CO.15:23 But each one in his own order: Christ the firstfruits, afterward those who are Christ's at His coming.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 1CO.1:5 | `that you were enriched in everything by Him in all...` |
| 1CO.1:6 | `even as the testimony of Christ was confirmed in y...` |
| 1CO.1:7 | `so that you come short in no gift, eagerly waiting...` |
| 1CO.1:8 | `who will also confirm you to the end, that you may...` |
| 1CO.1:15 | `lest anyone should say that I had baptized in my o...` |
| 1CO.1:23 | `but we preach Christ crucified, to the Jews astumb...` |
| 1CO.1:24 | `but to those who are called, both Jews and Greeks,...` |
| 1CO.1:28 | `and the base things of the world and the things wh...` |
| 1CO.1:29 | `that no flesh should glory in His presence....` |
| 1CO.2:1 | `nd I, brethren, when I came to you, did not come w...` |
| 1CO.2:5 | `that your faith should not be in the wisdom of men...` |
| 1CO.2:8 | `which none of the rulers of this age knew; for had...` |
| 1CO.3:1 | `nd I, brethren, could not speak to you as to spiri...` |
| 1CO.3:3 | `for you are still carnal. For where there are envy...` |
| 1CO.4:1 | `et aman so consider us, as servants of Christ and ...` |
| 1CO.4:13 | `being defamed, we entreat. We have been made as th...` |
| 1CO.5:1 | `tis actually reported that there is sexual immoral...` |
| 1CO.6:1 | `are any of you, having amatter against another, go...` |
| 1CO.6:10 | `nor thieves, nor covetous, nor drunkards, nor revi...` |
| 1CO.7:1 | `ow concerning the things of which you wrote to me:...` |
| 1CO.7:9 | `but if they cannot exercise self-control, let them...` |
| 1CO.8:1 | `ow concerning things offered to idols: We know tha...` |
| 1CO.8:6 | `yet for us there is one God, the Father, of whom a...` |
| 1CO.9:1 | `m I not an apostle? Am I not free? Have I not seen...` |
| 1CO.9:20 | `and to the Jews I became as a Jew, that I might wi...` |
| 1CO.9:21 | `to those who are without law, as without law (not ...` |
| 1CO.9:22 | `to the weak I became as aweak, that I might win th...` |
| 1CO.10:1 | `oreover, brethren, I do not want you to be unaware...` |
| 1CO.10:9 | `nor let us tempt Christ, as some of them also temp...` |
| 1CO.10:10 | `nor complain, as some of them also complained, and...` |
| 1CO.10:26 | `for 'the earth is the L ORD 'S, and all its fullne...` |
| 1CO.10:33 | `just as I also please all men in all things, not s...` |
| 1CO.11:1 | `mitate me, just as I also imitate Christ....` |
| 1CO.11:24 | `and when He had given thanks, He broke it and said...` |
| 1CO.12:1 | `ow concerning spiritual gifts, brethren, I do not ...` |
| 1CO.12:8 | `for to one is given the word of wisdom through the...` |
| 1CO.12:9 | `to another faith by the same Spirit, to another gi...` |
| 1CO.12:10 | `to another the working of miracles, to another pro...` |
| 1CO.12:24 | `but our presentable parts have no need. But God co...` |
| 1CO.12:25 | `that there should be no schism in the body, but th...` |
| 1CO.13:1 | `hough I speak with the tongues of men and of angel...` |
| 1CO.14:1 | `ursue love, and desire spiritual gifts, but especi...` |
| 1CO.14:19 | `yet in the church I would rather speak five words ...` |
| 1CO.15:1 | `oreover, brethren, I declare to you the gospel whi...` |
| 1CO.15:4 | `and that He was buried, and that He rose again the...` |
| 1CO.15:5 | `and that He was seen by Cephas, then by the twelve...` |
| 1CO.15:52 | `in amoment, in the twinkling of an eye, at the las...` |
| 1CO.16:1 | `ow concerning the collection for the saints, as I ...` |
| 1CO.16:16 | `that you also submit to such, and to everyone who ...` |
