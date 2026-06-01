'''
Mark a problem as reviewed. Updates last_solved to today and sets revisit_in_days.

Usage:
    sensei mark 217
    sensei mark contains-duplicate
    sensei mark "valid anagram"
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
    "e": (90,  "easy      → 90 days  (or prev×1.5 after 3+ reviews)"),
    "g": (30,  "good      → 30 days"),
    "h": (7,   "hard      → 7 days   (14 days after 2+ reviews)"),
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


def read_times_reviewed(source: str) -> int:
    """Extract the current times_reviewed value from source, default 0."""
    m = re.search(r"times_reviewed\s*=\s*(\d+)", source)
    return int(m.group(1)) if m else 0


def read_prev_interval(source: str) -> int:
    """Extract the current revisit_in_days value from source, default 0."""
    m = re.search(r"revisit_in_days\s*=\s*(\d+)", source)
    return int(m.group(1)) if m else 0


def compute_interval(rating: str, times_reviewed: int, prev_interval: int) -> int:
    """
    Graduated SRS interval based on rating and history.

    Bootstrap phase (new problems need rapid iteration before entering full SRS):
    - times_reviewed == 0 (first attempt / new problem): 3 days
    - times_reviewed == 1 (first review): 7 days
    - times_reviewed >= 2: full SRS based on rating

    Full SRS intervals:
    - Easy + reviewed 3+ times: previous × 1.5 (cap 180d)
    - Easy: 90 days
    - Good: 30 days
    - Hard + reviewed 2+ times: 14 days
    - Hard: 7 days
    - Struggled: 3 days
    """
    # Bootstrap phase — rating is ignored, memory needs rapid reinforcement
    if times_reviewed == 0:
        return 3
    if times_reviewed == 1:
        return 7

    # Full SRS — times_reviewed >= 2
    if rating == "e":
        if times_reviewed >= 3 and prev_interval > 0:
            return min(int(prev_interval * 1.5), 180)
        return 90
    elif rating == "g":
        return 30
    elif rating == "h":
        if times_reviewed >= 2:
            return 14
        return 7
    else:  # rating == "s" (struggled)
        return 3


def update_metadata(source: str, today_str: str, rating: str) -> str:
    """
    Replace last_solved and recompute revisit_in_days using graduated intervals.
    Increment times_reviewed.
    """
    times_reviewed = read_times_reviewed(source)
    prev_interval  = read_prev_interval(source)
    new_days       = compute_interval(rating, times_reviewed, prev_interval)

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
    # times_reviewed — increment if present, add if not
    if re.search(r"times_reviewed\s*=\s*\d+", source):
        def increment(m):
            n = int(m.group(1)) + 1
            return f"times_reviewed  = {n}"
        source = re.sub(r"times_reviewed\s*=\s*(\d+)", increment, source)
    else:
        # Add times_reviewed = 1 after the last metadata line
        source = re.sub(
            r"(topic_tags\s*=.*?\n)",
            rf"\1times_reviewed  = 1\n",
            source,
        )

    return source, new_days


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
    args = sys.argv[1:]
    if len(args) < 1:
        print(f"\n  {YELLOW}Usage: sensei mark <problem number or name>{RESET}")
        print(f"  {GREY}Examples:{RESET}")
        print(f"    sensei mark 217")
        print(f"    sensei mark contains-duplicate")
        print(f"    sensei mark \"valid anagram\"")
        print(f"    sensei mark 217 --rating e    (non-interactive)\n")
        sys.exit(1)

    rating_override = None
    if "--rating" in args:
        idx = args.index("--rating")
        if idx + 1 < len(args):
            rating_override = args[idx + 1].lower()
        args = [a for a in args if a != "--rating" and a not in (rating_override or [])]

    query = " ".join(args)
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

    if rating_override:
        if rating_override not in RATING_MAP:
            print(f"\n  {YELLOW}Invalid rating: {rating_override}. Use e, g, h, or s.{RESET}\n")
            sys.exit(1)
        rating_key = rating_override
        _, rating_label = RATING_MAP[rating_override]
    else:
        rating_key, rating_label = prompt_rating()

    today_str = date.today().isoformat()
    source    = read_file(match)
    updated, days = update_metadata(source, today_str, rating_key)
    write_file(match, updated)

    print(f"\n  {GREEN}✓{RESET}  Marked as solved today ({today_str})  ·  next review in {BOLD}{days} days{RESET}\n")


if __name__ == "__main__":
    main()
