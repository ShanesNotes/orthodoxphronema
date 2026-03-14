from __future__ import annotations

import json
from pathlib import Path

from pipeline.metadata import build_noah_queue as queue_mod
from pipeline.metadata import export_noah_bundle as bundle_mod
from pipeline.metadata import generate_pericope_index as pericope_mod
from pipeline.common.registry import load_registry


REPO_ROOT = Path(__file__).parent.parent


def _load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


# ── Phase 1A: Pre-heading verse gap fix ──────────────────────────────────────

def test_gen_first_pericope_starts_at_1_1(tmp_path):
    """GEN preamble must capture GEN.1:1, not start at GEN.2:7."""
    payload = pericope_mod.extract_pericopes(REPO_ROOT / "canon" / "OT" / "01_GEN.md")
    first = payload["pericopes"][0]
    assert first["start_anchor"] == "GEN.1:1"
    assert "Opening" in first["title"]


def test_gen_preamble_ends_before_first_heading(tmp_path):
    """GEN preamble must end at GEN.2:6 (last verse before '### The Garden of Eden')."""
    payload = pericope_mod.extract_pericopes(REPO_ROOT / "canon" / "OT" / "01_GEN.md")
    first = payload["pericopes"][0]
    assert first["end_anchor"] == "GEN.2:6"
    assert first["verse_count"] == 37


# ── Phase 1B: Heading-less and sparse book fallbacks ─────────────────────────

def test_psa_produces_151_pericopes():
    """PSA has zero ### headings; each chapter becomes 'Psalm N'."""
    payload = pericope_mod.extract_pericopes(REPO_ROOT / "canon" / "OT" / "24_PSA.md")
    assert len(payload["pericopes"]) == 151
    assert payload["pericopes"][0]["title"] == "Psalm 1"
    assert payload["pericopes"][150]["title"] == "Psalm 151"


def test_oba_produces_1_pericope():
    """OBA (single chapter, no headings) produces exactly 1 pericope."""
    payload = pericope_mod.extract_pericopes(REPO_ROOT / "canon" / "OT" / "35_OBA.md")
    assert len(payload["pericopes"]) == 1
    assert payload["pericopes"][0]["start_anchor"] == "OBA.1:1"


def test_heading_less_books_all_get_pericopes():
    """Every heading-less book must produce at least 1 pericope per chapter."""
    registry = load_registry()
    heading_less = ["1MA", "2MA", "PSA", "PRO", "WIS", "OBA", "HAB", "LJE"]
    for code in heading_less:
        meta = next(b for b in registry["books"] if b["code"] == code)
        path = REPO_ROOT / "canon" / meta["testament"] / f"{meta['position']:02d}_{code}.md"
        payload = pericope_mod.extract_pericopes(path, registry=registry)
        assert len(payload["pericopes"]) >= meta["chapters"], (
            f"{code}: expected >= {meta['chapters']} pericopes, got {len(payload['pericopes'])}"
        )


# ── Phase 1C: No null verse_count ────────────────────────────────────────────

def test_no_null_verse_count_gen():
    """No pericope in GEN should have verse_count=None."""
    payload = pericope_mod.extract_pericopes(REPO_ROOT / "canon" / "OT" / "01_GEN.md")
    for p in payload["pericopes"]:
        assert p["verse_count"] is not None, f"Null verse_count in {p['title']}"


def test_no_null_verse_count_isa():
    """ISA has sparse headings with many cross-chapter ranges — no nulls."""
    payload = pericope_mod.extract_pericopes(REPO_ROOT / "canon" / "OT" / "43_ISA.md")
    for p in payload["pericopes"]:
        assert p["verse_count"] is not None, f"Null verse_count in {p['title']}"


# ── Phase 1D: Full-canon queue ───────────────────────────────────────────────

def test_full_canon_queue_links_76_books(tmp_path):
    """Full-canon queue must link all 76 books continuously."""
    pericope_dir = tmp_path / "pericope"
    out_dir = tmp_path / "noah"
    out_path = queue_mod.build_full_canon_queue(out_dir=out_dir, pericope_out_dir=pericope_dir)
    rows = _load_jsonl(out_path)

    books = sorted(set(r["book_code"] for r in rows))
    assert len(books) == 76

    # Continuous chain
    assert rows[0]["previous_session_id"] is None
    assert rows[-1]["next_session_id"] is None
    for i in range(1, len(rows)):
        assert rows[i]["previous_session_id"] == rows[i - 1]["session_id"]
        assert rows[i - 1]["next_session_id"] == rows[i]["session_id"]


def test_full_canon_queue_global_index(tmp_path):
    """Global session index must be 1-based and continuous."""
    pericope_dir = tmp_path / "pericope"
    out_dir = tmp_path / "noah"
    out_path = queue_mod.build_full_canon_queue(out_dir=out_dir, pericope_out_dir=pericope_dir)
    rows = _load_jsonl(out_path)

    assert rows[0]["global_session_index"] == 1
    assert rows[-1]["global_session_index"] == len(rows)
    for i, row in enumerate(rows):
        assert row["global_session_index"] == i + 1


def test_full_canon_queue_starts_gen_ends_rev(tmp_path):
    pericope_dir = tmp_path / "pericope"
    out_dir = tmp_path / "noah"
    out_path = queue_mod.build_full_canon_queue(out_dir=out_dir, pericope_out_dir=pericope_dir)
    rows = _load_jsonl(out_path)

    assert rows[0]["book_code"] == "GEN"
    assert rows[-1]["book_code"] == "REV"
    assert rows[0]["queue_version"] == "noah-queue-v2"


# ── Phase 1F: No dropped verses ──────────────────────────────────────────────

def test_no_dropped_verses_gen():
    """Union of all GEN pericope ranges must cover every verse in the book."""
    payload = pericope_mod.extract_pericopes(REPO_ROOT / "canon" / "OT" / "01_GEN.md")
    registry = load_registry()
    from pipeline.common.registry import chapter_verse_counts
    cvc = chapter_verse_counts(registry, "GEN")

    # Compute expected total verses
    expected_total = sum(cvc.values())

    # Compute covered verses from pericopes
    covered = 0
    for p in payload["pericopes"]:
        if p["verse_count"] is not None:
            covered += p["verse_count"]

    assert covered == expected_total, (
        f"GEN: pericopes cover {covered} verses, expected {expected_total}"
    )


# ── Legacy: bundle export still works ────────────────────────────────────────

def test_build_noah_queue_generates_genesis_session_rows(tmp_path):
    pericope_dir = tmp_path / "pericope"
    out_dir = tmp_path / "noah"

    queue_path = queue_mod.build_queue("GEN", out_dir=out_dir, pericope_out_dir=pericope_dir)
    rows = _load_jsonl(queue_path)

    assert queue_path == out_dir / "session_queue.jsonl"
    assert rows
    # Post-fix: GEN.P001 is now the preamble, GEN.P002 is "The Garden of Eden"
    assert rows[0]["session_id"] == "GEN.P001"
    assert rows[0]["start_anchor"] == "GEN.1:1"
    assert rows[0]["writeback_policy"] == "read_only"
    assert rows[0]["prompt_template_id"] == "noah_journal_v1"
    assert rows[0]["previous_session_id"] is None
    assert rows[0]["next_session_id"] == "GEN.P002"
    assert rows[1]["previous_session_id"] == "GEN.P001"
    assert rows[0]["source_canon_path"] == "canon/OT/01_GEN.md"


def test_export_noah_bundle_writes_source_prompt_and_journal(tmp_path):
    pericope_dir = tmp_path / "pericope"
    queue_dir = tmp_path / "noah"
    export_dir = tmp_path / "exports"

    queue_path = queue_mod.build_queue("GEN", out_dir=queue_dir, pericope_out_dir=pericope_dir)
    bundle_dir = bundle_mod.export_bundle(queue_path, start_session=1, count=2, out_dir=export_dir)

    payload = json.loads((bundle_dir / "00_bundle.json").read_text(encoding="utf-8"))
    assert payload["session_count"] == 2
    assert payload["session_ids"] == ["GEN.P001", "GEN.P002"]
    assert payload["writeback_policy"] == "read_only"

    source_text = (bundle_dir / "01_GEN.P001_source.md").read_text(encoding="utf-8")
    prompt_text = (bundle_dir / "01_GEN.P001_prompt.md").read_text(encoding="utf-8")
    journal_text = (bundle_dir / "01_GEN.P001_journal.md").read_text(encoding="utf-8")

    assert 'session_id: "GEN.P001"' in source_text
    # GEN.P001 is now the preamble — starts at GEN.1:1
    assert "GEN.1:1 In the beginning" in source_text
    assert "## Literal scene" in prompt_text
    assert "## Patterns" in prompt_text
    assert "## Tension or surprise" in prompt_text
    assert "## Interior response" in prompt_text
    assert "## Question / prayer" in prompt_text
    assert "# Journal:" in journal_text
    assert journal_text.count("## ") == 5
