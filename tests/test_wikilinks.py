from __future__ import annotations

import json
from pathlib import Path

from pipeline.reference import wikilinks as wiki_mod


def test_find_reference_instances_supports_ranges_and_lists():
    dims = {"JOH": {5: 40}, "ACT": {10: 60}}
    line = "See Jn 5:33-35 and Acts 10:43, 47, 48."
    instances = wiki_mod.find_reference_instances(line, dims)
    assert [item.anchor_ids for item in instances] == [
        ("JOH.5:33", "JOH.5:34", "JOH.5:35"),
        ("ACT.10:43", "ACT.10:47", "ACT.10:48"),
    ]
    assert instances[0].replacement == "[[JOH.5:33]]-35"
    assert instances[1].replacement == "[[ACT.10:43]], [[ACT.10:47]], [[ACT.10:48]]"


def test_rewrite_line_preserves_existing_wikilinks():
    dims = {"JOH": {20: 30}, "REV": {21: 27}}
    line = "Grace (Jn 20:22) and [[REV.21:1]]."
    rewritten, changed = wiki_mod.rewrite_line(line, dims)
    assert rewritten == "Grace ([[JOH.20:22]]) and [[REV.21:1]]."
    assert changed == 1


def test_audit_path_reports_unsupported_chapter_ranges(tmp_path):
    path = tmp_path / "REV_footnotes.md"
    path.write_text(
        "---\nbook_code: REV\n---\n\n"
        "See 1Co 12-14 and Jn 20:22.\n",
        encoding="utf-8",
    )
    dims = {"1CO": {12: 31}, "JOH": {20: 31}}
    payload = wiki_mod.audit_path(path, dims)
    assert payload["total_refs"] == 1
    assert payload["convertible_refs"] == 1
    assert payload["unresolved_refs"] == 1


def test_unresolved_candidates_ignore_non_biblical_ranges():
    assert wiki_mod.unresolved_candidates("AD 53-56 and chapters 2-4") == []
    assert wiki_mod.unresolved_candidates("See Nm 22-24.") == ["Nm 22-24"]


def test_rewrite_path_updates_only_companion_body(tmp_path):
    path = tmp_path / "ROM_articles.md"
    path.write_text(
        "---\nbook_code: ROM\n---\n"
        "### Heading\n"
        "Use Rom 5:8 and Acts 10:43, 47, 48.\n"
        "```\nActs 2:4\n```\n",
        encoding="utf-8",
    )
    dims = {"ROM": {5: 21}, "ACT": {10: 60}}
    result = wiki_mod.rewrite_path(path, dims, in_place=True)
    text = path.read_text(encoding="utf-8")
    assert result["changed"] is True
    assert "[[ROM.5:8]]" in text
    assert "[[ACT.10:43]], [[ACT.10:47]], [[ACT.10:48]]" in text
    assert "Acts 2:4" in text


def test_write_json_report(tmp_path):
    out_path = tmp_path / "report.json"
    wiki_mod.write_json_report({"ok": True}, out_path)
    assert json.loads(out_path.read_text(encoding="utf-8")) == {"ok": True}
