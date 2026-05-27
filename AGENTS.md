# Jobbernaut Sensei — AI Agent Integration Guide

So you're an AI agent and you want to coach a human through LeetCode practice. Good. Sensei was built for this.

Every command outputs **clean JSON**. No parsing nightmares. No interactive prompts you can't handle. Just structured data you can act on.

---

## 🧰 The Tools

### `sensei status` — quick pulse

```bash
sensei status
```

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

**Agent use:** Open with this. Now you know their state — total problems, how many are rotting, what's coming up.

---

### `sensei revisit --json` — full review data

```bash
sensei revisit --json
sensei revisit --json --topic arrays
```

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

**Agent use:** Identify exactly what's overdue or due today. Use `--topic` to drill into weak areas — "you've done 10 arrays problems but only 2 graphs. Let's fix that."

---

### `sensei hint <problem>` — quiz mode 🔑

```bash
sensei hint 217
sensei hint contains-duplicate
sensei hint "valid anagram"
```

```json
{
  "label": "217. Contains Duplicate",
  "number": "217",
  "title": "Contains Duplicate",
  "difficulty": "easy",
  "topics": ["arrays", "hashing"],
  "url": "https://leetcode.com/problems/contains-duplicate/description/",
  "status": {
    "last_solved": "2026-05-14",
    "due_date": "2026-08-12",
    "days_until_due": 78
  }
}
```

**Agent use:** This is your quizzing command. It gives you everything you need to describe the problem (difficulty, topics, LeetCode URL) but **no solution code**. Ask the user to code it. When they're done, hit `sensei show` to compare.

---

### `sensei show <problem>` — full reveal

```bash
sensei show 217
sensei show contains-duplicate
sensei show "valid anagram"
```

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

**Agent use:** Use this to see their *actual saved code*. Analyze it. Suggest optimizations. Point out the O(n²) loop they should have caught. The `solution` field is their code — treat it as their answer key.

---

### `sensei mark <problem> --rating <e|g|h|s>` — update progress

```bash
sensei mark 217 --rating e    # 90 days (or 135 if they've aced it 3+ times)
sensei mark 217 --rating g    # 30 days
sensei mark 217 --rating h    # 7 days (or 14 if seen before)
sensei mark 217 --rating s    # 3 days (leech detection: 3+ struggles = flag)
```

**Rating schedule (graduated):**

| Rating | Flag | First time | After 3+ aces | Why |
|--------|------|-----------|----------------|-----|
| Easy 🟢 | `--rating e` | 90 days | 135 → 180 max | You clearly know this. See you in 3 months. |
| Good 🔵 | `--rating g` | 30 days | 30 days | Solid but not burned in. Month is fine. |
| Hard 🟡 | `--rating h` | 7 days | 14 days | Needed help. Come back sooner. |
| Struggled 🔴 | `--rating s` | 3 days | 3 days | You're stuck. Study the pattern, not just this problem. |

**Agent use:** After the session, pick the rating that matches their performance. The SRS algorithm handles the math — it grows intervals for problems they've mastered and keeps shrinking for ones they haven't. You just pick the rating.

---

### `sensei new <number> <slug> <category>` — scaffold

```bash
sensei new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set
```

Creates the folder, Python file, and pre-fills metadata (including `times_reviewed = 0` for the graduated SRS). Use this when they want to start a new problem.

---

### `sensei open <problem>` — open LeetCode in browser

```bash
sensei open 217
sensei open contains-duplicate
sensei open "valid anagram"
```

Opens the problem's LeetCode URL in the browser. Nothing else — no file editing, no solution peeking.

---

## 🎯 The Full Coaching Loop

```
1. START
   sensei status
   → "You have 22 problems tracked. 0 overdue. 4 coming up this week."

2. PLAN
   sensei status
   → Check if any problems are past due or due today.
   → If YES: Prioritize coaching those problems immediately.
   → If NO: Move on to new problems that consolidate existing patterns or introduce new ones.
   sensei revisit --json
   → "No problems are due today. Let's start with a new problem to consolidate your knowledge."

3. QUIZ (no spoilers)
   sensei hint 124
   → You get the problem URL. Ask them to code it blind.

4. THEY CODE
   → Wait for their solution.

5. REVIEW
   sensei show 124
   → Compare their attempt against their saved solution.
   → "You used recursion with global max. Good. But you could also use tuple returns."

6. MARK
   sensei mark 124 --rating g
   → "You got it with a few hints. Marked as 'good' → 30 days."

7. REPEAT
   → Back to step 2 for the next problem.
```

---

## 🤖 Example Agent Prompt Snippet

```markdown
You have access to the `sensei` CLI. All commands return JSON.

Commands:
- `sensei status` — Quick summary of all problems
- `sensei revisit --json` — Full review data (supports --topic)
- `sensei hint <problem>` — Problem metadata + URL only (for quizzing)
- `sensei show <problem>` — Problem details + solution code
- `sensei mark <problem> --rating e|g|h|s` — Update schedule
- `sensei new NUMBER SLUG CATEGORY` — Scaffold a new problem
- `sensei open <problem>` — Open LeetCode URL in browser

Workflow:
1. Run `sensei status` to check the user's state
2. Run `sensei revisit --json` to find due problems
3. Run `sensei hint <problem>` to fetch problem (no solution)
4. Ask the user to write their solution
5. Run `sensei show <problem>` to compare
6. Tutor — analyze their code, suggest optimizations
7. Run `sensei mark <problem> --rating <rating>` to update
```

---

## 📐 Output Schema Reference

All problem objects follow this schema:

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

---

Go forth and coach. Use `sensei hint` to quiz, `sensei show` to review, and `sensei mark` to close the loop.