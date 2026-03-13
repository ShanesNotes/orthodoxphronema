# Architectural Paradigms and Agentic Pipelines for the Preservation of Structured Textual Corpora


## Foundational Assessment of the Repository and Strategic Blueprint

An initial technical investigation into the target repository (ShanesNotes/orthodoxphronema) indicates that the live uniform resource locator is presently inaccessible to standard automated fetching protocols, likely indicating that the repository is either configured as private, is currently unindexed by external search aggregators, or exists within a restricted enterprise environment.<sup>1</sup> However, the comprehensive architectural blueprint and strategic directives governing the system are exhaustively detailed within the ingested artifact designated as PROJECT-KNOWLEDGE-STRATEGIC.md.<sup>2</sup> An analysis of this strategic documentation reveals a highly sophisticated, clean-source repository engineered specifically for the preservation of Orthodox Christian theological content, rooted in an immutable scripture substrate derived from the Orthodox Study Bible.<sup>2</sup>

The architectural philosophy of the Orthodox Phronema Archive is predicated on strict separation of concerns to prevent what the documentation identifies as "contamination".<sup>2</sup> In digital humanities and textual preservation, contamination occurs when interpretive commentary, scholarly footnotes, or dynamic cross-references bleed into the canonical textual substrate, thereby destroying the provenance and structural integrity of the primary source. To counter this, the repository enforces a non-negotiable architectural invariant: canonical scripture files residing within the canon/ directory must contain exclusively verse text and highly constrained YAML frontmatter, utilizing a strict one-verse-per-line format.<sup>2</sup>

The system manages the extreme complexity of theological linkages—spanning patristic commentary, liturgical lectionaries, and scholarly annotations—through an innovative "domain-sharded backlink proposal" scheduled for implementation in Phase 3 of the project roadmap.<sup>2</sup> Rather than embedding these complex relationships inline or relying on a centralized, monolithic relational database, the architecture utilizes a frozen, plaintext linking syntax (]) within authored Markdown files.<sup>2</sup> More critically, the machine-readable backlink artifacts are systematically sharded into discrete, atomized JSON files. These sidecar files follow a deterministic directory path governed by the canonical anchor, resulting in a structure such as metadata/anchor_backlinks/BOOK.CHAPTER.VERSE.json (for instance, metadata/anchor_backlinks/GEN.1.1.json).<sup>2</sup>

This decentralized, file-based approach is protected by a multi-stage pipeline acting as a "hard gate." Content transitions sequentially from src.texts to staging/raw, through staging/validated, and finally to the canon directory.<sup>2</sup> This transition is governed by distinct agentic roles—Ark for core architecture and canonical promotion, Ezra for strategic auditing, and Photius for parsing and staging recovery.<sup>2</sup> A partial pass during validation is treated programmatically as a total failure, ensuring that no orphaned nodes or dangling reference pointers can enter the final canonical text graph.<sup>2</sup> The subsequent sections of this report will evaluate this proprietary architecture against the current state of the art in agentic parsing, storage scalability, and global digital humanities standards.


## The Current State of the Art in Agentic Document Parsing Pipelines

The technological paradigm for extracting, parsing, and structuring complex textual corpora—encompassing scripture, legal jurisprudence, and academic humanities—has undergone a fundamental revolution in the 2024–2025 development cycle. The historical methodology relied heavily on static optical character recognition algorithms combined with brittle, heuristic rule sets designed to capture specific metadata based on physical whitespace or typography.<sup>3</sup> These legacy systems are entirely inadequate for navigating the semantic density, non-linear reading orders, and complex spatial layouts inherent in historical and legal documents. The current state of the art has decisively shifted toward "agentic" workflows.<sup>5</sup>

Agentic AI systems differentiate themselves from standard generative large language models by their capacity for autonomous planning, recursive reflection, tool invocation, and multi-step reasoning.<sup>7</sup> Rather than relying on a single model to parse a document from top to bottom, an agentic pipeline coordinates a distributed team of specialized, narrow-scope AI agents.<sup>6</sup> One agent may handle spatial layout analysis, another extracts tabular data, a third performs semantic chunking, and a coordinating agent verifies the logical consistency of the outputs against a predefined schema.<sup>6</sup>


### Zero-Shot Modular Workflows in the Legal Domain

Legal documents represent one of the most structurally demanding text types, characterized by intricate rhetorical strata, recursive cross-references, and dense argumentation that parallels the complexity of theological texts. The state of the art in legal document parsing is currently defined by zero-shot modular agentic workflows that completely bypass the need for expensive, supervised model fine-tuning.<sup>5</sup>

Recent empirical evaluations of Indian High Court judgments illustrate the efficacy of partitioning complex documents into their constituent logical structures—such as Facts, Arguments, Analysis, and Conclusion—prior to deploying extraction algorithms.<sup>5</sup> Modern frameworks deploy dual-agent architectures to achieve this. The Lexical Modular Summarizer is a three-stage pipeline heavily optimized for precise lexical overlap and structural fidelity.<sup>5</sup> Conversely, the Semantic Agentic Summarizer employs an integrated five-stage architecture that utilizes foundation models to evaluate deep semantic similarity.<sup>5</sup> When benchmarked against datasets like CivilSum and IN-Abs, these zero-shot agentic approaches achieved F1 scores up to 0.8902, rivaling the performance of heavily fine-tuned, domain-specific transformer models.<sup>5</sup>

Furthermore, the introduction of the open Argument Mining Framework has standardized the prototyping of these pipelines.<sup>10</sup> Advanced parsing systems in 2025 utilize frontier models to conduct profound discourse-level semantic analysis. These systems autonomously identify discrete argumentative units within unstructured text and map them onto complex ontological schemas, such as Philippe Bobbitt’s six constitutional modalities of legal reasoning.<sup>10</sup> The ability of an agentic pipeline to read an unstructured judicial ruling and autonomously map its arguments into a highly structured JSON ontology represents a monumental leap in the processing of complex corpora.


### Agentic Retrieval-Augmented Generation in the Humanities

Within the academic humanities and the preservation of historical records, agentic pipelines are utilized to overcome the severe limitations of standard Retrieval-Augmented Generation architectures. Naive retrieval systems perform a simple vector similarity search across a flat index of document chunks, a process that frequently returns overly narrow text fragments completely divorced from their global structural context, resulting in high rates of hallucination and information noise.<sup>9</sup>

To address the domain-specific nuances of religious and humanities texts, developers have introduced specialized systems such as SpiritRAG.<sup>9</sup> Built to navigate a highly complex, 7,500-document archive of United Nations resolutions concerning religion and spirituality, SpiritRAG functions as an interactive, agentic question-answering system.<sup>9</sup> Because concepts of theology and spirituality are notoriously difficult to operationalize using conventional keyword searches or naive embeddings, SpiritRAG utilizes a planner-executor-responder architecture.<sup>9</sup>

In these advanced humanistic workflows, the system dynamically infers the true intent of the researcher, detects shifts in document modality or language, and orchestrates secondary retrieval tools.<sup>13</sup> The orchestration layer strictly separates scientific and philosophical reasoning from computational execution. Top-layer orchestrator agents route tasks and interpret linguistic ambiguities, middle-layer contracts define the structured output requirements, and bottom-layer execution agents run deterministic extraction scripts over the parsed data.<sup>14</sup> This ensures that the outputs remain robust, mathematically traceable, and resistant to the cascading logic failures that plague standard generative AI models.<sup>9</sup>


<table>
  <tr>
   <td><strong>Pipeline Characteristic</strong>
   </td>
   <td><strong>Traditional Parsing & Extraction</strong>
   </td>
   <td><strong>State-of-the-Art Agentic Workflows (2024-2025)</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Execution Model</strong>
   </td>
   <td>Single-pass, heuristic rules, linear processing.<sup>3</sup>
   </td>
   <td>Multi-agent coordination, recursive reflection, self-correction.<sup>6</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Model Adaptation</strong>
   </td>
   <td>Requires extensive supervised fine-tuning on labeled data.<sup>5</sup>
   </td>
   <td>Operates effectively in zero-shot configurations via structured prompts.<sup>5</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Structural Comprehension</strong>
   </td>
   <td>Flat text concatenation, loss of hierarchical context.<sup>11</sup>
   </td>
   <td>Deep ontological mapping, discourse-level argument extraction.<sup>10</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Retrieval Architecture</strong>
   </td>
   <td>Naive dense vector similarity search.<sup>11</sup>
   </td>
   <td>Hierarchical indexing, planner-executor architectures, dynamic tool use.<sup>11</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Error Handling</strong>
   </td>
   <td>Brittle failures upon encountering layout shifts.<sup>6</sup>
   </td>
   <td>Autonomous routing around execution loops and tool misuse.<sup>13</sup>
   </td>
  </tr>
</table>



## Open Source Tooling for Religious Text Archiving and Digitization

The success of any agentic pipeline relies entirely on the quality of the underlying data ingestion phase. The process of liberating religious texts, scriptures, and ancient commentaries from physical manuscripts and digital facsimiles (PDFs) requires tooling capable of handling extreme typographic variance, diacritical marks, multiple column layouts, and complex margin annotations. A thorough review of the open-source ecosystem reveals a stark contrast between legacy utilities and modern, deep-learning-based extraction frameworks.


### The Limitations of Legacy Systems: An Analysis of pdftotext

For over a decade, digital humanities projects relied heavily on pdftotext, an open-source command-line utility based on the Poppler rendering library.<sup>3</sup> This tool operates by scanning the underlying byte stream of a PDF document and extracting the character codes to generate a plain text file.<sup>4</sup> While pdftotext has been widely utilized to build early religious corpora—such as extracting the Biblical text or the Jehovah’s Witnesses JW300 corpus for machine translation benchmarking—its mechanical limitations render it dangerous for modern, highly structured archival work.<sup>17</sup>

The fundamental flaw of pdftotext is its total lack of semantic layout comprehension.<sup>3</sup> The software relies entirely on heuristic algorithms that attempt to guess reading order based on the physical X and Y coordinates of text blocks on a page.<sup>3</sup> Consequently, when pdftotext processes a complex document like a scanned theological treatise, it routinely fails to distinguish between the primary body text, header metadata, inline footnotes, and multi-column tables. The utility is known to ignore clipping paths entirely, resulting in the concatenation of discrete spatial elements into a single, unreadable block of text.<sup>16</sup>

In situations involving tables, pdftotext frequently scrambles columns into rows, destroying the relational integrity of the data.<sup>19</sup> Furthermore, the utility struggles significantly with non-standard encodings, requiring manual intervention to support specialized fonts or right-to-left scripts such as Hebrew and Aramaic, often necessitating the manual installation of specific language packs to prevent character corruption.<sup>20</sup> For an architecture like the Orthodox Phronema Archive, where preventing the contamination of scripture by inline footnotes is an explicit architectural invariant, deploying pdftotext would introduce catastrophic levels of data corruption.<sup>2</sup>


### The Ascendance of IBM's Docling in the Open Source Ecosystem

The current benchmark for open-source document conversion and parsing is Docling, a self-contained, MIT-licensed toolkit developed by the AI for Knowledge team at IBM Research.<sup>21</sup> Achieving the status of the top trending repository on GitHub globally in late 2024, Docling fundamentally redefines the ingestion phase by transforming heterogeneous document formats into a unified, mathematically expressive JSON and Markdown representation known as the DoclingDocument.<sup>21</sup>

Docling achieves unparalleled extraction accuracy through its integration of highly specialized, lightweight AI models that run efficiently on commodity hardware.<sup>21</sup> The framework utilizes DocLayNet for advanced document layout analysis, allowing the system to natively identify and segment reading order, paragraphs, headers, and floating sidebars with extremely high confidence.<sup>21</sup> Additionally, the TableFormer model is deployed specifically to recognize and preserve complex tabular structures, overcoming the primary failure mode of legacy extraction utilities.<sup>21</sup>

For religious and historical archiving, Docling's support for Visual Language Models, such as GraniteDocling, provides transformative capabilities.<sup>22</sup> Leveraging MLX acceleration on supported hardware, the system can parse digitized manuscripts and scanned PDFs, executing extensive optical character recognition and multimodal alignment directly out of the box.<sup>22</sup> Furthermore, Docling seamlessly integrates into the modern agentic ecosystem, providing plug-and-play compatibility with frameworks like LangChain, LlamaIndex, and the Model Context Protocol, enabling local-first document processing without relying on expensive, proprietary cloud APIs.<sup>22</sup>


### Applied Architectures in Religious and Humanities Archiving

The integration of advanced parsing tools into live digital humanities and religious archiving projects provides empirical evidence of their superiority. The open-source community is actively pivoting toward these modern frameworks to construct resilient knowledge bases.

A prime example is the SanghaGPT initiative, a comprehensive retrieval-augmented generation system focused exclusively on classical Vietnamese Buddhist texts.<sup>25</sup> This project utilizes Docling within its primary data pipeline to ingest complex PDFs containing the Complete Works of An Sĩ and commentaries on the Avalokitesvara Sutra.<sup>25</sup> The system converts these documents into structured Markdown and JSONL formats, applies Named Entity Recognition to the extracted theological concepts, and generates multilingual vector embeddings to support semantic search and agentic question answering.<sup>25</sup>

Similarly, the Jewish Library MCP Server (mcp-otzaria-server) leverages modern protocols to expose an immense corpus of Jewish texts and documents to large language models.<sup>26</sup> By integrating the Model Context Protocol alongside advanced full-text search engines like Tantivy, the system allows agentic AI workflows to dynamically query religious texts, cite specific literature, and maintain high standards of factual grounding during academic research.<sup>26</sup>

In the broader context of scientific and academic research, frameworks like PaperQA2 have integrated Docling directly into their model-based PDF reading layers to facilitate multimodal contextual summarization of literature.<sup>28</sup> By supporting structured extraction systems that understand page numbers, document boundaries, and embedded media, these projects are succeeding where older systems relying on pdftotext failed.


<table>
  <tr>
   <td><strong>Assessment Vector</strong>
   </td>
   <td><strong>Legacy Heuristic Extraction (pdftotext)</strong>
   </td>
   <td><strong>Modern Agentic Parsing (Docling)</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Core Technology Mechanism</strong>
   </td>
   <td>Direct byte-stream character mapping.<sup>4</sup>
   </td>
   <td>Deep neural networks (DocLayNet, TableFormer).<sup>21</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Layout and Structure Fidelity</strong>
   </td>
   <td>Extremely low; relies on physical whitespace inference.<sup>3</sup>
   </td>
   <td>Exceptionally high; semantic understanding of headers, body, and margins.<sup>22</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Handling of Multicolumn and Tables</strong>
   </td>
   <td>High failure rate; structural collapse into continuous strings.<sup>19</sup>
   </td>
   <td>Preserves complex logical grids and matrix structures seamlessly.<sup>21</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Output Interoperability</strong>
   </td>
   <td>Generates flat, unstructured plaintext files.<sup>18</sup>
   </td>
   <td>Outputs natively into lossless JSON, valid Markdown, and HTML.<sup>22</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Hardware and Agent Integration</strong>
   </td>
   <td>Standalone command-line executable.<sup>29</sup>
   </td>
   <td>Native integration with LlamaIndex, LangChain, and MCP; supports local MLX acceleration.<sup>22</sup>
   </td>
  </tr>
</table>



## Storage Architectures at Scale: Graph Databases vs. JSON Sidecars

As a textual archive scales—incorporating millions of verses, cross-references, liturgical calendar mappings, and theological annotations—the foundational storage architecture becomes the primary bottleneck for both performance and system maintainability. The standard enterprise approach to managing highly interconnected data is the deployment of a dedicated graph database. However, the Orthodox Phronema Archive explicitly diverges from this industry consensus, proposing a lightweight architecture based on a flat-file Markdown repository augmented by domain-sharded JSON sidecars.<sup>2</sup> A rigorous comparison of the mechanical properties of both systems is required to evaluate the viability of this architectural decision.


### The Mechanics and Capabilities of Graph Databases

Graph databases, such as Neo4j, FalkorDB, and Memgraph, are NoSQL database management systems fundamentally engineered upon the mathematical principles of graph theory.<sup>30</sup> Unlike relational database management systems (RDBMS) which store data in rigid, tabular formats (rows and columns) and establish connections through the use of primary and foreign keys, graph databases store the connections themselves as first-class entities.<sup>30</sup>

The primary limitation of a relational database in a highly hyperlinked environment is the "join explosion" problem.<sup>30</sup> As the depth of a query increases—for example, searching for a specific theological motif, mapped to a saint, linked to a specific liturgical day, pointing back to a verse in the Old Testament—the relational database must compute complex, memory-intensive JOIN operations across multiple massive tables.<sup>32</sup>

Graph databases bypass this computational bottleneck through a mechanical design known as "index-free adjacency".<sup>31</sup> In a native graph database, every node (an entity, such as a scripture verse) contains direct physical memory pointers to its adjacent nodes via edges (relationships).<sup>30</sup> Consequently, when a query executes a traversal, the system does not need to scan massive global indexes or compute relational joins; it simply follows the memory pointers from one node to the next.<sup>30</sup> This results in traversal times that remain lightning-fast and mathematically constant, regardless of whether the database contains ten thousand or ten billion total nodes.<sup>31</sup>

To manipulate this data, graph databases utilize highly expressive, declarative query languages such as Cypher or GQL.<sup>33</sup> These languages are designed to visually represent relationships using ASCII-art style syntax, allowing developers to execute incredibly complex pattern-matching algorithms, shortest-path determinations, and recursive algorithmic traversals that would be functionally impossible to write in pure SQL.<sup>33</sup> From a scalability perspective, modern distributed graph databases can partition massive networks across multiple hardware servers, executing traversals in parallel using linear algebra operations across sparse adjacency matrices.<sup>30</sup>


### The Mechanics of the Domain-Sharded JSON Sidecar Approach

Despite the overwhelming query performance of graph databases, the Orthodox Phronema Archive utilizes a fundamentally different strategy. The core scripture substrate is stored as flat Markdown files, while the relationships (the edges of the graph) are isolated and stored in discrete JSON files, sharded by the unique canonical anchor of the verse.<sup>2</sup> For example, the system generates a distinct file located at metadata/anchor_backlinks/GEN.1.1.json to store every external pointer pointing to Genesis 1:1.<sup>2</sup>

To the enterprise software engineer accustomed to high-frequency transactional data, reading and writing to thousands of flat files appears regressive and non-performant.<sup>37</sup> A monolithic flat file is entirely non-scalable; it requires a global system lock for every write operation and massive memory overhead to read.<sup>37</sup> However, the specific data profile of a canonical religious archive changes the calculus entirely, revealing the JSON sidecar strategy to be exceptionally sound.

**1. Data Velocity and the Absence of High Concurrency** Graph databases are optimized for environments featuring massive read/write concurrency and constantly evolving, highly dynamic relationships (e.g., social networks, real-time fraud detection, live recommendation engines).<sup>31</sup> A canonical scripture archive is fundamentally read-heavy and mutation-averse.<sup>2</sup> The foundational nodes (the biblical verses) are entirely immutable. The edges (patristic commentary, liturgical mappings) are curated deliberately over extended periods by authorized agents, rather than generated concurrently by millions of live users. The immense infrastructural overhead of deploying, clustering, and tuning a Neo4j instance is a vast over-engineering of the problem.<sup>38</sup>

**2. Atomicity and Decentralized Version Control** The archive relies on Git as its ultimate source of truth.<sup>2</sup> Git functions as a decentralized, cryptographic database optimized entirely for plain text.<sup>2</sup> By storing backlink data in distinct JSON files, the architecture allows every single alteration to the relationship graph to be version-controlled, diff-able, and mathematically secured by SHA-256 checksums.<sup>2</sup> This satisfies the strategic requirement for "reconstruction-proof provenance." If a graph database were used, the project would have to build a highly complex, proprietary auditing and snapshot layer to replicate the innate historical durability provided freely by Git. Furthermore, moving or renaming a file within a modern operating system is guaranteed to be a fully atomic operation, ensuring data safety without the need for complex database transaction management.<sup>42</sup>

**3. Operating System Indexing as a Pseudo-Database** The key to the proposal’s viability is the concept of "domain-sharding." By fracturing the backlink graph into thousands of tiny, highly specific files (BOOK.CHAPTER.VERSE.json), the system completely sidesteps the file-lock and memory-choke problems of monolithic flat files.<sup>2</sup> More importantly, it repurposes the operating system’s native file system as a highly optimized key-value database.<sup>38</sup> Modern file systems utilize incredibly fast B-tree or Hash-based indexing to locate files. When an agent or user interface needs to retrieve the cross-references for Genesis 1:1, it does not need to parse a database index; the OS file path *is* the index. This results in an O(1) lookup time for direct entity resolution, providing near-instantaneous read access.<sup>38</sup>

**4. Absolute Durability and Platform Independence** The greatest threat to digital humanities and archival projects is technological obsolescence. Graph databases rely on proprietary query languages (Cypher, Gremlin) and require complex, continually updated software runtimes to function.<sup>36</sup> A flat-file JSON and Markdown repository is infinitely portable and perfectly durable.<sup>38</sup> It contains no software dependencies. It can be parsed natively by any programming language, served globally with zero database overhead via Content Delivery Networks (CDNs) or static site generators, and accessed during critical failure states using nothing more than a basic text editor.<sup>38</sup>


<table>
  <tr>
   <td><strong>Architectural Dimension</strong>
   </td>
   <td><strong>Native Graph Database (e.g., Neo4j)</strong>
   </td>
   <td><strong>Domain-Sharded JSON Sidecar + Markdown</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Data Storage Mechanism</strong>
   </td>
   <td>Nodes and edges in a proprietary memory structure.<sup>32</sup>
   </td>
   <td>Human-readable Markdown and machine-readable JSON.<sup>2</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Query Performance (Deep Traversals)</strong>
   </td>
   <td>Exceptional; utilizes index-free adjacency for constant time.<sup>31</sup>
   </td>
   <td>Limited; requires iterating across multiple JSON files.<sup>38</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Query Performance (Direct Node Lookup)</strong>
   </td>
   <td>Fast; requires initial index scan.<sup>30</sup>
   </td>
   <td>Exceptional; relies on O(1) file system path resolution.<sup>38</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Concurrency and Write Velocity</strong>
   </td>
   <td>Fully ACID compliant, supports massive parallel writes.<sup>40</sup>
   </td>
   <td>Poor parallel write capability; relies on Git merge protocols.<sup>2</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Provenance and Version Control</strong>
   </td>
   <td>Requires complex, bespoke snapshot implementation.<sup>43</sup>
   </td>
   <td>Natively supported via complete Git commit history.<sup>2</sup>
   </td>
  </tr>
  <tr>
   <td><strong>Infrastructural Overhead</strong>
   </td>
   <td>High; requires dedicated servers, tuning, and specific query skills.<sup>42</sup>
   </td>
   <td>Zero; relies purely on atomic OS operations and static hosting.<sup>38</sup>
   </td>
  </tr>
</table>


For a project whose explicitly stated goals prioritize immutability, protection against "silent breaks," and absolute architectural permanence over dynamic, real-time read/write scalability, the domain-sharded JSON sidecar is not merely a viable alternative to a graph database—it is the strategically superior choice.


## Digital Humanities Standards and the One-to-Many Liturgical Mapping Problem

One of the most complex challenges in digital archiving is the accurate representation of highly overlapping, non-linear text usage. In religious contexts, this manifests prominently as the "one-to-many liturgical mapping problem".<sup>44</sup>

A liturgical lectionary is fundamentally a complex reading plan designed to sequence specific fragments of scripture across an intricate chronological calendar for communal worship.<sup>45</sup> A lectionary does not progress linearly through a book. Instead, it extracts a fragmented pericope (e.g., Gospel of John 1:1-17), pairs it with a completely separate text (e.g., Psalm 104), and assigns this combination to a specific liturgical feast.<sup>45</sup> The complexity scales exponentially because the calendar itself shifts based on lunar calculations (the Moveable Feasts, dictated by the date of Easter), and different geographical or historical traditions utilize entirely different cycles.<sup>46</sup>

This creates a massive structural conflict. A single canonical verse is read across many different calendar days, and a single calendar day aggregates many non-contiguous verses.<sup>49</sup> Traditional hierarchical data models completely fail to represent this reality because they demand a single structural tree, forcing developers to either illegally overlap data nodes or endlessly duplicate the canonical text.<sup>50</sup> The digital humanities community has developed several comprehensive standards to resolve this friction, most notably the Text Encoding Initiative (TEI), Canonical Text Services (CTS), and the International Image Interoperability Framework (IIIF).


### The Text Encoding Initiative (TEI) and Standoff Markup

The Text Encoding Initiative (TEI) is the universally recognized XML-based standard for the encoding of digital scholarly editions.<sup>41</sup> Because XML demands a strict hierarchy where elements must nest perfectly inside one another without intersecting, the attempt to map a fragmented, overlapping lectionary over a sequentially encoded book of scripture generates the infamous "overlap problem".<sup>50</sup>

TEI resolves the one-to-many problem by utilizing standoff markup and complex pointing mechanisms rather than inline structuring.<sup>50</sup>



* **Milestone Elements:** Encoders inject empty XML tags—such as &lt;milestone>, &lt;pb> (page beginning), or &lt;cb> (column beginning)—directly into the continuous text stream. These elements do not contain text themselves but act as spatial anchors indicating exactly where a specific liturgical reading begins or ends, completely independent of the logical book/chapter hierarchy.<sup>50</sup>
* **Correspondence and Alignment Pointers:** To construct the actual lectionary calendar, TEI utilizes distinct files or separate XML branches that rely on attributes such as target and corresp.<sup>52</sup> Using the &lt;linkGrp> (link group) element, the standard can map a specific feast day to an array of explicit XPath expressions that target the predefined milestones in the core text.<sup>52</sup>
* **Canonical References:** TEI supports the @cRef attribute to allow unique, machine-readable referencing, theoretically enabling semantic web applications and linked open data.<sup>54</sup>

While TEI provides an incredibly robust solution to overlapping hierarchies, its extreme XML verbosity frequently becomes a severe burden.<sup>50</sup> Manipulating TEI documents requires parsing highly complex XPath expressions. Furthermore, creating custom structures to support specific lectionary logic requires the generation of complex ODD (One Document Does it all) specifications, demanding specialized XML processing environments that drastically increase the barrier to entry for content curation.<sup>55</sup>


### Canonical Text Services (CTS) and Hierarchical Namespaces

Canonical Text Services (CTS) approaches the one-to-many problem not through markup syntax, but by formalizing an ironclad citation and retrieval architecture.<sup>54</sup> Developed as part of the broader CITE architecture and implemented in massive corpora like the Homer Multitext project and the Coptic SCRIPTORIUM, CTS treats every text as an "Ordered Hierarchy of Content Objects" (OHCO).<sup>54</sup>

The functional core of CTS is the CTS URN (Uniform Resource Name). A CTS URN strictly identifies a text segment using a descending namespace string. For example, the string urn:cts:greekLit:tlg0012.tlg001:1.26 precisely defines the overarching namespace (greekLit), the author (tlg0012 for Homer), the specific work (tlg001 for the Iliad), and the exact structural citation (Book 1, line 26).<sup>54</sup>

To solve the complex mapping of liturgical variations—such as the discrepancy between the Hebrew numbering of the Psalms and the Septuagint numbering, where a single psalm might be split or combined depending on the tradition—CTS integrates a variation of the Functional Requirements for Bibliographic Records (FRBR) model.<sup>54</sup> This model clearly distinguishes between the abstract conceptual "Work" and its specific physical "Manifestation" or "Version".<sup>54</sup> Thus, the URN allows a purely semantic numbering system to map dynamically across multiple, structurally different historical manuscripts.<sup>54</sup>

The primary deficiency of the CTS approach is its heavy infrastructural dependency.<sup>54</sup> Utilizing CTS URNs requires standing up and continuously maintaining an active CTS API server capable of receiving the URN request, parsing the algorithm, executing the correct substring extraction against a backend database or XML corpus, and returning the requested passage.<sup>54</sup> For decentralized, static, or offline-first archives, managing an API endpoint introduces unwanted points of failure and operational overhead.<sup>54</sup>


### International Image Interoperability Framework (IIIF)

While TEI and CTS govern the semantic logic of textual relationships, the International Image Interoperability Framework (IIIF) provides the global standard for mapping relationships onto high-resolution visual surrogates (manuscript imagery).<sup>59</sup> IIIF relies on an advanced Presentation API generating JSON-LD manifests.<sup>61</sup>

In addressing the one-to-many problem, IIIF employs an abstract geometric concept known as a "Canvas".<sup>62</sup> An annotation—such as a transcribed fragment of a lectionary reading—does not simply point to a text file; it targets a highly specific spatial coordinate (a bounding box defined by X/Y parameters) on the Canvas.<sup>53</sup> Consequently, a single digital Canvas can simultaneously host thousands of different annotations generated by diverse global lectionary projects. Conversely, a single lectionary annotation can seamlessly target and aggregate multiple Canvases derived from entirely different physical manuscripts housed in distinct repositories worldwide.<sup>60</sup> While IIIF is unparalleled for visual spatial mapping, it is fundamentally an image delivery standard and must be paired with TEI or CTS to govern deep semantic cross-referencing.<sup>53</sup>


### Evaluating the Efficacy of the Domain-Sharded Backlink Proposal

The Orthodox Phronema Archive’s reliance on domain-sharded JSON sidecars (metadata/anchor_backlinks/BOOK.CHAPTER.VERSE.json) alongside deterministic Markdown syntax (]) represents a deliberate, calculated divergence from the monolithic standards of TEI and CTS.<sup>2</sup> An analysis of this architecture demonstrates that it is not merely sound; it is a highly optimized mechanism for solving the one-to-many mapping problem within the specific constraints of the project.



1. **Divergence from TEI Complexity:** Rather than utilizing standoff XML markup and complex &lt;linkGrp> XPath pointers that are computationally heavy and difficult for humans to read, the archive utilizes simple, frozen Markdown syntax.<sup>2</sup> While this sacrifices the microscopic inline semantic tagging capabilities of TEI, it achieves absolute human-readability and ensures seamless interoperability with modern knowledge-base tools (like Obsidian), drastically lowering the barrier for scholarly curation.<sup>2</sup>
2. **Divergence from CTS API Dependency:** Instead of requiring a live CTS server to parse URN algorithms and resolve text arrays, the archive utilizes the native operating system file path as the resolver.<sup>2</sup> The canonical anchor GEN.1:1 maps directly and deterministically to the exact location of the file metadata/anchor_backlinks/GEN.1.1.json.<sup>2</sup> This guarantees O(1) resolution speed without any external software dependencies or API maintenance.<sup>38</sup>
3. **Solving the Overlap Problem:** The JSON sidecar flawlessly handles the many-to-many constraints of a liturgical calendar. Because the backlink arrays for every verse are isolated in their own discrete JSON files, the backlink generator (slated for Phase 3) can easily populate GEN.1.1.json with an array of pointers representing every single lectionary day, theological commentary, or patristic homily that references that specific verse.<sup>2</sup> Because these sidecars are completely separated from the canonical Markdown files, the system allows the lectionary logic to be endlessly updated, appended, or recalculated without ever touching, modifying, or risking the integrity of the immutable scripture substrate.<sup>2</sup>

The decision to deliberately diverge from heavy digital humanities standards is highly defensible and strategically advantageous. Standards like TEI and CTS were engineered for massive, multi-institutional consortia attempting to unify disparate global libraries and provide deeply encoded critical editions featuring high variability.<sup>57</sup> The Orthodox Phronema Archive, conversely, operates as a focused, bounded graph rooted strictly in a single canonical source (the Orthodox Study Bible).<sup>2</sup> By substituting complex XML environments and fragile API servers with a strictly enforced directory structure, deterministic Markdown syntax, and atomically sharded JSON files, the project achieves comparable relational density while vastly improving the durability, offline usability, and mathematical auditability of the archive.


## Synthesis and Strategic Conclusions

The preservation and semantic structuring of historical and religious textual corpora are undergoing a profound technological transformation. The transition toward agentic document parsing pipelines, spearheaded by advanced open-source frameworks like IBM's Docling, has finally resolved the long-standing mechanical failures associated with legacy heuristic extraction tools. The ability of these modern systems to autonomously verify layout structures, preserve complex tables, and map documents into mathematically expressive data structures enables a level of archival fidelity that was previously unattainable.

Simultaneously, the architectural philosophy governing how these structured textual graphs are stored and interconnected is evolving. While enterprise graph databases provide unparalleled capabilities for executing deep, complex traversals across rapidly mutating datasets, their implementation introduces significant infrastructural overhead, operational fragility, and proprietary lock-in. For digital humanities projects focused on the long-term preservation of immutable canonical texts, such overhead is counterproductive.

The architectural framework defined within the Orthodox Phronema Archive represents a highly optimized, pragmatically decentralized approach to digital preservation. By anchoring its data in a flat-file Markdown repository secured by the cryptographic immutability of Git, the project guarantees absolute provenance. Its deployment of a domain-sharded JSON sidecar infrastructure for managing the complex, bidirectional linkages of the theological graph effectively nullifies the need for relational databases. Furthermore, this approach elegantly solves the notoriously complex one-to-many liturgical mapping problem by utilizing the host operating system's native file path logic as a highly performant, globally unique identifier system. In deliberately diverging from the heavy, API-dependent constraints of legacy digital humanities standards like TEI and CTS, the architecture establishes a robust, offline-capable, and future-proof paradigm for the preservation of complex textual relationships.


#### Works cited



1. github.com, accessed March 10, 2026, [https://github.com/ShanesNotes/orthodoxphronema](https://github.com/ShanesNotes/orthodoxphronema)
2. PROJECT-KNOWLEDGE-STRATEGIC.md
3. CarpetFuzz: Automatic Program Option Constraint Extraction from Documentation for Fuzzing - USENIX, accessed March 10, 2026, [https://www.usenix.org/system/files/sec23fall-prepub-467-wang-dawei.pdf](https://www.usenix.org/system/files/sec23fall-prepub-467-wang-dawei.pdf)
4. PDFDataExtractor: A Tool for Reading Scientific Text and Interpreting Metadata from the Typeset Literature in the Portable Document Format | Journal of Chemical Information and Modeling - ACS Publications, accessed March 10, 2026, [https://pubs.acs.org/doi/10.1021/acs.jcim.1c01198](https://pubs.acs.org/doi/10.1021/acs.jcim.1c01198)
5. The 14th International Joint Conference on Natural Language Processing & The 4th Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics - ACL Anthology, accessed March 10, 2026, [https://aclanthology.org/events/ijcnlp-2025/](https://aclanthology.org/events/ijcnlp-2025/)
6. Agentic Document Extraction: How AI is Learning to Read, Reason, and Act on Complex Files - Medium, accessed March 10, 2026, [https://medium.com/intelligent-document-insights/agentic-document-extraction-3dd95e87dbc2](https://medium.com/intelligent-document-insights/agentic-document-extraction-3dd95e87dbc2)
7. A matter of choice: People and possibilities in the age of AI - Human Development Reports, accessed March 10, 2026, [https://hdr.undp.org/system/files/documents/global-report-document/hdr2025reporten.pdf](https://hdr.undp.org/system/files/documents/global-report-document/hdr2025reporten.pdf)
8. From LLM Reasoning to Autonomous AI Agents: A Comprehensive Review - ResearchGate, accessed March 10, 2026, [https://www.researchgate.net/publication/391246469_From_LLM_Reasoning_to_Autonomous_AI_Agents_A_Comprehensive_Review](https://www.researchgate.net/publication/391246469_From_LLM_Reasoning_to_Autonomous_AI_Agents_A_Comprehensive_Review)
9. Gerold Schneider - ACL Anthology, accessed March 10, 2026, [https://aclanthology.org/people/gerold-schneider/](https://aclanthology.org/people/gerold-schneider/)
10. Other Workshops and Events (2025) - ACL Anthology, accessed March 10, 2026, [https://aclanthology.org/events/ws-2025/](https://aclanthology.org/events/ws-2025/)
11. Aman's AI Journal • Primers • Retrieval Augmented Generation, accessed March 10, 2026, [https://aman.ai/primers/ai/RAG/](https://aman.ai/primers/ai/RAG/)
12. Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: System Demonstrations - ACL Anthology, accessed March 10, 2026, [https://aclanthology.org/volumes/2025.emnlp-demos/](https://aclanthology.org/volumes/2025.emnlp-demos/)
13. AgenticIE: An Adaptive Agent for Information Extraction from Complex Regulatory Documents - arXiv.org, accessed March 10, 2026, [https://arxiv.org/html/2509.11773v2](https://arxiv.org/html/2509.11773v2)
14. Scaling Reproducibility: An AI-Assisted Workflow for Large-Scale ReanalysisThe authors used Claude Code and ChatGPT as research and writing assistants in preparing this manuscript. All interpretations, conclusions, and any errors remain solely the responsibility of the authors. - arXiv.org, accessed March 10, 2026, [https://arxiv.org/html/2602.16733](https://arxiv.org/html/2602.16733)
15. Scaling Reproducibility: An AI-Assisted Workflow for Large-Scale Reanalysis - OSF, accessed March 10, 2026, [https://osf.io/download/ru5fa/](https://osf.io/download/ru5fa/)
16. PhantomLint: Principled Detection of Hidden LLM Prompts in Structured Documents - arXiv.org, accessed March 10, 2026, [https://arxiv.org/html/2508.17884v1](https://arxiv.org/html/2508.17884v1)
17. arXiv:2108.05289v1 [cs.CL] 11 Aug 2021, accessed March 10, 2026, [https://arxiv.org/pdf/2108.05289](https://arxiv.org/pdf/2108.05289)
18. Creating a searchable knowledge-base from several PDF files - DEV Community, accessed March 10, 2026, [https://dev.to/surgbc/creating-a-searchable-knowledge-base-from-several-pdf-files-4deh](https://dev.to/surgbc/creating-a-searchable-knowledge-base-from-several-pdf-files-4deh)
19. Programmatically Extract PDF Tables - Stack Overflow, accessed March 10, 2026, [https://stackoverflow.com/questions/3424588/programmatically-extract-pdf-tables](https://stackoverflow.com/questions/3424588/programmatically-extract-pdf-tables)
20. pdftotext not outputting hebrew characters - linux - Server Fault, accessed March 10, 2026, [https://serverfault.com/questions/145256/pdftotext-not-outputting-hebrew-characters](https://serverfault.com/questions/145256/pdftotext-not-outputting-hebrew-characters)
21. Docling: An Efficient Open-Source Toolkit for AI-driven Document Conversion - arXiv, accessed March 10, 2026, [https://arxiv.org/html/2501.17887v1](https://arxiv.org/html/2501.17887v1)
22. GitHub - docling-project/docling: Get your documents ready for gen AI, accessed March 10, 2026, [https://github.com/docling-project/docling](https://github.com/docling-project/docling)
23. Documentation - Docling - GitHub Pages, accessed March 10, 2026, [https://docling-project.github.io/docling/](https://docling-project.github.io/docling/)
24. Introducing Kreuzberg: A Simple, Modern Library for PDF and Document Text Extraction in Python - Reddit, accessed March 10, 2026, [https://www.reddit.com/r/Python/comments/1if3axy/introducing_kreuzberg_a_simple_modern_library_for/](https://www.reddit.com/r/Python/comments/1if3axy/introducing_kreuzberg_a_simple_modern_library_for/)
25. hcmus-project-collection/sanghagpt - GitHub, accessed March 10, 2026, [https://github.com/hcmus-project-collection/sanghagpt](https://github.com/hcmus-project-collection/sanghagpt)
26. mcp-otzaria-server - A Jewish text MCP search server supporting functions such as full-text search - AIBase, accessed March 10, 2026, [https://mcp.aibase.com/server/1916343966200733697](https://mcp.aibase.com/server/1916343966200733697)
27. awesome-mcp-servers/docs/knowledge-management--memory.md at main - GitHub, accessed March 10, 2026, [https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/knowledge-management--memory.md](https://github.com/TensorBlock/awesome-mcp-servers/blob/main/docs/knowledge-management--memory.md)
28. GitHub - Future-House/paper-qa: High accuracy RAG for answering questions from scientific documents with citations, accessed March 10, 2026, [https://github.com/Future-House/paper-qa](https://github.com/Future-House/paper-qa)
29. Some Epstein file redactions are being undone with hacks. Un-redacted text from released documents began circulating on social media on Monday evening : r/technology - Reddit, accessed March 10, 2026, [https://www.reddit.com/r/technology/comments/1pu42mc/some_epstein_file_redactions_are_being_undone/](https://www.reddit.com/r/technology/comments/1pu42mc/some_epstein_file_redactions_are_being_undone/)
30. Graph Databases: A Technical Guide to Modern Data Relationships - FalkorDB, accessed March 10, 2026, [https://www.falkordb.com/blog/graph-database-guide/](https://www.falkordb.com/blog/graph-database-guide/)
31. Graph Database Vs. Relational Database: Which One Wins? - G2, accessed March 10, 2026, [https://www.g2.com/articles/graph-database-vs-relational-database](https://www.g2.com/articles/graph-database-vs-relational-database)
32. Graph vs Relational Databases - Difference Between Databases - Amazon AWS, accessed March 10, 2026, [https://aws.amazon.com/compare/the-difference-between-graph-and-relational-database/](https://aws.amazon.com/compare/the-difference-between-graph-and-relational-database/)
33. Compare Graph and Relational Databases - Microsoft Fabric, accessed March 10, 2026, [https://learn.microsoft.com/en-us/fabric/graph/graph-relational-databases](https://learn.microsoft.com/en-us/fabric/graph/graph-relational-databases)
34. Native vs. Non-Native Graph Database Architecture & Technology - Neo4j, accessed March 10, 2026, [https://neo4j.com/blog/cypher-and-gql/native-vs-non-native-graph-technology/](https://neo4j.com/blog/cypher-and-gql/native-vs-non-native-graph-technology/)
35. Graph Databases vs. Relational Databases | by Rohin Daswani - Medium, accessed March 10, 2026, [https://medium.com/@rohindaswani/graph-databases-vs-relational-databases-8d268ae77570](https://medium.com/@rohindaswani/graph-databases-vs-relational-databases-8d268ae77570)
36. Graph Databases are not worth it - Reddit, accessed March 10, 2026, [https://www.reddit.com/r/Database/comments/1hj71u0/graph_databases_are_not_worth_it/](https://www.reddit.com/r/Database/comments/1hj71u0/graph_databases_are_not_worth_it/)
37. JSON Flat file vs DB querying - Stack Overflow, accessed March 10, 2026, [https://stackoverflow.com/questions/30247663/json-flat-file-vs-db-querying](https://stackoverflow.com/questions/30247663/json-flat-file-vs-db-querying)
38. When should I consider a database instead of storing a single JSON file? : r/node - Reddit, accessed March 10, 2026, [https://www.reddit.com/r/node/comments/dfmrlj/when_should_i_consider_a_database_instead_of/](https://www.reddit.com/r/node/comments/dfmrlj/when_should_i_consider_a_database_instead_of/)
39. Using a JSON file as a database returns data faster then a dedicated Mysql server? - Reddit, accessed March 10, 2026, [https://www.reddit.com/r/node/comments/5ms5jz/using_a_json_file_as_a_database_returns_data/](https://www.reddit.com/r/node/comments/5ms5jz/using_a_json_file_as_a_database_returns_data/)
40. Performance Comparison of Graph Database and Relational Database - ResearchGate, accessed March 10, 2026, [https://www.researchgate.net/publication/370751317_Performance_Comparison_of_Graph_Database_and_Relational_Database](https://www.researchgate.net/publication/370751317_Performance_Comparison_of_Graph_Database_and_Relational_Database)
41. 3 The Promise and Challenges of Digital Humanities for the Study of, accessed March 10, 2026, [https://brill.com/display/book/9789004515116/BP000003.xml](https://brill.com/display/book/9789004515116/BP000003.xml)
42. Using flat files vs database/API as a transport between a frontend and backend, accessed March 10, 2026, [https://softwareengineering.stackexchange.com/questions/313153/using-flat-files-vs-database-api-as-a-transport-between-a-frontend-and-backend](https://softwareengineering.stackexchange.com/questions/313153/using-flat-files-vs-database-api-as-a-transport-between-a-frontend-and-backend)
43. Database vs Flat Text File: What are some technical reasons for choosing one over another when performance isn't an issue? - Stack Overflow, accessed March 10, 2026, [https://stackoverflow.com/questions/1499239/database-vs-flat-text-file-what-are-some-technical-reasons-for-choosing-one-ove](https://stackoverflow.com/questions/1499239/database-vs-flat-text-file-what-are-some-technical-reasons-for-choosing-one-ove)
44. Abstracts of Papers - Qucosa - Leipzig, accessed March 10, 2026, [https://ul.qucosa.de/api/qucosa%3A14648/attachment/ATT-3/](https://ul.qucosa.de/api/qucosa%3A14648/attachment/ATT-3/)
45. What is a "Lectionary" - Reading Scripture Together - Alexander Gregory Thomas, accessed March 10, 2026, [https://www.alexandergregorythomas.com/articles/lectionary](https://www.alexandergregorythomas.com/articles/lectionary)
46. Overview of the Lectionary and Liturgical Seasons - Catholic Resources, accessed March 10, 2026, [https://catholic-resources.org/Lectionary/Overview.htm](https://catholic-resources.org/Lectionary/Overview.htm)
47. Explaining the lectionary for readers - Catholicireland.net, accessed March 10, 2026, [https://www.catholicireland.net/explaining-the-lectionary-for-readers/](https://www.catholicireland.net/explaining-the-lectionary-for-readers/)
48. Tables | The Church of England, accessed March 10, 2026, [https://www.churchofengland.org/prayer-and-worship/worship-texts-and-resources/book-common-prayer/tables](https://www.churchofengland.org/prayer-and-worship/worship-texts-and-resources/book-common-prayer/tables)
49. Adamantius 24 (2018) 6-8 1. Contributi 1.1 Sezioni monografiche 1.1.1 The Coptic Book: Codicological Features, Places of Product, accessed March 10, 2026, [https://www.morcelliana.net/img/cms/Adamantius/Adamantius%20sez%20monografica%20Buzi%202018.pdf](https://www.morcelliana.net/img/cms/Adamantius/Adamantius%20sez%20monografica%20Buzi%202018.pdf)
50. 4.1.4.3 Text Encoding Initiative and Transcription Formats - Brill, accessed March 10, 2026, [https://referenceworks.brill.com/display/entries/THBO/COM-323619.xml?language=en](https://referenceworks.brill.com/display/entries/THBO/COM-323619.xml?language=en)
51. Balisage Paper: Serving IIIF and DTS APIs specifications from TEI data via XQuery with support from a SPARQL Endpoint, accessed March 10, 2026, [https://www.balisage.net/Proceedings/vol26/html/Liuzzo01/BalisageVol26-Liuzzo01.html](https://www.balisage.net/Proceedings/vol26/html/Liuzzo01/BalisageVol26-Liuzzo01.html)
52. 17 Linking, Segmentation, and Alignment - The TEI Guidelines - Text Encoding Initiative, accessed March 10, 2026, [https://tei-c.org/release/doc/tei-p5-doc/en/html/SA.html](https://tei-c.org/release/doc/tei-p5-doc/en/html/SA.html)
53. 12 Representation of Primary Sources - The TEI Guidelines - Text Encoding Initiative, accessed March 10, 2026, [https://www.tei-c.org/release/doc/tei-p5-doc/en/html/PH.html](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/PH.html)
54. Canonical References in Electronic Texts: Rationale and Best Practices - DHQ Static, accessed March 10, 2026, [https://dhq-static.digitalhumanities.org/pdf/000181.pdf](https://dhq-static.digitalhumanities.org/pdf/000181.pdf)
55. 23 Documentation Elements - The TEI Guidelines - Text Encoding Initiative, accessed March 10, 2026, [https://www.tei-c.org/release/doc/tei-p5-doc/en/html/TD.html](https://www.tei-c.org/release/doc/tei-p5-doc/en/html/TD.html)
56. White Paper Report - Coptic SCRIPTORIUM, accessed March 10, 2026, [https://copticscriptorium.org/download/Coptic-SCRIPTORIUM-white-paper-2016-NEH-PW-51672-14.pdf](https://copticscriptorium.org/download/Coptic-SCRIPTORIUM-white-paper-2016-NEH-PW-51672-14.pdf)
57. Digital Papyrology III - OAPEN, accessed March 10, 2026, [https://library.oapen.org/bitstream/handle/20.500.12657/98796/9783111070162.pdf?sequence=1&isAllowed=y](https://library.oapen.org/bitstream/handle/20.500.12657/98796/9783111070162.pdf?sequence=1&isAllowed=y)
58. What Is a CTS URN? » Perseus Digital Library Updates - Tufts University, accessed March 10, 2026, [https://sites.tufts.edu/perseusupdates/2021/01/05/what-is-a-cts-urn/](https://sites.tufts.edu/perseusupdates/2021/01/05/what-is-a-cts-urn/)
59. Home — IIIF | International Image Interoperability Framework, accessed March 10, 2026, [https://iiif.io/](https://iiif.io/)
60. International Image Interoperability Framework (IIIF) - The Jubilees Palimpsest Project, accessed March 10, 2026, [https://jubilees.stmarytx.edu/2019/brill-thb-iiif.html](https://jubilees.stmarytx.edu/2019/brill-thb-iiif.html)
61. IIIF Metadata API, accessed March 10, 2026, [https://iiif.io/api/metadata/0.9/](https://iiif.io/api/metadata/0.9/)
62. manuscript cultures - Universität Hamburg, accessed March 10, 2026, [https://fiona.uni-hamburg.de/21507602/manuscript-cultures-07.pdf](https://fiona.uni-hamburg.de/21507602/manuscript-cultures-07.pdf)
63. Integrating IIIF images into Digital Humanities databases: A step-by-step workflow proposal1 - Revistas científicas UNED, accessed March 10, 2026, [https://revistas.uned.es/index.php/RHD/article/download/43954/33242](https://revistas.uned.es/index.php/RHD/article/download/43954/33242)
64. Canonical Text Services in CLARIN - Reaching out to the Digital Classics and beyond, accessed March 10, 2026, [https://www.clarin.eu/sites/default/files/tiepmar-etal-CLARIN2016_paper_3.pdf](https://www.clarin.eu/sites/default/files/tiepmar-etal-CLARIN2016_paper_3.pdf)
