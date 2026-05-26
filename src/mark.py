'''
Mark a problem as reviewed. Updates last_solved to today and sets revisit_in_days.

Usage:
    python mark.py 217
    python mark.py contains-duplicate
    python mark.py "valid anagram"
'''

import os
import re
import sys
from datetime import date

# ── ANSI colours ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "docs"}

RATING_MAP = {
    "e": (90,  "easy    → 90 days"),
    "g": (30,  "good    → 30 days"),
    "h": (7,   "hard    → 7 days"),
    "s": (3,   "struggled → 3 days"),
}


def find_solution_files(root: str) -> list:
    """Walk the repo and return all .py solution files."""
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".py") and filename not in ("revisit.py", "mark.py"):
                files.append(os.path.join(dirpath, filename))
    return files


def normalise(s: str) -> str:
    """Lowercase, strip punctuation, collapse spaces — for fuzzy matching."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_match(query, files):
    """
    Match query against file paths.
    Accepts: problem number ("217"), slug ("contains-duplicate"), or title words ("valid anagram").
    """
    q = normalise(query)

    # Exact number match first
    if q.isdigit():
        for f in files:
            stem = os.path.splitext(os.path.basename(f))[0]
            parts = stem.split("-")
            if parts[0] == q:
                return f
        return None

    # Fuzzy match against normalised filename
    candidates = []
    for f in files:
        stem = normalise(os.path.splitext(os.path.basename(f))[0])
        if q in stem:
            candidates.append(f)

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        # Prefer the one whose stem starts closest to the query
        candidates.sort(key=lambda f: normalise(os.path.splitext(os.path.basename(f))[0]).index(q))
        return candidates[0]
    return None


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def update_metadata(source: str, today_str: str, new_days: int) -> str:
    """Replace last_solved and revisit_in_days in the source, increment times_reviewed."""
    # last_solved
    source = re.sub(
        r'(last_solved\s*=\s*)["\'][\d\-A-Za-z/]+["\']',
        f'last_solved     = "{today_str}"',
        source,
    )
    # revisit_in_days
    source = re.sub(
        r"(revisit_in_days\s*=\s*)\d+",
        f"revisit_in_days = {new_days}",
        source,
    )
    # times_reviewed — increment if present, else leave alone
    def increment(m):
        n = int(m.group(1)) + 1
        return f"times_reviewed  = {n}"
    source = re.sub(r"times_reviewed\s*=\s*(\d+)", increment, source)

    return source


def prompt_rating() -> tuple:
    """Ask the user how the session went and return (days, label)."""
    print(f"\n  How did it go?\n")
    for key, (days, label) in RATING_MAP.items():
        print(f"    [{BOLD}{key}{RESET}]  {label}")
    print()

    while True:
        try:
            raw = input("  → ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n  Aborted.")
            sys.exit(0)

        if raw in RATING_MAP:
            return RATING_MAP[raw]
        print(f"  {GREY}Please enter e, g, h, or s.{RESET}")


def main() -> None:
    if len(sys.argv) < 2:
        print(f"\n  {YELLOW}Usage: python mark.py <problem number or name>{RESET}")
        print(f"  {GREY}Examples:{RESET}")
        print(f"    python mark.py 217")
        print(f"    python mark.py contains-duplicate")
        print(f"    python mark.py \"valid anagram\"\n")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    root  = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "problems"))
    files = find_solution_files(root)
    match = find_match(query, files)

    if match is None:
        print(f"\n  {YELLOW}No match found for: \"{query}\"{RESET}\n")
        sys.exit(1)

    stem  = os.path.splitext(os.path.basename(match))[0]
    parts = stem.split("-")
    if parts[0].isdigit():
        label = f"{int(parts[0])}. {' '.join(parts[1:]).title()}"
    else:
        label = stem.replace("-", " ").title()

    rel = os.path.relpath(match, root)
    print(f"\n  {BOLD}{CYAN}{label}{RESET}")
    print(f"  {GREY}{rel}{RESET}")

    days, rating_label = prompt_rating()

    today_str = date.today().isoformat()
    source    = read_file(match)
    updated   = update_metadata(source, today_str, days)
    write_file(match, updated)

    print(f"\n  {GREEN}✓{RESET}  Marked as solved today ({today_str})  ·  next review in {BOLD}{days} days{RESET}\n")


if __name__ == "__main__":
    main()
