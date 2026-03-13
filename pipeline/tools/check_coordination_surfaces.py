"""
check_coordination_surfaces.py — Validate strategic coordination surfaces.

This tool checks the relationship between:
  - reports/book_status_dashboard.json
  - PROJECT_BOARD.md
  - memos/ezra_ops_board.md
  - memos/INDEX.md
  - memos/88_phase3_ratified_spec.md

The dashboard remains the machine-readable source of truth. This checker exists
to catch narrative drift before it becomes operating drift.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
import json
import re
from pathlib import Path

from pipeline.common.paths import MEMOS_DIR, REPORTS_ROOT, REPO_ROOT

PROJECT_BOARD_PATH = REPO_ROOT / "PROJECT_BOARD.md"
OPS_BOARD_PATH = MEMOS_DIR / "ezra_ops_board.md"
MEMO_INDEX_PATH = MEMOS_DIR / "INDEX.md"
PHASE3_MEMO_PATH = MEMOS_DIR / "88_phase3_ratified_spec.md"
DASHBOARD_PATH = REPORTS_ROOT / "book_status_dashboard.json"
REPORT_PATH = REPORTS_ROOT / "coordination_state.json"

_LAST_UPDATED_RE = re.compile(r"^\> \*\*Last updated:\*\* ([0-9]{4}-[0-9]{2}-[0-9]{2})$", re.MULTILINE)
_METRIC_ROW_RE = re.compile(r"^\| (?P<metric>[^|]+?) \| `?(?P<value>[^|`]+?)`? \|$", re.MULTILINE)
_STATUS_RE = re.compile(r"^\*\*Status:\*\* `([^`]+)`", re.MULTILINE)


@dataclass(frozen=True)
class CheckOutcome:
    name: str
    status: str
    details: str


def load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def parse_last_updated(markdown: str) -> date | None:
    match = _LAST_UPDATED_RE.search(markdown)
    if not match:
        return None
    return date.fromisoformat(match.group(1))


def parse_metrics(markdown: str) -> dict[str, str]:
    return {
        match.group("metric").strip(): match.group("value").strip()
        for match in _METRIC_ROW_RE.finditer(markdown)
    }


def parse_memo_status(markdown: str) -> str | None:
    match = _STATUS_RE.search(markdown)
    return match.group(1) if match else None


def dashboard_summary(dashboard: dict) -> dict[str, int]:
    books = dashboard.get("books", [])
    promoted = dashboard.get("counts_by_status", {}).get("promoted", 0)
    fresh = 0
    stale = 0
    for book in books:
        freshness = book.get("dossier_freshness", {})
        freshness_status = freshness.get("status") if isinstance(freshness, dict) else freshness
        if freshness_status == "FRESH":
            fresh += 1
        elif freshness_status == "STALE":
            stale += 1
    return {
        "promoted": promoted,
        "fresh_dossiers": fresh,
        "stale_dossiers": stale,
    }


def compare_metric(
    metrics: dict[str, str],
    metric_name: str,
    expected: int,
    rendered_expected: str | None = None,
) -> CheckOutcome:
    if metric_name not in metrics:
        return CheckOutcome(metric_name, "PASS", "metric omitted from strategic board")
    actual = metrics[metric_name]
    target = rendered_expected or str(expected)
    if actual != target:
        return CheckOutcome(
            metric_name,
            "FAIL",
            f"board shows {actual!r}, dashboard-derived truth is {target!r}",
        )
    return CheckOutcome(metric_name, "PASS", f"board matches {target}")


def compare_last_updated(board_date: date | None, dashboard_date: date) -> CheckOutcome:
    if board_date is None:
        return CheckOutcome("project_board_last_updated", "FAIL", "board missing Last updated header")
    if board_date < dashboard_date:
        return CheckOutcome(
            "project_board_last_updated",
            "WARN",
            f"board date {board_date.isoformat()} lags dashboard {dashboard_date.isoformat()}",
        )
    return CheckOutcome("project_board_last_updated", "PASS", "board date is current")


def compare_phase3_language(phase3_status: str | None, ops_text: str, index_text: str) -> list[CheckOutcome]:
    outcomes: list[CheckOutcome] = []
    if phase3_status is None:
        outcomes.append(CheckOutcome("phase3_memo_status", "FAIL", "memo 88 is missing a status line"))
        return outcomes

    if phase3_status == "draft" and "**Governing** Phase 3 spec" in index_text:
        outcomes.append(
            CheckOutcome(
                "memo_index_phase3_status",
                "FAIL",
                "index calls Memo 88 governing while the memo header is still draft",
            )
        )
    else:
        outcomes.append(CheckOutcome("memo_index_phase3_status", "PASS", "memo index wording is consistent"))

    if phase3_status == "draft" and "Ratified Phase 3 spec" in ops_text:
        outcomes.append(
            CheckOutcome(
                "ops_board_phase3_status",
                "FAIL",
                "ops board calls Memo 88 ratified while the memo header is still draft",
            )
        )
    else:
        outcomes.append(CheckOutcome("ops_board_phase3_status", "PASS", "ops board wording is consistent"))
    return outcomes


def build_report() -> dict:
    dashboard = load_json(DASHBOARD_PATH)
    board_text = read_text(PROJECT_BOARD_PATH)
    ops_text = read_text(OPS_BOARD_PATH)
    index_text = read_text(MEMO_INDEX_PATH)
    phase3_text = read_text(PHASE3_MEMO_PATH)

    board_metrics = parse_metrics(board_text)
    board_date = parse_last_updated(board_text)
    dashboard_date = date.fromisoformat(dashboard["generated"])
    phase3_status = parse_memo_status(phase3_text)
    summary = dashboard_summary(dashboard)

    checks: list[CheckOutcome] = [
        compare_last_updated(board_date, dashboard_date),
        compare_metric(board_metrics, "Total promoted books", summary["promoted"]),
        compare_metric(
            board_metrics,
            "Promoted books with stale dossiers",
            summary["stale_dossiers"],
        ),
        compare_metric(
            board_metrics,
            "Fresh promotion dossiers",
            summary["fresh_dossiers"],
            rendered_expected=f"{summary['fresh_dossiers']}/{summary['promoted']}",
        ),
    ]
    checks.extend(compare_phase3_language(phase3_status, ops_text, index_text))
    failing = [check for check in checks if check.status == "FAIL"]
    warning = [check for check in checks if check.status == "WARN"]
    report_status = "FAIL" if failing else "WARN" if warning else "PASS"
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "status": report_status,
        "inputs": {
            "dashboard": display_path(DASHBOARD_PATH),
            "project_board": display_path(PROJECT_BOARD_PATH),
            "ops_board": display_path(OPS_BOARD_PATH),
            "memo_index": display_path(MEMO_INDEX_PATH),
            "phase3_memo": display_path(PHASE3_MEMO_PATH),
        },
        "dashboard_summary": summary,
        "checks": [asdict(check) for check in checks],
    }


def write_report(report: dict, path: Path = REPORT_PATH) -> Path:
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Check board/dashboard/memo consistency.")
    parser.add_argument("--report", action="store_true", help="Write reports/coordination_state.json")
    args = parser.parse_args()

    report = build_report()
    if args.report:
        write_report(report)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
