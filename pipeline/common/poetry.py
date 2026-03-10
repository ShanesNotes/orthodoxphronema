"""Shared helpers for pdftotext-driven poetry and wisdom extraction."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Pattern, Sequence


DEFAULT_POETRY_SPLIT_WORD_PAIRS: tuple[tuple[str, str], ...] = (
    (r"\bhav e\b", "have"),
    (r"\blov e\b", "love"),
    (r"\bev il\b", "evil"),
    (r"\bov er\b", "over"),
    (r"\bev er\b", "ever"),
    (r"\bev ery\b", "every"),
    (r"\bnev er\b", "never"),
    (r"\bev en\b", "even"),
    (r"\bwiv es\b", "wives"),
    (r"\bliv e\b", "live"),
    (r"\bliv ing\b", "living"),
    (r"\bgiv e\b", "give"),
    (r"\bserv e\b", "serve"),
    (r"\bsav e\b", "save"),
    (r"\breceiv e\b", "receive"),
    (r"\bdeceiv e\b", "deceive"),
    (r"\bresolv e\b", "resolve"),
    (r"\bobser v\b", "observ"),
    (r"\bbeliev e\b", "believe"),
    (r"\bforgiv e\b", "forgive"),
    (r"\bprov e\b", "prove"),
    (r"\bprov ok\b", "provok"),
    (r"\bheav en\b", "heaven"),
    (r"\bsalv ation\b", "salvation"),
    (r"\bdriv e\b", "drive"),
    (r"\bv essel\b", "vessel"),
    (r"\bm e\b", "me"),
    (r"\bm ultiply\b", "multiply"),
    (r"\bm an\b", "man"),
    (r"\bB lessed\b", "Blessed"),
    (r"\bB ut\b", "But"),
    (r"\bT he\b", "The"),
    (r"\bA nd\b", "And"),
    (r"\bF or\b", "For"),
    (r"\bN or\b", "Nor"),
    (r"\bW ho\b", "Who"),
    (r"\bW hy\b", "Why"),
    (r"\bY ou\b", "You"),
)


@dataclass(frozen=True)
class PoetryExtractionConfig:
    """Configuration for sequential pdftotext-driven poetry extraction."""

    book_code: str
    chapter_header_prefixes: tuple[str, ...] = ()
    chapter_header_regexes: tuple[str, ...] = ()
    first_chapter_bootstrap_phrases: tuple[str, ...] = ()
    split_word_pairs: tuple[tuple[str, str], ...] = DEFAULT_POETRY_SPLIT_WORD_PAIRS
    chapter_start_phrases: dict[int, Sequence[str]] = None


def clean_poetry_text(
    text: str,
    split_word_pairs: Sequence[tuple[str, str]] = DEFAULT_POETRY_SPLIT_WORD_PAIRS,
) -> str:
    """Normalize OCR punctuation, whitespace, and common pdftotext kerning splits."""
    cleaned = text.replace("\t", " ")
    cleaned = cleaned.replace("“", '"').replace("”", '"')
    cleaned = cleaned.replace("‘", "'").replace("’", "'")
    cleaned = cleaned.replace("—", "--").replace("–", "-")
    cleaned = re.sub(r" {2,}", " ", cleaned)
    for pattern, replacement in split_word_pairs:
        cleaned = re.sub(pattern, replacement, cleaned)
    return cleaned.strip()


def compile_chapter_header_patterns(config: PoetryExtractionConfig) -> tuple[Pattern[str], ...]:
    """Compile configurable book-header patterns such as 'Psalm 1' or 'Proverbs 3'."""
    patterns: list[Pattern[str]] = []
    # 1. Standalone digits (common in Job/Proverbs in pdftotext output)
    patterns.append(re.compile(r"^\s*(?P<chapter>\d+)\s*$", re.IGNORECASE))
    
    # 2. Prefixed headers
    for prefix in config.chapter_header_prefixes:
        patterns.append(
            re.compile(
                rf"^(?:{re.escape(prefix)})\s+(?P<chapter>\d+)\b[\s:.-]*(?P<text>.*)$",
                re.IGNORECASE,
            )
        )
    for regex in config.chapter_header_regexes:
        patterns.append(re.compile(regex, re.IGNORECASE))
    return tuple(patterns)


def match_chapter_header(
    line: str,
    patterns: Sequence[Pattern[str]],
) -> tuple[int, str] | None:
    """Return (chapter_num, trailing_text) when a configured header is detected."""
    for pattern in patterns:
        match = pattern.match(line)
        if not match:
            continue
        groupdict = match.groupdict()
        chapter_raw = groupdict.get("chapter") or (match.group(1) if len(match.groups()) >= 1 else None)
        if chapter_raw is None:
            continue
        trailing = groupdict.get("text")
        if trailing is None:
            trailing = match.group(2) if len(match.groups()) >= 2 else line[match.end() :]
        return int(chapter_raw), trailing.strip()
    return None


def parse_leading_verse_number(line: str) -> tuple[int, str] | None:
    """Return (verse_num, trailing_text) if the line starts with a verse number."""
    match = re.match(r"^(\d+)\s*(.*)", line)
    if not match:
        return None
    return int(match.group(1)), match.group(2)


def matches_bootstrap_phrase(
    line: str,
    phrases: Sequence[str],
    split_word_pairs: Sequence[tuple[str, str]] = DEFAULT_POETRY_SPLIT_WORD_PAIRS,
) -> bool:
    """True when a cleaned line contains one of the configured bootstrap phrases."""
    if not phrases:
        return False
    cleaned = clean_poetry_text(line, split_word_pairs).lower()
    return any(phrase.lower() in cleaned for phrase in phrases)


def matches_phrase_list(line: str, phrases: Sequence[str], split_word_pairs) -> bool:
    if not phrases:
        return False
    cleaned = clean_poetry_text(line, split_word_pairs).lower()
    return any(clean_poetry_text(phrase, split_word_pairs).lower() in cleaned for phrase in phrases)


# Inline verse number: preceded by punctuation/whitespace, followed by capital or lowercase letter, with optional space
RE_INLINE_VERSE = re.compile(r"(?:[.!?†ω]|\s|^)(\d+)\s*([A-Za-z])")

# Narrative heading: Title Case words, usually on its own line, relatively short
RE_NARRATIVE_HEADING = re.compile(r"^\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,8})\s*$")

def extract_poetry_lines(lines: Sequence[str], config: PoetryExtractionConfig) -> str:
    """Run the sequential verse-buffer state machine for poetry / wisdom text."""
    header_patterns = compile_chapter_header_patterns(config)
    print("DEBUG CONFIG:")
    print("bootstrap:", config.first_chapter_bootstrap_phrases)
    print("starts:", config.chapter_start_phrases.get(1) if config.chapter_start_phrases else None)
    
    current_chapter = 0
    current_verse = 0
    verse_buffer = ""
    output_lines: list[str] = []
    pending_narrative_heading = ""

    def flush_verse() -> None:
        nonlocal verse_buffer
        if current_chapter > 0 and current_verse > 0 and verse_buffer:
            cleaned = clean_poetry_text(verse_buffer, config.split_word_pairs)
            # Remove redundant verse number artifact at start of text
            cleaned = re.sub(rf"^{current_verse}\s*", "", cleaned)
            output_lines.append(f"{config.book_code}.{current_chapter}:{current_verse} {cleaned}")
        verse_buffer = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 1. Check Manifest-Driven Chapter Starts
        if config.chapter_start_phrases:
            next_ch = current_chapter + 1
            if next_ch in config.chapter_start_phrases:
                if matches_phrase_list(line, config.chapter_start_phrases[next_ch], config.split_word_pairs):
                    print(f"DEBUG: Manifest match for chapter {next_ch} on line: {line}")
                    flush_verse()
                    current_chapter = next_ch
                    current_verse = 1
                    output_lines.append(f"\n## Chapter {current_chapter}\n")
                    if pending_narrative_heading:
                        output_lines.append(pending_narrative_heading + "\n")
                        pending_narrative_heading = ""
                    # Don't skip processing the line, it contains verse 1 text

        if current_chapter == 0 and matches_bootstrap_phrase(
            line,
            config.first_chapter_bootstrap_phrases,
            config.split_word_pairs,
        ):
            print(f"DEBUG: Bootstrap match on line: {line}")
            flush_verse()
            current_chapter = 1
            current_verse = 1
            output_lines.append(f"\n## Chapter {current_chapter}\n")
            verse_buffer = line
            continue

        # Look for narrative headings first
        nh_match = RE_NARRATIVE_HEADING.match(line)
        if nh_match:
            # We don t flush yet, just store it as pending
            pending_narrative_heading = f"### {nh_match.group(1)}"
            continue

        header = match_chapter_header(line, header_patterns)
        if header is not None:
            new_ch, trailing = header
            
            # Sequence disambiguation: if the number could be the NEXT VERSE, it's a verse, not a chapter.
            # Unless we have a pending narrative heading, which strongly signals a chapter boundary.
            is_valid_advance = (new_ch == current_chapter + 1) and (new_ch != current_verse + 1)
            if pending_narrative_heading and (new_ch == current_chapter + 1):
                is_valid_advance = True
                
            is_bootstrap = (current_chapter == 0 and new_ch == 1)
            
            if is_bootstrap or is_valid_advance:
                # Don't advance if manifest is active and we didn't match it
                if not config.chapter_start_phrases or new_ch <= current_chapter:
                    flush_verse()
                    current_chapter = new_ch
                    current_verse = 1
                    output_lines.append(f"\n## Chapter {current_chapter}\n")
                    if pending_narrative_heading:
                        output_lines.append(pending_narrative_heading + "\n")
                        pending_narrative_heading = ""
                    verse_buffer = trailing
                    continue

        if current_chapter == 0:
            continue

        # If we had a pending heading but didn t find a chapter number,
        # it was just a regular section header.
        if pending_narrative_heading:
            output_lines.append(pending_narrative_heading + "\n")
            pending_narrative_heading = ""

        # Look for verse numbers in the line (start or inline)
        pos = 0
        while pos < len(line):
            match = RE_INLINE_VERSE.search(line, pos)
            if not match:
                chunk = line[pos:]
                if current_verse > 0:
                    verse_buffer += " " + chunk
                else:
                    output_lines.append(f"### {clean_poetry_text(chunk, config.split_word_pairs)}")
                break
            
            v_num = int(match.group(1))
            pre_text = line[pos:match.start(1)]
            if current_verse > 0:
                verse_buffer += " " + pre_text
            
            if v_num == current_verse + 1 or v_num == current_verse + 2:
                if v_num == current_verse + 2:
                    flush_verse()
                    current_verse = v_num - 1
                    flush_verse()
                else:
                    flush_verse()
                
                current_verse = v_num
                verse_buffer = match.group(2)
                pos = match.end(2)
            else:
                if current_verse > 0:
                    verse_buffer += match.group(0)
                pos = match.end(0)

    flush_verse()
    return "\n".join(output_lines)
