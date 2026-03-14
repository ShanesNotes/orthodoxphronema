from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from pipeline.tools import review_footnotes as rf


def test_ordered_books_respects_registry_position_and_range():
    registry = {
        "books": [
            {"code": "EXO", "position": 2, "testament": "OT"},
            {"code": "GEN", "position": 1, "testament": "OT"},
            {"code": "LEV", "position": 3, "testament": "OT"},
        ]
    }
    assert [b["code"] for b in rf.ordered_books(registry)] == ["GEN", "EXO", "LEV"]
    assert [b["code"] for b in rf.ordered_books(registry, start_book="EXO")] == ["EXO", "LEV"]
    assert [b["code"] for b in rf.ordered_books(registry, end_book="EXO")] == ["GEN", "EXO"]
    assert [b["code"] for b in rf.ordered_books(registry, book="LEV")] == ["LEV"]


def test_audit_structure_flags_range_continuations_without_overreporting_line_starts(tmp_path: Path):
    path = tmp_path / "LEV_footnotes.md"
    path.write_text(
        "---\nbook_code: LEV\ncontent_type: footnotes\n---\n\n"
        "## Footnotes\n\n"
        "### 1:5\n"
        "*(anchor: LEV.1:5)*\n\n"
        "Regular content.\n\n"
        "### 9:11\n"
        "*(anchor: LEV.9:11)*\n\n"
        "-22. Broken continuation.\n"
        "1:9 The whole burnt offering was totally consumed.\n",
        encoding="utf-8",
    )
    report = rf.audit_structure("LEV", path)
    issue_types = {item["type"] for item in report["findings"]}
    assert "dangling_range_continuation" in issue_types
    assert "inline_heading_spill" not in issue_types


def test_audit_structure_handles_punctuation_only_previous_line(tmp_path: Path):
    path = tmp_path / "GEN_footnotes.md"
    path.write_text(
        "---\nbook_code: GEN\ncontent_type: footnotes\n---\n\n"
        "## Footnotes\n\n"
        "### 1:1\n"
        "*(anchor: GEN.1:1)*\n\n"
        ",\n"
        "13:55 Broken split should not crash.\n",
        encoding="utf-8",
    )
    report = rf.audit_structure("GEN", path)
    assert report["issue_count"] == 0


def test_audit_source_entities_splits_patristic_apostolic_and_liturgical(tmp_path: Path):
    path = tmp_path / "SIR_footnotes.md"
    path.write_text(
        "---\nbook_code: SIR\ncontent_type: footnotes\n---\n\n"
        "## Footnotes\n\n"
        "### 1:1\n"
        "*(anchor: SIR.1:1)*\n\n"
        "St. Athanasius reads this typologically (Meth). "
        "See also St. John Chrysostom and St. Paul, and compare the Creed.\n",
        encoding="utf-8",
    )
    report = rf.audit_source_entities(path)
    assert report["patristic"]["matched_entities_count"] >= 3
    assert report["patristic"]["entity_counts"]["ATHANASIUS"] >= 1
    assert report["patristic"]["entity_counts"]["JOHN_CHRYSOSTOM"] >= 1
    assert report["patristic"]["entity_counts"]["METHODIUS"] >= 1
    assert report["apostolic"]["entity_counts"]["PAUL_APOSTLE"] >= 1
    assert report["liturgical_creedal"]["entity_counts"]["NICENE_CREED"] >= 1


def test_text_cleaner_json_mode_writes_valid_json_without_crashing(tmp_path: Path):
    sample = tmp_path / "sample.md"
    sample.write_text("Simple line with no obvious issues.\n", encoding="utf-8")
    report_dir = tmp_path / "reports"
    proc = subprocess.run(
        [
            sys.executable,
            "skills/text-cleaner/scripts/clean.py",
            "--file",
            str(sample),
            "--profile",
            "default",
            "--dry-run",
            "--json",
            "--report-dir",
            str(report_dir),
        ],
        cwd=Path(__file__).resolve().parent.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode in (0, 1)
    payload = json.loads(proc.stdout)
    assert "summary" in payload
