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
