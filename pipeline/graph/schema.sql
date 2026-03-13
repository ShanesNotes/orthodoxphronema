CREATE TABLE IF NOT EXISTS archive_nodes (
    node_id VARCHAR PRIMARY KEY,
    node_type VARCHAR NOT NULL,
    label VARCHAR NOT NULL,
    domain VARCHAR,
    metadata_json JSON
);

CREATE TABLE IF NOT EXISTS archive_edges (
    edge_id VARCHAR PRIMARY KEY,
    source_node_id VARCHAR NOT NULL,
    target_node_id VARCHAR NOT NULL,
    edge_type VARCHAR NOT NULL,
    metadata_json JSON
);
