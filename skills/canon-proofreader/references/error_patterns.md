# Error Patterns Reference

Detailed examples of each error category caught by the canon-proofreader,
with notes on false-positive avoidance.

## P1 — Missing Space After Punctuation

**Pattern:** Punctuation immediately followed by a letter with no space.

**Examples from audit:**
- `MAT.1:25` — `Son.And` → `Son. And`
- `LUK.2:21` — `Child,His` → `Child, His`
- `ACT.1:12` — `Jerusalem,Sabbath` → `Jerusalem, Sabbath`
- `ROM.9:32` — `law.For` → `law. For`

**False positive guards:**
- Abbreviations like `v.1` or `i.e.` — excluded by requiring uppercase after period
- Verse anchors `GEN.1:1` — excluded by anchor-stripping before analysis
- Ellipsis `...` — excluded by requiring single period not preceded by period

**Concentrated in:** NT narrative books (MAT, LUK, ACT, ROM)

## P2 — Space Before Punctuation

**Pattern:** Whitespace immediately before closing punctuation.

**Examples:**
- `word .` → `word.`
- `text )` → `text)`
- `him ,` → `him,`
- `Lord 's` → `Lord's`

**Note:** Also catches space before possessive `'s`.

## P3 — Double Words

**Pattern:** Same word appearing twice consecutively.

**Examples:**
- `the the Lord` → `the Lord`
- `of of` → `of`

**Guard:** Minimum word length of 2 to avoid matching single-letter repetitions
that may be intentional (e.g., initials).

## P4 — Fused Preposition+Word

**Pattern:** A preposition fused to the following word without a space.

**Examples:**
- `ofthe` → `of the`
- `inthe` → `in the`
- `tothe` → `to the`
- `fromthe` → `from the`
- `withthe` → `with the`
- `ofhis` → `of his`
- `inhis` → `in his`

**False positive list:** Extensive — `often`, `into`, `together`, `forever`,
`within`, `without`, `offspring`, `inherit`, etc. All maintained in
`_load_false_positive_words()`.

**Aspell cross-check:** The script also checks whether the fused form is a
known dictionary word. If aspell recognizes the token, it's not flagged.

## P5 — Multiple Consecutive Spaces

**Pattern:** Two or more spaces in sequence within verse text.

**Usually from:** Docling extraction artifacts, column-merge residue.

## P6 — Spelling (Aspell)

**Pattern:** Words not recognized by aspell AND not in the biblical names allowlist.

**Allowlist:** `schemas/biblical_names.txt` — contains proper nouns from the
Septuagint/OSB text (place names, person names, transliterated terms).

**Common aspell false positives in biblical text:**
- Archaic English: `hast`, `hath`, `doth`, `thou`, `thee`, `thine`, `ye`
- Septuagint terms: `Sheol`, `Gehenna`, `Selah`, `Hallelujah`
- Transliterations: `Amen`, `Hosanna`, `Maranatha`

These should be in the allowlist; if they're flagged, add them.

## P7 — Unbalanced Quotes

**Pattern:** Odd number of double-quote characters in a verse.

**Note:** Single quotes are NOT checked for balance because apostrophes
(possessives, contractions) make single-quote counting unreliable.

**The OSB uses curly/smart quotes** — the regex handles `"`, `"`, `"`, `'`, `'`, `'`.

## P8 — Fused Conjunction+Word

**Pattern:** A conjunction fused to the following word.

**Examples:**
- `andhe` → `and he`
- `andthe` → `and the`
- `buthe` → `but he`
- `forhe` → `for he`
- `thathe` → `that he`
- `whenhe` → `when he`

**Same false-positive and aspell guards as P4.**
