"""
pipeline.common — Shared utilities for the Orthodox Phronema pipeline.

Re-exports for convenience.
"""
from pipeline.common.paths import (
    REPO_ROOT,
    REGISTRY_PATH,
    STAGING_ROOT,
    CANON_ROOT,
    REPORTS_ROOT,
    BRENTON_DIR,
    MEMOS_DIR,
    SCHEMAS_DIR,
    PDF_PATH,
)
from pipeline.common.registry import (
    load_registry, book_meta, chapter_verse_counts,
    book_testament, page_ranges, load_residual_classes,
    classifications_requiring_entry_ratification,
)
from pipeline.common.frontmatter import parse_frontmatter, split_frontmatter, update_frontmatter_field
from pipeline.common.patterns import (
    RE_ANCHOR,
    RE_ANCHOR_FULL,
    RE_ANCHOR_PARTS,
    RE_VERSE_LINE,
    RE_CHAPTER_HDR,
    RE_FM_FIELD,
    RE_FOOTNOTE_MARKERS,
    RE_SPACED_CAPS,
    RE_ANCHOR_PREFIX,
    KNOWN_SPLIT_JOIN_WORDS,
    SHORT_PREFIXES,
)
from pipeline.common.text import (
    normalize_text, sha256_hex, discover_staged_books,
    discover_staged_paths, normalize_whitespace,
)
from pipeline.common.paths import BRENTON_SOURCE_DIR, GREEK_SOURCE_DIR
