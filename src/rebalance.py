'''
Rebalance the review schedule by spreading overloaded days.

Finds days where more than --cap reviews are scheduled, then pushes the
most-reviewed problems on those days to the nearest low-load date within
a ±50% window of their current interval.

Most-reviewed problems are displaced first — they have the most stable
memory and are the safest to defer.  Problems that are struggling
(low times_reviewed, short interval) are never touched.

Usage:
    sensei rebalance              # dry run (preview only)
    sensei rebalance --apply      # write changes to disk
    sensei rebalance --cap 4      # treat days with > 4 reviews as overloaded
    sensei rebalance --apply --cap 5

Default cap is controlled by DAILY_LOAD_CAP in src/config.py.
'''

import json
import os
import re
import sys
from datetime import date, timedelta

from utils import find_solution_files, parse_metadata, SKIP_DIRS
from config import DAILY_LOAD_CAP

# ── ANSI colours ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREY   = "\033[90m"
RED    = "\033[91m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

DEFAULT_CAP = DAILY_LOAD_CAP

# Max % the interval can shift in either direction during rebalance.
# e.g. 0.5 → a problem due in 30 days can be moved to 15–45.
REBALANCE_WINDOW_PCT = 0.50

# Minimum absolute spread (days) applied even for short intervals.
REBALANCE_MIN_WINDOW = 2


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def collect_problems(root: str, today: date) -> list:
    """
    Walk root and return every tracked problem as a dict with:
        filepath, label, due_date, interval, times_reviewed, last_solved
    """
    files = find_solution_files(root, exclude_files={"revisit.py", "mark.py"})
    problems = []
    for f in files:
        meta = parse_metadata(f)
        if meta is None:
            continue
        stem  = os.path.splitext(os.path.basename(f))[0]
        parts = stem.split("-")
        if parts[0].isdigit():
            label = f"{int(parts[0])}. {' '.join(parts[1:]).title()}"
        else:
            label = stem.replace("-", " ").title()

        due_date = meta["last_solved"] + timedelta(days=meta["revisit_in_days"])
        problems.append({
            "filepath":      f,
            "label":         label,
            "due_date":      due_date,
            "interval":      meta["revisit_in_days"],
            "times_reviewed": meta["times_reviewed"],
            "last_solved":   meta["last_solved"],
        })
    return problems


def is_load_exempt(p: dict) -> bool:
    """
    Problems exempt from the daily cap:
      - Struggled (s-rated): interval == 1 day
      - Brand-new problems:  times_reviewed <= 1
    These are never displaced and don't count toward load.
    """
    return p["interval"] <= 1 or p["times_reviewed"] <= 1


def build_load_map(problems: list) -> dict:
    """Return {due_date: count} for non-exempt tracked problems."""
    load = {}
    for p in problems:
        if not is_load_exempt(p):
            load[p["due_date"]] = load.get(p["due_date"], 0) + 1
    return load


# Cascade multipliers for the rebalance window.  When the ±50% window is
# packed, we retry with ±100%, then ±200%, then a forward-only unlimited scan.
REBALANCE_WINDOW_MULTIPLIERS = [0.5, 1.0, 2.0]
# Hard forward-scan limit (days) used as the last-resort pass.
REBALANCE_FORWARD_LIMIT = 365


def _search_window(current_due: date, window: int, today: date,
                   load_map: dict, exclude_date: date, cap: int) -> date | None:
    """Search earliest-first within [current_due-window, current_due+window]."""
    lo = max(current_due - timedelta(days=window), today + timedelta(days=1))
    hi = current_due + timedelta(days=window)

    best_day  = None
    best_load = float("inf")

    for offset in range(0, (hi - lo).days + 1):
        candidate = lo + timedelta(days=offset)
        if candidate == exclude_date:
            continue
        c_load = load_map.get(candidate, 0)
        if c_load < cap and c_load < best_load:
            best_load = c_load
            best_day  = candidate
            if best_load == 0:
                break

    return best_day


def find_best_date(current_due: date, interval: int, today: date, load_map: dict,
                   exclude_date: date, cap: int) -> date | None:
    """
    Try progressively wider windows (±50%, ±100%, ±200%) to find a date
    whose load is strictly below `cap`.  If all windows fail, do a forward-only
    scan up to REBALANCE_FORWARD_LIMIT days from today.

    Returns the first viable date found, or None if none exists.
    """
    for mult in REBALANCE_WINDOW_MULTIPLIERS:
        window = max(int(interval * mult), REBALANCE_MIN_WINDOW)
        result = _search_window(current_due, window, today, load_map, exclude_date, cap)
        if result is not None:
            return result

    # Last resort: scan forward from tomorrow until a free slot appears
    candidate = today + timedelta(days=1)
    for _ in range(REBALANCE_FORWARD_LIMIT):
        if candidate != exclude_date and load_map.get(candidate, 0) < cap:
            return candidate
        candidate += timedelta(days=1)

    return None


def update_problem_due_date(filepath: str, new_due: date, last_solved: date) -> None:
    """
    Rewrite revisit_in_days in the .py file so that
    last_solved + revisit_in_days == new_due.
    """
    new_interval = (new_due - last_solved).days
    source = read_file(filepath)
    source = re.sub(
        r"(revisit_in_days\s*=\s*)\d+",
        f"revisit_in_days = {new_interval}",
        source,
    )
    write_file(filepath, source)


def main() -> None:
    args   = sys.argv[1:]
    apply  = "--apply" in args
    do_json = "--json" in args

    cap = DEFAULT_CAP
    if "--cap" in args:
        idx = args.index("--cap")
        if idx + 1 < len(args):
            try:
                cap = int(args[idx + 1])
            except ValueError:
                print(f"\n  {YELLOW}--cap requires an integer.{RESET}\n")
                sys.exit(1)

    root = os.path.join(os.getcwd(), "problems")
    if not os.path.isdir(root):
        print(f"\n  {YELLOW}problems/ directory not found. Run 'sensei init' first.{RESET}\n")
        sys.exit(1)

    today    = date.today()
    problems = collect_problems(root, today)

    if not problems:
        print(f"\n  {GREY}No tracked problems found.{RESET}\n")
        return

    load_map = build_load_map(problems)

    # Find overloaded days (future only — don't touch past/today)
    overloaded_days = sorted(
        d for d, cnt in load_map.items() if cnt > cap and d > today
    )

    if not overloaded_days:
        if do_json:
            print(json.dumps({"status": "balanced", "moves": []}))
        else:
            print(f"\n  {GREEN}[OK]{RESET}  Schedule is already balanced (max {cap} reviews/day).\n")
        return

    moves   = []
    changed = set()

    for day in overloaded_days:
        # Get non-exempt problems on this day, sorted by times_reviewed DESC then
        # interval DESC (most-reviewed / most-stable are displaced first).
        # Exempt problems (s-rated, brand-new) are never displaced.
        day_problems = [
            p for p in problems
            if p["due_date"] == day and p["filepath"] not in changed
            and not is_load_exempt(p)
        ]
        day_problems.sort(key=lambda p: (p["times_reviewed"], p["interval"]), reverse=True)

        for p in day_problems:
            if load_map.get(day, 0) <= cap:
                break  # day is now under cap

            best = find_best_date(p["due_date"], p["interval"], today, load_map,
                                  exclude_date=p["due_date"], cap=cap)
            if best is None:
                continue

            # Record the move
            moves.append({
                "label":    p["label"],
                "filepath": p["filepath"],
                "from":     p["due_date"].isoformat(),
                "to":       best.isoformat(),
                "times_reviewed": p["times_reviewed"],
            })

            # Update in-memory load map
            load_map[p["due_date"]] = load_map.get(p["due_date"], 0) - 1
            load_map[best]          = load_map.get(best, 0) + 1

            # Track change
            p["due_date"] = best
            changed.add(p["filepath"])

    if not moves:
        if do_json:
            print(json.dumps({"status": "no_moves", "moves": []}))
        else:
            print(f"\n  {YELLOW}No moves found — overloaded days may have no displaceable problems.{RESET}\n")
        return

    if do_json:
        print(json.dumps({
            "status":   "applied" if apply else "dry_run",
            "cap":      cap,
            "moves":    moves,
        }, indent=2))
        if apply:
            for p in problems:
                if p["filepath"] in changed:
                    update_problem_due_date(p["filepath"], p["due_date"], p["last_solved"])
        return

    # ── Human-readable output ─────────────────────────────────────────────────
    mode_label = f"{GREEN}APPLIED{RESET}" if apply else f"{YELLOW}DRY RUN{RESET}"
    print(f"\n  {BOLD}{CYAN}sensei rebalance{RESET}  [{mode_label}]  cap={cap}\n")
    print(f"  {'Problem':<42} {'From':<12} {'To':<12} {'Reviews':>7}")
    print(f"  {GREY}{'─' * 74}{RESET}")

    for m in moves:
        label = m["label"][:40]
        print(
            f"  {label:<42} {m['from']:<12} {CYAN}{m['to']:<12}{RESET} "
            f"{GREY}{m['times_reviewed']:>7}x{RESET}"
        )

    print(f"\n  {BOLD}{len(moves)} move(s){RESET} identified.")

    if apply:
        for p in problems:
            if p["filepath"] in changed:
                update_problem_due_date(p["filepath"], p["due_date"], p["last_solved"])
        print(f"  {GREEN}[OK]{RESET}  Changes written to disk.\n")
    else:
        print(f"  {GREY}Run with --apply to write changes.{RESET}\n")


if __name__ == "__main__":
    main()
