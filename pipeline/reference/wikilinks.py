"""
wikilinks.py — Shared parsing, auditing, and rewrite helpers for biblical wikilinks.
"""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import json
from pathlib import Path
import re

from pipeline.common.frontmatter import parse_frontmatter
from pipeline.common.paths import REGISTRY_PATH, REPO_ROOT
from pipeline.common.registry import chapter_verse_counts, load_registry
from pipeline.reference.reference_aliases import canonical_biblical_code

WIKILINK_RE = re.compile(r"\[\[([A-Za-z0-9]{1,8})\.(\d+):(\d+)\]\](?:-(\d+))?")
BARE_RE = re.compile(
    r"(?<![\w\[])"
    r"(?P<book>[1-4]?[A-Za-z]{1,8})\s+"
    r"(?P<chapter>\d+):(?P<verse>\d+)"
    r"(?P<tail>-\d+|(?:,\s*\d+)*)"
)
CHAPTER_RANGE_RE = re.compile(
    r"(?<![\w\[])"
    r"(?P<book>[1-4]?[A-Za-z]{1,8})\s+"
    r"(?P<start>\d+)-(?P<end>\d+)"
)
COMPANION_SUFFIXES = ("_footnotes.md", "_articles.md")


@dataclass(frozen=True)
class ReferenceInstance:
    start: int
    end: int
    raw_text: str
    anchor_ids: tuple[str, ...]
    reference_type: str
    replacement: str | None = None


def registry_dimensions(path: Path | str = REGISTRY_PATH) -> dict[str, dict[int, int]]:
    registry = load_registry(path)
    dims: dict[str, dict[int, int]] = {}
    for book in registry.get("books", []):
        cvc = chapter_verse_counts(registry, book["code"])
        if cvc:
            dims[book["code"]] = cvc
    return dims


def normalize_anchor_id(
    book_token: str,
    chapter_text: str,
    verse_text: str,
    dimensions: dict[str, dict[int, int]] | None = None,
) -> str | None:
    dimensions = dimensions or registry_dimensions()
    book_code = canonical_biblical_code(book_token.strip().rstrip(".,;:)]}"))
    if book_code is None:
        return None
    chapter = int(chapter_text)
    verse = int(verse_text)
    cvc = dimensions.get(book_code)
    if cvc is None or chapter not in cvc or verse < 1 or verse > cvc[chapter]:
        return None
    return f"{book_code}.{chapter}:{verse}"


def _relative_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def iter_text_blocks(path: Path) -> Iterable[tuple[list[tuple[int, str]], str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    _, body_start = parse_frontmatter(lines)
    current: list[tuple[int, str]] = []
    in_code_fence = False

    def flush() -> tuple[list[tuple[int, str]], str] | None:
        nonlocal current
        if not current:
            return None
        context = " ".join(text.strip() for _, text in current if text.strip()).strip()
        block = current
        current = []
        if not context:
            return None
        return block, context

    for idx in range(body_start, len(lines)):
        line_no = idx + 1
        line = lines[idx]
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            payload = flush()
            if payload:
                yield payload
            continue
        if in_code_fence:
            continue
        if not stripped:
            payload = flush()
            if payload:
                yield payload
            continue
        if stripped.startswith("#") or stripped.startswith("*(anchor:"):
            payload = flush()
            if payload:
                yield payload
            continue
        current.append((line_no, line))

    payload = flush()
    if payload:
        yield payload


def _expand_anchor_ids(
    book_code: str,
    chapter: int,
    verses: list[int],
    dimensions: dict[str, dict[int, int]],
) -> tuple[str, ...] | None:
    cvc = dimensions.get(book_code)
    if cvc is None or chapter not in cvc:
        return None
    max_verse = cvc[chapter]
    if any(verse < 1 or verse > max_verse for verse in verses):
        return None
    return tuple(f"{book_code}.{chapter}:{verse}" for verse in verses)


def find_reference_instances(
    line: str,
    dimensions: dict[str, dict[int, int]] | None = None,
) -> list[ReferenceInstance]:
    dimensions = dimensions or registry_dimensions()
    instances: list[ReferenceInstance] = []
    occupied: list[tuple[int, int]] = []

    for match in WIKILINK_RE.finditer(line):
        anchor_id = normalize_anchor_id(match.group(1), match.group(2), match.group(3), dimensions)
        if anchor_id is None:
            continue
        verses = [int(match.group(3))]
        ref_type = "wikilink"
        if match.group(4) is not None:
            end_verse = int(match.group(4))
            start_verse = int(match.group(3))
            if end_verse < start_verse:
                continue
            verses = list(range(start_verse, end_verse + 1))
            ref_type = "wikilink_range"
        book_code, chapter_text = anchor_id.split(".", 1)
        chapter = int(chapter_text.split(":", 1)[0])
        expanded = _expand_anchor_ids(book_code, chapter, verses, dimensions)
        if expanded is None:
            continue
        instances.append(
            ReferenceInstance(
                start=match.start(),
                end=match.end(),
                raw_text=match.group(0),
                anchor_ids=expanded,
                reference_type=ref_type,
            )
        )
        occupied.append(match.span())

    def overlaps(start: int, end: int) -> bool:
        return any(not (end <= seen_start or start >= seen_end) for seen_start, seen_end in occupied)

    for match in BARE_RE.finditer(line):
        if overlaps(match.start(), match.end()):
            continue
        book_code = canonical_biblical_code(match.group("book"))
        if book_code is None:
            continue
        chapter = int(match.group("chapter"))
        start_verse = int(match.group("verse"))
        tail = match.group("tail") or ""
        if tail.startswith("-"):
            end_verse = int(tail[1:])
            if end_verse < start_verse:
                continue
            verses = list(range(start_verse, end_verse + 1))
            ref_type = "bare"
            replacement = f"[[{book_code}.{chapter}:{start_verse}]]-{end_verse}"
        elif "," in tail:
            tail_verses = [int(item.strip()) for item in tail.split(",") if item.strip()]
            verses = [start_verse] + tail_verses
            ref_type = "bare"
            replacement = ", ".join(f"[[{book_code}.{chapter}:{verse}]]" for verse in verses)
        else:
            verses = [start_verse]
            ref_type = "bare"
            replacement = f"[[{book_code}.{chapter}:{start_verse}]]"

        expanded = _expand_anchor_ids(book_code, chapter, verses, dimensions)
        if expanded is None:
            continue
        instances.append(
            ReferenceInstance(
                start=match.start(),
                end=match.end(),
                raw_text=match.group(0),
                anchor_ids=expanded,
                reference_type=ref_type,
                replacement=replacement,
            )
        )

    return sorted(instances, key=lambda item: (item.start, item.end))


def rewrite_line(line: str, dimensions: dict[str, dict[int, int]] | None = None) -> tuple[str, int]:
    dimensions = dimensions or registry_dimensions()
    instances = find_reference_instances(line, dimensions)
    replacements = [instance for instance in instances if instance.reference_type == "bare" and instance.replacement]
    if not replacements:
        return line, 0

    rewritten = line
    for instance in reversed(replacements):
        rewritten = rewritten[:instance.start] + instance.replacement + rewritten[instance.end:]
    return rewritten, len(replacements)


def unresolved_candidates(line: str) -> list[str]:
    results: list[str] = []
    for match in CHAPTER_RANGE_RE.finditer(line):
        if canonical_biblical_code(match.group("book")) is None:
            continue
        results.append(match.group(0))
    return results


def audit_path(path: Path, dimensions: dict[str, dict[int, int]] | None = None) -> dict:
    dimensions = dimensions or registry_dimensions()
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    _, body_start = parse_frontmatter(lines)
    total_refs = 0
    convertible = 0
    already_linked = 0
    unresolved: list[dict] = []

    in_code_fence = False
    for idx in range(body_start, len(lines)):
        line = lines[idx]
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence or stripped.startswith("#") or stripped.startswith("*(anchor:"):
            continue

        instances = find_reference_instances(line, dimensions)
        total_refs += len(instances)
        for instance in instances:
            if instance.reference_type.startswith("wikilink"):
                already_linked += 1
            elif instance.reference_type == "bare" and instance.replacement:
                convertible += 1
        for candidate in unresolved_candidates(line):
            unresolved.append(
                {
                    "line_number": idx + 1,
                    "raw_text": candidate,
                    "reason": "chapter_only_or_unsupported_range",
                }
            )

    return {
        "path": _relative_path(path),
        "total_refs": total_refs,
        "convertible_refs": convertible,
        "already_linked_refs": already_linked,
        "unresolved_refs": len(unresolved),
        "unresolved_examples": unresolved[:10],
    }


def rewrite_path(
    path: Path,
    dimensions: dict[str, dict[int, int]] | None = None,
    in_place: bool = False,
) -> dict:
    dimensions = dimensions or registry_dimensions()
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    _, body_start = parse_frontmatter(lines)
    in_code_fence = False
    converted = 0

    for idx in range(body_start, len(lines)):
        stripped = lines[idx].strip()
        if stripped.startswith("```"):
            in_code_fence = not in_code_fence
            continue
        if in_code_fence or stripped.startswith("#") or stripped.startswith("*(anchor:"):
            continue
        rewritten, changed = rewrite_line(lines[idx], dimensions)
        if changed:
            lines[idx] = rewritten
            converted += changed

    output = "\n".join(lines)
    if text.endswith("\n"):
        output += "\n"
    changed = output != text
    if changed and in_place:
        path.write_text(output, encoding="utf-8")

    return {
        "path": _relative_path(path),
        "changed": changed,
        "converted_refs": converted,
    }


def is_target_companion(path: Path) -> bool:
    return path.name.endswith(COMPANION_SUFFIXES)


def discover_target_paths(roots: Iterable[Path], book_code: str | None = None) -> list[Path]:
    paths: list[Path] = []
    for root in roots:
        if root.is_file():
            if is_target_companion(root):
                paths.append(root)
            continue
        for path in root.rglob("*.md"):
            if not is_target_companion(path):
                continue
            if book_code and not path.name.startswith(f"{book_code}_"):
                continue
            paths.append(path)
    return sorted(set(paths))


def write_json_report(payload: dict, out_path: Path) -> Path:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out_path
