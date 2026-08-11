'''
Scaffold a new problem file from the template.

Usage:
    sensei new 217 contains-duplicate 1-arrays-and-hashing
    sensei new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set
    sensei new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set --open
'''

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date

# ── ANSI colours ──────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


def slug_to_folder(number: str, slug: str) -> str:
    """'217' + 'contains-duplicate' → '217-Contains-Duplicate'"""
    titled = "-".join(part.title() for part in slug.split("-"))
    return f"{number}-{titled}"


def slug_to_title(slug: str) -> str:
    """'contains-duplicate' → 'Contains Duplicate'"""
    return slug.replace("-", " ").title()


def build_content(number: str, slug: str, difficulty: str, tags: list, today: str) -> str:
    url       = f"https://leetcode.com/problems/{slug}/"
    tags_repr = "[" + ", ".join(f'"{t}"' for t in tags) + "]"
    return f'''\'\'\'
{url}
\'\'\'

last_solved     = "{today}"
revisit_in_days = 1
times_reviewed  = 0
difficulty      = "{difficulty}"
topic_tags      = {tags_repr}

class Solution:
    def solve(self) -> None:
        # TODO: implement
        pass
'''


def fetch_leetcode_metadata(slug: str) -> dict | None:
    """
    Hit the unofficial LeetCode GraphQL endpoint to get problem number,
    difficulty, and topic tags. Returns None on any failure.
    """
    query = json.dumps({
        "query": f'{{ question(titleSlug: "{slug}") {{ questionFrontendId difficulty topicTags {{ slug }} }} }}'
    }).encode()
    req = urllib.request.Request(
        "https://leetcode.com/graphql",
        data=query,
        headers={
            "Content-Type": "application/json",
            "Referer": f"https://leetcode.com/problems/{slug}/",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
        q = data.get("data", {}).get("question")
        if not q:
            return None
        return {
            "number":     q["questionFrontendId"],
            "difficulty": q["difficulty"].lower(),
            "tags":       [t["slug"] for t in q.get("topicTags", [])],
        }
    except Exception:
        return None


def open_in_editor(path: str) -> None:
    import subprocess
    editor = os.environ.get("EDITOR", "")
    if editor:
        subprocess.run([editor, path])
    else:
        subprocess.run(["code", path])


def main() -> None:
    raw = sys.argv[1:]
    url_mode = bool(raw) and raw[0].startswith("http")

    if url_mode:
        _main_url(raw)
    else:
        _main_legacy()


def _main_url(raw: list) -> None:
    parser = argparse.ArgumentParser(prog="new", description="Scaffold from a LeetCode URL.")
    parser.add_argument("url",      help="LeetCode problem URL")
    parser.add_argument("category", help="Topic folder, e.g. 1-arrays-and-hashing")
    parser.add_argument("-d", "--difficulty", default=None, choices=["easy", "medium", "hard"])
    parser.add_argument("-t", "--tags",       default=None, nargs="+", metavar="TAG")
    parser.add_argument("--open", action="store_true")
    args = parser.parse_args(raw)

    m = re.match(r'https?://leetcode\.com/problems/([^/?#]+)', args.url)
    if not m:
        print(f"\n  {YELLOW}Could not parse slug from URL.{RESET}\n")
        sys.exit(1)
    slug = m.group(1).rstrip("/")

    meta = fetch_leetcode_metadata(slug)
    if meta:
        number     = meta["number"]
        difficulty = args.difficulty or meta["difficulty"]
        tags       = args.tags       or meta["tags"] or ["topic"]
    else:
        print(f"\n  {YELLOW}[warn]{RESET}  LeetCode API unavailable — falling back to manual flags.\n")
        if not args.difficulty or not args.tags:
            print(f"  Please provide {BOLD}-d{RESET} and {BOLD}-t{RESET} flags when the API is unreachable.\n")
            sys.exit(1)
        # derive number from slug best-effort (first numeric run), else prompt user
        num_match = re.match(r'^(\d+)', slug)
        number     = num_match.group(1) if num_match else "0"
        difficulty = args.difficulty
        tags       = args.tags

    _scaffold(number, slug, args.category, difficulty, tags, args.open)


def _main_legacy() -> None:
    parser = argparse.ArgumentParser(prog="new", description="Scaffold a new LeetCode problem file.")
    parser.add_argument("number",   help="LeetCode problem number, e.g. 217")
    parser.add_argument("slug",     help="LeetCode slug, e.g. contains-duplicate")
    parser.add_argument("category", help="Topic folder, e.g. 1-arrays-and-hashing")
    parser.add_argument("-d", "--difficulty", default="medium", choices=["easy", "medium", "hard"])
    parser.add_argument("-t", "--tags", nargs="+", default=["topic"], metavar="TAG")
    parser.add_argument("--open", action="store_true")
    args = parser.parse_args()
    _scaffold(args.number, args.slug, args.category, args.difficulty, args.tags, args.open)


def _scaffold(number: str, slug: str, category: str, difficulty: str, tags: list, open_after: bool) -> None:
    folder_name = slug_to_folder(number, slug)
    problem_dir = os.path.join(os.getcwd(), "problems", category, folder_name)
    file_name   = f"{folder_name}.py"
    file_path   = os.path.join(problem_dir, file_name)

    if os.path.exists(file_path):
        print(f"\n  {YELLOW}Already exists:{RESET} {os.path.relpath(file_path, os.getcwd())}\n")
        sys.exit(1)

    os.makedirs(problem_dir, exist_ok=True)

    today   = date.today().isoformat()
    content = build_content(number, slug, difficulty, tags, today)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    title = slug_to_title(slug)
    rel   = os.path.relpath(file_path, os.getcwd())
    print(f"\n  {GREEN}[OK]{RESET}  Created  {BOLD}{CYAN}{number}. {title}{RESET}")
    print(f"       {GREY}{rel}{RESET}\n")

    if open_after:
        open_in_editor(file_path)


if __name__ == "__main__":
    main()
