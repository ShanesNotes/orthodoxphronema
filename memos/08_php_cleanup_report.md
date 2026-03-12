# Philippians Cleanup Report — 2026-03-11

## Summary
- Input: `staging/validated/NT/PHP.md`
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
| R6 | Drop-cap omissions detected (NO auto-fix) | 26 |
| R7 | Brenton-assisted fused compound splits | 0 |

## Before/After Examples (first 20 + last 20 changed lines)

L158:
  - `PHP.4:22 All the saints greet you, but especially those who are of Caesar'shousehold.`
  + `PHP.4:22 All the saints greet you, but especially those who are of Caesar's household.`


## Unresolved: Drop-Cap Omissions (R6 — human review required)

These verses begin with a lowercase letter, indicating the PDF drop-cap
first letter was not captured by Docling. Run dropcap_verify.py for
Brenton-backed classification.

| Anchor | Text (first 50 chars) |
|--------|-----------------------|
| PHP.1:10 | `that you may approve the things that are excellent...` |
| PHP.1:11 | `being filled with the fruits of righteousness whic...` |
| PHP.1:13 | `so that it has become evident to the whole palace ...` |
| PHP.1:14 | `and most of the brethren in the Lord, having becom...` |
| PHP.1:17 | `but the latter out of love, knowing that I am appo...` |
| PHP.1:20 | `according to my earnest expectation and hope that ...` |
| PHP.1:26 | `that your rejoicing for me may be more abundant in...` |
| PHP.1:28 | `and not in any way terrified by your adversaries, ...` |
| PHP.1:30 | `having the same conflict which you saw in me and n...` |
| PHP.2:1 | `herefore if there is any consolation in Christ, if...` |
| PHP.2:6 | `who, being in the form of God, did not consider it...` |
| PHP.2:7 | `but made Himself of no reputation, taking the form...` |
| PHP.2:10 | `that at the name of Jesus every knee should bow, o...` |
| PHP.2:11 | `and that every tongue should confess that Jesus Ch...` |
| PHP.2:13 | `for it is God who works in you both to will and to...` |
| PHP.2:15 | `that you may become blameless and harmless, childr...` |
| PHP.2:26 | `since he was longing for you all, and was distress...` |
| PHP.2:30 | `because for the work of Christ he came close to de...` |
| PHP.3:1 | `inally, my brethren, rejoice in the Lord. For me t...` |
| PHP.3:9 | `and be found in Him, not having my own righteousne...` |
| PHP.3:10 | `that I may know Him and the power of His resurrect...` |
| PHP.3:11 | `if, by any means, I may attain to the resurrection...` |
| PHP.3:19 | `whose end is destruction, whose god is their belly...` |
| PHP.3:21 | `who will transform our lowly body that it may be c...` |
| PHP.4:1 | `herefore, my beloved and longed-for brethren, my j...` |
| PHP.4:7 | `and the peace of God, which surpasses all understa...` |
