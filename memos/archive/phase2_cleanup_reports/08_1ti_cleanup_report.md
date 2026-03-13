# 1 Timothy Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/1TI.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 6

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 7 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 20 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L56:
  - `1TI.2:2 The deacons, literally'servants,' are ordained to serve the Church and must meet high qualifications (1Ti 3:8-13). The apostles were the first to take on the service tasks of deacons, and when the workload became too great they called for'seven men of good reputation, full of the Holy Spirit and wisdom, whom we may appoint over this business' (Acts 6:3). Besides serving the material needs of the people, deacons occupy acrucial role in the liturgical life of the Church.`
  + `1TI.2:2 The deacons, literally's ervants,' are ordained to serve the Church and must meet high qualifications (1Ti 3:8-13). The apostles were the first to take on the service tasks of deacons, and when the workload became too great they called for's even men of good reputation, full of the Holy Spirit and wisdom, whom we may appoint over this business' (Acts 6:3). Besides serving the material needs of the people, deacons occupy acrucial role in the liturgical life of the Church.`

L76:
  - `1TI.2:16 T he New Testament teaches that all four 'orders' which form the government of the Church -laity, deacons, presbyters, and bishops-are necessary to the proper functioning of the body of Christ. All four are clearly visible in Paul'sfirst letter to Timothy.`
  + `1TI.2:16 T he New Testament teaches that all four 'orders' which form the government of the Church -laity, deacons, presbyters, and bishops-are necessary to the proper functioning of the body of Christ. All four are clearly visible in Paul's first letter to Timothy.`

L161:
  - `1TI.5:22 Do not lay hands on anyone hastily, nor share in other people'ssins; keep yourself pure.`
  + `1TI.5:22 Do not lay hands on anyone hastily, nor share in other people's sins; keep yourself pure.`

L162:
  - `1TI.5:23 No longer drink only water, but use alittle wine for your stomach'ssake and your frequent infirmities.`
  + `1TI.5:23 No longer drink only water, but use alittle wine for your stomach's sake and your frequent infirmities.`

L163:
  - `1TI.5:24 Some men'ssins are clearly evident, preceding them to judgment, but those of some men follow later.`
  + `1TI.5:24 Some men's sins are clearly evident, preceding them to judgment, but those of some men follow later.`

L188:
  - `1TI.6:14 that you keep this commandment without spot, blameless until our Lord Jesus Christ'sappearing,`
  + `1TI.6:14 that you keep this commandment without spot, blameless until our Lord Jesus Christ's appearing,`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| 1TI.1:19 | `having faith and agood conscience, which some havi...` |
| 1TI.1:20 | `of whom are Hymenaeus and Alexander, whom I delive...` |
| 1TI.2:6 | `who gave Himself aransom for all, to be testified ...` |
| 1TI.2:7 | `for which I was appointed apreacher and an apostle...` |
| 1TI.2:9 | `in like manner also, that the women adorn themselv...` |
| 1TI.2:10 | `but, which is proper for women professing godlines...` |
| 1TI.2:17 | `and Titus 1:7-9 underscore this role. Nonetheless,...` |
| 1TI.3:1 | `his is afaithful saying: If aman desires the posit...` |
| 1TI.3:3 | `not given to wine, not violent, not greedy for mon...` |
| 1TI.3:6 | `not anovice, lest being puffed up with pride he fa...` |
| 1TI.3:15 | `but if I am delayed, I write so that you may know ...` |
| 1TI.4:1 | `ow the Spirit expressly says that in latter times ...` |
| 1TI.4:5 | `for it is sanctified by the word of God and prayer...` |
| 1TI.5:1 | `onot rebuke an older man, but exhort him as afathe...` |
| 1TI.5:12 | `having condemnation because they have cast off the...` |
| 1TI.6:1 | `et as many bondservants as are under the yoke coun...` |
| 1TI.6:4 | `he is proud, knowing nothing, but is obsessed with...` |
| 1TI.6:14 | `that you keep this commandment without spot, blame...` |
| 1TI.6:15 | `which He will manifest in His own time, He who is ...` |
| 1TI.6:16 | `who alone has immortality, dwelling in unapproacha...` |
