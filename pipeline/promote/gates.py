"""Composable promotion gates (D1-D5 + V4/V7).

Each gate function returns a GateResult. promote_book() runs them in order
and exits on the first failure.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from pipeline.common.types import CheckResult

RE_V4_WARNING = re.compile(
    r'V4\s+Missing verses in ch\.(\d+): jumps from (\d+) to (\d+)'
)

ABSORBED_CONTENT_KEYWORDS = [
    "absorbed", "fused into", "fused with", "embedded in",
    "merged into", "merged with", "appended to",
]


@dataclass
class GateResult:
    """Result of a promotion gate check."""
    passed: bool
    messages: list[str] = field(default_factory=list)
    exit_code: int = 0


def gate_editorial(editorial_path: Path) -> GateResult:
    """D1: Block if unresolved editorial candidates exist."""
    if not editorial_path.exists():
        return GateResult(passed=True)
    with open(editorial_path, encoding="utf-8") as f:
        editorial = json.load(f)
    n = editorial.get("total_candidates", 0)
    if n > 0:
        return GateResult(
            passed=False,
            messages=[
                f"BLOCKED: {n} editorial candidate(s) unresolved in"
                f" {editorial_path.name}",
                "Resolve all editorial candidates before promotion.",
            ],
            exit_code=3,
        )
    return GateResult(passed=True)


def gate_freshness(
    existing_dossier_path: Path,
    body_checksum: str,
    dry_run: bool,
) -> GateResult:
    """D2: Block if staged text changed since last dossier."""
    if not existing_dossier_path.exists() or dry_run:
        return GateResult(passed=True)
    with open(existing_dossier_path, encoding="utf-8") as f:
        prev_dossier = json.load(f)
    prev_checksum = prev_dossier.get("body_checksum", "")
    if prev_checksum and prev_checksum != body_checksum:
        return GateResult(
            passed=False,
            messages=[
                "BLOCKED: Staged text has changed since last dossier generation.",
                f"  Dossier checksum: {prev_checksum[:16]}...",
                f"  Current checksum: {body_checksum[:16]}...",
                "Re-run with --dry-run first to regenerate dossier evidence.",
            ],
            exit_code=3,
        )
    return GateResult(passed=True)


def gate_errors(errors: list[str]) -> GateResult:
    """Block on V1-V9 validation errors."""
    if errors:
        msgs = [f"ERRORS ({len(errors)}) \u2014 promotion aborted:"]
        msgs.extend(f"  {e}" for e in errors)
        return GateResult(passed=False, messages=msgs, exit_code=1)
    return GateResult(passed=True)


def gate_sidecar_fields(sidecar: dict | None) -> GateResult:
    """D3: Block if sidecar uses 'class' instead of 'classification'."""
    if sidecar is None:
        return GateResult(passed=True)
    for r in sidecar.get("residuals", []):
        if "class" in r and "classification" not in r:
            anchor = r.get("anchor", "?")
            return GateResult(
                passed=False,
                messages=[
                    f"BLOCKED: Residual {anchor} uses 'class' instead of"
                    " 'classification'. Normalize the sidecar field name.",
                ],
                exit_code=3,
            )
    return GateResult(passed=True)


def gate_v4_coverage(
    v4_result: CheckResult | list[str] | None,
    sidecar: dict | None,
    book_code: str | None = None,
) -> GateResult:
    """Block if V4 gaps are not covered by residuals sidecar."""
    if v4_result is None:
        return GateResult(passed=True)

    if isinstance(v4_result, CheckResult):
        v4_missing = set(v4_result.data.get("missing_anchors", []))
        if not v4_missing and book_code:
            for gap in v4_result.data.get("gaps", []):
                ch = gap.get("chapter")
                for verse in gap.get("missing_verses", []):
                    v4_missing.add(f"{book_code}.{ch}:{verse}")
    else:
        v4_missing: set[str] = set()
        if book_code:
            for warning in v4_result:
                match = RE_V4_WARNING.match(warning)
                if not match:
                    continue
                ch, from_v, to_v = int(match.group(1)), int(match.group(2)), int(match.group(3))
                for verse in range(from_v + 1, to_v):
                    v4_missing.add(f"{book_code}.{ch}:{verse}")

    if not v4_missing:
        return GateResult(passed=True)

    if sidecar is None:
        return GateResult(
            passed=False,
            messages=[
                f"BLOCKED: {len(v4_missing)} V4 gap(s) with no residuals sidecar.",
                "Create a _residuals.json sidecar to document these gaps.",
            ],
            exit_code=3,
        )

    sidecar_anchors = {r["anchor"] for r in sidecar.get("residuals", [])}
    uncovered = v4_missing - sidecar_anchors
    if uncovered:
        msgs = [f"BLOCKED: {len(uncovered)} V4 gap(s) not covered by residuals sidecar:"]
        msgs.extend(f"  {a}" for a in sorted(uncovered))
        return GateResult(passed=False, messages=msgs, exit_code=3)

    blocking_entries = [
        r for r in sidecar.get("residuals", [])
        if r.get("blocking") and r["anchor"] in v4_missing
    ]
    if blocking_entries:
        msgs = [f"BLOCKED: {len(blocking_entries)} structural issue(s) flagged as blocking:"]
        msgs.extend(f"  {r['anchor']}: {r['description']}" for r in blocking_entries)
        return GateResult(passed=False, messages=msgs, exit_code=3)

    return GateResult(passed=True)


def gate_absorbed_content(sidecar: dict | None) -> GateResult:
    """D4: Block if residual describes absorbed/fused content."""
    if sidecar is None:
        return GateResult(passed=True)
    for r in sidecar.get("residuals", []):
        desc = r.get("description", "").lower()
        for keyword in ABSORBED_CONTENT_KEYWORDS:
            if keyword in desc:
                anchor = r.get("anchor", "?")
                return GateResult(
                    passed=False,
                    messages=[
                        f"BLOCKED: Residual {anchor} describes absorbed/fused"
                        f" content ('{keyword}'). This content may be recoverable"
                        " \u2014 resolve before promotion.",
                    ],
                    exit_code=3,
                )
    return GateResult(passed=True)


def gate_ratification(
    sidecar: dict | None,
    ratified_classes: set[str],
) -> GateResult:
    """D5: Block if non-empty residuals lack human ratification."""
    if sidecar is None:
        return GateResult(passed=True)

    residuals_list = sidecar.get("residuals", [])

    if residuals_list:
        ratified_by = sidecar.get("ratified_by")
        if not ratified_by or str(ratified_by).lower() != "human":
            return GateResult(
                passed=False,
                messages=[
                    f"BLOCKED: Non-empty residuals sidecar requires"
                    f" ratified_by: 'human' (got: {ratified_by!r}).",
                ],
                exit_code=3,
            )

    if sidecar.get("ratified_date") is None:
        if any(r.get("blocking") for r in residuals_list):
            return GateResult(
                passed=False,
                messages=["BLOCKED: Residuals sidecar not yet ratified by human."],
                exit_code=3,
            )
        elif residuals_list:
            return GateResult(
                passed=False,
                messages=["BLOCKED: Non-empty residuals sidecar has no ratified_date."],
                exit_code=3,
            )

    # Per-entry ratification for policy-sensitive classifications
    for r in residuals_list:
        cls = r.get("classification", "")
        if cls in ratified_classes and not r.get("ratified"):
            anchor = r.get("anchor", "?")
            return GateResult(
                passed=False,
                messages=[
                    f"BLOCKED: Residual {anchor} ({cls}) requires explicit"
                    " per-entry ratification",
                ],
                exit_code=3,
            )

    return GateResult(passed=True)


def gate_completeness(
    v7_result: CheckResult | list[str] | None,
    allow_incomplete: bool,
) -> GateResult:
    """V7: Block if completeness issues and --allow-incomplete not set."""
    if isinstance(v7_result, CheckResult):
        warnings = v7_result.warnings if v7_result.status == "WARN" else []
    else:
        warnings = list(v7_result or [])

    if warnings and not allow_incomplete:
        msgs = [f"BLOCKED ({len(warnings)} completeness issue(s)):"]
        msgs.extend(f"  {w}" for w in warnings)
        msgs.append("Re-run with --allow-incomplete to acknowledge and proceed.")
        return GateResult(passed=False, messages=msgs, exit_code=2)
    return GateResult(passed=True)
