from __future__ import annotations

import json

from pipeline.tools import check_coordination_surfaces as coord_mod


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_build_report_passes_with_aligned_surfaces(tmp_path, monkeypatch):
    reports = tmp_path / "reports"
    memos = tmp_path / "memos"
    reports.mkdir(parents=True)
    dashboard_path = reports / "book_status_dashboard.json"
    project_board = tmp_path / "PROJECT_BOARD.md"
    ops_board = memos / "ezra_ops_board.md"
    memo_index = memos / "INDEX.md"
    phase3_memo = memos / "88_phase3_ratified_spec.md"

    dashboard_path.write_text(
        json.dumps(
            {
                "generated": "2026-03-13",
                "counts_by_status": {"promoted": 76},
                "books": [
                    {"dossier_freshness": {"status": "FRESH"}},
                    {"dossier_freshness": {"status": "FRESH"}},
                ],
            }
        ),
        encoding="utf-8",
    )
    _write(
        project_board,
        "# Board\n\n> **Last updated:** 2026-03-13\n\n## Metrics\n\n"
        "| Metric | Current |\n"
        "|---|---|\n"
        "| Total promoted books | `76` |\n"
        "| Promoted books with stale dossiers | `0` |\n"
        "| Fresh promotion dossiers | `2/76` |\n",
    )
    _write(ops_board, "# Ops\n\nMemo 88 is the proposed governing spec awaiting ratification.\n")
    _write(memo_index, "# Index\n\nMemo 88 is the proposed governing Phase 3 spec.\n")
    _write(
        phase3_memo,
        "# Memo 88\n\n**Status:** `draft`\n",
    )

    monkeypatch.setattr(coord_mod, "DASHBOARD_PATH", dashboard_path)
    monkeypatch.setattr(coord_mod, "PROJECT_BOARD_PATH", project_board)
    monkeypatch.setattr(coord_mod, "OPS_BOARD_PATH", ops_board)
    monkeypatch.setattr(coord_mod, "MEMO_INDEX_PATH", memo_index)
    monkeypatch.setattr(coord_mod, "PHASE3_MEMO_PATH", phase3_memo)

    report = coord_mod.build_report()
    assert report["status"] == "PASS"


def test_build_report_fails_on_phase3_and_metric_drift(tmp_path, monkeypatch):
    reports = tmp_path / "reports"
    memos = tmp_path / "memos"
    reports.mkdir(parents=True)
    dashboard_path = reports / "book_status_dashboard.json"
    project_board = tmp_path / "PROJECT_BOARD.md"
    ops_board = memos / "ezra_ops_board.md"
    memo_index = memos / "INDEX.md"
    phase3_memo = memos / "88_phase3_ratified_spec.md"

    dashboard_path.write_text(
        json.dumps(
            {
                "generated": "2026-03-13",
                "counts_by_status": {"promoted": 76},
                "books": [{"dossier_freshness": {"status": "FRESH"}} for _ in range(76)],
            }
        ),
        encoding="utf-8",
    )
    _write(
        project_board,
        "# Board\n\n> **Last updated:** 2026-03-12\n\n## Metrics\n\n"
        "| Metric | Current |\n"
        "|---|---|\n"
        "| Total promoted books | `51` |\n"
        "| Promoted books with stale dossiers | `74` |\n",
    )
    _write(ops_board, "# Ops\n\nRatified Phase 3 spec.\n")
    _write(memo_index, "# Index\n\n**Governing** Phase 3 spec.\n")
    _write(phase3_memo, "# Memo 88\n\n**Status:** `draft`\n")

    monkeypatch.setattr(coord_mod, "DASHBOARD_PATH", dashboard_path)
    monkeypatch.setattr(coord_mod, "PROJECT_BOARD_PATH", project_board)
    monkeypatch.setattr(coord_mod, "OPS_BOARD_PATH", ops_board)
    monkeypatch.setattr(coord_mod, "MEMO_INDEX_PATH", memo_index)
    monkeypatch.setattr(coord_mod, "PHASE3_MEMO_PATH", phase3_memo)

    report = coord_mod.build_report()
    assert report["status"] == "FAIL"
    names = {check["name"] for check in report["checks"] if check["status"] == "FAIL"}
    assert "Total promoted books" in names
    assert "memo_index_phase3_status" in names
    assert "ops_board_phase3_status" in names
