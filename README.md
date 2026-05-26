# neetcode-150

My Python solutions for the NeetCode 150 problems, with a built-in spaced-repetition review system.

---

## Repository Structure

```
neetcode-150/
├── src/
│   ├── mark.py                         # mark a problem as reviewed
│   ├── revisit.py                      # daily review runner
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

## Daily Loop

### 1. Morning — see what's due
```bash
python src/revisit.py
```

> If the package is installed (`pip install -e .`), you can also just run `revisit`.

### 2. After solving — mark it
```bash
python src/mark.py 217
python src/mark.py "valid anagram"
python src/mark.py contains-duplicate
```

> If the package is installed, you can also just run `mark 217`, etc.

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

## Daily Review (detail)

Run this every day to see what needs your attention:

```bash
python src/revisit.py
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

### Flags

| Command | What it does |
|---------|-------------|
| `python src/revisit.py` | Overdue + due today + upcoming 7 days |
| `python src/revisit.py --all` | Everything, including far-future problems |
| `python src/revisit.py --topic arrays` | Filter by topic tag (partial match) |

---

## Adding a New Problem

### 1. Create the folder

Follow the naming convention exactly:

```
{topic-folder}/{number}-{Title-In-Kebab-Case}/
```

Examples:
```
problems/1-arrays-and-hashing/1-Two-Sum/
problems/2-two-pointers/167-Two-Sum-II/
problems/5-sliding-window/3-Longest-Substring-Without-Repeating-Characters/
```

### 2. Copy the Python template

```bash
cp src/copy_templates/problem.py problems/1-arrays-and-hashing/1-Two-Sum/1-Two-Sum.py
```

Then open the file and fill in:

```python
'''
https://leetcode.com/problems/two-sum/
'''

last_solved     = "2026-05-14"           # today's date in YYYY-MM-DD
revisit_in_days = 3                      # when to review next
difficulty      = "easy"                 # easy / medium / hard
topic_tags      = ["arrays", "hash-map"] # your tags

from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}
        for i, n in enumerate(nums):
            diff = target - n
            if diff in seen:
                return [seen[diff], i]
            seen[n] = i
```

### 3. Optionally copy the Markdown template for notes

```bash
cp src/copy_templates/problem.md problems/1-arrays-and-hashing/1-Two-Sum/1-Two-Sum.md
```

---

## The 4 Metadata Fields

Every `.py` solution file must have these 4 lines for `revisit.py` to track it:

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
