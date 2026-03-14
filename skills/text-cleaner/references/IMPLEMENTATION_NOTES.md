# clean.py — Implementation Notes

## Overview

`clean.py` is a generalized, profile-driven multi-pass text extraction cleaner refactored from the canon-proofreader. It detects extraction artifacts (fused words, punctuation spacing, spelling errors) across any text corpus using configurable YAML profiles.

## Architecture

### Core Components

1. **Profile System** (`Profile` dataclass)
   - Load from `profiles/{name}.yaml` or fall back to hardcoded defaults
   - Defines line format, anchor extraction regex, protected zones, allowlists, and error detection parameters
   - Compiles regex patterns for efficiency

2. **Detection Passes**
   - **P1–P5, P7**: Regex-based checks (mostly auto-fixable)
   - **P4, P8**: Fused compounds using aspell-gated detection
   - **P6**: Aspell-based spell check against allowlist
   - **P7**: Unbalanced quote counting (report-only)

3. **Aspell-Gated Detection**
   - The single most effective technique for reducing false positives
   - Only flag a token if:
     1. Full token is NOT recognized by aspell (i.e., it's misspelled)
     2. Remainder (after stripping suspected prefix) IS recognized by aspell
   - This eliminates ~97% of false positives vs. pure regex matching

4. **Output Formats**
   - Human-readable: summary to stderr, detailed report as JSON
   - Machine-readable: `--json` flag for CI/automation pipelines

### File Structure

```
scripts/clean.py              ← Main entry point (this file)
profiles/
  └─ {name}.yaml             ← Profile configurations
references/
  └─ IMPLEMENTATION_NOTES.md  ← You are here
```

## Profile System

### YAML Format

Each profile defines:

```yaml
name: profile-name
description: "Description"

line_format: anchor|plain|numbered   # How to parse lines
anchor_regex: '^...'                  # For extracting anchors
protected_zones:
  - '^---\s*$'                        # Lines never to modify
  - '^#{1,4}\s'

allowlist: schemas/path.txt           # Domain-specific word list

fused_prefixes: [a, b]                # Prefixes to check for fusion
prepositions: [of, in, to, ...]       # For P4 detection
conjunctions: [and, but, ...]         # For P8 detection
false_positives:                      # Real words that look fused
  - dwelled
  - offended
  - ancestor
```

### Important: YAML Boolean Escaping

Some words are YAML reserved keywords and must be quoted:
- `"on"`, `"off"`, `"yes"`, `"no"`, `"true"`, `"false"`, `"null"`

Always quote list items in profiles to avoid parsing errors:

```yaml
prepositions:
  - "of"      ← correct
  - of        ← will parse as boolean False/True
```

### Built-in Profiles

1. **default** — Generic extracted text (plain format, minimal config)
2. **canon** — Biblical scripture (anchored format, biblical names allowlist)

### Creating New Profiles

1. Create `profiles/myprofile.yaml` with appropriate settings
2. Test with `clean.py --file FILE --profile myprofile --dry-run`
3. Iterate on false_positives and allowlist entries
4. Document in SKILL.md when stable

## Usage Examples

### Basic Single File

```bash
# Dry-run with default profile
python3 clean.py --file path/to/file.md --dry-run

# Apply auto-fixable corrections
python3 clean.py --file path/to/file.md --profile canon --apply

# JSON output for scripting
python3 clean.py --file path/to/file.md --profile canon --json
```

### Batch Processing

```bash
# Scan a directory
python3 clean.py --dir /path/to/corpus/ --profile canon --dry-run

# Use predefined scopes
python3 clean.py --scope canon_ot --profile canon --dry-run
python3 clean.py --scope staging_nt --profile canon --json

# Available scopes:
# - canon, canon_ot, canon_nt
# - staging, staging_ot, staging_nt
```

### Selective Passes

```bash
# Regex only (P1–P5, P7, P8)
python3 clean.py --file file.md --pass regex --dry-run

# Spell check only (P6)
python3 clean.py --file file.md --pass spell --dry-run

# Both (default)
python3 clean.py --file file.md --pass all --dry-run
```

## Error Categories

All profiles share the same error taxonomy:

| Code | Category | Auto-Fix? | Example |
|------|----------|-----------|---------|
| P1 | Missing space after punctuation | Yes | `word.Next` → `word. Next` |
| P2 | Space before punctuation | Yes | `word .` → `word.` |
| P3 | Double/repeated words | Yes | `the the` → `the` |
| P4 | Fused preposition+word | No | `ofthe` → `of the` |
| P5 | Multiple consecutive spaces | Yes | `word  next` → `word next` |
| P6 | Spelling (aspell) | No | Unknown words |
| P7 | Unbalanced quotes | No | Mismatched quote counts |
| P8 | Fused conjunction+word | No | `andhe` → `and he` |

## Implementation Details

### Profile Loading

1. Try to load `PROFILES_DIR / f"{name}.yaml"` using PyYAML
2. If YAML library not available or file missing, fall back to hardcoded defaults
3. Merge profile values with defaults to ensure all required fields exist

### Line Processing

Behavior depends on `line_format`:

- **anchor**: Extract anchor and text using `anchor_regex`, process text only
- **plain**: Process entire non-blank line as content (no anchor)
- **numbered**: (Reserved for future use, treated as plain for now)

### Protected Zones

Lines matching any `protected_zones` regex are skipped entirely (never modified or analyzed in detail).

### False Positives

Pre-loaded from profile's `false_positives` list. Prevents flagging real English words that happen to start with a prefix (e.g., "dwelled" shouldn't be flagged as "d welled").

### Allowlist

If `allowlist_path` is specified:
1. Load word list from `{repo_root}/{allowlist_path}`
2. Use during P6 spell check to skip known domain-specific terms
3. If file missing, skip with warning

### Repo Discovery

Script automatically finds repo root by walking up from script location until it finds `pipeline/__init__.py`. This allows the script to work from any working directory.

## Output

### Dry-Run Mode (Default)

- Reports findings to stderr
- Writes JSON report to `reports/text-cleaner/clean_{profile}_{date}.json`
- Does NOT modify any files

### Apply Mode (`--apply`)

- Applies auto-fixable corrections (P1, P2, P3, P5) to source files
- Still writes JSON report
- Still reports to stderr
- Exit code: 0 if no review-needed findings, 1 if findings exist

### JSON Report Format

```json
{
  "generated": "2026-03-14",
  "profile": "canon",
  "format": "json",
  "applied": false,
  "summary": {
    "total_findings": 13,
    "auto_fixable": 0,
    "review_needed": 13,
    "files_checked": 1,
    "lines_checked": 1531,
    "lines_fixed": 0
  },
  "by_category": {
    "P6": 13
  },
  "by_file": {
    "canon/OT/01_GEN.md": 13
  },
  "findings": [
    {
      "file": "canon/OT/01_GEN.md",
      "line": 729,
      "anchor": "GEN.22:24",
      "code": "P6",
      "message": "Unknown word: 'achah'",
      "original": "achah",
      "suggested": "",
      "auto_fixable": false,
      "context": ""
    }
  ]
}
```

## Performance Notes

- **Repo Discovery**: O(1) walk up from script location
- **File Glob**: Uses `Path.glob("*.md")` — fast on modern filesystems
- **Regex**: All regex patterns compiled once at Profile creation
- **Aspell**: Batched to minimize subprocess calls (~1 call per file)
- **Threading**: Currently single-threaded; could parallelize file processing if needed

## Dependencies

- **Standard Library**: `argparse`, `json`, `re`, `subprocess`, `pathlib`, `dataclasses`, etc.
- **Optional**: `yaml` (PyYAML) — falls back to hardcoded defaults if unavailable
- **External**: `aspell` command-line tool (for spell checking)

## Integration with ARK System

This script is designed to work alongside:

- **canon-proofreader** (legacy wrapper, now delegates to text-cleaner)
- **canon-validator** (post-cleaning validation)
- **canon-spell-audit** (domain-specific spelling audits)
- **pipeline/validate/pdf_edge_case_check.py** (edge case detection)

## Troubleshooting

### No findings on known-bad file

- Check profile is loaded: `--profile myprofile` in command
- Check passes are enabled: use `--pass all` (default) or `--pass regex,spell`
- Check file isn't protected: review `protected_zones` in profile
- Test aspell availability: `which aspell`

### False positives overwhelming

- Update profile's `false_positives` list with new safe words
- Expand `allowlist` file with domain-specific terms
- Adjust `fused_prefixes` if some prefixes are causing noise

### YAML parsing errors in profile

- Quote all potentially problematic values: `"on"`, `"off"`, `"yes"`, `"no"`, `"true"`, `"false"`
- Use spaces after list items: `- "value"` not `-"value"`
- Validate YAML: `python3 -c "import yaml; yaml.safe_load(open('profile.yaml'))"`

## Future Enhancements

- Parallel file processing with `concurrent.futures`
- Support for more line formats (markdown, numbered paragraphs)
- Context-aware corrections (e.g., quote balancing within sections)
- Integration with domain-specific language models for smarter fusion detection
- Profile composition (inherit from base profile)

## References

- **SKILL.md**: High-level skill documentation
- **error_patterns.md**: Detailed examples of each error category
- **proofread.py**: Original canon-specific implementation (for reference)
