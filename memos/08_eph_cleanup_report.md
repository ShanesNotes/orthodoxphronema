# Ephesians Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/EPH.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 1

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 1 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 51 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L135:
  - `EPH.4:7 But to each one of us grace was given according to the measure of Christ'sgift.`
  + `EPH.4:7 But to each one of us grace was given according to the measure of Christ's gift.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| EPH.1:4 | `just as He chose us in Him before the foundation o...` |
| EPH.1:5 | `having predestined us to adoption as sons by Jesus...` |
| EPH.1:6 | `to the praise of the glory of His grace, by which ...` |
| EPH.1:8 | `which He made to abound toward us in all wisdom an...` |
| EPH.1:9 | `having made known to us the mystery of His will, a...` |
| EPH.1:10 | `that in the dispensation of the fullness of the ti...` |
| EPH.1:12 | `that we who first trusted in Christ should be to t...` |
| EPH.1:14 | `who ais the guarantee of our inheritance until the...` |
| EPH.1:17 | `that the God of our Lord Jesus Christ, the Father ...` |
| EPH.1:18 | `the eyes of your understanding abeing enlightened;...` |
| EPH.1:19 | `and what is the exceeding greatness of His power t...` |
| EPH.1:20 | `which He worked in Christ when He raised Him from ...` |
| EPH.1:21 | `far above all principality and power and might and...` |
| EPH.1:23 | `which is His body, the fullness of Him who fills a...` |
| EPH.2:6 | `and raised us up together, and made us sit togethe...` |
| EPH.2:7 | `that in the ages to come He might show the exceedi...` |
| EPH.2:9 | `not of works, lest anyone should boast....` |
| EPH.2:12 | `that at that time you were without Christ, being a...` |
| EPH.2:15 | `having abolished in His flesh the enmity, that is,...` |
| EPH.2:16 | `and that He might reconcile them both to God in on...` |
| EPH.2:20 | `having been built on the foundation of the apostle...` |
| EPH.2:21 | `in whom the whole building, being fitted together,...` |
| EPH.2:22 | `in whom you also are being built together for adwe...` |
| EPH.3:1 | `or this reason I, Paul, the prisoner of Christ Jes...` |
| EPH.3:2 | `if indeed you have heard of the dispensation of th...` |
| EPH.3:3 | `how that by revelation He made known to me the mys...` |
| EPH.3:6 | `that the Gentiles should be fellow heirs, of the s...` |
| EPH.3:9 | `and to make all see what is the fellowship aof the...` |
| EPH.3:10 | `to the intent that now the manifold wisdom of God ...` |
| EPH.3:11 | `according to the eternal purpose which He accompli...` |
| EPH.3:12 | `in whom we have boldness and access with confidenc...` |
| EPH.3:21 | `to Him be glory in the church by Christ Jesus to a...` |
| EPH.4:2 | `with all lowliness and gentleness, with longsuffer...` |
| EPH.4:12 | `for the equipping of the saints for the work of mi...` |
| EPH.4:18 | `having their understanding darkened, being alienat...` |
| EPH.4:19 | `who, being past feeling, have given themselves ove...` |
| EPH.4:21 | `if indeed you have heard Him and have been taught ...` |
| EPH.4:22 | `that you put off, concerning your former conduct, ...` |
| EPH.4:23 | `and be renewed in the spirit of your mind,...` |
| EPH.4:24 | `and that you put on the new man which was created ...` |
| EPH.4:27 | `nor give place to the devil....` |
| EPH.5:1 | `herefore be imitators of God as dear children....` |
| EPH.5:4 | `neither filthiness, nor foolish talking, nor coars...` |
| EPH.5:26 | `that He might sanctify and cleanse her with the wa...` |
| EPH.5:27 | `that He might present her to Himself aglorious chu...` |
| EPH.6:1 | `hildren, obey your parents in the Lord, for this i...` |
| EPH.6:6 | `not with eyeservice, as men-pleasers, but as bonds...` |
| EPH.6:7 | `with goodwill doing service, as to the Lord, and n...` |
| EPH.6:15 | `and having shod your feet with the preparation of ...` |
| EPH.6:16 | `above all, taking the shield of faith with which y...` |
| EPH.6:22 | `whom I have sent to you for this very purpose, tha...` |
