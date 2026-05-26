# Jobbernaut Sensei — AI Agent Integration Guide

This document describes how to use the `sensei` CLI as a tool for AI coding agents (Cline, Claude Code, GitHub Copilot, ChatGPT, etc.). It is designed to be included in an agent's system prompt or tool configuration.

---

## Overview

`sensei` is a spaced-repetition CLI for LeetCode practice. Every command outputs **clean JSON**, making it a natural fit for agent-driven tutoring workflows. An AI agent can:

1. Check what problems are due
2. Fetch a specific problem + the user's saved solution
3. Provide tutoring feedback
4. Update the review schedule — all through the same CLI

---

## Available Tools

### `sensei status`

**Purpose:** Quick assessment of the user's practice state.

```bash
sensei status
```

**Output:**
```json
{
  "total": 22,
  "overdue": 0,
  "due_today": 0,
  "upcoming": 4,
  "problems": [
    {
      "label": "124. Binary Tree Maximum Path Sum",
      "difficulty": "hard",
      "last_solved": "2026-05-26",
      "due_date": "2026-05-29",
      "days_until_due": 3,
      "topics": ["trees"],
      "topic_folder": "7-trees"
    }
  ]
}
```

**Agent usage:** Use this first to understand how many problems the user has, how many are overdue, and get a quick overview.

---

### `sensei revisit --json`

**Purpose:** Get the full review data for all tracked problems.

```bash
sensei revisit --json
sensei revisit --json --topic arrays
```

**Output:**
```json
{
  "generated": "2026-05-26",
  "total_tracked": 22,
  "problems": [
    {
      "label": "124. Binary Tree Maximum Path Sum",
      "difficulty": "hard",
      "last_solved": "2026-05-26",
      "due_date": "2026-05-29",
      "days_until_due": 3,
      "topics": ["trees"],
      "topic_folder": "7-trees",
      "filepath": "problems/7-trees/124-Binary-Tree-Maximum-Path-Sum/124-Binary-Tree-Maximum-Path-Sum.py"
    }
  ]
}
```

**Agent usage:** Use this to identify which specific problems are overdue or due today, then tutor the user on each one. Supports `--topic` filtering for targeted sessions.

---

### `sensei show <problem>`

**Purpose:** Inspect a single problem — metadata + the user's saved solution code.

```bash
sensei show 217
sensei show contains-duplicate
sensei show "valid anagram"
```

**Output:**
```json
{
  "label": "217. Contains Duplicate",
  "number": "217",
  "title": "Contains Duplicate",
  "filepath": "problems/1-arrays-and-hashing/217-Contains-Duplicate/217-Contains-Duplicate.py",
  "metadata": {
    "last_solved": "2026-05-14",
    "revisit_in_days": 90,
    "difficulty": "easy",
    "topic_tags": ["arrays", "hashing"],
    "due_date": "2026-08-12"
  },
  "solution": "class Solution:\n    def containsDuplicate(self, nums: List[int]) -> bool:\n        return not len(set(nums)) == len(nums)"
}
```

**Agent usage:** Use this to fetch the exact problem the user needs to review. Analyze their solution, provide hints, suggest optimizations, or ask them to explain their approach. The `solution` field contains their actual saved code.

---

### `sensei mark <problem>`

**Purpose:** Mark a problem as solved and update the spaced-repetition schedule.

**Interactive mode** (agent should NOT use this):
```bash
sensei mark 217
```
Prompts the user for a difficulty rating.

**Non-interactive mode** (agent-friendly):
```bash
sensei mark 217 --rating e    # 90 days
sensei mark 217 --rating g    # 30 days
sensei mark 217 --rating h    # 7 days
sensei mark 217 --rating s    # 3 days
```

**Output:**
```
  217. Contains Duplicate
  problems/.../217-Contains-Duplicate.py

  ✓  Marked as solved today (2026-05-26)  ·  next review in 90 days
```

**Rating schedule:**

| Rating | Flag | Next Review | When to use |
|--------|------|-------------|-------------|
| Easy | `--rating e` | 90 days | User solved it immediately without help |
| Good | `--rating g` | 30 days | User solved it with minor hints |
| Hard | `--rating h` | 7 days | User needed significant guidance |
| Struggled | `--rating s` | 3 days | User couldn't solve it; needs intensive review |

**Agent usage:** After tutoring a user on a problem, use this to update their progress. Choose the rating based on how well they performed during the session.

---

### `sensei new`

**Purpose:** Scaffold a new problem file.

```bash
sensei new NUMBER SLUG CATEGORY [-d DIFFICULTY] [-t TAGS] [--open]
```

**Example:**
```bash
sensei new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set
```

**Agent usage:** Use this when the user wants to start practicing a new LeetCode problem. Creates the folder, Python file, and pre-fills metadata.

---

### `sensei open`

**Purpose:** Open a problem in the user's editor and browser.

```bash
sensei open 217
sensei open contains-duplicate
sensei open 217 --no-browser
```

**Agent usage:** Use this when the user wants to jump directly into coding a specific problem.

---

## Recommended Agent Workflow

```
1. START → sensei status
   │  Assess the user's current state
   │
2. PLAN → sensei revisit --json
   │  Identify which problems are due
   │
3. TUTOR → sensei show 217
   │  Fetch problem + user's solution
   │  Analyze, provide hints/code review
   │
4. MARK → sensei mark 217 --rating g
   │  Update the schedule based on performance
   │
5. REPEAT → back to step 2
```

## Example Agent Prompt Snippet

```markdown
You have access to the `sensei` CLI tool for LeetCode practice.

Available commands:
- `sensei status` — Quick summary of all problems
- `sensei revisit --json` — Full review data
- `sensei show <problem>` — Problem details + solution code
- `sensei mark <problem> --rating e|g|h|s` — Mark as solved
- `sensei new NUMBER SLUG CATEGORY` — Scaffold a new problem
- `sensei open <problem>` — Open in editor

Workflow:
1. Run sensei status to check the user's practice state
2. Run sensei revisit --json to find due problems
3. Run sensei show <problem> to see their solution
4. Tutor accordingly
5. Run sensei mark <problem> --rating <rating> to update
```

---

## Output Schema Reference

All problem objects in JSON output follow this schema:

| Field | Type | Example |
|-------|------|---------|
| `label` | `string` | `"217. Contains Duplicate"` |
| `difficulty` | `string` | `"easy"` / `"medium"` / `"hard"` |
| `last_solved` | `string (ISO date)` | `"2026-05-14"` |
| `due_date` | `string (ISO date)` | `"2026-08-12"` |
| `days_until_due` | `int` | `78` |
| `topics` | `array of strings` | `["arrays", "hashing"]` |
| `topic_folder` | `string` | `"1-arrays-and-hashing"` |
| `filepath` | `string` | Relative path to solution file |

Additional fields in `sensei show`:

| Field | Type | Example |
|-------|------|---------|
| `number` | `string` | `"217"` |
| `title` | `string` | `"Contains Duplicate"` |
| `metadata` | `object` | Full metadata object |
| `solution` | `string` | User's saved Python solution |