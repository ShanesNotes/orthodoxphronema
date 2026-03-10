"""
fix_split_words.py — Join words split by Docling column artifacts.

Finds and joins split words like "ov er", "belov ed", "silv er", etc.
Uses the same logic as validate_canon.py V11 check but applies fixes.
"""

import argparse
import re
from pathlib import Path

import sys as _sys; from pathlib import Path as _Path
_R = _Path(__file__).resolve().parent
while _R != _R.parent and not (_R / "pipeline" / "__init__.py").exists(): _R = _R.parent
if str(_R) not in _sys.path: _sys.path.insert(0, str(_R))
from pipeline.common.patterns import KNOWN_SPLIT_JOIN_WORDS

# Suffixes ending in v that are often split
_SPLIT_V_SUFFIXES = r'ov|ev|iv|erv|alv|elv|olv|eav|av|arv|ilv'
RE_SPLIT_WORD = re.compile(rf'(?<=[a-z])({_SPLIT_V_SUFFIXES}) ([a-z])')

RE_LOWER_TOKEN = re.compile(r'\b[a-z]{1,10}\b')

def fix_line(line: str) -> tuple[str, int]:
    fixes = 0
    # Approach 1: Regex suffixes
    # We want to be careful not to create new words that are wrong.
    # But usually "ov er" -> "over" is safe.
    
    # We will only fix if the resulting word is in KNOWN_SPLIT_JOIN_WORDS
    # or if it is a common split pattern.
    
    new_line = line
    
    # Simple replacement for known patterns
    for word in KNOWN_SPLIT_JOIN_WORDS:
        # Find all ways this word could be split (one space)
        for i in range(1, len(word)):
            split_form = word[:i] + " " + word[i:]
            # Only match if it is a whole word split
            pattern = rf'\b{re.escape(split_form)}\b'
            if re.search(pattern, new_line):
                new_line, count = re.subn(pattern, word, new_line)
                fixes += count
                
    # Approach 2: V-suffix regex
    # Handle cases like "lov e" -> "love" even if not in KNOWN list (though it is now)
    def v_joiner(m):
        joined = m.group(1) + m.group(2)
        # Check if joined word is likely correct or if we should be conservative
        # For now, let's be slightly aggressive on V-splits as they are rare in normal text
        return joined

    # Only apply to body part (after anchor)
    anchor_match = re.match(r'^([A-Z0-9]+\.\d+:\d+)\s', new_line)
    if anchor_match:
        anchor = anchor_match.group(1)
        body = new_line[anchor_match.end():]
        body, count = RE_SPLIT_WORD.subn(v_joiner, body)
        if count > 0:
            fixes += count
            new_line = f"{anchor} {body}"

    return new_line, fixes

def process_file(path: Path, in_place: bool = False):
    print(f"Processing {path} ...")
    lines = path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    total_fixes = 0
    
    in_frontmatter = False
    frontmatter_done = False
    
    for line in lines:
        if line.strip() == "---":
            if not frontmatter_done:
                in_frontmatter = not in_frontmatter
                if not in_frontmatter:
                    frontmatter_done = True
            new_lines.append(line)
            continue
            
        if in_frontmatter:
            new_lines.append(line)
            continue
            
        fixed_line, count = fix_line(line)
        new_lines.append(fixed_line)
        total_fixes += count
        
    if total_fixes > 0:
        print(f"  Fixed {total_fixes} split word(s)")
        if in_place:
            path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    else:
        print("  No split words found.")

def main():
    parser = argparse.ArgumentParser(description="Fix split words in staged canon files.")
    parser.add_argument("files", nargs="+", type=Path, help="Staged canon .md files")
    parser.add_argument("--in-place", action="store_true", help="Apply fixes in place")
    args = parser.parse_args()
    
    for f in args.files:
        if f.exists():
            process_file(f, args.in_place)

if __name__ == "__main__":
    main()
