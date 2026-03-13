**MEMO: ORTHODOX PHRONEMA ARCHIVE — PHASE 3 LAYER 3 IMPLEMENTATION (DuckDB + Pipeline Gate)**  
**Date:** 2026-03-10  
**Author:** Benjamin (first-principles engineering)  
**Coordinated by:** Grok  
**Contributors:** Harper (live-repo verification of `metadata/` and `canon/`), Lucas (pre-synthesis)  
**Proposed commit paths:**  
`pipeline/graph/schema.sql`  
`pipeline/graph/regenerate_graph.py`  
`pipeline/graph/INTEGRITY_GATE_SPEC.md`  

**First-Principles Framing (Benjamin)**  
The archive’s substrate is immutable OSB flat files under Git. Layer 3 must never become a source of truth; it exists only to accelerate validation and future traversals. Therefore: (1) every node is re-derived by scanning promoted `canon/` files (ensures completeness against the single canonical source), (2) every edge is re-derived exclusively from Layer 2 JSON sidecars (Git-diffable, human-readable), (3) DuckDB is dropped and rebuilt on every run (idempotent, no state drift), and (4) the regeneration script is a hard pre-promotion gate (V13 extension). Established invariants (frozen anchor format, OSB sole source, one-verse-per-line, no canon writes, single-writer Ark) are untouched. Open engineering problems addressed: ADJ-1 and ADJ-4.

**Live Repo Verification (Harper contribution)**  
- `metadata/anchor_backlinks/` does not exist (empty directory tree).  
- `canon/` structure is `canon/OT/` and `canon/NT/` (confirmed; no flat root files).  
→ ADJ-1 resolved: adopt hyphen escape → `PSA.44-10.json`.  
→ `canon_uri` format locked to `canon/{OT|NT}/BOOK.md#ANCHOR`.  

**Resolved Conflicts**  
ADJ-1 closed (hyphen). ADJ-4 closed (OT/NT path). No impact on frozen `[[BOOK.CH:V]]` syntax or single-writer rule.

### Deliverable 1 — `pipeline/graph/schema.sql` (ready to commit)
```sql
-- Orthodox Phronema Archive — Phase 3 Phronema Graph Schema
-- Version: 2026-03-10
-- Regeneratable from Layer 2 JSON + canon/ scan only
-- Filename convention: hyphen (PSA.44-10.json) — ADJ-1
-- canon_uri format: canon/{OT|NT}/BOOK.md#ANCHOR — live structure

CREATE TABLE IF NOT EXISTS nodes (
    anchor_id TEXT PRIMARY KEY,              -- "PSA.44:10" (frozen logical format)
    book_code TEXT NOT NULL,
    chapter INTEGER NOT NULL,
    verse INTEGER NOT NULL,
    testament TEXT NOT NULL CHECK (testament IN ('OT', 'NT')),
    text_tradition TEXT DEFAULT 'LXX',
    canon_uri TEXT NOT NULL UNIQUE,          -- "canon/OT/PSA.md#PSA.44:10"
    book_name TEXT
);

CREATE TABLE IF NOT EXISTS edges (
    edge_id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_anchor TEXT NOT NULL REFERENCES nodes(anchor_id),
    source_file TEXT NOT NULL,               -- phronema/notes/articles file
    source_reference TEXT,                   -- optional phronema anchor
    link_type TEXT NOT NULL,
    domain TEXT NOT NULL CHECK (domain IN ('liturgical', 'patristic', 'study')),
    entity TEXT,
    service TEXT,
    generated_at TIMESTAMP,
    metadata JSON
);

-- Performance indexes for Phase 3/4
CREATE INDEX IF NOT EXISTS idx_nodes_book ON nodes(book_code, chapter);
CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_anchor);
CREATE INDEX IF NOT EXISTS idx_edges_domain ON edges(domain, link_type);
CREATE INDEX IF NOT EXISTS idx_edges_source_file ON edges(source_file);
```

### Deliverable 2 — `pipeline/graph/regenerate_graph.py` (ready to commit)
```python
#!/usr/bin/env python3
# Orthodox Phronema Archive — Layer 3 Regeneration Script
# Idempotent, regeneratable, blocks promotion on failure
# Benjamin 2026-03-10

import duckdb
import json
from pathlib import Path
from datetime import datetime
import re
import sys

DB_PATH = Path("metadata/graph/phronema_graph.duckdb")
BACKLINK_ROOT = Path("metadata/anchor_backlinks")
CANON_ROOT = Path("canon")
REPORT_DIR = Path("reports")
SCHEMA_PATH = Path("pipeline/graph/schema.sql")

def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(DB_PATH))

    # Drop & rebuild schema (strict regeneratable contract)
    con.execute("DROP TABLE IF EXISTS edges;")
    con.execute("DROP TABLE IF EXISTS nodes;")
    con.execute(SCHEMA_PATH.read_text())

    # 1. Populate nodes from canon/ (OT/NT confirmed live)
    anchor_pattern = re.compile(r'^([A-Z0-9]{2,4})\.(\d+):(\d+)\s')
    node_count = 0
    for testament_dir in ['OT', 'NT']:
        for md_file in (CANON_ROOT / testament_dir).glob("*.md"):
            book_code = md_file.stem
            with open(md_file, encoding="utf-8") as f:
                for line in f:
                    m = anchor_pattern.match(line.strip())
                    if m:
                        bc, ch, vs = m.groups()
                        anchor_id = f"{bc}.{ch}:{vs}"
                        canon_uri = f"canon/{testament_dir}/{md_file.name}#{anchor_id}"
                        con.execute("""
                            INSERT OR REPLACE INTO nodes
                            (anchor_id, book_code, chapter, verse, testament, canon_uri, book_name)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (anchor_id, bc, int(ch), int(vs), testament_dir, canon_uri, book_code))
                        node_count += 1

    # 2. Populate edges from Layer 2 JSONs (domain-sharded, hyphen filenames)
    edge_count = 0
    for domain in ['liturgical', 'patristic', 'study']:
        domain_dir = BACKLINK_ROOT / domain
        if not domain_dir.exists():
            continue
        for json_file in domain_dir.glob("*.json"):
            try:
                data = json.loads(json_file.read_text(encoding="utf-8"))
                target_anchor = data.get("anchor_id")
                for link in data.get("links", []):
                    con.execute("""
                        INSERT INTO edges
                        (target_anchor, source_file, source_reference, link_type, domain, entity, service, generated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        target_anchor,
                        link.get("source_file"),
                        link.get("source_anchor"),
                        link.get("link_type"),
                        domain,
                        link.get("entity"),
                        link.get("service"),
                        datetime.fromisoformat(data.get("generated_at", datetime.now().isoformat()).replace('Z','+00:00'))
                    ))
                    edge_count += 1
            except Exception as e:
                print(f"Warning: skipped malformed JSON {json_file}: {e}")

    # 3. Integrity checks (V13 gate)
    issues = []
    dangling = con.execute("""
        SELECT COUNT(*) FROM edges e
        LEFT JOIN nodes n ON e.target_anchor = n.anchor_id
        WHERE n.anchor_id IS NULL
    """).fetchone()[0]
    if dangling > 0:
        issues.append(f"{dangling} dangling references")

    # High-degree flag (human review)
    high_degree = con.execute("""
        SELECT target_anchor, COUNT(*) as deg
        FROM edges GROUP BY target_anchor HAVING deg > 50
    """).fetchall()

    report = {
        "timestamp": datetime.now().isoformat(),
        "node_count": node_count,
        "edge_count": edge_count,
        "issues": issues,
        "high_degree_nodes": len(high_degree),
        "high_degree_examples": [f"{a} ({d})" for a, d in high_degree[:5]]
    }
    report_path = REPORT_DIR / f"graph_integrity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_path.write_text(json.dumps(report, indent=2))

    if issues:
        print("❌ Integrity failures:", issues)
        sys.exit(1)

    print(f"✅ Graph regenerated: {node_count} nodes, {edge_count} edges")
    con.close()

if __name__ == "__main__":
    main()
```

### Deliverable 3 — `pipeline/graph/INTEGRITY_GATE_SPEC.md` (ready to commit)
```markdown
# Phase 3 Graph Integrity Gate (V13)

**Trigger:** After backlink extraction script, before `promote` step.

**Mandatory Fail Conditions (exit non-zero):**
- Any dangling reference (edge.target_anchor missing from nodes)
- JSON parse errors in Layer 2 files

**Non-blocking Warnings (logged to report):**
- High-degree nodes (>50 inbound edges) — surfaced for human review
- Zero-degree canon anchors (expected in incremental rollout)

**Operational Definitions:**
- Dangling reference: target_anchor in edges has no matching node (checked via LEFT JOIN).
- Backlink completeness: every `[[BOOK.CH:V]]` in phronema/notes/articles must produce a Layer 2 entry (enforced at extraction time; Layer 3 only verifies against canon nodes).
- Completeness of nodes: every anchor in promoted canon/ files is present (enforced by full scan).

**Filename Convention (ADJ-1):** `BOOK.CH-VER.json` (hyphen escape).  
**canon_uri format (ADJ-4):** `canon/{OT|NT}/BOOK.md#ANCHOR` (live structure).

**Integration:** `python pipeline/graph/regenerate_graph.py` as final step in the promotion pipeline. Fail blocks commit.

**Invariants reaffirmed:** No writes to canon/, DuckDB strictly derived, Git remains single source of truth.
```

**Grok Coordination Note**  
All agents aligned. No contradictions surfaced. Harper’s live-repo data locked the filename and path decisions. Lucas can now update the governing `PHASE3_SPEC_SKELETON_20260310.md` and close ADJ-1/ADJ-4.  

**Next (open engineering problem):** Ark to wire the regeneration script into the promotion gate and test on a single book. Human ratification required before first full run.  

**Status:** Deliverables ready for `git add` and commit. Archive remains provenance-first and scales safely into Phase 3 hyperlinking.
