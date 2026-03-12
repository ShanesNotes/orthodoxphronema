"""Shared helpers for pdftotext-driven poetry and wisdom extraction."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Pattern, Sequence


DEFAULT_POETRY_SPLIT_WORD_PAIRS = (
    (r"\bwhatev er\b", "whatever"),
    (r"\bS erv e\b", "Serve"),
    (r"\bServ e\b", "Serve"),
    (r"\btrem bling\b", "trembling"),
    (r"\bS av e\b", "Save"),
    (r"\bSav e\b", "Save"),
    (r"\bS ing\b", "Sing"),
    (r"\bSing\b", "Sing"),
    (r"\bP raise\b", "Praise"),
    (r"\bP raise Him\b", "Praise Him"),
    (r"\bP reserv e\b", "Preserve"),
    (r"\bH ear\b", "Hear"),
    (r"\bH ow\b", "How"),
    (r"\bH av e\b", "Have"),
    (r"\bL isten\b", "Listen"),
    (r"\blov e\b", "love"),
    (r"\bL ord\b", "Lord"),
    (r"\bO Lord\b", "O Lord"),
    (r"\bG iv e\b", "Give"),
    (r"\bGiv e\b", "Give"),
    (r"\bJ udge\b", "Judge"),
    (r"\bT o\b", "To"),
    (r"\bT he\b", "The"),
    (r"\bA nd\b", "And"),
    (r"\bB lessed\b", "Blessed"),
    (r"\bB ut\b", "But"),
    (r"\bF or\b", "For"),
    (r"\bN or\b", "Nor"),
    (r"\bW ho\b", "Who"),
    (r"\bW hy\b", "Why"),
    (r"\bY ou\b", "You"),
    (r"\bm y\b", "my"),
    (r"\by ou\b", "you"),
    (r"\by our\b", "your"),
    (r"\by ours\b", "yours"),
    (r"\bm ade\b", "made"),
    (r"\bm ake\b", "make"),
    (r"\bm ay\b", "may"),
    (r"\bm an\b", "man"),
    (r"\bm en\b", "men"),
    (r"\bm any\b", "many"),
    (r"\bm ore\b", "more"),
    (r"\bm ost\b", "most"),
    (r"\bm ercy\b", "mercy"),
    (r"\bm outh\b", "mouth"),
    (r"\bm ock\b", "mock"),
    (r"\bm ultiplied\b", "multiplied"),
    (r"\bm ultitude\b", "multitude"),
    (r"\bnam e\b", "name"),
    (r"\bpray er\b", "prayer"),
    (r"\brem em ber\b", "remember"),
    (r"\bSalv ation\b", "Salvation"),
    (r"\bsay ing\b", "saying"),
    (r"\bstream s\b", "streams"),
    (r"\btem ple\b", "temple"),
    (r"\bthem selves\b", "themselves"),
    (r"\btram ple\b", "trample"),
    (r"\btroublesom e\b", "troublesome"),
    (r"\bv ain\b", "vain"),
    (r"\bv anity\b", "vanity"),
    (r"\bv ery\b", "very"),
    (r"\bv iolence\b", "violence"),
    (r"\bv oice\b", "voice"),
    (r"\bev il\b", "evil"),
    (r"\bev ildoer\b", "evildoer"),
    (r"\benem y\b", "enemy"),
    (r"\benem ies\b", "enemies"),
    (r"\bey es\b", "eyes"),
    (r"\bcom e\b", "come"),
    (r"\bwaterless\b", "waterless"),
    (r"\banim als\b", "animals"),
    (r"\basham ed\b", "ashamed"),
    (r"\bam ong\b", "among"),
    (r"\bbecam e\b", "became"),
    (r"\bbecom e\b", "become"),
    (r"\bbey ond\b", "beyond"),
    (r"\bcom m and\b", "command"),
    (r"\bcom m anded\b", "commanded"),
    (r"\bem pty\b", "empty"),
    (r"\benm ity\b", "enmity"),
    (r"\bEv ery\b", "Every"),
    (r"\bexam ines\b", "examines"),
    (r"\bey e\b", "eye"),
    (r"\bHav e\b", "Have"),
    (r"\binstrum ents\b", "instruments"),
    (r"\bjudgm ent\b", "judgment"),
    (r"\bjudgm ents\b", "judgments"),
    (r"\bm editate\b", "meditate"),
    (r"\bm editates\b", "meditates"),
    (r"\bm ercies\b", "mercies"),
    (r"\bm idst\b", "midst"),
    (r"\bm iserable\b", "miserable"),
    (r"\bm ock\b", "mock"),
    (r"\bm oon\b", "moon"),
    (r"\bm orning\b", "morning"),
    (r"\bm ouths\b", "mouths"),
    (r"\bov ertake\b", "overtake"),
    (r"\brem em brance\b", "remembrance"),
    (r"\brem orse\b", "remorse"),
    (r"\bstam ped\b", "stamped"),
    (r"\bv isit\b", "visit"),
    (r"\by okes\b", "yokes"),
    (r"\bOv er\b", "Over"),
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
    cleaned = re.sub(r"\s+([,.;:?!])", r"\1", cleaned)
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


# Inline verse number: preceded by punctuation/whitespace, followed by capital or lowercase letter OR a quote
# Also matches standalone verse numbers at the end of a line.
RE_INLINE_VERSE = re.compile(r"(?:[.!?†ω]|\s|^)(\d+)(?:\s*([A-Za-z\"'])|$)")

# Narrative heading: Title Case word followed by any words (handles 'to', 'of', etc.)
RE_NARRATIVE_HEADING = re.compile(r"^\s*([A-Z][a-zA-Z',]+(?:\s+[a-zA-Z',]+){0,10})\s*$")

def extract_poetry_lines(lines: Sequence[str], config: PoetryExtractionConfig) -> str:
    """Run the sequential verse-buffer state machine for poetry / wisdom text."""
    header_patterns = compile_chapter_header_patterns(config)
    print("DEBUG CONFIG:")
    print("bootstrap:", config.first_chapter_bootstrap_phrases)
    
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

    previous_line_was_empty = True
    for line_raw in lines:
        line = line_raw.strip()
        if not line:
            previous_line_was_empty = True
            continue

        # 1. Check Manifest-Driven Chapter Starts
        if config.chapter_start_phrases:
            next_ch = current_chapter + 1
            if next_ch in config.chapter_start_phrases:
                if matches_phrase_list(line, config.chapter_start_phrases[next_ch], config.split_word_pairs):
                    flush_verse()
                    current_chapter = next_ch
                    current_verse = 1
                    output_lines.append(f"\n## Chapter {current_chapter}\n")
                    if pending_narrative_heading:
                        output_lines.append(pending_narrative_heading + "\n")
                        pending_narrative_heading = ""
                    # Don't skip processing the line, it contains verse 1 text

        # Centered Detection (for -layout mode)
        leading_spaces = len(line_raw) - len(line_raw.lstrip())
        is_centered = 20 <= leading_spaces <= 60 and len(line) < 60

        # Look for centered standalone digits (Proverbs/Job chapter numbers)
        is_standalone_digit = bool(re.match(r"^\d+$", line))
        
        # New: Digits at start of line followed by text (Historical books)
        is_digit_start = bool(re.match(r"^\d+\s+[A-Z]", line))
        
        header = match_chapter_header(line, header_patterns)
        
        # If no standard header but we have a pending heading and the line starts with a number
        if header is None and pending_narrative_heading and re.match(r"^\d+\b", line):
            m_num = re.match(r"^(\d+)\b\s*(.*)", line)
            if m_num:
                new_ch = int(m_num.group(1))
                if new_ch == current_chapter + 1 or (current_chapter == 0 and new_ch == 1):
                    header = (new_ch, m_num.group(2))

        if (is_centered and is_standalone_digit) or (is_digit_start and pending_narrative_heading) or (header is not None):
            if header:
                new_ch, trailing = header
            else:
                m_num = re.match(r"^(\d+)", line)
                new_ch = int(m_num.group(1))
                trailing = line[m_num.end():].strip()

            # Sequence disambiguation: MUST be strictly sequential for standalone digits
            is_valid_advance = (new_ch == current_chapter + 1)
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

        if current_chapter == 0 and matches_bootstrap_phrase(
            line,
            config.first_chapter_bootstrap_phrases,
            config.split_word_pairs,
        ):
            flush_verse()
            current_chapter = 1
            current_verse = 1
            output_lines.append(f"\n## Chapter {current_chapter}\n")
            verse_buffer = line
            continue

        # Look for narrative headings
        nh_match = RE_NARRATIVE_HEADING.match(line)
        if nh_match:
            # We require centering AND a previous blank line for a narrative heading
            if is_centered and previous_line_was_empty:
                # We don t flush yet, just store it as pending
                pending_narrative_heading = f"### {nh_match.group(1)}"
                previous_line_was_empty = False
                continue

        if current_chapter == 0:
            previous_line_was_empty = False
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
                if current_verse > 0:
                    verse_buffer += " " + line[pos:]
                break

            # If we matched a verse number, flush the previous one
            v_num = int(match.group(1))
            
            # Anchor check: verse numbers should be sequential or close
            # (In poetry, numbers can be inline like '† 2' or '†ω 2')
            if current_verse == 0 or (v_num == current_verse + 1) or (v_num > current_verse and v_num < current_verse + 5):
                flush_verse()
                current_verse = v_num
                verse_buffer = match.group(2) or ""
                pos = match.end(2) if match.group(2) else match.end(1)
            else:
                if current_verse > 0:
                    verse_buffer += match.group(0)
                pos = match.end(0)

        previous_line_was_empty = False

    flush_verse()
    return "\n".join(output_lines)
