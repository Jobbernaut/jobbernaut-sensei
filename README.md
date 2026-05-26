# Jobbernaut Sensei

My Python solutions for LeetCode problems, with a built-in spaced-repetition review system.

---

## Repository Structure

```
jobbernaut-sensei/
├── src/
│   ├── mark.py                         # mark a problem as reviewed
│   ├── new.py                          # scaffold a new problem file
│   ├── lopen.py                        # open a problem in editor + browser
│   ├── revisit.py                      # daily review runner
│   ├── hooks/
│   │   └── pre-commit                  # git hook: validate problem metadata
│   ├── completions/
│   │   └── _jobbernaut                 # zsh tab-completion for all commands
│   └── copy_templates/
│       ├── problem.py                  # copy this when starting a new problem
│       └── problem.md                  # copy this for your notes (optional)
├── problems/
│   ├── 1-arrays-and-hashing/
│   │   └── 217-Contains-Duplicate/
│   │       ├── 217-Contains-Duplicate.py
│   │       └── 217-Contains-Duplicate.md
│   ├── 2-two-pointers/
│   │   └── ...
│   └── ...
├── pyproject.toml
└── README.md
```

---

## Setup

```bash
pip install -e .
```

This installs the `mark`, `new`, `open`, and `revisit` commands globally so you can run them without `python src/`.

---

## Daily Loop

### 1. Morning — see what's due
```bash
revisit
# or: python src/revisit.py
```

### 2. Start a problem — scaffold it
```bash
new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set
# or: python src/new.py ...
```

### 3. Open a problem — jump back in
```bash
open 217
# or: python src/lopen.py 217
```

### 4. After solving — mark it
```bash
mark 217
mark "valid anagram"
mark contains-duplicate
# or: python src/mark.py ...
```

You'll be prompted with one question:

```
  How did it go?

    [e]  easy      → 90 days
    [g]  good      → 30 days
    [h]  hard      → 7 days
    [s]  struggled → 3 days
```

Press one key. `last_solved` and `revisit_in_days` are updated automatically.

---

## Commands

### `revisit` — daily review runner

```bash
revisit
```

**Example output:**
```
📅  LeetCode Revisit — Thursday, May 14 2026

🔴  OVERDUE
──────────────────────────────────────────────────────────────────────────
  7d ago       [easy  ]    217. Contains Duplicate          (arrays, hash-set)

🟡  DUE TODAY
──────────────────────────────────────────────────────────────────────────
  today        [medium ]    1. Two Sum                       (arrays, hash-map)

🟢  UPCOMING (7 days)
──────────────────────────────────────────────────────────────────────────
  in 2d        [medium ]   49. Group Anagrams                (arrays, hash-map)

──────────────────────────────────────────────────────────────────────────
  2 problem(s) need attention today.  Total tracked: 3
```

| Flag | What it does |
|------|-------------|
| _(none)_ | Overdue + due today + upcoming 7 days |
| `--all` | Everything, including far-future problems |
| `--topic arrays` | Filter by topic tag (partial match) |
| `--export` | Export all problems to `export.csv` |
| `--export-md` | Export all problems to `export.md` |

---

### `new` — scaffold a new problem

Creates the folder and pre-fills all metadata:

```bash
new 217 contains-duplicate 1-arrays-and-hashing
new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set
new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set --open
```

| Argument | Description |
|----------|-------------|
| `number` | LeetCode problem number |
| `slug` | LeetCode URL slug, e.g. `contains-duplicate` |
| `category` | Topic folder, e.g. `1-arrays-and-hashing` |
| `-d / --difficulty` | `easy` / `medium` / `hard` (default: `medium`) |
| `-t / --tags` | One or more topic tags |
| `--open` | Open the file in `$EDITOR` / `code` immediately |

The URL is derived automatically from the slug:
```
contains-duplicate  →  https://leetcode.com/problems/contains-duplicate/
```

---

### `open` — open a problem

Opens the solution file in your editor and the LeetCode page in your browser:

```bash
open 217
open contains-duplicate
open "valid anagram"
open 217 --no-browser   # editor only
```

Accepts problem number, slug, or title words — same fuzzy matching as `mark`.

---

### `mark` — mark a problem as reviewed

```bash
mark 217
mark "valid anagram"
mark contains-duplicate
```

Updates `last_solved` to today and sets `revisit_in_days` based on your rating.

---

## Adding a New Problem

The `new` command handles everything in one step:

```bash
new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set --open
```

### Manual alternative

1. **Create the folder** following the naming convention:
   ```
   problems/{category}/{number}-{Title-In-Kebab-Case}/
   ```

2. **Copy the Python template:**
   ```bash
   cp src/copy_templates/problem.py problems/1-arrays-and-hashing/217-Contains-Duplicate/217-Contains-Duplicate.py
   ```

3. **Optionally copy the Markdown template for notes:**
   ```bash
   cp src/copy_templates/problem.md problems/1-arrays-and-hashing/217-Contains-Duplicate/217-Contains-Duplicate.md
   ```

---

## The 4 Metadata Fields

Every `.py` solution file must have these 4 lines for `revisit` to track it:

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `last_solved` | `str` | `"2026-05-14"` | ISO 8601 date — update every time you re-solve |
| `revisit_in_days` | `int` | `3` | How many days until next review |
| `difficulty` | `str` | `"medium"` | `easy` / `medium` / `hard` |
| `topic_tags` | `list` | `["arrays", "hash-map"]` | Used for `--topic` filtering |

**Suggested `revisit_in_days` schedule (spaced repetition):**
- First time solving: `3`
- Solved it clean on review: double it → `7`, then `14`, then `30`
- Struggled on review: reset to `1` or `3`

---

## Pre-commit Hook

Validates that every staged `.py` file under `problems/` has all 4 metadata fields filled in with non-placeholder values before allowing a commit.

**Install once:**
```bash
cp src/hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

---

## Zsh Shell Completions

Tab-complete problem numbers/names for `mark`, `open`, and category names for `new`.

**Add to `~/.zshrc`:**
```zsh
fpath=(/path/to/jobbernaut-sensei/src/completions $fpath)
autoload -Uz compinit && compinit
```

Then reload: `source ~/.zshrc`

---

## Topic Folder Names

All topic folders live under `problems/`. Full paths look like `problems/1-arrays-and-hashing/`.

| # | Folder |
|---|--------|
| 1 | `1-arrays-and-hashing` |
| 2 | `2-two-pointers` |
| 3 | `3-sliding-window` |
| 4 | `4-stack` |
| 5 | `5-binary-search` |
| 6 | `6-linked-list` |
| 7 | `7-trees` |
| 8 | `8-tries` |
| 9 | `9-heap-priority-queue` |
| 10 | `10-backtracking` |
| 11 | `11-graphs` |
| 12 | `12-advanced-graphs` |
| 13 | `13-1d-dynamic-programming` |
| 14 | `14-2d-dynamic-programming` |
| 15 | `15-greedy` |
| 16 | `16-intervals` |
| 17 | `17-math-and-geometry` |
| 18 | `18-bit-manipulation` |
