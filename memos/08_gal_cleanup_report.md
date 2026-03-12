# Galatians Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/GAL.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 8

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 7 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 1 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 22 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L20:
  - `GAL.0:1 1. A defense of Paul'sapostolic authority (1:1-2:21 ) The gift of the Holy Spirit to the Church (5:1-6:18 ) The Cross of Christ The life of faith Liv ing in the love of the Spirit (5:1 3-6:1 0) Concluding Remarks (6:11-18) The rule of faith (6:1 1 -1 7 ) Benediction (6:1 8)`
  + `GAL.0:1 1. A defense of Paul's apostolic authority (1:1-2:21 ) The gift of the Holy Spirit to the Church (5:1-6:18 ) The Cross of Christ The life of faith Liv ing in the love of the Spirit (5:1 3-6:1 0) Concluding Remarks (6:11-18) The rule of faith (6:1 1 -1 7 ) Benediction (6:1 8)`

L43:
  - `GAL.1:15 But when it pleased God, who separated me from my mother'swomb and called me through His grace,`
  + `GAL.1:15 But when it pleased God, who separated me from my mother's womb and called me through His grace,`

L50:
  - `GAL.1:19 But I saw none of the other apostles except James, the Lord'sbrother.`
  + `GAL.1:19 But I saw none of the other apostles except James, the Lord's brother.`

L69:
  - `GAL.2:9 and when James, Cephas, and John, who seemed to be pillars, perceived the grace that had been given to me, they gave me and Barnabas the right hand of fellowship, that we should go to the Gentiles and they to the circumcised .`
  + `GAL.2:9 and when James, Cephas, and John, who seemed to be pillars, perceived the grace that had been given to me, they gave me and Barnabas the right hand of fellowship, that we should go to the Gentiles and they to the circumcised.`

L115:
  - `GAL.3:15 Brethren, I speak in the manner of men: Though it is only aman'scovenant, yet if it is confirmed, no one annuls or adds to it.`
  + `GAL.3:15 Brethren, I speak in the manner of men: Though it is only aman's covenant, yet if it is confirmed, no one annuls or adds to it.`

L138:
  - `GAL.3:29 And if you are Christ's, then you are Abraham'sseed, and heirs according to the promise.`
  + `GAL.3:29 And if you are Christ's, then you are Abraham's seed, and heirs according to the promise.`

L209:
  - `GAL.5:24 And those who are Christ'shave crucified the flesh with its passions and desires.`
  + `GAL.5:24 And those who are Christ's have crucified the flesh with its passions and desires.`

L218:
  - `GAL.6:2 Bear one another'sburdens, and so fulfill the law of Christ.`
  + `GAL.6:2 Bear one another's burdens, and so fulfill the law of Christ.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| GAL.1:1 | `aul, an apostle (not from men nor through man, but...` |
| GAL.1:2 | `and all the brethren who are with me, To the churc...` |
| GAL.1:4 | `who gave Himself for our sins, that He might deliv...` |
| GAL.1:5 | `to whom be glory forever and ever. Amen....` |
| GAL.1:7 | `which is not another; but there are some who troub...` |
| GAL.1:16 | `to reveal His Son in me, that I might preach Him a...` |
| GAL.1:17 | `nor did I go up to Jerusalem to those who were apo...` |
| GAL.2:1 | `hen after fourteen years I went up again to Jerusa...` |
| GAL.2:5 | `to whom we did not yield submission even for an ho...` |
| GAL.2:9 | `and when James, Cephas, and John, who seemed to be...` |
| GAL.2:12 | `for before certain men came from James, he would e...` |
| GAL.3:1 | `foolish Galatians! Who has bewitched you that you ...` |
| GAL.3:6 | `just as Abraham 'believed God, and it was accounte...` |
| GAL.3:14 | `that the blessing of Abraham might come upon the G...` |
| GAL.4:1 | `ow I say that the heir, as long as he is achild, d...` |
| GAL.4:2 | `but is under guardians and stewards until the time...` |
| GAL.4:5 | `to redeem those who were under the law, that we mi...` |
| GAL.4:24 | `which things are symbolic. For these are the atwo ...` |
| GAL.4:25 | `for this Hagar is Mount Sinai in Arabia, and corre...` |
| GAL.4:26 | `but the Jerusalem above is free, which is the moth...` |
| GAL.5:1 | `tand fast therefore in the liberty by which Christ...` |
| GAL.6:1 | `rethren, if aman is overtaken in any trespass, you...` |
