'''
NeetCode 150 progress dashboard.

Usage:
    sensei progress           # terminal dashboard
    sensei progress --json    # machine-readable output
'''

import json
import os
import re
import sys
from datetime import date, timedelta

import revisit

# ── ANSI colours ──────────────────────────────────────────────────────────────
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

BAR_WIDTH = 10


def _bar(done, total):
    filled = round(BAR_WIDTH * done / total) if total else 0
    return "█" * filled + "░" * (BAR_WIDTH - filled)


def _parse_neetcode150(md_path):
    """
    Parse NEETCODE150.md and return a list of sections:
        [{"topic": str, "problems": [{"number": int, "title": str, "difficulty": str}]}]
    """
    sections = []
    current_topic = None
    current_problems = []

    section_re  = re.compile(r'^## \d+\. (.+)$')
    problem_re  = re.compile(r'^- \[[ x]\] (\d+)\. (.+) \((Easy|Medium|Hard)\)$')

    try:
        with open(md_path, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                m = section_re.match(line)
                if m:
                    if current_topic is not None:
                        sections.append({"topic": current_topic, "problems": current_problems})
                    current_topic = m.group(1)
                    current_problems = []
                    continue
                m = problem_re.match(line)
                if m and current_topic is not None:
                    current_problems.append({
                        "number":     int(m.group(1)),
                        "title":      m.group(2),
                        "difficulty": m.group(3).lower(),
                    })
        if current_topic is not None:
            sections.append({"topic": current_topic, "problems": current_problems})
    except OSError:
        pass

    return sections


def _solved_numbers(problems_root):
    """Return a set of problem numbers (int) that exist in the filesystem."""
    solved = set()
    problems = revisit.collect_problems(problems_root)
    for p in problems:
        label = p["label"].strip()
        m = re.match(r'^(\d+)\.', label)
        if m:
            solved.add(int(m.group(1)))
    return solved, problems


def _velocity(all_problems):
    """Return problems solved per week based on the last 28 days."""
    today = date.today()
    cutoff = today - timedelta(days=28)
    recent = sum(1 for p in all_problems if p["last_solved"] >= cutoff)
    return round(recent / 4, 1)


def main():
    do_json = "--json" in sys.argv

    problems_root = os.path.join(os.getcwd(), "problems")
    if not os.path.isdir(problems_root):
        if do_json:
            print(json.dumps({"error": "problems/ not found"}))
        else:
            print(f"\n{GREY}  problems/ directory not found. Run 'sensei init' first.{RESET}\n")
        sys.exit(1)

    md_path = os.path.join(problems_root, "NEETCODE150.md")
    sections = _parse_neetcode150(md_path)

    if not sections:
        msg = "Could not parse NEETCODE150.md"
        if do_json:
            print(json.dumps({"error": msg}))
        else:
            print(f"\n{GREY}  {msg}{RESET}\n")
        sys.exit(1)

    solved_nums, all_problems = _solved_numbers(problems_root)
    today = date.today()

    # ── aggregate stats ───────────────────────────────────────────────────────
    total_problems = sum(len(s["problems"]) for s in sections)
    total_solved   = sum(1 for s in sections for p in s["problems"] if p["number"] in solved_nums)

    diff_totals = {"easy": 0, "medium": 0, "hard": 0}
    diff_solved = {"easy": 0, "medium": 0, "hard": 0}
    for s in sections:
        for p in s["problems"]:
            d = p["difficulty"]
            diff_totals[d] += 1
            if p["number"] in solved_nums:
                diff_solved[d] += 1

    by_topic = []
    for s in sections:
        t_total  = len(s["problems"])
        t_solved = sum(1 for p in s["problems"] if p["number"] in solved_nums)
        by_topic.append({"topic": s["topic"], "done": t_solved, "total": t_total})

    vel = _velocity(all_problems)
    remaining = total_problems - total_solved
    if vel > 0:
        weeks_left = remaining / vel
        projected_date = (today + timedelta(weeks=weeks_left)).isoformat()
        projected_weeks = round(weeks_left)
    else:
        projected_date  = None
        projected_weeks = None

    # ── JSON output ───────────────────────────────────────────────────────────
    if do_json:
        print(json.dumps({
            "completed": total_solved,
            "total":     total_problems,
            "by_difficulty": {
                d: {"done": diff_solved[d], "total": diff_totals[d]}
                for d in ("easy", "medium", "hard")
            },
            "by_topic":            by_topic,
            "velocity_per_week":   vel,
            "projected_completion": projected_date,
        }, indent=2))
        return

    # ── terminal output ───────────────────────────────────────────────────────
    pct = round(100 * total_solved / total_problems) if total_problems else 0
    overall_bar = _bar(total_solved, total_problems)

    print(f"\n{BOLD}{CYAN}NeetCode 150 — Progress Report{RESET}\n")
    print(f"  Completed:   {BOLD}{total_solved} / {total_problems}{RESET}  ({pct}%)  {overall_bar}\n")

    print(f"  {BOLD}By Difficulty:{RESET}")
    for d in ("easy", "medium", "hard"):
        done  = diff_solved[d]
        total = diff_totals[d]
        p2    = round(100 * done / total) if total else 0
        print(f"    {d.capitalize():<8} {done:>2} / {total:<4} ({p2:>3}%)")

    print(f"\n  {BOLD}By Topic:{RESET}")
    max_topic_len = max(len(t["topic"]) for t in by_topic)
    for t in by_topic:
        done  = t["done"]
        total = t["total"]
        p2    = round(100 * done / total) if total else 0
        bar   = _bar(done, total)
        topic = t["topic"].ljust(max_topic_len)
        colour = GREEN if done == total else (YELLOW if done > 0 else GREY)
        print(f"    {colour}{topic}{RESET}  {done:>2} / {total:<4}  {p2:>3}%  {bar}")

    print(f"\n  {BOLD}Velocity:{RESET}    ~{vel} problems/week  (last 4 weeks)")
    if projected_date:
        print(f"  {BOLD}Projected:{RESET}   ~{projected_weeks} weeks to completion  ({projected_date})")
    else:
        print(f"  {BOLD}Projected:{RESET}   N/A  (no recent activity)")

    print()
