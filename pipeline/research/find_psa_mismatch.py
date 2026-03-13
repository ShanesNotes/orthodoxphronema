import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PSA_PATH = REPO_ROOT / "staging" / "validated" / "OT" / "PSA.md"
REGISTRY = REPO_ROOT / "schemas" / "anchor_registry.json"

def find_mismatch():
    with open(REGISTRY) as f:
        registry = json.load(f)
    
    psa_meta = next(b for b in registry["books"] if b["code"] == "PSA")
    expected_counts = psa_meta["chapter_verse_counts"]
    
    text = PSA_PATH.read_text(encoding="utf-8")
    verses_by_chapter = {}
    
    for m in re.finditer(r'^PSA\.(\d+):(\d+)', text, re.MULTILINE):
        ch = int(m.group(1))
        v = int(m.group(2))
        verses_by_chapter.setdefault(ch, []).append(v)
    
    for ch_idx, expected_v in enumerate(expected_counts):
        ch_num = ch_idx + 1
        actual_v_list = verses_by_chapter.get(ch_num, [])
        actual_count = len(actual_v_list)
        if actual_count != expected_v:
            print(f"Chapter {ch_num}: expected {expected_v}, got {actual_count} (max verse: {max(actual_v_list) if actual_v_list else 0})")

if __name__ == "__main__":
    find_mismatch()
