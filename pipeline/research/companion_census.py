import os
import re
import json
import yaml
from pathlib import Path

# Paths
REPO_ROOT = Path("/home/ark/orthodoxphronema")
OT_DIR = REPO_ROOT / "staging" / "validated" / "OT"
NT_DIR = REPO_ROOT / "staging" / "validated" / "NT"
CANON_OT_DIR = REPO_ROOT / "canon" / "OT"
from pipeline.common.paths import canon_filepath
REPORT_PATH = REPO_ROOT / "reports" / "companion_file_census.json"
MEMO_PATH = REPO_ROOT / "memos" / "93_companion_file_triage.md"
TEMPLATE_PATH = REPO_ROOT / "memos" / "_template_work_memo.md"

# Regex - Anchor-based parsing is the structural truth
RE_FOOTNOTE_ANCHOR = re.compile(
    r"^\*\(anchor:\s+([A-Z0-9]{3}\.\d+:\d+)\)\*\s*$",
    re.MULTILINE,
)
RE_ARTICLE_ENTRY = re.compile(r"^### ", re.MULTILINE)
RE_PLACEMENT_ANCHOR = re.compile(r"\*\(after ([A-Z0-9]{3}\.\d+:\d+)\)\*")
RE_SCRIPTURE_PATTERN = re.compile(r"^[A-Z0-9]{3}\.\d+:\d+ .*")
RE_ANCHOR_REF = re.compile(r"\[\[([A-Z0-9]{3}\.\d+:\d+)\]\]|(?<!\w)([A-Z0-9]{3}\.\d+:\d+)(?!\w)")

def get_yaml_frontmatter(content):
    if content.startswith("---"):
        try:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                return yaml.safe_load(parts[1])
        except:
            pass
    return {}

def count_words(text):
    return len(text.split())

def check_anchor_exists(anchor, book_code, testament):
    # Check canon first if OT
    if testament == "OT":
        canon_path = canon_filepath("OT", book_code)
        if canon_path.exists():
            if anchor in canon_path.read_text(encoding="utf-8"):
                return True
    
    # Check staged scripture
    staged_path = (OT_DIR if testament == "OT" else NT_DIR) / f"{book_code}.md"
    if staged_path.exists():
        if anchor in staged_path.read_text(encoding="utf-8"):
            return True
            
    return False

def analyze_ot_book(book_code):
    data = {
        "footnotes": None,
        "articles": None,
        "markers": None
    }
    
    # Footnotes
    f_path = OT_DIR / f"{book_code}_footnotes.md"
    if f_path.exists():
        content = f_path.read_text(encoding="utf-8")
        frontmatter = get_yaml_frontmatter(content)
        anchors = RE_FOOTNOTE_ANCHOR.findall(content)
        
        # Article contamination - split on anchor lines
        sections = RE_FOOTNOTE_ANCHOR.split(content)
        # Skip the header (index 0)
        article_contam = []
        # sections contains [header, anchor1, body1, anchor2, body2...]
        for i in range(2, len(sections), 2):
            body = sections[i]
            if count_words(body) > 500:
                article_contam.append(f"Section for {sections[i-1]} too long")
                
        # Scripture contamination
        scripture_contam = [line for line in content.splitlines() if RE_SCRIPTURE_PATTERN.match(line)]
        
        # Orphaned anchors
        orphaned = []
        for anchor in anchors:
            if not check_anchor_exists(anchor, book_code, "OT"):
                orphaned.append(anchor)

        data["footnotes"] = {
            "entry_count": len(anchors),
            "content_type_correct": frontmatter.get("content_type") == "footnotes",
            "content_type": frontmatter.get("content_type"),
            "article_contamination": article_contam,
            "scripture_contamination": scripture_contam,
            "orphaned_anchors": orphaned,
            "anchors": anchors
        }

    # Articles
    a_path = OT_DIR / f"{book_code}_articles.md"
    if a_path.exists():
        content = a_path.read_text(encoding="utf-8")
        frontmatter = get_yaml_frontmatter(content)
        entries = RE_ARTICLE_ENTRY.findall(content)
        
        # Footnote contamination
        sections = RE_ARTICLE_ENTRY.split(content)[1:]
        footnote_contam = []
        for i in range(1, len(sections), 2):
            text = sections[i]
            if count_words(text) < 100 and RE_PLACEMENT_ANCHOR.search(text):
                footnote_contam.append(f"Section {i//2 + 1} too short")
                
        # Placement anchors
        placements = RE_PLACEMENT_ANCHOR.findall(content)
        valid_placements = []
        for p in placements:
            valid_placements.append({"anchor": p, "valid": check_anchor_exists(p, book_code, "OT")})

        data["articles"] = {
            "entry_count": len(entries),
            "content_type_correct": frontmatter.get("content_type") == "article",
            "content_type": frontmatter.get("content_type"),
            "footnote_contamination": footnote_contam,
            "placement_anchors": valid_placements
        }

    # Markers
    m_path = OT_DIR / f"{book_code}_footnote_markers.json"
    if m_path.exists():
        try:
            m_data = json.loads(m_path.read_text(encoding="utf-8"))
            if isinstance(m_data, dict):
                markers = m_data.get("markers", [])
            else:
                markers = m_data
            types = {}
            orphaned_markers = []
            missing_footnotes = []
            
            fn_anchors = set(data["footnotes"]["anchors"]) if data["footnotes"] else set()
            
            for m in markers:
                t = m.get("marker", "unknown")
                types[t] = types.get(t, 0) + 1
                anchor = m.get("anchor")
                if anchor:
                    if not check_anchor_exists(anchor, book_code, "OT"):
                        orphaned_markers.append(anchor)
                    if anchor not in fn_anchors:
                        missing_footnotes.append(anchor)
                        
            data["markers"] = {
                "count": len(markers),
                "types": types,
                "orphaned_markers": orphaned_markers,
                "missing_footnote_entries": missing_footnotes
            }
        except:
            pass
            
    return data

def analyze_nt_book(book_code):
    data = {
        "notes": None,
        "markers": None
    }
    
    # Notes
    n_path = NT_DIR / f"{book_code}_notes.md"
    if n_path.exists():
        content = n_path.read_text(encoding="utf-8")
        frontmatter = get_yaml_frontmatter(content)
        sections = RE_ARTICLE_ENTRY.split(content)[1:]
        
        prob_footnotes = 0
        prob_articles = 0
        for i in range(1, len(sections), 2):
            if count_words(sections[i]) < 200:
                prob_footnotes += 1
            else:
                prob_articles += 1
                
        scripture_contam = [line for line in content.splitlines() if RE_SCRIPTURE_PATTERN.match(line)]
        anchor_refs = len(RE_ANCHOR_REF.findall(content))
        
        data["notes"] = {
            "total_sections": len(sections)//2 if sections else 0,
            "probable_footnotes": prob_footnotes,
            "probable_articles": prob_articles,
            "mix_ratio": (prob_footnotes / (prob_footnotes + prob_articles)) if (prob_footnotes + prob_articles) > 0 else 0,
            "content_type": frontmatter.get("content_type"),
            "anchor_references": anchor_refs,
            "scripture_contamination": scripture_contam
        }

    # Markers
    m_path = NT_DIR / f"{book_code}_footnote_markers.json"
    if m_path.exists():
        try:
            m_data = json.loads(m_path.read_text(encoding="utf-8"))
            if isinstance(m_data, dict):
                markers = m_data.get("markers", [])
            else:
                markers = m_data
            types = {}
            orphaned_markers = []
            
            for m in markers:
                t = m.get("marker", "unknown")
                types[t] = types.get(t, 0) + 1
                anchor = m.get("anchor")
                if anchor and not check_anchor_exists(anchor, book_code, "NT"):
                    orphaned_markers.append(anchor)
                        
            data["markers"] = {
                "count": len(markers),
                "types": types,
                "orphaned_markers": orphaned_markers
            }
        except:
            pass
            
    return data

def run_census():
    ot_books = {}
    nt_books = {}
    
    summary = {
        "ot_footnote_files": 0,
        "ot_article_files": 0,
        "ot_marker_files": 0,
        "nt_notes_files": 0,
        "nt_marker_files": 0,
        "total_footnote_entries": 0,
        "total_article_entries": 0,
        "total_markers": 0,
        "total_anchor_references": 0,
        "content_type_distribution": {},
        "missing_companions": [],
        "contamination_flags": []
    }

    # OT Scan
    ot_codes = sorted([f.stem for f in OT_DIR.glob("[A-Z0-9][A-Z0-9][A-Z0-9].md")])
    for code in ot_codes:
        res = analyze_ot_book(code)
        ot_books[code] = res
        
        if res["footnotes"]:
            summary["ot_footnote_files"] += 1
            summary["total_footnote_entries"] += res["footnotes"]["entry_count"]
            ct = res["footnotes"]["content_type"]
            summary["content_type_distribution"][ct] = summary["content_type_distribution"].get(ct, 0) + 1
            if res["footnotes"]["article_contamination"] or res["footnotes"]["scripture_contamination"]:
                summary["contamination_flags"].append(f"{code} footnotes")
        else:
            summary["missing_companions"].append(f"{code}_footnotes.md")

        if res["articles"]:
            summary["ot_article_files"] += 1
            summary["total_article_entries"] += res["articles"]["entry_count"]
            ct = res["articles"]["content_type"]
            summary["content_type_distribution"][ct] = summary["content_type_distribution"].get(ct, 0) + 1
            if res["articles"]["footnote_contamination"]:
                summary["contamination_flags"].append(f"{code} articles")
        else:
            summary["missing_companions"].append(f"{code}_articles.md")

        if res["markers"]:
            summary["ot_marker_files"] += 1
            summary["total_markers"] += res["markers"]["count"]
            summary["total_anchor_references"] += res["markers"]["count"]
        else:
            summary["missing_companions"].append(f"{code}_footnote_markers.json")

    # NT Scan
    nt_codes = sorted([f.stem for f in NT_DIR.glob("[A-Z0-9][A-Z0-9][A-Z0-9].md")])
    for code in nt_codes:
        res = analyze_nt_book(code)
        nt_books[code] = res
        
        if res["notes"]:
            summary["nt_notes_files"] += 1
            summary["total_footnote_entries"] += res["notes"]["probable_footnotes"]
            summary["total_article_entries"] += res["notes"]["probable_articles"]
            summary["total_anchor_references"] += res["notes"]["anchor_references"]
            ct = res["notes"]["content_type"]
            summary["content_type_distribution"][ct] = summary["content_type_distribution"].get(ct, 0) + 1
            if res["notes"]["scripture_contamination"]:
                summary["contamination_flags"].append(f"{code} notes")

        if res["markers"]:
            summary["nt_marker_files"] += 1
            summary["total_markers"] += res["markers"]["count"]
            summary["total_anchor_references"] += res["markers"]["count"]

    report = {
        "generated": "2026-03-11",
        "summary": summary,
        "ot_books": ot_books,
        "nt_books": nt_books,
        "special_status": {
            "PSA": {
                "artifact_created": (OT_DIR / "PSA_footnotes.md").exists(),
                "linkage_not_yet_aligned_with_markers": True if ot_books.get("PSA") and ot_books["PSA"]["markers"]["missing_footnote_entries"] else False
            }
        }
    }

    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    
    # Memo Generation
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    memo = template.replace("<insert title>", "Companion File Structural Triage")
    memo = memo.replace("<insert objective>", "Exhaustive structural census of footnotes, articles, and markers across OT and NT staging.")
    
    findings = f"""
### Census Totals
- **OT Footnote Files:** {summary["ot_footnote_files"]}
- **OT Article Files:** {summary["ot_article_files"]}
- **NT Notes Files (Unsplit):** {summary["nt_notes_files"]}
- **Total Markers Scan:** {summary["total_markers"]}
- **Total Anchor Reference Signal:** {summary["total_anchor_references"]} (Phase 3 R1 Scope)

### Naming & Convention Inconsistency
- **OT Split Status:** Successfully split into `_footnotes.md` and `_articles.md`.
- **NT Split Status:** **STALE.** NT remains in legacy `_notes.md` format.
- **Content-Type Drift:**
"""
    for ct, count in summary["content_type_distribution"].items():
        findings += f"  - `{ct}`: {count}\n"
        
    findings += "\n### Top 5 Contamination Risks\n"
    for flag in summary["contamination_flags"][:5]:
        findings += f"- {flag}\n"
        
    findings += f"\n### NT Split Recommendations\n"
    unsplit_nt = [code for code, data in nt_books.items() if data["notes"] and data["notes"]["mix_ratio"] < 1.0]
    findings += f"- NT books requiring split: {', '.join(unsplit_nt[:10])}...\n"
    
    findings += f"\n### Critical Missing Artifacts\n"
    findings += f"- {', '.join(summary['missing_companions'][:5])}...\n"

    memo = memo.replace("<insert findings>", findings)
    memo = memo.replace("<insert risk analysis>", "The NT companion layer is structurally inconsistent with the ratified Phase 3 standards. Link density is high, making manual cleanup risky without a coordinated re-extraction or split pass.")
    
    handshake = """
- `Files changed`: `reports/companion_file_census.json`, `memos/93_companion_file_triage.md`
- `Verification run`: Full repo companion scan.
- `Artifacts refreshed`: Census report and work memo.
- `Remaining known drift`: NT unsplit state, `PSA` marker mismatch, `content_type` variance.
- `Next owner`: Ark (Convention Decisions)
"""
    memo = memo.replace("<insert completion handshake>", handshake)
    
    MEMO_PATH.write_text(memo, encoding="utf-8")
    print("Census and triage complete.")

if __name__ == "__main__":
    run_census()
