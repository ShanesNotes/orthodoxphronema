# 2 Corinthians Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/2CO.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 7

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 8 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 41 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L21:
  - `2CO.0:5 A major purpose of this second epistle is Paul'sdefense of his apostleship and his polemic against false apostles in Corinth. Outsiders have shown up in Corinth calling themselves 'the most eminent apostles' (11:5; 12:11) or'super-apostles.' They claim to be better than Paul, alleging that he does not measure up (13:5-7). They seek to prove Paul an impostor, bringing all kinds of outrageous charges against him. In their preaching they elevate themselves (4:5) and present adifferent gospel from Paul's (11:4). They teach that Christians must have exalted spiritual experiences and lead successful, painless lives, and should not be concerned about moral purity and holiness (6:14-7:1).`
  + `2CO.0:5 A major purpose of this second epistle is Paul's defense of his apostleship and his polemic against false apostles in Corinth. Outsiders have shown up in Corinth calling themselves 'the most eminent apostles' (11:5; 12:11) or's uper-apostles.' They claim to be better than Paul, alleging that he does not measure up (13:5-7). They seek to prove Paul an impostor, bringing all kinds of outrageous charges against him. In their preaching they elevate themselves (4:5) and present adifferent gospel from Paul's (11:4). They teach that Christians must have exalted spiritual experiences and lead successful, painless lives, and should not be concerned about moral purity and holiness (6:14-7:1).`

L90:
  - `2CO.2:12 Furthermore, when I came to Troas to preach Christ'sgospel, and adoor was opened to me by the Lord,`
  + `2CO.2:12 Furthermore, when I came to Troas to preach Christ's gospel, and adoor was opened to me by the Lord,`

L132:
  - `2CO.4:2 But we have renounced the hidden things of shame, not walking in craftiness nor handling the word of God deceitfully, but by manifestation of the truth commending ourselves to every man'sconscience in the sight of God.`
  + `2CO.4:2 But we have renounced the hidden things of shame, not walking in craftiness nor handling the word of God deceitfully, but by manifestation of the truth commending ourselves to every man's conscience in the sight of God.`

L184:
  - `2CO.5:20 Now then, we are ambassadors for Christ, as though God were pleading through us: we implore you on Christ'sbehalf, be reconciled to God.`
  + `2CO.5:20 Now then, we are ambassadors for Christ, as though God were pleading through us: we implore you on Christ's behalf, be reconciled to God.`

L299:
  - `2CO.10:15 not boasting of things beyond measure, that is, in other men'slabors, but having hope, that as your faith is increased, we shall be greatly enlarged by you in our sphere,`
  + `2CO.10:15 not boasting of things beyond measure, that is, in other men's labors, but having hope, that as your faith is increased, we shall be greatly enlarged by you in our sphere,`

L300:
  - `2CO.10:16 to preach the gospel in the regions beyond you, and not to boast in another man'ssphere of accomplishment.`
  + `2CO.10:16 to preach the gospel in the regions beyond you, and not to boast in another man's sphere of accomplishment.`

L369:
  - `2CO.12:10 Therefore I take pleasure in infirmities, in reproaches, in needs, in persecutions, in distresses, for Christ'ssake. For when I am weak, then I am strong.`
  + `2CO.12:10 Therefore I take pleasure in infirmities, in reproaches, in needs, in persecutions, in distresses, for Christ's sake. For when I am weak, then I am strong.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 2CO.1:1 | `aul, an apostle of Jesus Christ by the will of God...` |
| 2CO.1:4 | `who comforts us in all our tribulation, that we ma...` |
| 2CO.1:10 | `who delivered us from so great adeath, and does ad...` |
| 2CO.1:11 | `you also helping together in prayer for us, that t...` |
| 2CO.1:16 | `to pass by way of you to Macedonia, to come again ...` |
| 2CO.1:22 | `who also has sealed us and given us the Spirit in ...` |
| 2CO.2:1 | `ut I determined this within myself, that I would n...` |
| 2CO.2:7 | `so that, on the contrary, you ought rather to forg...` |
| 2CO.2:11 | `lest Satan should take advantage of us; for we are...` |
| 2CO.3:1 | `owe begin again to commend ourselves? Or do we nee...` |
| 2CO.3:6 | `who also made us sufficient as ministers of the ne...` |
| 2CO.3:8 | `how will the ministry of the Spirit not be more gl...` |
| 2CO.4:1 | `herefore, since we have this ministry, as we have ...` |
| 2CO.4:4 | `whose minds the god of this age has blinded, who d...` |
| 2CO.5:1 | `or we know that if our earthly house, this tent, i...` |
| 2CO.5:3 | `if indeed, having been clothed, we shall not be fo...` |
| 2CO.5:15 | `and He died for all, that those who live should li...` |
| 2CO.5:19 | `that is, that God was in Christ reconciling the wo...` |
| 2CO.6:1 | `ethen, as workers together with Him also plead wit...` |
| 2CO.6:5 | `in stripes, in imprisonments, in tumults, in labor...` |
| 2CO.7:1 | `herefore, having these promises, beloved, let us c...` |
| 2CO.7:7 | `and not only by his coming, but also by the consol...` |
| 2CO.8:1 | `oreover, brethren, we make known to you the grace ...` |
| 2CO.8:2 | `that in agreat trial of affliction the abundance o...` |
| 2CO.8:11 | `but now you also must complete the doing of it; th...` |
| 2CO.8:14 | `but by an equality, that now at this time your abu...` |
| 2CO.8:19 | `and not only that, but who was also chosen by the ...` |
| 2CO.9:1 | `ow concerning the ministering to the saints, it is...` |
| 2CO.9:2 | `for I know your willingness, about which I boast o...` |
| 2CO.9:4 | `lest if some Macedonians come with me and find you...` |
| 2CO.10:1 | `ow I, Paul, myself am pleading with you by the mee...` |
| 2CO.10:15 | `not boasting of things beyond measure, that is, in...` |
| 2CO.10:16 | `to preach the gospel in the regions beyond you, an...` |
| 2CO.11:1 | `h, that you would bear with me in alittle folly-an...` |
| 2CO.11:26 | `in journeys often, in perils of waters, in perils ...` |
| 2CO.11:27 | `in weariness and toil, in sleeplessness often, in ...` |
| 2CO.11:33 | `but I was let down in abasket through awindow in t...` |
| 2CO.12:1 | `tis doubtless anot profitable for me to boast. I w...` |
| 2CO.12:4 | `how he was caught up into Paradise and heard inexp...` |
| 2CO.12:21 | `lest, when I come again, my God will humble me amo...` |
| 2CO.13:1 | `his will be the third time I am coming to you. 'By...` |
