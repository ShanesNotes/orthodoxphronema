from __future__ import annotations

import json
from pathlib import Path

from pipeline.cleanup import purity_audit


def _write_book(path: Path, body: str) -> None:
    path.write_text(
        "---\n"
        "book_code: TST\n"
        "book_name: Test\n"
        "---\n\n"
        + body,
        encoding="utf-8",
    )


def test_scan_chapter_open_dropcaps_ignores_review_markers(tmp_path):
    book = tmp_path / "TST.md"
    _write_book(
        book,
        "## Chapter 1\n\n"
        "TST.1:1 *** ow the word came to the prophet.\n",
    )

    candidates = purity_audit.scan_chapter_open_dropcaps(book)
    assert len(candidates) == 1
    assert candidates[0]["category"] == "chapter_open_dropcap"
    assert candidates[0]["token"] == "ow"
    assert "***" not in candidates[0]["source_hint"]


def test_scan_split_word_residue_detects_suffix_and_known_join_cases(tmp_path):
    book = tmp_path / "TST.md"
    _write_book(
        book,
        "TST.1:1 he went ov er the hill and received heav enly vision.\n",
    )

    candidates = purity_audit.scan_split_word_residue(book)
    categories = {cand["category"] for cand in candidates}
    tokens = {cand["token"] for cand in candidates}
    assert categories == {"split_word_residue"}
    assert any("ov er" in token for token in tokens)
    assert any("heav en" in token for token in tokens)


def test_run_purity_audit_merges_chapter_split_and_fused_article_candidates(tmp_path):
    book = tmp_path / "TST.md"
    _write_book(
        book,
        "## Chapter 1\n\n"
        "TST.1:1 ow there was aman in the city.\n"
        "TST.1:2 he went ov er the hill.\n",
    )

    report = purity_audit.run_purity_audit(book)
    assert report["total_candidates"] == 3
    assert report["by_category"] == {
        "chapter_open_dropcap": 1,
        "fused_article_explicit": 1,
        "split_word_residue": 1,
    }
    assert "Inline *** review markers were ignored during detection" in report["notes"]


def test_editorial_out_merges_with_existing_sidecar(tmp_path):
    book = tmp_path / "TST.md"
    sidecar = tmp_path / "TST_editorial_candidates.json"
    _write_book(
        book,
        "## Chapter 1\n\n"
        "TST.1:1 he established adecree for them.\n",
    )
    sidecar.write_text(
        json.dumps(
            {
                "book": "TST",
                "file": str(book),
                "generated": "2026-03-10",
                "total_candidates": 1,
                "by_category": {"truncation": 1},
                "candidates": [
                    {
                        "line": 7,
                        "anchor": "TST.1:7",
                        "category": "truncation",
                        "token": "truncated",
                        "confidence": 0.9,
                        "source_hint": "heuristic",
                        "manual_status": "pending",
                    }
                ],
                "notes": ["Existing truncation audit"],
            }
        ),
        encoding="utf-8",
    )

    report = purity_audit.run_purity_audit(book)
    merged = purity_audit.merge_editorial_report(
        json.loads(sidecar.read_text(encoding="utf-8")),
        report,
    )

    assert merged["total_candidates"] == 3
    assert merged["by_category"] == {
        "chapter_open_dropcap": 1,
        "fused_article_explicit": 1,
        "truncation": 1,
    }
    assert "Existing truncation audit" in merged["notes"]


def test_replace_owned_categories_clears_stale_purity_entries():
    existing = {
        "book": "TST",
        "file": "staging/validated/OT/TST.md",
        "generated": "2026-03-10",
        "total_candidates": 3,
        "by_category": {
            "chapter_open_dropcap": 2,
            "fused_article_explicit": 1,
            "truncation": 1,
        },
        "candidates": [
            {"anchor": "TST.1:1", "category": "chapter_open_dropcap"},
            {"anchor": "TST.1:2", "category": "fused_article_explicit"},
            {"anchor": "TST.1:3", "category": "truncation"},
        ],
        "notes": ["Existing truncation audit"],
    }

    cleaned = purity_audit.replace_owned_categories(
        existing,
        {"chapter_open_dropcap", "fused_article_explicit"},
    )

    assert cleaned["total_candidates"] == 1
    assert cleaned["by_category"] == {"truncation": 1}
    assert cleaned["candidates"] == [{"anchor": "TST.1:3", "category": "truncation"}]
