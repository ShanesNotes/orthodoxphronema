#!/usr/bin/env python3
"""
Fix anchor_registry.json:
- Remove chapter_verse_counts from 12 books where the plan's data has wrong chapter counts.
- Set correct `chapters` value for those books.
- Leave EXO and all other books with correct cvc intact.
"""
import json

REGISTRY = "/home/ark/orthodoxphronema/schemas/anchor_registry.json"

# Books where plan's cvc array length != canonical chapter count.
# Provide correct chapter count; cvc will be removed (needs correct data before extraction).
CORRECTIONS = {
    "1SA": 31,
    "2SA": 24,
    "TOB": 14,
    "JDT": 16,
    "1MA": 16,
    "2MA": 15,
    "PSA": 151,
    "JOB": 42,
    "SIR": 51,
    "EZK": 48,
    "1CO": 16,
    "EPH": 6,
}

with open(REGISTRY, "r", encoding="utf-8") as f:
    data = json.load(f)

fixed = []
for book in data["books"]:
    code = book["code"]
    if code in CORRECTIONS:
        book["chapters"] = CORRECTIONS[code]
        book.pop("chapter_verse_counts", None)
        fixed.append(code)

with open(REGISTRY, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Fixed {len(fixed)} books: {fixed}")

# Final audit
with open(REGISTRY) as f:
    data2 = json.load(f)
print("\nFinal audit (books WITHOUT chapter_verse_counts):")
missing = [(b["code"], b.get("chapters","?")) for b in data2["books"] if "chapter_verse_counts" not in b]
for code, ch in missing:
    print(f"  {code} (chapters={ch}) — needs correct cvc before extraction")
print(f"\nBooks WITH chapter_verse_counts: {len(data2['books']) - len(missing)}/76")
