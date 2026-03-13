# Research Architectural Blueprint for DuckDB-Powered Theological Citation Graphs


## Executive Overview

The Orthodox Phronema Archive utilizes a highly structured, flat-file directed acyclic graph (DAG) architecture. Within this system, plain-text Markdown files serve as primary knowledge nodes, while approximately 31,000 theological and scriptural anchors—formatted to strict Society of Biblical Literature (SBL) standards (e.g., GEN.1:1, 1MA.2:5)—function as semantic edges connecting these nodes.<sup>1</sup> Phase 3 of this architectural evolution requires transitioning from an upstream extraction pipeline (R1), which outputs heavily typed JSON Lines (JSONL) records, into a high-performance Online Analytical Processing (OLAP) database engine capable of executing complex graph traversals and lexical searches.<sup>1</sup>

DuckDB has been selected as the target analytical engine due to its in-process nature, vectorized execution model, and extensible ecosystem. The upstream R1 pipeline guarantees a rigid output payload consisting of exact fields: source_file, line_number, raw_match, anchor_id, reference_type (frozen or bare), and context.<sup>1</sup> To effectively generate a production-ready DuckDB schema and ingestion protocol, the data engineering architecture must resolve several complex pipeline requirements.

This exhaustive research report investigates the operational stability of DuckDB's duckpgq graph extension, the compositional limitations of unifying Full-Text Search (FTS) with Property Graph Queries, the optimal recursive ingestion mechanisms for domain-sharded metadata directories, the implementation of advanced graph integrity validations derived from academic standards such as OpenAlex and OpenCitations, and the mathematical inflection points dictating the transition from JSONL to Apache Parquet intermediate storage. The findings detailed herein provide the definitive theoretical and mechanical foundation required for subsequent downstream code generation and schema deployment.


## 

---
1. DuckPGQ Stability and Production Readiness (Early 2026)

The integration of graph analytics into relational database systems represents a significant evolution in data modeling. Historically, highly connected data required exportation to dedicated native graph databases (e.g., Neo4j, TigerGraph), which introduced substantial network latency and maintenance overhead.<sup>2</sup> The duckpgq community extension circumvents this paradigm by introducing SQL/PGQ (Property Graph Queries)—a sub-language formally introduced in the ISO SQL:2023 standard—directly into DuckDB's vectorized analytical engine.<sup>4</sup>


### Current Production Readiness Designations

As of early 2026, it is imperative for data engineering teams to recognize the official support classification of the duckpgq extension. DuckDB operates a dual-tier extension ecosystem consisting of "Core" extensions (which receive Long-Term Support and guarantee stability) and "Community" extensions.<sup>6</sup> The duckpgq module, maintained primarily by the Database Architectures group at Centrum Wiskunde & Informatica (CWI), resides strictly within the community tier.<sup>4</sup>

The extension is explicitly documented as an ongoing research project.<sup>4</sup> The core maintainers have issued explicit disclaimers indicating that users should anticipate incomplete features, occasional instability, and unexpected behaviors.<sup>4</sup> In parallel, other major community ecosystem projects, such as DuckLake, are targeting their 1.0 production-ready releases for March or April of 2026.<sup>8</sup> While duckpgq is maturing rapidly alongside these initiatives, it lacks the enterprise-grade Service Level Agreements (SLAs) characteristic of DuckDB's core engine.<sup>7</sup>

Consequently, for the Orthodox Phronema Archive, duckpgq should be positioned strategically. It is exceptionally well-suited for backend metadata generation, analytical discovery, and the compilation of static routing tables. However, it should not yet be deployed in the critical path of a synchronous, user-facing web application without establishing robust, secondary fallback querying mechanisms.


### Performance Limitations at the 10k–50k Edge Scale

Evaluating the physical limitations of duckpgq requires an understanding of its internal memory mechanics. When a CREATE PROPERTY GRAPH statement is executed, the extension does not permanently alter the underlying relational tables. Instead, when a GRAPH_TABLE pattern match is invoked, the extension utilizes highly optimized, vectorized User-Defined Functions (UDFs) to generate a Compressed Sparse Row (CSR) representation of the graph topology on the fly, entirely in memory.<sup>3</sup>

The CSR format is a highly compact data structure that allows for rapid contiguous memory access, dramatically outperforming traditional node-pointer hopping.<sup>9</sup> Because the extraction pipeline for the Orthodox Phronema Archive generates approximately 31,000 scripture anchors (edges) mapped against a finite set of Markdown files (vertices) <sup>1</sup>, the total scale of the graph falls within the 10,000 to 50,000 edge range.

From a computational complexity perspective, generating a CSR representation for 50,000 edges is mathematically trivial for DuckDB. Modern CPU architectures feature L3 caches that can easily store the entirety of a 50,000-edge CSR array. The extension has been successfully benchmarked on the LDBC Social Network Benchmark (SNB) and the Financial Benchmark (finbench) datasets, which contain millions of highly complex vertices and routing edges.<sup>10</sup> At the 31,000 edge scale, the pipeline will encounter absolutely zero memory bottlenecks, and path-finding algorithms (such as ANY SHORTEST or variable-length paths denoted by Kleene stars) will execute with sub-millisecond latency.<sup>9</sup>


### Known Failure Modes and Breaking Changes

Deploying duckpgq in a 2026 production pipeline demands defensive engineering practices to mitigate documented failure modes and breaking changes:



1. **Algorithmic Scoping Failures:** The most prominent known bug involves the execution of native graph algorithms. The official documentation issues a strict warning that graph algorithm functions, including local_clustering_coefficient and pagerank, may sporadically fail and return a csr_cte does not exist error.<sup>11</sup> This failure mode is rooted in the extension's Common Table Expression (CTE) binding logic, where the dynamically generated CSR structure drops out of scope during execution.<sup>11</sup> Pipelines must wrap algorithm execution in try-catch exception handling.
2. **Schema Rigidity and Silent Empty Sets:** The SQL/PGQ standard enforces a rigid hyper-schema over the base tables. The CREATE PROPERTY GRAPH statement establishes explicit SOURCE KEY and DESTINATION KEY constraints that function similarly to foreign keys.<sup>11</sup> If the upstream R1 JSONL pipeline introduces even minor structural mutations—such as altering the anchor_id format from GEN.1:1 to GEN_1_1—the edge mappings will silently fail to bind to the vertex tables. Rather than throwing a hard schema validation error, subsequent GRAPH_TABLE queries will simply return empty sets.<sup>11</sup> Continuous schema validation at the ingestion boundary is mandatory.
3. **Parser Conflicts:** DuckDB utilizes a runtime-extensible parsing mechanism. Extensions like duckpgq inject custom parsers that act as failovers when the default SQL parser cannot comprehend the visual MATCH (a)-[e]->(b) syntax.<sup>13</sup> Complex subqueries that mix highly specialized core DuckDB dialects with PGQ syntax occasionally confuse the parser hierarchy, necessitating the isolation of graph queries into discrete, encapsulated CTEs.<sup>13</sup>

<table>
  <tr>
   <td>
<strong>Operational Metric</strong>
   </td>
   <td><strong>duckpgq Capability</strong>
   </td>
   <td><strong>Phronema Pipeline Requirement</strong>
   </td>
   <td><strong>Alignment Assessment</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Scale Capacity</strong>
   </td>
   <td>Millions of edges (LDBC SNB benchmarked) <sup>10</sup>
   </td>
   <td>~31,000 edges <sup>1</sup>
   </td>
   <td>Extreme over-capacity; zero RAM bottlenecks.
   </td>
  </tr>
  <tr>
   <td><strong>Data Structure</strong>
   </td>
   <td>On-the-fly Compressed Sparse Row (CSR) <sup>9</sup>
   </td>
   <td>Fast, repetitive batch analytics
   </td>
   <td>Highly suitable for vectorized OLAP.
   </td>
  </tr>
  <tr>
   <td><strong>Stability Status</strong>
   </td>
   <td>Community Extension / Research <sup>4</sup>
   </td>
   <td>Mission-critical metadata generation
   </td>
   <td>Requires fallback mechanisms and error handling.
   </td>
  </tr>
  <tr>
   <td><strong>Algorithmic Reliability</strong>
   </td>
   <td>Documented csr_cte scoping bugs <sup>11</sup>
   </td>
   <td>PageRank, Clustering algorithms
   </td>
   <td>Moderate risk; requires defensive try-catch wrappers.
   </td>
  </tr>
</table>



## 

---
2. Composing Full-Text Search and Graph Queries

A critical analytical requirement for the Orthodox Phronema Archive is the ability to execute hybrid queries that simultaneously filter nodes based on lexical context and traverse topological graph structures. Specifically, analysts require the ability to run a full-text search over the localized context field—identifying specific theological discussions, such as the concept of "ex nihilo" or "theosis"—and immediately retrieve the graph traversal paths originating from those specific Markdown nodes.<sup>1</sup>


### The Architectural Conflict of Query Composition

In DuckDB, combining the fts (Full-Text Search) extension and the duckpgq extension into a single, unified query statement presents a profound structural conflict rooted in relational algebra and index architecture.

The fts extension, inspired by SQLite's FTS5 module, relies on an inverted index generated via the PRAGMA create_fts_index statement.<sup>14</sup> When querying this index, DuckDB utilizes the Okapi BM25 ranking function, which calculates document relevance based on term frequency and inverse document frequency.<sup>14</sup> This function, match_bm25(), is invoked within the SELECT or WHERE clause to dynamically score and filter text relations.<sup>14</sup>

Conversely, the duckpgq extension relies on the GRAPH_TABLE table function, which must be invoked within the FROM clause of a SQL statement.<sup>11</sup> The GRAPH_TABLE function utilizes visual pattern matching syntax (MATCH (n)-[e]->(m)) to traverse the predefined schema established by the CREATE PROPERTY GRAPH statement.<sup>11</sup>

These two paradigms cannot be syntactically composed into a single, atomic clause. The GRAPH_TABLE function is designed to operate on statically bound relations; it cannot accept dynamically generated, BM25-scored relations directly within its localized vertex binding syntax (e.g., one cannot write MATCH (n:Person WHERE match_bm25(n.context, 'theosis') > 0)). Attempting to embed a scalar macro scoring function inside the highly specialized visual graph parser will result in immediate syntax failure, as the custom PGQ parser cannot reconcile the lexical macro before the CSR matrix is instantiated.<sup>11</sup>


### The Correct Two-Step CTE Execution Pattern

To achieve the desired compositional outcome, the data pipeline must adhere to a strict two-step execution pattern utilizing Common Table Expressions (CTEs). This pattern effectively bifurcates the workload into a lexical filtering phase and a topological traversal phase, leveraging DuckDB's query optimizer to enforce predicate pushdown.


#### Phase 1: Lexical Materialization (The FTS CTE)

The initial CTE is tasked exclusively with interrogating the inverted index. It executes the match_bm25 scoring algorithm against the context column and filters the results based on a predefined relevance threshold.<sup>14</sup> This phase projects a heavily truncated set of primary keys (e.g., source_file or a surrogate node ID) that represent the localized sub-graph of relevant Markdown nodes.


    SQL

WITH fts_filtered_nodes AS ( \
    SELECT  \
        source_file,  \
        match_bm25(source_file, 'ex nihilo') AS relevance_score \
    FROM archive_nodes \
    WHERE match_bm25(source_file, 'ex nihilo') IS NOT NULL \
) \



#### Phase 2: Topological Traversal and Join

The subsequent query block invokes the GRAPH_TABLE function to execute the required path-finding algorithm (such as ANY SHORTEST path to a specific scriptural anchor).<sup>11</sup> Rather than forcing the GRAPH_TABLE to comprehend the FTS index, the main query executes an INNER JOIN between the output of the GRAPH_TABLE projection and the fts_filtered_nodes CTE.


    SQL

SELECT  \
    g.start_node,  \
    g.anchor_id,  \
    g.path_hops, \
    f.relevance_score \
FROM GRAPH_TABLE (phronema_graph \
    MATCH p = ANY SHORTEST (a:Node)-[e:Cites]->+(b:Scripture) \
    COLUMNS (a.source_file AS start_node, b.anchor_id AS anchor_id, path_length(p) AS path_hops) \
) AS g \
INNER JOIN fts_filtered_nodes AS f  \
    ON g.start_node = f.source_file \
ORDER BY f.relevance_score DESC; \


This pattern is highly optimal. By materializing the FTS results in the leading CTE, the DuckDB execution engine inherently understands that the starting vertex pool for the graph traversal is constrained. While DuckPGQ currently has limited support for complex sub-path variable binding <sup>9</sup>, standard join filtering applied immediately to the GRAPH_TABLE output ensures that memory consumption remains minimal and that computational cycles are not wasted traversing edges originating from semantically irrelevant documents.


## 

---
3. Directory Ingestion Patterns for Domain-Sharded Architectures

The third phase of the Phronema pipeline generates highly structured JSON Lines (JSONL) files stored in domain-sharded subdirectories. The explicit directory structure follows the pattern metadata/anchor_backlinks/{domain}/ANCHOR.json, where the {domain} classification represents critical theological taxonomies such as liturgical/, patristic/, and study/.<sup>1</sup> Ingesting these deeply nested, disparate files into DuckDB while mathematically preserving the parent directory name as a queryable database column is a foundational requirement for downstream metadata aggregation.


### The Vulnerability of the Union Pattern

A traditional methodology for merging multiple files with potentially diverging schemas is the application of the UNION ALL BY NAME SQL pattern.<sup>17</sup> DuckDB provides robust support for this feature, allowing independent read_json_auto queries to be stacked vertically.<sup>17</sup> When a specific column exists in one relation but not another, DuckDB intelligently fills the absent schema spaces with NULL values rather than failing the execution.<sup>17</sup>

To capture the domain utilizing this pattern, an engineer would construct discrete statements, manually injecting the domain as a string literal:


    SQL

SELECT 'liturgical' AS domain, * FROM read_json_auto('metadata/anchor_backlinks/liturgical/*.json') \
UNION ALL BY NAME \
SELECT 'patristic' AS domain, * FROM read_json_auto('metadata/anchor_backlinks/patristic/*.json') \


While explicitly readable, this architecture is functionally brittle. The primary liability of the union pattern is hardcoded stasis. If the upstream R1 extraction pipeline evolves and introduces a new thematic domain directory (e.g., canonical/ or historical/), the static ingestion script will silently ignore the new data silo.<sup>1</sup> This results in silent data loss, violating the zero-tolerance constraints outlined in the engineering specifications.<sup>1</sup>


### The Failure of Native Hive Partitioning

DuckDB possesses a native mechanism known as Hive Partitioning, explicitly engineered to map folder structures into database columns automatically during the read_json or read_parquet ingestion phase.<sup>18</sup> Setting the parameter hive_partitioning=true commands DuckDB to parse the directory tree and extract variables.<sup>19</sup>

However, Native Hive partitioning demands strict adherence to a specific directory nomenclature: folders must be formatted as explicit key-value pairs separated by an equals sign.<sup>18</sup> A valid Hive partition path appears as .../domain=liturgical/ANCHOR.json.<sup>18</sup> Because the Orthodox Phronema Archive utilizes pure noun designations (e.g., .../liturgical/ANCHOR.json) rather than key-value designations, the hive_partitioning parameter will fail to reliably parse the taxonomy.<sup>1</sup> Attempting to force DuckDB to interpret non-compliant directories via this parameter often leads to parsing errors or empty partition columns.


### The Superior Pattern: Recursive Globbing and filename=true

The most robust, zero-maintenance ingestion pattern leverages DuckDB's recursive wildcard glob syntax combined with the internal virtual column mechanism.<sup>20</sup>

Since DuckDB version 1.3.0, the read_json_auto function automatically exposes a virtual column titled filename.<sup>19</sup> This column captures the exact relative or absolute file path of the source artifact for every individual row parsed into the engine.<sup>22</sup>

The optimized pipeline pattern utilizes a double-wildcard recursive glob */*.json to capture all subdirectories within the anchor_backlinks parent folder simultaneously. This guarantees that any future taxonomic domains added by the R1 pipeline are instantly and automatically ingested without requiring modifications to the SQL script.<sup>19</sup>


    SQL

CREATE VIEW phronema_backlinks AS  \
WITH raw_ingestion AS ( \
    SELECT *, filename  \
    FROM read_json_auto('metadata/anchor_backlinks/*/*.json', filename=true) \
) \
SELECT  \
    source_file, \
    line_number, \
    raw_match, \
    anchor_id, \
    reference_type, \
    context, \
    -- Extract the domain folder name from the physical file path string \
    split_part(filename, '/', -2) AS taxonomy_domain \
FROM raw_ingestion; \


In this architecture, DuckDB executes a highly parallelized, single-pass ingestion over the entire directory tree. The string manipulation function split_part(filename, '/', -2) acts on the virtual filename column, splitting the path array by the forward-slash delimiter and extracting the penultimate segment—which mathematically equates to the domain folder name (e.g., patristic). This pattern delivers absolute reliability, guarantees schema evolution tolerance, and perfectly fulfills the engineering requirement to preserve the domain state as a queryable column.


## 

---
4. Graph Integrity and Validation Completeness

Citation graphs, whether mapping academic literature or theological intertextuality, are highly susceptible to silent corruption. An edge pointing to an invalid node, or multiple edges duplicating the same semantic link, rapidly degrades the reliability of downstream analytics. While rudimentary pipeline checks generally cover dangling references (an edge without a target) and orphaned nodes (a vertex with zero inbound or outbound edges), enterprise-grade scholarly graphs require far more rigorous validation frameworks.

A survey of the data ingestion pipelines engineered by leading open-source scholarly knowledge graphs—specifically **OpenAlex** and **OpenCitations**—reveals sophisticated, standard-practice validation paradigms that must be transposed to the Phronema pipeline to ensure data purity.<sup>23</sup>


### Survey of OpenCitations and OpenAlex Methodologies

**OpenCitations** is a community-guided infrastructure dedicated to the publication of open bibliographic and citation data.<sup>25</sup> To maintain the purity of its multi-billion edge graph, OpenCitations developed the OpenCitations Data Model (OCDM), heavily rooted in Semantic Web technologies.<sup>26</sup> Their pipeline employs continuous validation mechanisms, utilizing tools designed to detect syntactical and semantic ingestion errors before they propagate into the core index.<sup>27</sup> A defining standard practice of OpenCitations is its rigorous adherence to **Provenance Tracking** (PROV-O), which mathematically documents the origin, the modification history, and the agent responsible for every singular edge in the graph.<sup>26</sup>

**OpenAlex**, built from the ashes of the Microsoft Academic Graph (MAG), catalogs over 450 million scholarly works by merging highly disparate data sources (Crossref, PubMed, DataCite) into a unified schema.<sup>23</sup> OpenAlex's ingestion pipeline implements automated **Entity Deduplication Algorithms** and **Canonical Identifier Mapping**, ensuring that citations flow logically and that multiple textual representations of an identical concept map to a singular, canonical entity identifier (PID).<sup>23</sup>


### Transposing Validation Patterns to the Theological Pipeline

Applying these advanced academic standards to the Orthodox Phronema Archive requires implementing multiple deterministic integrity checks on the JSONL records prior to their binding within the duckpgq graph memory space. The upstream R1 pipeline outputs specific fields (source_file, line_number, raw_match, anchor_id, reference_type, context) <sup>1</sup> that must be evaluated against the following advanced criteria:


#### 1. Canonical Identifier Disambiguation and Regex Enforcement

OpenAlex and OpenCitations solve external identifier mismatches by assigning strict global identifiers (OMIDs) to act as proxies for disambiguation.<sup>26</sup> The Phronema pipeline utilizes the SBL string format as its persistent identifier (PID).<sup>1</sup> A standard practice integrity check must validate that the anchor_id column strictly conforms to the exact alphanumeric morphology outlined in the engineering specification.

The validation script must utilize DuckDB's POSIX regular expression engine (regexp_matches) to ensure every anchor_id strictly satisfies the boundary pattern ^[A-Z0-9]{2,4}\.\d+:\d+$.<sup>1</sup> Any row violating this mathematical constraint must be quarantined, preventing malformed strings from causing the GRAPH_TABLE schema mapping to fail.


#### 2. Spatial Deduplication and Edge Collisions

OpenAlex relies heavily on entity deduplication to prevent bloated graph topologies.<sup>23</sup> In the Phronema Markdown pipeline, authors utilize two syntaxes: "frozen" (explicitly bracketed links) and "bare" (implicit prose references).<sup>1</sup> Because the inner string of a frozen link ([[GEN.1:1]]) perfectly matches the morphology of a bare link (GEN.1:1), spatial collisions are a severe threat.<sup>1</sup>

If the upstream R1 pipeline's abstract syntax tree (AST) overlap logic fails, the JSONL payload will contain parallel, duplicate records representing the exact same semantic link. The DuckDB validation schema must execute a grouping check:


    SQL

SELECT source_file, anchor_id, line_number, COUNT(*) as collision_count \
FROM raw_ingestion \
GROUP BY source_file, anchor_id, line_number \
HAVING collision_count > 1; \


Any count greater than one indicates a structural extraction anomaly where a bare reference was erroneously extracted from within a frozen link boundary. These duplicates must be purged to maintain the statistical validity of the citation frequencies.


#### 3. Context Window Semantic Boundary Validation

The context field generated by R1 contains the localized paragraph string surrounding the anchor.<sup>1</sup> OpenCitations ensures the semantic correctness of textual data before ingestion.<sup>27</sup> For the Phronema pipeline, an integrity check must measure the byte-length of the context payload using DuckDB's length() function.

If the context string is aggressively truncated (e.g., under 5 characters) or excessively massive (e.g., an unclosed Markdown AST block spanning 20,000 characters), it indicates a catastrophic failure in the upstream parser's token boundary logic. Records falling outside a mathematically sound standard deviation (e.g., 50 to 2000 characters) must be flagged for manual review to preserve the efficiency of the downstream Okapi BM25 Full-Text Search index.


#### 4. Hallucinated Reference Detection

With the increasing proliferation of AI-assisted authoring, academic infrastructures have had to develop mechanisms to detect "hallucinated" citations—references that are morphologically plausible but mathematically non-existent in reality.<sup>31</sup>

For the theological pipeline, it is entirely possible for an author to type 1MAC.99:99. This perfectly passes the SBL regex constraint but points to a physical coordinate that does not exist in the Book of 1 Maccabees. An advanced integrity check must execute a LEFT JOIN between the ingested anchor_id fields and a statically validated dimensional table containing the actual biblical canon maximums (e.g., Max Chapters per Book, Max Verses per Chapter). Any anchor pointing to a coordinate that physically exceeds the canonical maximums must be instantly classified as a hallucination and purged from the graph edge tables.


#### 5. Provenance and Temporal Consistency

Adopting the PROV-O ontology principles of OpenCitations <sup>26</sup>, the pipeline must ensure temporal logic. The source_file field acts as the primary provenance marker. By cross-referencing this file path with the underlying Git metadata (commit timestamps), a validation check can ensure that the graph remains chronologically sound, preventing logical errors where older document states are incorrectly mapped over newer revisions.


## 

---
5. Storage Optimization: JSONL vs. Parquet Thresholds

The upstream R1 extraction engine emits data in strictly typed JSON Lines (JSONL) format, establishing a highly resilient, machine-readable artifact impervious to the escaping errors common in CSV exports.<sup>1</sup> A fundamental architectural decision for the data engineering team is whether to introduce an intermediate ETL step—utilizing external Python libraries such as PyArrow or Pandas—to convert these JSONL files into Apache Parquet format prior to DuckDB ingestion, or to load the JSONL directly into memory using DuckDB's read_json_auto.

To make this determination, one must understand the analytical mechanics of DuckDB and the mathematical thresholds governing file format supremacy.


### Analytical Mechanics of DuckDB File Ingestion

DuckDB is explicitly engineered for Online Analytical Processing (OLAP) workloads, operating natively on vectorized, columnar memory structures.<sup>32</sup> When querying JSONL files, the database engine must execute a full table scan, decoding untyped text strings row-by-row and dynamically inferring schemas on the fly.<sup>33</sup> While DuckDB's C++ JSON reader is extraordinarily fast and parallelized <sup>33</sup>, processing raw text is inherently CPU-intensive.

Conversely, Apache Parquet is a performance-driven binary format built natively for columnar data.<sup>34</sup> Parquet files feature rigid embedded schema definitions, dictionary compression algorithms, and critical statistical metadata block headers known as zone maps.<sup>34</sup>

These zone maps allow DuckDB to execute **Predicate Pushdown**.<sup>33</sup> If a query filters for references where the anchor_id contains GEN, DuckDB can read the Parquet zone map and entirely skip scanning the row groups that do not contain the string GEN.<sup>36</sup> This capability drastically reduces disk I/O and exponentially accelerates analytical query execution.<sup>36</sup> Furthermore, Parquet's dictionary compression drastically reduces the physical footprint of repetitive strings, such as the reference_type field (which only contains two states: "frozen" or "bare").<sup>1</sup>


### The Row Group Threshold and Multi-Threading

Despite the undeniable performance supremacy of Parquet for multi-gigabyte data warehousing, applying this standard blindly to micro-scale pipelines introduces unnecessary architectural friction. DuckDB's internal parallelization engine divides processing workloads strictly by Parquet "Row Groups".<sup>37</sup>

A Parquet row group is a contiguous partition of rows. The default minimum threshold for a single DuckDB Parquet row group is **122,880 rows**.<sup>36</sup> DuckDB parallelizes execution at the row group level; therefore, if a Parquet file has a single, giant row group, it can only be processed by a single CPU thread.<sup>37</sup>

The Orthodox Phronema Archive's extracted dataset consists of approximately 31,000 scripture anchors.<sup>1</sup> Because 31,000 is vastly smaller than the 122,880 row threshold, converting the dataset to Parquet would result in a single row group.<sup>37</sup> Consequently, querying that Parquet file would be entirely single-threaded, completely neutralizing the multi-core processing advantages of the DuckDB engine.<sup>37</sup>


### The Inflection Point for Format Transition

At a scale of 31,000 rows, inserting a processing step to invoke Python libraries to translate JSONL into Parquet constitutes a severe engineering anti-pattern. The data volume translates to merely a few megabytes of physical disk space. DuckDB's highly optimized read_json_auto scanner will ingest and parse a 31,000-row JSONL file into its internal columnar representation in fractional milliseconds.<sup>19</sup> This ingestion is typically faster than the time it takes for an external Python script to boot its interpreter and initialize a Parquet writer logic sequence.

**The Trade-off Shift Threshold:**

The necessity for Parquet conversion is fundamentally dictated by scaling laws. The threshold where the processing overhead of Parquet conversion becomes mathematically justified over direct JSONL ingestion shifts under the following conditions:



1. **Row Count Exceeds 100,000 to 1,000,000:** As established by DuckDB's execution architecture, once the dataset consistently surpasses the 100,000 row mark, the data can be partitioned into multiple row groups.<sup>37</sup> At this volume, DuckDB can engage multi-threaded parallel scanning across the Parquet file, and the columnar compression begins to yield measurable latency reductions over flat JSON table scans.<sup>37</sup>
2. **I/O Bound Cloud Operations:** If the Phase 3 backend architecture transitions from localized solid-state disk storage to cloud-based object storage (e.g., AWS S3 or Google Cloud Storage), downloading raw JSON text over the network becomes a severe bottleneck. Parquet's aggressive compression ratios heavily mitigate network latency, making it superior for cloud-native querying regardless of the row count.<sup>39</sup>
3. **Highly Selective Filtering:** If the downstream queries rely heavily on highly selective filtering across massive text blocks (e.g., scanning the context field), Parquet's min-max indices and bloom filters provide unparalleled speedups through filter pushdown.<sup>21</sup>

**Conclusion:** At the current scale of ~31,000 anchors, direct ingestion of the R1 JSONL output via read_json_auto is not only sufficient, it is the optimal, low-friction engineering path. The pipeline should absolutely eschew Parquet conversion until the archive's corpus organically triples in size.


## 

---
6. Synthesis and Architectural Recommendations

To effectively deploy the DuckDB backend for the Orthodox Phronema Archive, the data engineering team should implement the following integrated recommendations to finalize the pipeline schema and ingestion scripting:



* **Graph Engine Utilization:** Treat the duckpgq extension as a powerful, exploratory UDF routing tool rather than a hardened, fault-tolerant transactional layer. Engineers must build robust SQL exception handling around all graph algorithms to elegantly degrade upon encountering undocumented internal CTE scoping bugs.<sup>11</sup> Ensure the anchor_id schemas remain perfectly rigid to prevent silent empty-set returns during CREATE PROPERTY GRAPH execution.<sup>11</sup>
* **Dual-Layer Query Strategy:** When attempting to intersect Full-Text Search indexing with graph topologies, abandon attempts to achieve unified query composition. Hardcode a two-step execution pattern where an initial CTE heavily filters the textual nodes via the match_bm25 algorithm <sup>14</sup> before those isolated identifiers are passed to the GRAPH_TABLE projection algorithm as bounded INNER JOIN predicates. This simulates predicate pushdown for the graph engine.
* **Dynamic Directory Ingestion:** Reject brittle UNION ALL patterns and natively failing Hive partitioning structures. Configure the read_json_auto ingestion script to utilize recursive file globbing (*/*.json) combined with the DuckDB filename=true virtual column mechanism.<sup>20</sup> Execute a discrete string split operation (split_part(filename, '/', -2)) to programmatically isolate and expose the domain categories (liturgical, patristic, study), ensuring silent adaptability as new taxonomies are introduced to the archive.<sup>17</sup>
* **Data Integrity Hardening:** Translate the rigorous semantic web standards of OpenCitations and OpenAlex to the flat-file pipeline.<sup>23</sup> Establish a mandatory DuckDB validation schema acting as a quarantine layer. This schema must utilize Regex to validate the SBL PID morphology (^[A-Z0-9]{2,4}\.\d+:\d+$) <sup>1</sup>, flag spatial extraction duplicates (COUNT(*) > 1), measure out-of-bounds context string lengths, and purge hallucinated coordinates via a join to a canonical dimension table prior to allowing records to enter the core graph memory space.
* **Storage Simplification:** Eliminate intermediary ETL conversion scripts. Rely entirely on DuckDB's native JSONL parsing capabilities for the ~31,000 anchor dataset, circumventing the unnecessary computational overhead of Parquet generation. Delay the implementation of columnar binary formats until the archive organically crosses the multi-threaded parallelization threshold of 100,000+ nodes, thereby preserving pipeline simplicity and execution speed.<sup>37</sup>

By adhering to these specific, mechanism-driven architectural guardrails, the resulting analytical pipeline will provide a fluid, highly precise mathematical mapping of the Orthodox Phronema Archive's vast theological pathways, seamlessly unifying lexical search capabilities with advanced topological traversal.


#### Works cited



1. Markdown Anchor Extraction Engineering Specificati....txt
2. DuckPGQ: Efficient Property Graph Queries in an Analytical RDBMS - DuckDB, accessed March 11, 2026, [https://duckdb.org/library/duckpgq/](https://duckdb.org/library/duckpgq/)
3. DuckPGQ: Efficient Property Graph Queries in an analytical RDBMS - CWI, accessed March 11, 2026, [https://ir.cwi.nl/pub/32773/32773.pdf](https://ir.cwi.nl/pub/32773/32773.pdf)
4. DuckPGQ, accessed March 11, 2026, [https://duckpgq.org/](https://duckpgq.org/)
5. duckpgq – DuckDB Community Extensions, accessed March 11, 2026, [https://duckdb.org/community_extensions/extensions/duckpgq](https://duckdb.org/community_extensions/extensions/duckpgq)
6. Announcing DuckDB 1.5.0, accessed March 11, 2026, [https://duckdb.org/2026/03/09/announcing-duckdb-150](https://duckdb.org/2026/03/09/announcing-duckdb-150)
7. Release Calendar - DuckDB, accessed March 11, 2026, [https://duckdb.org/release_calendar](https://duckdb.org/release_calendar)
8. Timeline for production readiness · duckdb ducklake · Discussion #550 - GitHub, accessed March 11, 2026, [https://github.com/duckdb/ducklake/discussions/550](https://github.com/duckdb/ducklake/discussions/550)
9. DuckPGQ: Efficient Property Graph Queries in an analytical RDBMS - CIDR (Conference on Innovative Data Systems Research), accessed March 11, 2026, [https://www.cidrdb.org/cidr2023/papers/p66-wolde.pdf](https://www.cidrdb.org/cidr2023/papers/p66-wolde.pdf)
10. Uncovering Financial Crime with DuckDB and Graph Queries, accessed March 11, 2026, [https://duckdb.org/2025/10/22/duckdb-graph-queries-duckpgq](https://duckdb.org/2025/10/22/duckdb-graph-queries-duckpgq)
11. Graph Queries - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/guides/sql_features/graph_queries](https://duckdb.org/docs/stable/guides/sql_features/graph_queries)
12. DuckPGQ DuckCon #6 2025 - DuckDB, accessed March 11, 2026, [https://blobs.duckdb.org/events/duckcon6/daniel-ten-wolde-duckpgq-unlocking-graph-analytics-in-duckdb-with-sql-pgq.pdf](https://blobs.duckdb.org/events/duckcon6/daniel-ten-wolde-duckpgq-unlocking-graph-analytics-in-duckdb-with-sql-pgq.pdf)
13. Runtime-Extensible SQL Parsers Using PEG - DuckDB, accessed March 11, 2026, [https://duckdb.org/2024/11/22/runtime-extensible-parsers](https://duckdb.org/2024/11/22/runtime-extensible-parsers)
14. Full-Text Search - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/guides/sql_features/full_text_search](https://duckdb.org/docs/stable/guides/sql_features/full_text_search)
15. Full-Text Search Extension - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/core_extensions/full_text_search](https://duckdb.org/docs/stable/core_extensions/full_text_search)
16. SQL/PGQ - DuckPGQ, accessed March 11, 2026, [https://duckpgq.org/documentation/sql_pgq/](https://duckpgq.org/documentation/sql_pgq/)
17. Vertical Stacking as the Relational Model Intended: UNION ALL BY NAME - DuckDB, accessed March 11, 2026, [https://duckdb.org/2025/01/10/union-by-name](https://duckdb.org/2025/01/10/union-by-name)
18. Hive Partitioning - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/data/partitioning/hive_partitioning](https://duckdb.org/docs/stable/data/partitioning/hive_partitioning)
19. Loading JSON - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/data/json/loading_json](https://duckdb.org/docs/stable/data/json/loading_json)
20. Reading Multiple Files - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/data/multiple_files/overview](https://duckdb.org/docs/stable/data/multiple_files/overview)
21. DuckDB Documentation, accessed March 11, 2026, [https://blobs.duckdb.org/docs/duckdb-docs.pdf](https://blobs.duckdb.org/docs/duckdb-docs.pdf)
22. Add filename and line index to CSV and JSON parsed rows (optionally) #9987 - GitHub, accessed March 11, 2026, [https://github.com/duckdb/duckdb/discussions/9987](https://github.com/duckdb/duckdb/discussions/9987)
23. OpenAlex: The open catalog to the global research system | OpenAlex, accessed March 11, 2026, [https://openalex.org/](https://openalex.org/)
24. The OpenAIRE Graph: Why Continuous Validation Matters, accessed March 11, 2026, [https://www.openaire.eu/the-openaire-graph-why-continuous-validation-matters](https://www.openaire.eu/the-openaire-graph-why-continuous-validation-matters)
25. open access - OpenCitations blog, accessed March 11, 2026, [https://opencitations.hypotheses.org/category/open-access](https://opencitations.hypotheses.org/category/open-access)
26. OpenCitations Meta | Quantitative Science Studies - MIT Press Direct, accessed March 11, 2026, [https://direct.mit.edu/qss/article/5/1/50/119554/OpenCitations-Meta](https://direct.mit.edu/qss/article/5/1/50/119554/OpenCitations-Meta)
27. A Tool for Validating and Monitoring Bibliographic Data in Open Research Information Systems: the OpenCitations Collections - CEUR-WS.org, accessed March 11, 2026, [https://ceur-ws.org/Vol-3937/paper13.pdf](https://ceur-ws.org/Vol-3937/paper13.pdf)
28. [2504.12195] Validating and monitoring bibliographic and citation data in OpenCitations collections - arXiv.org, accessed March 11, 2026, [https://arxiv.org/abs/2504.12195](https://arxiv.org/abs/2504.12195)
29. Using OpenAlex to Assess Canadian Research Outputs: An Exploratory Analysis Vincent Larivière, Carolina Pradier, Diego Kozlowsk, accessed March 11, 2026, [https://cca-reports.ca/wp-content/uploads/2025/11/using-open-alex-to-assess-canadian-research-outputs-knowledge-synthesis-paper.pdf](https://cca-reports.ca/wp-content/uploads/2025/11/using-open-alex-to-assess-canadian-research-outputs-knowledge-synthesis-paper.pdf)
30. Pattern Matching - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/sql/functions/pattern_matching](https://duckdb.org/docs/stable/sql/functions/pattern_matching)
31. CheckIfExist: Detecting Citation Hallucinations in the Era of AI-Generated Content - arXiv.org, accessed March 11, 2026, [https://arxiv.org/html/2602.15871v1](https://arxiv.org/html/2602.15871v1)
32. High Performance Data Visualization in the Browser with DuckDB and Parquet - Travis Horn, accessed March 11, 2026, [https://travishorn.com/high-performance-data-visualization-in-the-browser-with-duckdb-and-parquet/](https://travishorn.com/high-performance-data-visualization-in-the-browser-with-duckdb-and-parquet/)
33. Why DuckDB is my first choice for data processing - Hacker News, accessed March 11, 2026, [https://news.ycombinator.com/item?id=46645176](https://news.ycombinator.com/item?id=46645176)
34. CSV Files: Dethroning Parquet as the Ultimate Storage File Format — or Not? - DuckDB, accessed March 11, 2026, [https://duckdb.org/2024/12/05/csv-files-dethroning-parquet-or-not](https://duckdb.org/2024/12/05/csv-files-dethroning-parquet-or-not)
35. Query Engines: Gatekeepers of the Parquet File Format - DuckDB, accessed March 11, 2026, [https://duckdb.org/2025/01/22/parquet-encodings](https://duckdb.org/2025/01/22/parquet-encodings)
36. Parquet Tips - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/data/parquet/tips](https://duckdb.org/docs/stable/data/parquet/tips)
37. File Formats - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/guides/performance/file_formats](https://duckdb.org/docs/stable/guides/performance/file_formats)
38. Reading and Writing Parquet Files - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/data/parquet/overview](https://duckdb.org/docs/stable/data/parquet/overview)
39. Working with Huge Databases - DuckDB, accessed March 11, 2026, [https://duckdb.org/docs/stable/guides/performance/working_with_huge_databases](https://duckdb.org/docs/stable/guides/performance/working_with_huge_databases)
