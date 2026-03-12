"""
canon_purity_fixer.py — Global cleanup of OCR residue and non-standard syntax in canon/.
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent
CANON_DIR = REPO_ROOT / "canon" / "OT"

# Exhaustive kerning splits and OCR artifacts dictionary
PURITY_MAP = [
    (r"\bhtness\b", "brightness"),
    (r"\blov es\b", "loves"),
    (r"\bgav e\b", "gave"),
    (r"\bm e\b", "me"),
    (r"\ba t\b", "at"),
    (r"\by our\b", "your"),
    (r"\by ou\b", "you"),
    (r"\bm y\b", "my"),
    (r"\bbelov ed\b", "beloved"),
    (r"\bturtledov es\b", "turtledoves"),
    (r"\bsilv er\b", "silver"),
    (r"\bkenard\b", "spikenard"),
    (r"\bikenard\b", "spikenard"),
    (r"\bdov es\b", "doves"),
    (r"\blov ely\b", "lovely"),
    (r"\bhav e\b", "have"),
    (r"\blov e\b", "love"),
    (r"\bev il\b", "evil"),
    (r"\bov er\b", "over"),
    (r"\bev er\b", "ever"),
    (r"\bev ery\b", "every"),
    (r"\bnev er\b", "never"),
    (r"\bwiv es\b", "wives"),
    (r"\bliv e\b", "live"),
    (r"\bliv ing\b", "living"),
    (r"\bgiv e\b", "give"),
    (r"\bserv e\b", "serve"),
    (r"\bsav e\b", "save"),
    (r"\breceiv e\b", "receive"),
    (r"\bdeceiv e\b", "deceive"),
    (r"\bresolv e\b", "resolve"),
    (r"\bbeliev e\b", "believe"),
    (r"\bforgiv e\b", "forgive"),
    (r"\bprov e\b", "prove"),
    (r"\bheav en\b", "heaven"),
    (r"\bheav ens\b", "heavens"),
    (r"\bsalv ation\b", "salvation"),
    (r"\bv oice\b", "voice"),
    (r"\bv ain\b", "vain"),
    (r"\bm an\b", "man"),
    (r"\bm any\b", "many"),
    (r"\bm ercy\b", "mercy"),
    (r"\bwhatev er\b", "whatever"),
    (r"\btrem bling\b", "trembling"),
    (r"\bstream s\b", "streams"),
    (r"\bheav y\b", "heavy"),
    (r"\bheav ier\b", "heavier"),
    (r"\bhav ing\b", "having"),
    (r"\bcaptiv es\b", "captives"),
    (r"\bcaptiv ity\b", "captivity"),
    (r"\ba way\b", "away"),
    (r"\bm idst\b", "midst"),
    (r"\bm orning\b", "morning"),
    (r"\bdrov e\b", "drove"),
    (r"\briv er\b", "river"),
    (r"\briv ers\b", "rivers"),
    (r"\bdepriv e\b", "deprive"),
    (r"\bm yself\b", "myself"),
    (r"\bheals\b", "heals"),
    (r"\bheal\b", "heal"),
    (r"\btransgression\b", "transgression"),
    (r"\bTRANSGRESSION\b", "TRANSGRESSION"),
    (r"\btransgressions\b", "transgressions"),
    (r"\bhum ble\b", "humble"),
    (r"\bam ong\b", "among"),
    (r"\bgov ern\b", "govern"),
    (r"\bsev en\b", "seven"),
    (r"\baliv e\b", "alive"),
    (r"\bprev ail\b", "prevail"),
    (r"\btrav eled\b", "traveled"),
    (r"\bgiv en\b", "given"),
    (r"\bresolv es\b", "resolves"),
    (r"\bdiv isions\b", "divisions"),
    (r"\bthem selv es\b", "themselves"),
    (r"\bhoov es\b", "hooves"),
    (r"\bdiv iding\b", "dividing"),
    (r"\bpav ed\b", "paved"),
    (r"\bgriev ous\b", "grievous"),
    (r"\bleav e\b", "leave"),
    (r"\breceiv ed\b", "received"),
    (r"\beffectiv e\b", "effective"),
    (r"\bharv est\b", "harvest"),
    (r"\bprov ided\b", "provided"),
    (r"\bprov ision\b", "provision"),
    (r"\bserv ed\b", "served"),
    (r"\bserv es\b", "serves"),
    (r"\blov ed\b", "loved"),
]

AWAY_FIX_VERBS = ["pass", "wither", "driven", "turn", "sent", "melt", "flow", "took", "winnow", "waste", "go", "far", "run"]

def fix_purity(text: str) -> str:
    # 1. Apply generic kerning maps
    for pattern, replacement in PURITY_MAP:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # 2. Contextual "a way" -> "away"
    for verb in AWAY_FIX_VERBS:
        text = re.sub(rf"\b{verb}\s+a\s+way\b", f"{verb} away", text, flags=re.IGNORECASE)
        text = re.sub(rf"\ba\s+way\s+from\b", "away from", text, flags=re.IGNORECASE)

    # 3. Spacing after anchors
    text = re.sub(r'^([A-Z0-9]{3}\.\d+:\d+)([A-Za-z])', r'\1 \2', text, flags=re.MULTILINE)
    
    # 4. Spacing before verse digits leaked into text
    text = re.sub(r'([a-z,])\s+\d+\s+([a-z])', r'\1 \2', text)
    
    # 5. Global 'v [a-z]' split recovery (highly specific to OSB OCR)
    # Target: 'hav e', 'ev er', 'lov e', 'liv e'
    text = re.sub(r'\b([a-z]+[aeiou])v\s+e([a-z]*)\b', r'\1ve\2', text, flags=re.IGNORECASE)

    return text

def process_all_books():
    print("Starting final exhaustive global canon purity cleanup...")
    for file_path in CANON_DIR.glob("*.md"):
        original_text = file_path.read_text(encoding="utf-8")
        cleaned_text = fix_purity(original_text)
        if cleaned_text != original_text:
            file_path.write_text(cleaned_text, encoding="utf-8")
            print(f"    Fixed issues in {file_path.name}")
    print("Purity cleanup complete.")

if __name__ == "__main__":
    process_all_books()
