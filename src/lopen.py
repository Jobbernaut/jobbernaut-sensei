'''
Open a problem file in your editor and its LeetCode URL in the browser.

Usage:
    python lopen.py 217
    python lopen.py contains-duplicate
    python lopen.py "valid anagram"
    python lopen.py 217 --no-browser
'''

import os
import re
import sys

# ── ANSI colours ──────────────────────────────────────────────────────────────
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "docs"}


def find_solution_files(root: str) -> list:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".py"):
                files.append(os.path.join(dirpath, filename))
    return files


def normalise(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_match(query: str, files: list):
    q = normalise(query)

    if q.isdigit():
        for f in files:
            stem  = os.path.splitext(os.path.basename(f))[0]
            parts = stem.split("-")
            if parts[0] == q:
                return f
        return None

    candidates = []
    for f in files:
        stem = normalise(os.path.splitext(os.path.basename(f))[0])
        if q in stem:
            candidates.append(f)

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        candidates.sort(
            key=lambda f: normalise(os.path.splitext(os.path.basename(f))[0]).index(q)
        )
        return candidates[0]
    return None


def extract_url(path: str):
    """Return the first leetcode.com/problems URL found in the file, or None."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                m = re.search(r"https://leetcode\.com/problems/[^\s'\"]+", line)
                if m:
                    url = m.group(0).rstrip("/") + "/"
                    if "PROBLEM-SLUG" not in url:
                        return url
    except OSError:
        pass
    return None


def open_in_editor(path: str) -> None:
    editor = os.environ.get("EDITOR", "")
    if editor:
        os.system(f'{editor} "{path}"')
    else:
        os.system(f'code "{path}"')


def open_in_browser(url: str) -> None:
    os.system(f'open "{url}"')


def main() -> None:
    argv       = sys.argv[1:]
    no_browser = "--no-browser" in argv
    argv       = [a for a in argv if a != "--no-browser"]

    if not argv:
        print(f"\n  {YELLOW}Usage: python lopen.py <number | slug | title words>{RESET}")
        print(f"  {YELLOW}       python lopen.py 217 --no-browser{RESET}\n")
        sys.exit(1)

    query     = " ".join(argv)
    repo_root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    prob_root = os.path.join(repo_root, "problems")
    files     = find_solution_files(prob_root)
    match     = find_match(query, files)

    if match is None:
        print(f"\n  {YELLOW}No match found for: \"{query}\"{RESET}\n")
        sys.exit(1)

    stem  = os.path.splitext(os.path.basename(match))[0]
    parts = stem.split("-")
    if parts[0].isdigit():
        label = f"{int(parts[0])}. {' '.join(parts[1:]).title()}"
    else:
        label = stem.replace("-", " ").title()

    rel = os.path.relpath(match, repo_root)
    print(f"\n  {BOLD}{CYAN}{label}{RESET}")
    print(f"  {GREY}{rel}{RESET}")

    open_in_editor(match)

    if not no_browser:
        url = extract_url(match)
        if url:
            print(f"  {GREY}→ {url}{RESET}")
            open_in_browser(url)

    print()


if __name__ == "__main__":
    main()
