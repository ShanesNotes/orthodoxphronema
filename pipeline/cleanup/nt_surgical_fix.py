"""
nt_surgical_fix.py — High-confidence structural and purity repair for NT staging.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
NT_DIR = REPO_ROOT / "staging" / "validated" / "NT"

# Purity map from Wisdom/Canon cleanup
PURITY_MAP = [
    (r"\bhav e\b", "have"), (r"\blov e\b", "love"), (r"\bev il\b", "evil"),
    (r"\bov er\b", "over"), (r"\bev er\b", "ever"), (r"\bev ery\b", "every"),
    (r"\bnev er\b", "never"), (r"\bwiv es\b", "wives"), (r"\bliv e\b", "live"),
    (r"\bliv ing\b", "living"), (r"\bgiv e\b", "give"), (r"\bserv e\b", "serve"),
    (r"\bsav e\b", "save"), (r"\breceiv e\b", "receive"), (r"\bdeceiv e\b", "deceive"),
    (r"\bresolv e\b", "resolve"), (r"\bbeliev e\b", "believe"), (r"\bforgiv e\b", "forgive"),
    (r"\bprov e\b", "prove"), (r"\bheav en\b", "heaven"), (r"\bheav ens\b", "heavens"),
    (r"\bsalv ation\b", "salvation"), (r"\bv oice\b", "voice"), (r"\bv ain\b", "vain"),
    (r"\bm y\b", "my"), (r"\by ou\b", "you"), (r"\by our\b", "your"),
    (r"\bm an\b", "man"), (r"\bm many\b", "many"), (r"\bm ercy\b", "mercy"),
    (r"\bwhatev er\b", "whatever"), (r"\btrem bling\b", "trembling"),
    (r"\bheav y\b", "heavy"), (r"\bheav ier\b", "heavier"), (r"\bhav ing\b", "having"),
    (r"\bcaptiv es\b", "captives"), (r"\bcaptiv ity\b", "captivity"),
    (r"\ba way\b", "away"), (r"\bm idst\b", "midst"), (r"\bm orning\b", "morning"),
    (r"\bhum ble\b", "humble"), (r"\bam ong\b", "among"), (r"\bgov ern\b", "govern"),
    (r"\bsev en\b", "seven"), (r"\baliv e\b", "alive"), (r"\bprev ail\b", "prevail"),
    (r"\btrav eled\b", "traveled"), (r"\bgiv en\b", "given"), (r"\bresolv es\b", "resolves"),
]

def fix_content(text: str, book_code: str) -> str:
    lines = text.splitlines()
    new_lines = []
    
    for line in lines:
        # 1. V9 Split: BOOK.CH:V Digit Text -> BOOK.CH:V\nBOOK.CH:V+1 Text
        # Pattern: ^ACT.1:2 3 text...
        # Allow multiple spaces or even a newline-like gap
        match = re.match(rf'^({book_code}\.(\d+):(\d+))\s+(\d+)\s+([A-Z\"\'\(\[].*)', line)
        if not match:
            # Try matching even if there's no space after the anchor
            match = re.match(rf'^({book_code}\.(\d+):(\d+))(\d+)\s+([A-Z\"\'\(\[].*)', line)
            
        if match:
            anchor, ch, v, next_v, body = match.groups()
            if int(next_v) == int(v) + 1:
                new_lines.append(anchor)
                new_lines.append(f"{book_code}.{ch}:{next_v} {body}")
                continue
        
        # 2. V12 Leakage: 'word, 2 text' -> 'word, text'
        line = re.sub(r'([a-z,])\s+\d+\s+([a-z])', r'\1 \2', line)
        
        # 3. Purity dictionary
        for pattern, replacement in PURITY_MAP:
            line = re.sub(pattern, replacement, line, flags=re.IGNORECASE)
            
        new_lines.append(line)
        
    return "\n".join(new_lines) + "\n"

def process_nt():
    print("Starting high-confidence NT surgical recovery...")
    for file_path in NT_DIR.glob("[A-Z][A-Z0-9][A-Z].md"):
        print(f"  Repairing {file_path.name}...")
        original_text = file_path.read_text(encoding="utf-8")
        book_code = file_path.stem
        repaired_text = fix_content(original_text, book_code)
        if repaired_text != original_text:
            file_path.write_text(repaired_text, encoding="utf-8")
            print(f"    Surgically repaired {file_path.name}")
    print("NT cleanup complete.")

if __name__ == "__main__":
    process_nt()
