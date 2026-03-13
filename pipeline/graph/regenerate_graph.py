"""
regenerate_graph.py — Build the derived DuckDB graph from backlink shards.
"""
from __future__ import annotations

import argparse
from collections import OrderedDict
import json
from pathlib import Path

from pipeline.common.paths import METADATA_ROOT
from pipeline.graph.build_backlinks import BACKLINKS_ROOT, detect_domain

GRAPH_PATH = METADATA_ROOT / "graph" / "phronema_graph.duckdb"
SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def load_backlink_payloads(backlinks_root: Path = BACKLINKS_ROOT) -> list[dict]:
    payloads: list[dict] = []
    for path in sorted(backlinks_root.glob("*/*.json")):
        payloads.append(json.loads(path.read_text(encoding="utf-8")))
    return payloads


def collect_graph_rows(backlinks_root: Path = BACKLINKS_ROOT) -> tuple[list[dict], list[dict]]:
    node_map: OrderedDict[str, dict] = OrderedDict()
    edge_map: OrderedDict[str, dict] = OrderedDict()

    for payload in load_backlink_payloads(backlinks_root):
        anchor_id = payload["anchor_id"]
        anchor_node_id = f"anchor:{anchor_id}"
        node_map.setdefault(
            anchor_node_id,
            {
                "node_id": anchor_node_id,
                "node_type": "canon_anchor",
                "label": anchor_id,
                "domain": "canon",
                "metadata_json": json.dumps(
                    {
                        "anchor_id": anchor_id,
                        "canon_uri": payload["canon_uri"],
                        "text_tradition": payload["text_tradition"],
                    },
                    sort_keys=True,
                ),
            },
        )
        for link in payload.get("links", []):
            source_node_id = f"source:{link['source_file']}"
            node_map.setdefault(
                source_node_id,
                {
                    "node_id": source_node_id,
                    "node_type": "source_document",
                    "label": link["source_file"],
                    "domain": detect_domain(link["source_file"]),
                    "metadata_json": json.dumps(
                        {"source_file": link["source_file"]},
                        sort_keys=True,
                    ),
                },
            )
            edge_id = f"{source_node_id}->{anchor_node_id}@{link['line_number']}:{link['raw_match']}"
            edge_map.setdefault(
                edge_id,
                {
                    "edge_id": edge_id,
                    "source_node_id": source_node_id,
                    "target_node_id": anchor_node_id,
                    "edge_type": link["reference_type"],
                    "metadata_json": json.dumps(
                        {
                            "context": link["context"],
                            "line_number": link["line_number"],
                            "raw_match": link["raw_match"],
                        },
                        sort_keys=True,
                    ),
                },
            )
    return list(node_map.values()), list(edge_map.values())


def regenerate_graph(backlinks_root: Path = BACKLINKS_ROOT, output_path: Path = GRAPH_PATH) -> Path:
    try:
        import duckdb  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "duckdb is not installed; install the optional graph dependency before regenerating the graph"
        ) from exc

    output_path.parent.mkdir(parents=True, exist_ok=True)
    nodes, edges = collect_graph_rows(backlinks_root)
    conn = duckdb.connect(str(output_path))
    try:
        conn.execute(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.execute("DELETE FROM archive_edges")
        conn.execute("DELETE FROM archive_nodes")
        if nodes:
            conn.executemany(
                """
                INSERT INTO archive_nodes (node_id, node_type, label, domain, metadata_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                [(row["node_id"], row["node_type"], row["label"], row["domain"], row["metadata_json"]) for row in nodes],
            )
        if edges:
            conn.executemany(
                """
                INSERT INTO archive_edges (edge_id, source_node_id, target_node_id, edge_type, metadata_json)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        row["edge_id"],
                        row["source_node_id"],
                        row["target_node_id"],
                        row["edge_type"],
                        row["metadata_json"],
                    )
                    for row in edges
                ],
            )
    finally:
        conn.close()
    return output_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Regenerate the derived DuckDB graph.")
    parser.add_argument("--backlinks-root", type=Path, default=BACKLINKS_ROOT)
    parser.add_argument("--output", type=Path, default=GRAPH_PATH)
    args = parser.parse_args()

    out_path = regenerate_graph(args.backlinks_root, output_path=args.output)
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
