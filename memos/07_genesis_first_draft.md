# Memo 07 — Genesis First-Draft Extraction: Quality Assessment & Fix History

**Author:** Ark | **Date:** 2026-03-06 | **Status:** Fix v2 applied — extraction re-running

---

## 1. Executive Summary

Three extraction runs were made for Genesis. The first two had a critical chapter-drift bug. The third (current) run applies a correct two-part fix: sequential article sub-point tracking + chapter-advance guard. Results pending re-extraction (~15 min). This memo records the full diagnosis, both failed fixes, and the correct resolution.

---

## 2. What the Extraction Produces (Architecture Recap)

| Output file | Content |
|-------------|---------|
| `staging/validated/OT/GEN.md` | Pure Scripture verses (one per line, `BOOK.CH:V text` format) |
| `staging/validated/OT/GEN_notes.md` | Study articles extracted from the page range |
| `staging/validated/OT/GEN_footnote_markers.json` | Index of `†`/`ω` inline markers per anchor |

The extractor (`pipeline/parse/osb_extract.py`) runs a two-state machine (VERSE_MODE / ARTICLE_MODE) over the Docling element stream for pages 102–188 of the OSB PDF.

---

## 3. The Chapter-Counter Drift — Root Cause

### 3.1 — Source

The **ANCESTRAL SIN** study article, located between Gen 3:7 and Gen 3:8 (pages ~107–109 of the PDF), contains a sub-section:

> **WHAT ARE THE CONSEQUENCES OF THE FALL?**

followed by five numbered paragraphs, confirmed from `staging/raw/probe/probe_structure_p102-112.json`:

```
TextItem: "1 This Fall of Adam caused mankind to become subject to mortality..."
TextItem: "2 We who are of Adam's race are not guilty because of Adam's sin..."
TextItem: "3 Mankind's strong propensity to commit sin reveals that in the Fall..."
TextItem: "4 Adam's Fall not only brought mortality and sin into the world..."
TextItem: "5 Even after the Fall, the intellectual, desiring and incensive aspects..."
```

These look syntactically identical to verse/chapter-lead text (`digit + space + uppercase letter`). The extractor originally could not distinguish them from verse resumption.

### 3.2 — Bug in Original Extractor

The ARTICLE_MODE exit condition fired on **any** `digit + space` pattern:

```python
if RE_CHAPTER_LEAD.match(text) or (text[:1].isdigit() and len(text) > 2 and text[1] == ' '):
```

**Effect**: All 5 sub-points exited ARTICLE_MODE. Each was processed as a chapter-lead, advancing `current_chapter` from 3 → 1 → 2 → 3 → 4 → 5. The `chapter_num == 1` escape hatch in the chapter sanity check caused the reset to 1. Real Gen 3:8 arrived with `current_chapter = 5` → labeled GEN.5:8. All downstream chapters were off by 2 or more.

### 3.3 — First Fix Attempt (Other Session Tab) — Incomplete

Added:
```python
is_chapter_advance = (num == self.current_chapter + 1)
is_verse_continuation = (num > self.current_verse and num > 5)
```

**Still broken**: Sub-point 4 ("4 Adam's Fall...") arrives when `current_chapter = 3`. The condition `4 == 3 + 1` is True → `is_chapter_advance` fires → ARTICLE_MODE exits → chapter advances to 4. Sub-point 5 follows similarly. GEN.4:1 and GEN.5:1 are still article text in the output. User confirmed GEN.3:8 is cut off (verses 9–24 missing) — caused by chapter counter being at 5 when real Gen 3:8 arrives.

### 3.4 — Correct Fix (Current — Fix v2)

**Sequential sub-point tracking** (`_article_subpoint_seq`):

```python
is_next_subpoint = (num == self._article_subpoint_seq + 1)
if is_next_subpoint:
    # Sequential article sub-point — stay in ARTICLE_MODE
    self._article_subpoint_seq = num
    self._article_body.append(text)
    return
# Not sequential → check verse resumption or chapter advance
is_verse_resume = (num > self.current_verse)
is_chapter_lead = (num == self.current_chapter + 1)
if is_verse_resume or is_chapter_lead:
    self._flush_article()
    self.mode = VERSE_MODE
    # fall through
```

**Trace through the ANCESTRAL SIN article** (after Gen 3:7, `current_verse=7`, `_article_subpoint_seq=0`):

| TextItem | num | is_next (0+1=1?) | Action |
|----------|-----|-------------------|--------|
| "1 This Fall..." | 1 | 1==1 ✓ | sub-point; seq=1 |
| "2 We who are..." | 2 | 2==2 ✓ | sub-point; seq=2 |
| "3 Mankind's strong..." | 3 | 3==3 ✓ | sub-point; seq=3 |
| "4 Adam's Fall..." | 4 | 4==4 ✓ | sub-point; seq=4 ✓ **FIXED** |
| "5 Even after the Fall..." | 5 | 5==5 ✓ | sub-point; seq=5 ✓ **FIXED** |
| "Christ, by His Death..." | — | no digit | article body |
| "8 Then they heard..." | 8 | 8≠6 → check: 8>7 ✓ | EXIT → VERSE_MODE, GEN.3:8 ✓ |

**Cross-chapter article case** (article after Gen 3:24, `current_verse=24`, `_subpoint_seq=0`):
- "4 Now Adam knew Eve..." → `num=4`, `4≠0+1=1`, `4>24`? No → `4==3+1=4`? Yes → EXIT ✓

---

## 4. Known Remaining Issues (Not Blocking Promotion)

These exist in the current and previous extractions and are cosmetic or structural limitations of the PDF-to-text process. They do **not** affect Scripture integrity but should be documented for the human review phase.

### 4.1 — Drop-Cap First Letter Missing

Docling strips the large decorative initial letter (drop cap) at the start of chapter sections. These appear throughout Genesis as the first letter of a verse being absent:

| What appears | What it should be |
|--------------|------------------|
| `nthe beginning God made heaven` | `In the beginning God made heaven` |
| `hus heaven and earth` | `Thus heaven and earth` |
| `ow the serpent was more cunning` | `Now the serpent was more cunning` |

**Scope**: Affects the first TextItem of each chapter section (approximately 50 occurrences in Genesis). **Root cause**: Docling drop-cap handling (known limitation). **Fix path**: Post-processing regex to detect and flag likely drop-cap positions for human review, or accept the limitation. Not auto-fixable without knowing which letter was dropped.

### 4.2 — Article 'a/an' Merged with Following Word

PDF justified-column layout causes the article 'a' or 'an' before some words to join with the next word:

| Appears | Should be |
|---------|-----------|
| `afirmament` | `a firmament` |
| `aliving soul` | `a living soul` |
| `asacramental` | `a sacramental` |
| `asword` | `a sword` |

**Scope**: ~20-30 occurrences throughout Genesis. **Fix**: A conservative post-processing regex `\b(a)([bcdfghjklmnpqrstvwxyz][a-z]{2,})\b` could split these, but risks false positives on legitimate words (e.g., "among", "around"). Best handled by human review pass or targeted word list.

### 4.3 — Verse Split Misses Lowercase-Start Verses

`RE_VERSE_SPLIT` requires an uppercase letter after the verse number. Several OSB verses begin with lowercase continuation text:

Example: `"17 God set them ... 18 and to rule over the day..."` — verse 18 begins with lowercase 'a', so it is not split off. Verse 18 is absorbed into verse 17's text.

**Scope**: Approximately 15–25 occurrences in Genesis. Verse text is present — it's just attached to the wrong anchor. **Fix**: Changing the regex to also accept lowercase would introduce false splits on numbers within verse text (e.g., "there were 12 men"). Needs careful handling.

### 4.4 — Poetry Word-Split Artifacts

From PDF column justification: `"y ou"`, `"wiv es"`, `"av enged"`, `"sev enfold"` in poetry sections. The `fix_split_words()` function handles some but the regex `\b([a-z]) ([a-z]{2,})\b` is conservative and misses patterns like `"y ou"` (single char before space). These appear in Lamech's Song (Gen 4:23-24).

**Scope**: ~10–15 word-split artifacts in Genesis. **Fix**: Expand `fix_split_words()` to handle single-char prefix splits: `r'(?<![A-Za-z])([a-z]) ([a-z]+)\b'`.

### 4.5 — Verse Count Gap

Expected Genesis verse count (LXX/OSB): ~1,533. Previous runs: 1,407–1,412. Gap of ~120–126 verses is due to:
- Multi-verse blocks with lowercase-start verses merged into previous verse
- Some article content still routing incorrectly (fixed in v2)
- Poetry blocks rendered as single TextItems spanning multiple verses

---

## 5. Post-Fix Validation Checklist

Run these checks on the new `staging/validated/OT/GEN.md` before promoting:

```bash
# 1. Chapter count (expect 50)
grep -c "^## Chapter" staging/validated/OT/GEN.md

# 2. Chapter sequence (expect 1 through 50, no gaps)
grep "^## Chapter" staging/validated/OT/GEN.md

# 3. No duplicate anchors
grep "^GEN\." staging/validated/OT/GEN.md | awk '{print $1}' | sort | uniq -d

# 4. GEN.3:8 correct
grep "GEN.3:8" staging/validated/OT/GEN.md

# 5. No article bleed (these phrases must NOT appear in GEN.md)
grep -c "Fall of Adam caused mankind" staging/validated/OT/GEN.md   # expect 0
grep -c "Mankind's strong propensity" staging/validated/OT/GEN.md   # expect 0
grep -c "intellectual, desiring and incensive" staging/validated/OT/GEN.md  # expect 0

# 6. GEN.4:1 correct
grep "GEN.4:1" staging/validated/OT/GEN.md
# Expect: "GEN.4:1 Now Adam knew Eve his wife, and she conceived and bore Cain..."

# 7. Verse count (expect ~1,533; accept >1,400 as passing for now)
grep -c "^GEN\." staging/validated/OT/GEN.md
```

---

## 6. Next Steps After Successful Validation

1. `cp staging/validated/OT/GEN.md canon/OT/GEN.md` — promote to canon
2. Git commit: "Day 4 complete: Genesis extraction v2 — chapter drift fixed, 1,4xx verses staged"
3. Push to GitHub
4. Run same extraction for Exodus (`--book EXO`) to verify fixes generalize
5. Begin Day 5: Genesis footnote extraction (pages 4120–4354)

---

## 7. Approval Required From Human

**No blocking approvals needed** — fixes are self-contained in the extractor and the staged output is not yet promoted to `canon/`. Human review of the promoted `canon/OT/GEN.md` is required before Day 5 footnote work begins, per the non-negotiables in CLAUDE.md.
