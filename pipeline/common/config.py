"""Pipeline configuration constants — extracted magic numbers.

Each constant documents its provenance and purpose. Import from here
rather than embedding raw numbers in pipeline code.
"""

# ── Chapter advance (osb_extract.py → ChapterTracker) ────────────────────────
# Primary threshold: advance only when current_verse >= this fraction of max_v.
# 80% comfortably excludes false advances while tolerating ~20% missed verses.
CHAPTER_ADVANCE_THRESHOLD = 0.80

# Fallback: if primary threshold isn't met but verse numbering would go backward,
# advance if current_verse >= this fraction (catches Docling drops > 20%).
CHAPTER_ADVANCE_FALLBACK = 0.60

# ── Brenton word-match (validate_canon.py V10, fix_articles.py) ──────────────
# Minimum fraction of Brenton significant words found in adjacent OSB verse
# to flag as absorbed content.
BRENTON_WORD_MATCH_THRESHOLD = 0.40

# ── Heading repetition limit (validate_canon.py V8) ──────────────────────────
# Maximum times a heading can repeat before V8 flags it.
HEADING_REPETITION_LIMIT = 3

# ── Article confidence (fix_articles.py) ─────────────────────────────────────
# Auto-apply threshold: candidates above this are applied automatically.
ARTICLE_CONFIDENCE_AUTO = 0.70

# Review threshold: candidates above this but below auto are flagged for review.
ARTICLE_CONFIDENCE_REVIEW = 0.50
