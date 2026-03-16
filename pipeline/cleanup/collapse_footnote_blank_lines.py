import os
import re
import sys

def clean_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Calculate lines before
    lines_before = content.count('\n') + (1 if content and content[-1] != '\n' else 0)
    
    # Collapse 2+ blank lines (3+ newlines) to 1 blank line (2 newlines)
    # We handle potential whitespace on those "blank" lines.
    # Pattern: a newline, followed by 2 or more occurrences of (optional whitespace + newline)
    new_content = re.sub(r'\n([ \t]*\n){2,}', r'\n\n', content)
    
    # Calculate lines after
    lines_after = new_content.count('\n') + (1 if new_content and new_content[-1] != '\n' else 0)
    lines_removed = lines_before - lines_after
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return lines_before, lines_after, lines_removed

def main():
    files_ot = [os.path.join('study/footnotes/OT', f) for f in os.listdir('study/footnotes/OT') if f.endswith('.md')]
    files_nt = [os.path.join('study/footnotes/NT', f) for f in os.listdir('study/footnotes/NT') if f.endswith('.md')]
    all_files = sorted(files_ot + files_nt)
    
    total_before = 0
    total_after = 0
    total_removed = 0
    
    print(f"{'File':<40} | {'Before':>10} | {'After':>10} | {'Removed':>10}")
    print("-" * 77)
    
    for filepath in all_files:
        before, after, removed = clean_file(filepath)
        print(f"{filepath:<40} | {before:>10} | {after:>10} | {removed:>10}")
        total_before += before
        total_after += after
        total_removed += removed
    
    print("-" * 77)
    print(f"{'TOTAL':<40} | {total_before:>10} | {total_after:>10} | {total_removed:>10}")
    
    print("\nSummary Statistics:")
    print(f"Total files changed: {len(all_files)}")
    print(f"Total lines before: {total_before}")
    print(f"Total lines after: {total_after}")
    print(f"Total blank lines removed: {total_removed}")

if __name__ == '__main__':
    main()
