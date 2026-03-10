"""
patterns.py — Shared regex patterns and word sets used across the pipeline.
"""
from __future__ import annotations

import re

# Anchor patterns — four named variants covering all use cases
RE_ANCHOR = re.compile(r'^([A-Z0-9]+)\.(\d+):(\d+)\s')
RE_ANCHOR_FULL = re.compile(r'^([A-Z0-9]+)\.(\d+):(\d+)\s+(.*)$')
RE_ANCHOR_PARTS = re.compile(r'^([A-Z0-9]+)\.(\d+):(\d+)$')
RE_VERSE_LINE = re.compile(r'^([A-Z0-9]+\.(\d+):(\d+)) (.+)')

# Chapter and frontmatter
RE_CHAPTER_HDR = re.compile(r'^## Chapter (\d+)')
RE_FM_FIELD = re.compile(r'^(\w+):\s*(.+)')

# Footnote markers and spaced caps (study article headers)
RE_FOOTNOTE_MARKERS = re.compile(r'[†ω]+')
RE_SPACED_CAPS = re.compile(r'^([A-Z][,]? ){2,}[A-Z]$')

# Anchor prefix (no trailing space, for use in normalize_reference_text)
RE_ANCHOR_PREFIX = re.compile(r'^([A-Z0-9]+)\.(\d+):(\d+)')

# Known split-word join targets
KNOWN_SPLIT_JOIN_WORDS = {
    "above", "alive", "alone", "approve", "arrive", "ashore",
    "believe", "beloved", "bereave", "beware", "brave",
    "captive", "carve", "cave", "conceive", "conserve",
    "curve", "deceive", "deliver", "derive", "deserve",
    "dissolve", "dive", "dove", "drive", "drove",
    "elusive", "Eve", "eve", "evening", "ever", "every",
    "evil", "evolve", "exclusive", "executive", "expensive",
    "forgave", "forgive", "forever",
    "gave", "give", "glove", "grave", "grieve", "groove", "grove",
    "have", "hive",
    "improve", "involve",
    "knave", "knive",
    "lave", "leave", "live", "love",
    "move",
    "native", "naive", "nerve", "neve", "never", "novel",
    "observe", "olive", "over", "oven",
    "pave", "perceive", "persevere", "preserve", "positive", "prove",
    "rave", "receive", "relative", "relieve", "remove", "reprieve",
    "reserve", "resolve", "retrieve", "revive", "revolve", "rove",
    "salve", "save", "serve", "severe", "shave", "shove", "shrive",
    "slave", "sleeve", "solve", "starve", "stave", "stove", "strive", "strove",
    "survive", "swerve",
    "thieve", "thrive", "throve", "trove", "twelve",
    "valve", "verve", "vine", "vive",
    "waive", "wave", "weave", "wive", "wove",
}

# Short prefixes for fix_omissions
SHORT_PREFIXES = {"a", "an", "in", "of", "to", "on", "as", "at", "by", "or"}
