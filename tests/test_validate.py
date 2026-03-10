"""
test_validate.py — Validation edge cases for validate_canon.py (V4, V9, sidecar).
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path


def _make_canon_file(verses: list[tuple[int, int, str]], book_code: str = "TST") -> Path:
    """Create a minimal canon .md temp file with frontmatter + verses."""
    lines = [
        "---",
        f"book_code: {book_code}",
        "book_name: Test Book",
        "testament: OT",
        "canon_position: 1",
        "source: test",
        "parse_date: 2026-01-01",
        "status: staged",
        "---",
    ]
    current_ch = 0
    for ch, v, text in verses:
        if ch != current_ch:
            lines.append(f"## Chapter {ch}")
            current_ch = ch
        lines.append(f"{book_code}.{ch}:{v} {text}")

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    )
    tmp.write("\n".join(lines) + "\n")
    tmp.flush()
    tmp.close()
    return Path(tmp.name)


def test_clean_file(validate_canon):
    """All verses sequential → no errors, no warnings."""
    path = _make_canon_file([
        (1, 1, "In the beginning"),
        (1, 2, "And the earth was"),
        (1, 3, "Then God said"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    assert errors == []
    # V7 warning is expected (no registry entry for TST), filter it out
    non_v7 = [w for w in warnings if not w.startswith("V7")]
    assert non_v7 == []


def test_v4_gap_detection(validate_canon):
    """Jump from v3 to v5 produces a V4 warning."""
    path = _make_canon_file([
        (1, 1, "verse one"),
        (1, 2, "verse two"),
        (1, 3, "verse three"),
        (1, 5, "verse five"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v4_warnings = [w for w in warnings if w.startswith("V4")]
    assert len(v4_warnings) == 1
    assert "jumps from 3 to 5" in v4_warnings[0]


def test_v9_embedded_verse(validate_canon):
    """v3 text contains '4 and...' with v4 missing → V9 error."""
    path = _make_canon_file([
        (1, 1, "verse one"),
        (1, 2, "verse two"),
        (1, 3, "verse three 4 and then verse four text"),
        (1, 5, "verse five"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v9_errors = [e for e in errors if e.startswith("V9")]
    assert len(v9_errors) == 1
    assert "Embedded verse TST.1:4" in v9_errors[0]


def test_v9_no_false_positive(validate_canon):
    """v3 text contains '400 men' with v4 missing → V9 does NOT fire for 400."""
    path = _make_canon_file([
        (1, 1, "verse one"),
        (1, 2, "verse two"),
        (1, 3, "he had 400 men with him"),
        (1, 5, "verse five"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v9_errors = [e for e in errors if e.startswith("V9")]
    # V9 should fire for bare "4" inside "400"? No — the regex (?<!\d)4(?!\d) won't match
    # because "4" in "400" is preceded/followed by other digits. V9 should NOT fire.
    assert len(v9_errors) == 0


def test_generate_sidecar(validate_canon, tmp_path):
    """--generate-sidecar creates correct JSON from V4 gaps."""
    # Create a canon file with a gap (v3→v5 missing v4, and v6→v8 missing v7)
    path = _make_canon_file([
        (1, 1, "verse one"),
        (1, 2, "verse two"),
        (1, 3, "verse three"),
        (1, 5, "verse five"),
        (1, 6, "verse six"),
        (1, 8, "verse eight"),
    ], book_code="TST")

    errors, warnings = validate_canon.validate_file(Path(path), strict=False)

    # Monkey-patch REPO_ROOT so sidecar writes to tmp_path
    orig_root = validate_canon.REPO_ROOT
    validate_canon.REPO_ROOT = tmp_path
    try:
        out = validate_canon.generate_sidecar(Path(path), warnings, "TST")
    finally:
        validate_canon.REPO_ROOT = orig_root

    assert out is not None
    assert out.exists()
    assert out.name == "TST_residuals.json"

    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["book_code"] == "TST"
    assert data["registry_version"] is not None
    assert data["ratified_by"] is None
    assert data["ratified_date"] is None
    assert len(data["residuals"]) == 2

    anchors = [r["anchor"] for r in data["residuals"]]
    assert "TST.1:4" in anchors
    assert "TST.1:7" in anchors

    for r in data["residuals"]:
        assert r["classification"] == "docling_issue"
        assert r["blocking"] is False

    # Safety: calling again should refuse to overwrite
    validate_canon.REPO_ROOT = tmp_path
    try:
        out2 = validate_canon.generate_sidecar(Path(path), warnings, "TST")
    finally:
        validate_canon.REPO_ROOT = orig_root
    assert out2 is None


def test_generate_sidecar_from_validation_result(validate_canon, tmp_path):
    """Structured validation result should generate sidecars without warning parsing."""
    path = _make_canon_file([
        (1, 1, "verse one"),
        (1, 3, "verse three"),
    ], book_code="TST")

    validation = validate_canon.run_validation(Path(path), strict=False)

    orig_root = validate_canon.REPO_ROOT
    validate_canon.REPO_ROOT = tmp_path
    try:
        out = validate_canon.generate_sidecar(Path(path), validation, "TST")
    finally:
        validate_canon.REPO_ROOT = orig_root

    assert out is not None
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["residuals"][0]["anchor"] == "TST.1:2"


# ── V8 heading repetition / density tests ─────────────────────────────────


def _make_canon_with_headings(headings_per_chapter, num_chapters=1,
                              book_code="TST"):
    """Create a canon file with specific headings in each chapter.

    headings_per_chapter: list of lists of heading strings per chapter.
    """
    lines = [
        "---",
        f"book_code: {book_code}",
        "book_name: Test Book",
        "testament: OT",
        "canon_position: 1",
        "source: test",
        "parse_date: 2026-01-01",
        "status: staged",
        "---",
    ]
    verse_num = 1
    for ch_idx in range(num_chapters):
        ch = ch_idx + 1
        lines.append(f"## Chapter {ch}")
        for heading in headings_per_chapter[ch_idx]:
            lines.append(f"### {heading}")
        for v in range(1, 4):
            lines.append(f"{book_code}.{ch}:{v} verse text {verse_num}")
            verse_num += 1

    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".md", delete=False, encoding="utf-8"
    )
    tmp.write("\n".join(lines) + "\n")
    tmp.flush()
    tmp.close()
    return Path(tmp.name)


def test_v8_heading_repetition_detected(validate_canon):
    """Same heading 5x → V8 error."""
    path = _make_canon_with_headings(
        [["The Same Heading"] * 5],
        num_chapters=1,
    )
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v8_errors = [e for e in errors if "V8" in e and "Heading repetition" in e]
    assert len(v8_errors) >= 1
    assert "5 times" in v8_errors[0]


def test_v8_heading_density_warning(validate_canon):
    """15 headings in 1 chapter → V8 density warning."""
    path = _make_canon_with_headings(
        [[f"Heading {i}" for i in range(15)]],
        num_chapters=1,
    )
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v8_density = [w for w in warnings if "V8" in w and "density" in w.lower()]
    assert len(v8_density) >= 1


def test_v8_legitimate_headings_pass(validate_canon):
    """3 unique headings across 3 chapters → no V8 issues."""
    path = _make_canon_with_headings(
        [["Heading A"], ["Heading B"], ["Heading C"]],
        num_chapters=3,
    )
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v8_errors = [e for e in errors if "V8" in e and "Heading repetition" in e]
    v8_density = [w for w in warnings if "V8" in w and "density" in w.lower()]
    assert v8_errors == []
    assert v8_density == []


# ── V11 split-word tests ──────────────────────────────────────────────────


def test_v11_split_word_detected(validate_canon):
    """'oliv eoil' in verse text → V11 warning."""
    path = _make_canon_file([
        (1, 1, "The shield was not anointed with oliv eoil."),
        (1, 2, "verse two"),
        (1, 3, "verse three"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v11 = [w for w in warnings if w.startswith("V11")]
    assert len(v11) >= 1
    assert "oliv e" in v11[0] or "Split-word" in v11[0]


def test_v11_joined_fragment_split_detected(validate_canon):
    """Observed live split like 'ov er' or 'v alley' → V11 warning."""
    path = _make_canon_file([
        (1, 1, "Let the sun stand still ov er Gibeon and the moon in the v alley."),
        (1, 2, "verse two"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v11 = [w for w in warnings if w.startswith("V11")]
    assert len(v11) >= 2
    assert any("ov er" in warning for warning in v11)
    assert any("v alley" in warning for warning in v11)


def test_v11_normal_text_passes(validate_canon):
    """Clean text with no split words → no V11 warnings."""
    path = _make_canon_file([
        (1, 1, "The olive oil was pure and holy."),
        (1, 2, "He gave thanks for the beloved child."),
        (1, 3, "She loved the Lord forever."),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v11 = [w for w in warnings if w.startswith("V11")]
    assert v11 == []


def test_v8_heading_without_following_verse_is_error(validate_canon):
    path = _make_canon_with_headings(
        [["Heading A", "Heading B"]],
        num_chapters=1,
    )
    errors, warnings = validate_canon.validate_file(path, strict=False)
    assert any(
        e.startswith("V8") and "not followed by any verse content" in e
        for e in errors
    )


# ── V12 inline verse-number leakage tests ─────────────────────────────────


def test_v12_inline_verse_number_detected(validate_canon):
    """Verse 14 with ', 14 so' → V12 warning."""
    path = _make_canon_file([
        (1, 1, "verse one"),
        (1, 2, "verse two"),
        (1, 13, "verse thirteen"),
        (1, 14, "the house was filled with glory, 14 so the priests could not"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v12 = [w for w in warnings if w.startswith("V12")]
    assert len(v12) >= 1


def test_v12_normal_verse_passes(validate_canon):
    """Verse 14 with 'had 14 sheep' → no V12 (no punctuation trigger)."""
    path = _make_canon_file([
        (1, 1, "verse one"),
        (1, 2, "verse two"),
        (1, 13, "verse thirteen"),
        (1, 14, "he had 14 sheep in the field"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v12 = [w for w in warnings if w.startswith("V12")]
    assert v12 == []


# ── V11 expanded suffix tests ────────────────────────────────────────────────


def test_v11_eav_suffix(validate_canon):
    """'heav en' detected by eav suffix."""
    path = _make_canon_file([
        (1, 1, "the heav en and earth were created"),
        (1, 2, "verse two"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v11 = [w for w in warnings if w.startswith("V11")]
    assert len(v11) >= 1
    assert any("heav e" in w or "eav" in w for w in v11)


def test_v11_av_suffix(validate_canon):
    """'hav e' detected by av suffix."""
    path = _make_canon_file([
        (1, 1, "they shall hav e dominion over the fish"),
        (1, 2, "verse two"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v11 = [w for w in warnings if w.startswith("V11")]
    assert len(v11) >= 1


def test_v11_arv_suffix(validate_canon):
    """'harv est' detected by arv suffix."""
    path = _make_canon_file([
        (1, 1, "the harv est was plentiful in the land"),
        (1, 2, "verse two"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v11 = [w for w in warnings if w.startswith("V11")]
    assert len(v11) >= 1


def test_v11_ilv_suffix(validate_canon):
    """'silv er' detected by ilv suffix."""
    path = _make_canon_file([
        (1, 1, "the silv er was weighed in the temple"),
        (1, 2, "verse two"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v11 = [w for w in warnings if w.startswith("V11")]
    assert len(v11) >= 1


def test_v11_known_split_join_expanded(validate_canon):
    """Expanded KNOWN_SPLIT_JOIN_WORDS: 'heav en', 'silv er', etc. detected."""
    path = _make_canon_file([
        (1, 1, "the heav en opened and silv er fell"),
        (1, 2, "they shall hav e the harv est"),
    ])
    errors, warnings = validate_canon.validate_file(path, strict=False)
    v11 = [w for w in warnings if w.startswith("V11")]
    # Should catch at least the regex-based splits
    assert len(v11) >= 2
