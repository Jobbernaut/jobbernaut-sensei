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
#   "s" ( 1d):  0 →  0  →   1 day        (fixed — no spread)
#   "h" ( 3d): -1 → +1  →   2 –  4 days
#   "g" ( 7d): -2 → +7  →   5 – 14 days
#   "e" (30d): -15 → +15 → 15 – 45 days
#   "t" (90d): -45 → 0  →  45 – 90 days
#
# Together: 1 ∪ 2–4 ∪ 5–14 ∪ 15–45 ∪ 45–90 = full 1–90 coverage, contiguous.
SPREAD_WINDOW = {
    "t": (-45,  0),
    "e": (-15, 15),
    "g": ( -2,  7),
    "h": ( -1,  1),
    "s": (  0,  0),
}

# ── New-problem progression gate ──────────────────────────────────────────────
# A problem that has only been reviewed N times cannot be scheduled beyond the
# cap for that tier, regardless of how well it was solved.  This enforces the
# 1 → 3 → 7 → 30 → full-SRS ladder for new material.
#
#   times_reviewed = 0  (first solve)  → max 1 day
#   times_reviewed = 1                 → max 3 days
#   times_reviewed = 2                 → max 7 days
#   times_reviewed = 3                 → max 30 days
#   times_reviewed >= 4                → no cap (full SRS)
#
# Rating still determines direction: rating `s` on review 3 → 1 day (well under
# the 30-day cap).  Rating `e` on review 0 → capped at 1 day.
PROGRESSION_CAPS = {
    0: 1,
    1: 3,
    2: 7,
    3: 30,
    # 4+: None (no cap)
}


def get_progression_cap(times_reviewed: int) -> int | None:
    """Return the max allowed interval for this review count, or None if uncapped."""
    return PROGRESSION_CAPS.get(times_reviewed)


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def is_load_exempt(meta: dict) -> bool:
    """
    Problems exempt from the daily cap (do not count toward load):
      - Struggled (s-rated): revisit_in_days == 1
      - Brand-new problems:  times_reviewed <= 1
    These can pile onto any day without triggering overload logic.
    """
    return meta.get("revisit_in_days", 0) <= 1 or meta.get("times_reviewed", 0) <= 1


def get_all_due_dates(root: str, exclude_filepath: str = None) -> list:
    """
    Return a list of due dates for all tracked problems that count toward
    the daily load cap.  Exempt problems (s-rated, brand-new) are excluded
    so they never inflate the load count.
    Optionally exclude the problem currently being marked so it isn't
    counted against itself.
    """
    files = find_solution_files(root, exclude_files={"revisit.py", "mark.py"})
    due_dates = []
    for f in files:
        if exclude_filepath and os.path.abspath(f) == os.path.abspath(exclude_filepath):
            continue
        meta = parse_metadata(f)
        if meta and not is_load_exempt(meta):
            due = meta["last_solved"] + timedelta(days=meta["revisit_in_days"])
            due_dates.append(due)
    return due_dates


# Problems reviewed this many times or more are biased toward the LATER end of
# their spread window during tie-breaking.  Low-reviewed problems prefer the
# earliest minimum-load day; high-reviewed problems prefer the latest.
HIGH_REVIEW_THRESHOLD = 5

# ── Smooth-overload escalation ────────────────────────────────────────────────
# If the minimum-load day found within a rating's spread window already has
# this many (or more) reviews, the spread window is considered "impossible"
# and the rating is automatically escalated one tier so the problem lands on
# a quieter day further out.
#
# Escalation chain:  s → h → g → e → t  (each step doubles or more the interval)
#
# Example: rating=s (1 day) but tomorrow has 8 reviews → try h (3 days window).
#          If that window is also packed → try g (7 days), etc.
SMOOTH_OVERLOAD_CAP = 2

RATING_ESCALATION = {
    "s": "h",
    "h": "g",
    "g": "e",
    "e": "t",
    "t": None,   # already at the top tier — no further escalation possible
}


def compute_spread_interval(base_days: int, rating: str, today: date,
                            all_due_dates: list, times_reviewed: int = 0) -> tuple:
    """
    Within the spread window for this rating, find the day with the fewest
    already-scheduled reviews and return (interval_from_today, effective_rating).

    If every candidate day in the window has >= SMOOTH_OVERLOAD_CAP reviews,
    the rating is escalated one tier (s→h→g→e→t) and the search is retried.
    The returned effective_rating reflects any escalation that occurred.

    Tie-breaking is biased by times_reviewed:
      - Low review count  (< HIGH_REVIEW_THRESHOLD): prefer EARLIEST minimum day
      - High review count (>= HIGH_REVIEW_THRESHOLD): prefer LATEST minimum day
        → pushes well-reviewed problems out of clusters, freeing slots for
          problems that truly need frequent review.

    Early exit if a zero-load day is found.
    """
    effective_rating = rating

    while True:
        lo, hi = SPREAD_WINDOW[effective_rating]
        # Recompute base_date from the effective tier's base interval each loop
        tier_base_days = RATING_MAP[effective_rating][0]
        base_date = today + timedelta(days=tier_base_days)

        prefer_late = times_reviewed >= HIGH_REVIEW_THRESHOLD

        # Build candidate list in preference order based on review count
        offsets = range(lo, hi + 1) if not prefer_late else range(hi, lo - 1, -1)

        best_day  = None
        best_load = float("inf")

        for offset in offsets:
            candidate = base_date + timedelta(days=offset)
            if candidate <= today:
                continue
            load = sum(1 for d in all_due_dates if d == candidate)
            if load < best_load:
                best_load = load
                best_day  = candidate
                if best_load == 0:
                    break  # can't do better than a fully free day

        # Fallback: if every candidate was in the past (shouldn't happen normally)
        if best_day is None:
            best_day = base_date

        # Never escalate `s` — it must return tomorrow regardless of load.
        # (If tomorrow is heavy, that's a scheduling problem; but the user
        #  explicitly needs to re-review a struggled problem the next day.)
        if effective_rating == "s":
            break

        # If the best available day is still heavily loaded, escalate one tier
        if best_load >= SMOOTH_OVERLOAD_CAP:
            next_rating = RATING_ESCALATION.get(effective_rating)
            if next_rating is not None:
                effective_rating = next_rating
                continue  # retry with the escalated tier's wider window

        break  # found a reasonable day, or already at the top tier (t)

    return (best_day - today).days, effective_rating


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


def update_metadata(source: str, today_str: str, rating: str, actual_days: int = None,
                    new_times_reviewed: int = None) -> tuple:
    """
    Replace last_solved, revisit_in_days, and times_reviewed in the solution file source.
    actual_days is the post-spread interval to store (defaults to base interval).
    new_times_reviewed is written if the field already exists in source;
    if absent it is inserted after revisit_in_days.
    """
    if actual_days is None:
        actual_days = compute_interval(rating)

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

    if new_times_reviewed is not None:
        if re.search(r"times_reviewed\s*=\s*\d+", source):
            # Field already exists — update it in-place
            source = re.sub(
                r"(times_reviewed\s*=\s*)\d+",
                f"times_reviewed  = {new_times_reviewed}",
                source,
            )
        else:
            # Insert after revisit_in_days line
            source = re.sub(
                r"(revisit_in_days\s*=\s*\d+)",
                f"\\1\ntimes_reviewed  = {new_times_reviewed}",
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

    # Read current times_reviewed (0 for legacy files without the field)
    existing_meta      = parse_metadata(match)
    cur_times_reviewed = existing_meta["times_reviewed"] if existing_meta else 0
    new_times_reviewed = cur_times_reviewed + 1

    if no_spread:
        actual_days    = base_days
        spread_note    = ""
        effective_rating = rating_key
    else:
        all_due_dates = get_all_due_dates(root, exclude_filepath=match)
        actual_days, effective_rating = compute_spread_interval(
            base_days, rating_key, today, all_due_dates,
            times_reviewed=cur_times_reviewed,
        )
        if effective_rating != rating_key:
            # Rating was auto-escalated because every nearby day was overloaded
            _, orig_label = RATING_MAP[rating_key]
            _, esc_label  = RATING_MAP[effective_rating]
            spread_note = (
                f" {YELLOW}(overloaded — escalated {rating_key}→{effective_rating}, "
                f"{actual_days}d){RESET}"
            )
        elif actual_days != base_days:
            spread_note = f" {GREY}(spread from {base_days}d){RESET}"
        else:
            spread_note = ""

    # ── Progression gate ──────────────────────────────────────────────────────
    # New problems must climb the 1→3→7→30→full ladder regardless of rating.
    # This prevents a first-solve rated `e` from jumping to 30 days.
    prog_cap = get_progression_cap(cur_times_reviewed)
    if prog_cap is not None and actual_days > prog_cap:
        capped_note = (
            f" {YELLOW}(capped at {prog_cap}d — review #{cur_times_reviewed + 1}){RESET}"
        )
        actual_days = prog_cap
        spread_note = capped_note  # overwrite spread note; cap takes priority

    updated, days = update_metadata(source, today_str, rating_key, actual_days,
                                    new_times_reviewed=new_times_reviewed)
    write_file(match, updated)

    print(f"\n  {GREEN}[OK]{RESET}  Marked as solved today ({today_str}) - next review in {BOLD}{days} days{RESET}{spread_note}\n")

    # ── Schedule health check ──────────────────────────────────────────────────
    # After each mark, scan for overloaded days (> HEALTH_CAP reviews).
    # If clusters exist, print a one-line warning so the user knows to rebalance.
    HEALTH_CAP = 2
    all_due = get_all_due_dates(root)  # includes the just-marked problem
    from collections import Counter
    load = Counter(all_due)
    hot_days = sorted(d for d, cnt in load.items() if cnt > HEALTH_CAP and d > today)
    if hot_days:
        worst      = max(load[d] for d in hot_days)
        worst_date = max(hot_days, key=lambda d: load[d])
        print(
            f"  {YELLOW}⚠  Schedule health:{RESET} {len(hot_days)} overloaded day(s) "
            f"(peak {BOLD}{worst}{RESET} reviews on {worst_date}). "
            f"Run {BOLD}sensei rebalance{RESET} to spread the load.\n"
        )


if __name__ == "__main__":
    main()

