# Colossians Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/COL.md`
- Mode: **in-place**
- Brenton reference: disabled
- Lines changed: 0

## Rules Applied

| Rule | Description | Count |
|------|-------------|-------|
| R1 | Split fused article compounds (allowlist) | 0 |
| R2 | Split fused possessives ('s + word) | 0 |
| R3 | Rejoin word-split artifacts (allowlist) | 0 |
| R4 | Rejoin hyphen-split line breaks (allowlist) | 0 |
| R5 | Remove trailing space before punctuation | 0 |
| R6 | Drop-cap omissions detected (NO auto-fix) | 27 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| COL.1:4 | `since we heard of your faith in Christ Jesus and o...` |
| COL.1:5 | `because of the hope which is laid up for you in he...` |
| COL.1:6 | `which has come to you, as it has also in all the w...` |
| COL.1:7 | `as you also learned from Epaphras, our dear fellow...` |
| COL.1:8 | `who also declared to us your love in the Spirit....` |
| COL.1:10 | `that you may walk worthy of the Lord, fully pleasi...` |
| COL.1:14 | `in whom we have redemption through His blood, athe...` |
| COL.1:20 | `and by Him to reconcile all things to Himself, by ...` |
| COL.1:22 | `in the body of His flesh through death, to present...` |
| COL.1:23 | `if indeed you continue in the faith, grounded and ...` |
| COL.1:25 | `of which I became aminister according to the stewa...` |
| COL.1:26 | `the mystery which has been hidden from ages and fr...` |
| COL.2:1 | `or I want you to know what agreat conflict I have ...` |
| COL.2:2 | `that their hearts may be encouraged, being knit to...` |
| COL.2:3 | `in whom are hidden all the treasures of wisdom and...` |
| COL.2:10 | `and you are complete in Him, who is the head of al...` |
| COL.2:14 | `having wiped out the handwriting of requirements t...` |
| COL.2:17 | `which are ashadow of things to come, but the subst...` |
| COL.2:19 | `and not holding fast to the Head, from whom all th...` |
| COL.2:22 | `which all concern things which perish with the usi...` |
| COL.3:1 | `fthen you were raised with Christ, seek those thin...` |
| COL.3:7 | `in which you yourselves once walked when you lived...` |
| COL.3:10 | `and have put on the new man who is renewed in know...` |
| COL.3:11 | `where there is neither Greek nor Jew, circumcised ...` |
| COL.4:1 | `asters, give your bondservants what is just and fa...` |
| COL.4:9 | `with Onesimus, afaithful and beloved brother, who ...` |
| COL.4:11 | `and Jesus who is called Justus. These are my only ...` |
