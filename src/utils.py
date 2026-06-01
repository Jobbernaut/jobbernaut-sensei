'''
Shared utilities for the sensei CLI.

Provides:
    parse_metadata(filepath)              → dict | None
    find_solution_files(root, exclude)    → list[str]
    normalise(s)                          → str
    find_match(query, files)              → str | None
    extract_url(filepath)                 → str | None
'''

import ast
import os
import re
from datetime import date

# Default directories to never descend into
SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "docs"}


def parse_metadata(filepath: str) -> dict | None:
    """
    Reads a .py solution file and extracts the 4 required metadata variables:
        last_solved, revisit_in_days, difficulty, topic_tags

    Returns a dict on success, or None if any required field is missing/malformed.
    """
    required = {"last_solved", "revisit_in_days", "difficulty", "topic_tags"}
    meta = {}

    try:
        with open(filepath, "r") as f:
            source = f.read()
    except OSError:
        return None

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in required:
                    try:
                        meta[target.id] = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        pass

    if not required.issubset(meta.keys()):
        return None

    try:
        meta["last_solved"]     = date.fromisoformat(meta["last_solved"])
        meta["revisit_in_days"] = int(meta["revisit_in_days"])
    except (ValueError, TypeError):
        return None

    if not isinstance(meta["topic_tags"], list):
        meta["topic_tags"] = [meta["topic_tags"]]

    return meta


def find_solution_files(root: str, exclude_files: set | None = None) -> list:
    """
    Walk root recursively and return all .py solution files.

    exclude_files: optional set of bare filenames to skip, e.g. {"mark.py", "revisit.py"}.
    """
    if exclude_files is None:
        exclude_files = set()

    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for filename in filenames:
            if filename.endswith(".py") and filename not in exclude_files:
                files.append(os.path.join(dirpath, filename))
    return files


def normalise(s: str) -> str:
    """Lowercase and strip all non-alphanumeric characters for fuzzy matching."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def find_match(query: str, files: list) -> str | None:
    """
    Fuzzy-match query against a list of .py file paths.

    Accepts:
        - problem number:  "217"
        - slug:            "contains-duplicate"
        - title words:     "valid anagram"

    Returns the best matching filepath, or None.
    """
    q = normalise(query)

    # Exact number match first
    if q.isdigit():
        for f in files:
            stem  = os.path.splitext(os.path.basename(f))[0]
            parts = stem.split("-")
            if parts[0] == q:
                return f
        return None

    # Substring match against normalised filename
    candidates = []
    for f in files:
        stem = normalise(os.path.splitext(os.path.basename(f))[0])
        if q in stem:
            candidates.append(f)

    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        # Prefer the match whose stem positions the query earliest (leftmost)
        candidates.sort(key=lambda f: normalise(os.path.splitext(os.path.basename(f))[0]).index(q))
        return candidates[0]
    return None


def extract_url(filepath: str) -> str | None:
    """
    Return the first leetcode.com/problems URL found in the file, or None.
    Skips template placeholder URLs containing 'PROBLEM-SLUG'.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                m = re.search(r"https://leetcode\.com/problems/[^\s'\"]+", line)
                if m:
                    url = m.group(0).rstrip("/") + "/"
                    if "PROBLEM-SLUG" not in url:
                        return url
    except OSError:
        pass
    return None
