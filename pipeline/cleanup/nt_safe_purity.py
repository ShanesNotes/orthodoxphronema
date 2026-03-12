"""
nt_safe_purity.py — Non-structural OCR purity cleanup for NT.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
NT_DIR = REPO_ROOT / "staging" / "validated" / "NT"

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
    (r"\bakingdom\b", "a kingdom"), (r"\bhavelost\b", "have lost"), (r"\bstriveanxiously\b", "strive anxiously"),
]

def fix_line(line: str) -> str:
    # 1. Spacing after anchors (Standardization)
    line = re.sub(r'^([A-Z0-9]{3}\.\d+:\d+)([A-Za-z])', r'\1 \2', line)
    
    # 2. V12 Digit Leakage (Safe prose pattern)
    line = re.sub(r'([a-z,])\s+\d+\s+([a-z])', r'\1 \2', line)
    
    # 3. Purity dictionary
    for pattern, replacement in PURITY_MAP:
        line = re.sub(pattern, replacement, line, flags=re.IGNORECASE)
        
    return line

def process_nt():
    print("Starting safe NT purity cleanup...")
    for file_path in NT_DIR.glob("[A-Z][A-Z0-9][A-Z].md"):
        print(f"  Cleaning {file_path.name}...")
        original_lines = file_path.read_text(encoding="utf-8").splitlines()
        new_lines = [fix_line(l) for l in original_lines]
        
        if new_lines != original_lines:
            file_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
            print(f"    Cleaned {file_path.name}")
    print("Safe NT cleanup complete.")

if __name__ == "__main__":
    process_nt()
