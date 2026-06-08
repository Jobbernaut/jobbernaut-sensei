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

from utils import find_solution_files, find_match

# ── ANSI colours ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

RATING_MAP = {
    "t": (90, "trivial   → 90 days"),
    "e": (30, "easy      → 30 days"),
    "g": (7,  "good      → 7 days"),
    "h": (3,  "hard      → 3 days"),
    "s": (1,  "struggled → 1 day"),
}


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def compute_interval(rating: str) -> int:
    """
    Hardcoded SRS intervals by rating.

    - Trivial:   90 days
    - Easy:      30 days
    - Good:       7 days
    - Hard:       3 days
    - Struggled:  1 day
    """
    return RATING_MAP[rating][0]


def update_metadata(source: str, today_str: str, rating: str) -> tuple:
    """
    Replace last_solved and recompute revisit_in_days using hardcoded intervals.
    """
    new_days = compute_interval(rating)

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

    return source, new_days


def prompt_rating() -> tuple:
    """Ask the user how the session went and return (rating_key, label)."""
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
            _, label = RATING_MAP[raw]
            return raw, label
        print(f"  {GREY}Please enter t, e, g, h, or s.{RESET}")


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 1:
        print(f"\n  {YELLOW}Usage: sensei mark <problem number or name>{RESET}")
        print(f"  {GREY}Examples:{RESET}")
        print(f"    sensei mark 217")
        print(f"    sensei mark contains-duplicate")
        print(f"    sensei mark \"valid anagram\"")
        print(f"    sensei mark 217 --rating g    (non-interactive)\n")
        sys.exit(1)

    rating_override = None
    if "--rating" in args:
        idx = args.index("--rating")
        if idx + 1 < len(args):
            rating_override = args[idx + 1].lower()
        args = [a for a in args if a != "--rating" and a not in (rating_override or [])]

    query = " ".join(args)
    root  = os.path.join(os.getcwd(), "problems")

    if not os.path.isdir(root):
        print(f"\n  {YELLOW}problems/ directory not found. Run 'sensei init' first.{RESET}\n")
        sys.exit(1)

    files = find_solution_files(root, exclude_files={"revisit.py", "mark.py"})
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
            print(f"\n  {YELLOW}Invalid rating: {rating_override}. Use t, e, g, h, or s.{RESET}\n")
            sys.exit(1)
        rating_key = rating_override
        _, rating_label = RATING_MAP[rating_override]
    else:
        rating_key, rating_label = prompt_rating()

    today_str = date.today().isoformat()
    source    = read_file(match)
    updated, days = update_metadata(source, today_str, rating_key)
    write_file(match, updated)

    print(f"\n  {GREEN}[OK]{RESET}  Marked as solved today ({today_str}) - next review in {BOLD}{days} days{RESET}\n")


if __name__ == "__main__":
    main()
