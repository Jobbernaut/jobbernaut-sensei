'''
Mark a problem as reviewed. Updates last_solved to today and sets revisit_in_days.

Usage:
    sensei mark 217
    sensei mark contains-duplicate
    sensei mark "valid anagram"
    sensei mark 217 --rating g          (non-interactive)
    sensei mark 217 --rating g --no-spread  (disable load smoothing)
'''

import os
import re
import sys
from datetime import date, timedelta

from utils import find_solution_files, find_match, parse_metadata

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

# Per-rating spread window (lo_offset, hi_offset) relative to the base interval.
# The mark command will shift the due date within this window toward the
# least-loaded day.  Keeps SRS integrity while smoothing daily review load.
#
#   "t" (90d): ±8%  →  85 – 100 days
#   "e" (30d): ±10% →  27 –  37 days
#   "g"  (7d): ±14% →   6 –  10 days
#   "h"  (3d): 0–2  →   3 –   5 days  (never early)
#   "s"  (1d): 0–1  →   1 –   2 days  (never early)
SPREAD_WINDOW = {
    "t": (-5, 10),
    "e": (-3,  7),
    "g": (-1,  3),
    "h": ( 0,  2),
    "s": ( 0,  1),
}


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def get_all_due_dates(root: str, exclude_filepath: str = None) -> list:
    """
    Return a list of due dates for all tracked problems.
    Optionally exclude the problem currently being marked so it isn't
    counted against itself.
    """
    files = find_solution_files(root, exclude_files={"revisit.py", "mark.py"})
    due_dates = []
    for f in files:
        if exclude_filepath and os.path.abspath(f) == os.path.abspath(exclude_filepath):
            continue
        meta = parse_metadata(f)
        if meta:
            due = meta["last_solved"] + timedelta(days=meta["revisit_in_days"])
            due_dates.append(due)
    return due_dates


def compute_spread_interval(base_days: int, rating: str, today: date, all_due_dates: list) -> int:
    """
    Within the spread window for this rating, find the day with the fewest
    already-scheduled reviews and return the offset from today.

    Tie-breaking: prefer the earliest day (closest to the base interval).
    Early exit if a day with zero load is found.
    """
    lo, hi = SPREAD_WINDOW[rating]
    base_date = today + timedelta(days=base_days)

    best_day  = base_date
    best_load = sum(1 for d in all_due_dates if d == base_date)

    for offset in range(lo, hi + 1):
        if offset == 0:
            continue  # base_date already evaluated above
        candidate = base_date + timedelta(days=offset)
        if candidate <= today:
            continue
        load = sum(1 for d in all_due_dates if d == candidate)
        if load < best_load:
            best_load = load
            best_day  = candidate
            if best_load == 0:
                break  # can't do better than a fully free day

    return (best_day - today).days


def compute_interval(rating: str) -> int:
    """
    Base SRS interval by rating (before load-smoothing).

    - Trivial:   90 days
    - Easy:      30 days
    - Good:       7 days
    - Hard:       3 days
    - Struggled:  1 day
    """
    return RATING_MAP[rating][0]


def update_metadata(source: str, today_str: str, rating: str, actual_days: int) -> tuple:
    """
    Replace last_solved and revisit_in_days in the solution file source.
    actual_days is the post-spread interval to store.
    """
    # last_solved
    source = re.sub(
        r'(last_solved\s*=\s*)["\'][\d\-A-Za-z/]+["\']',
        f'last_solved     = "{today_str}"',
        source,
    )
    # revisit_in_days
    source = re.sub(
        r"(revisit_in_days\s*=\s*)\d+",
        f"revisit_in_days = {actual_days}",
        source,
    )

    return source, actual_days


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
        print(f"    sensei mark 217 --rating g           (non-interactive)")
        print(f"    sensei mark 217 --rating g --no-spread  (skip smoothing)\n")
        sys.exit(1)

    # ── Flag parsing ──────────────────────────────────────────────────────────
    no_spread = "--no-spread" in args
    args = [a for a in args if a != "--no-spread"]

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

    today     = date.today()
    today_str = today.isoformat()
    source    = read_file(match)
    base_days = compute_interval(rating_key)

    if no_spread:
        actual_days = base_days
        spread_note = ""
    else:
        all_due_dates = get_all_due_dates(root, exclude_filepath=match)
        actual_days   = compute_spread_interval(base_days, rating_key, today, all_due_dates)
        spread_note   = (
            f" {GREY}(spread from {base_days}d){RESET}"
            if actual_days != base_days
            else ""
        )

    updated, days = update_metadata(source, today_str, rating_key, actual_days)
    write_file(match, updated)

    print(f"\n  {GREEN}[OK]{RESET}  Marked as solved today ({today_str}) - next review in {BOLD}{days} days{RESET}{spread_note}\n")


if __name__ == "__main__":
    main()
