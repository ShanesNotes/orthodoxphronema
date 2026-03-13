# Structural Drift Evidence Packet (2026-03-12)

This packet summarizes implementation-ready evidence regarding structural drift in promotion gates, parser record types, and the common layer. This is an evidence-packaging artifact for Ark's repair mission.

## Task 1: Promotion Gate Drift Packet

### Missing Gate Enforcement
The `pipeline/promote/promote.py` script has diverged from the composable gates defined in `pipeline/promote/gates.py`. It uses an internal, simplified logic that bypasses several safety checks.

- **Gate D1 (Editorial Candidates):** `gate_editorial` (checking for unresolved editorial candidates) is not called in `promote.py`.
- **Gate D2 (Freshness):** `gate_freshness` (checking if staged text changed since last dossier) is not called.
- **Gate D3 (Field Normalization):** `gate_sidecar_fields` (blocking on 'class' vs 'classification' drift) is not called.
- **Gate D4 (Absorbed Content):** `gate_absorbed_content` (blocking on 'absorbed/fused' keywords in residuals) is not called.
- **Gate D5 (Ratification):** `promote.py` (L183) has a partial implementation that differs from `gates.py`. It allows promotion of unratified sidecars if all entries are non-blocking, whereas `gates.py` (L150) blocks if non-empty.

### Dossier Schema Drift
Tests in `tests/test_promote_gate.py` expect fields in the promotion dossier that are currently missing from the `generate_dossier` implementation in `promote.py`.

- **Missing `allow_incomplete`:** `tests/test_promote_gate.py:510` (`KeyError: 'allow_incomplete'`)
- **Missing `staged_path`:** `tests/test_promote_gate.py:578` (`KeyError: 'staged_path'`)
- **Missing `residuals_path`:** `tests/test_promote_gate.py:595` (`KeyError: 'residuals_path'`)
- **Actual Behavior:** `promote.py:101-133` (`generate_dossier`) only populates `book_code`, `testament`, `timestamp`, `registry_version`, `body_checksum`, `validation`, `residuals_sidecar`, and `decision`.

### Validation Status Drift
- **Mismatch:** `tests/test_promote_gate.py:542` expects `INFO` status for V7 when it is informational, but `promote.py:121` maps all warnings to `WARN` and everything else to `PASS`.
- **Failing Test:** `TestDossierSchema.test_dossier_preserves_warn_and_skip_statuses`.

---

## Task 2: Parser Typed-Record Migration Packet

The `pipeline/parse/osb_extract.py` script is in a state of "half-migration" to typed records. It still attempts dict-style access (`v["key"]`) on `VerseRecord` and `FootnoteMarker` objects, which are now `dataclasses`.

### Verse Record Access (L739-L926)
Dict-style access on `VerseRecord` objects causes `TypeError: 'VerseRecord' object is not subscriptable`.
- **L546:** `return self._anchor(v["chapter"], v["verse"])` -> `v.chapter`, `v.verse`
- **L739:** `merged = self.verses[-1]["text"] + " " + text` -> `self.verses[-1].text`
- **L747:** `popped_anchor = popped["anchor"]` -> `popped.anchor`
- **L755:** `merged, popped["chapter"], self.book_code` -> `popped.chapter`
- **L756:** `start_verse=popped["verse"]` -> `popped.verse`
- **L760:** `self.verses[-1]["text"] = merged` (DataClasses are immutable by default if `frozen=True`, check `types.py`)
- **L852:** `if self.verses and self.verses[-1]["anchor"] == anchor:` -> `self.verses[-1].anchor`
- **L853:** `self.verses[-1]["text"] += " " + vtext`
- **L914:** `chapters.setdefault(v["chapter"], []).append(v)` -> `v.chapter`
- **L926:** `anchor = v["anchor"]` -> `v.anchor`

### Marker Trace Structure (L176, L863, L1039)
Dict-style access on `FootnoteMarker` objects causes `TypeError: string indices must be integers, not 'str'`.
- **L176:** `return tuple(pr["text"]), tuple(pr["footnotes"])` (Accessing `FootnoteMarker` in a pair)
- **L863:** `if fm["anchor"] != anchor` -> `fm.anchor`
- **L1039:** `key = (fm["anchor"], fm["marker"])` -> `fm.anchor`, `fm.marker`

### Failing Tests
- `test_boundary_marker_trace_attaches_to_preceding_verse`
- `test_inline_marker_trace_contains_provenance_fields`
- `test_lc_split_relabels_marker_ownership`
- `test_write_outputs_emits_structured_footnote_marker_sidecar`
- `test_process_element_article_mode_entry_and_exit`
- `test_process_element_text_chapter_advance`
- `test_process_element_column_split_resplits_previous_verse`
- `test_process_element_section_header_emits_heading`

---

## Task 3: Common Layer Contract Census

### Incomplete Refactor / Stale Contracts
- **`pipeline/common/registry.py`:** `page_ranges` returns a `dict` (L51-57), but `tests/test_common.py:74` expects a tuple of two values (`text_range, fn_range`). This is an incomplete refactor of the `page_ranges` signature.
- **`pipeline/common/frontmatter.py`:** Missing `update_frontmatter` function. `tests/test_common.py:144` fails with `ImportError`. `frontmatter.py` only has `update_frontmatter_field`.
- **`pipeline/common/text.py`:** `discover_staged_books` and `discover_staged_paths` have signature mismatches.
  - `tests/test_common.py:239` passes a `list` of codes as the first argument.
  - `text.py` expects `staging_root: Path | None = None`.
  - Recommendation: Update `discover_staged_books` to accept `codes: list[str] | None` as an optional filter, or update the test to use a different utility.

### Accidental Regressions
- **`pipeline/common/patterns.py`:** `KNOWN_SPLIT_JOIN_WORDS` is missing `"overlooked"`.
  - **Failing Test:** `test_known_split_join_words_superset` (L201).
  - **Expected:** Restore `"overlooked"` to the set.

---

## Completion Handshake

- **Files read:**
  - `pipeline/promote/promote.py`
  - `pipeline/promote/gates.py`
  - `tests/test_promote_gate.py`
  - `pipeline/parse/osb_extract.py`
  - `pipeline/common/types.py`
  - `tests/test_verse_split.py`
  - `pipeline/common/registry.py`
  - `pipeline/common/frontmatter.py`
  - `pipeline/common/text.py`
  - `pipeline/common/patterns.py`
  - `tests/test_common.py`
- **Verification run:**
  - `pytest tests/test_promote_gate.py tests/test_verse_split.py tests/test_common.py -q`
  - Result: 27 failed, 55 passed.
- **Artifacts refreshed:**
  - `memos/99_structural_drift_evidence_packet.md` (Created)
- **Remaining known drift:**
  - All items identified in the checklist above.
- **Next owner:** Ark (Architecture/Implementation)
