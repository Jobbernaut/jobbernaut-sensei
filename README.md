<div align="center">
  <img src="assets/overkill-labs.png" height="80" alt="OverKill Labs" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/leetcode.png" height="80" alt="LeetCode" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="assets/neetcode.png" height="80" alt="NeetCode" />

  <h1>LeetCode Sensei</h1>
  <p>An <strong>OverKill Labs</strong> spaced-repetition CLI for LeetCode practice.</p>
</div>

---

> Your LeetCode practice, but you actually remember what you solved.

**Sensei** is a spaced-repetition CLI that stops you from grinding LeetCode into the void. Every command outputs clean JSON — it's built for humans but **designed for AI agents**.

```bash
pip install leetcode-sensei
sensei init
```

---

## 🔥 Why This Exists

You solve 200 LeetCode problems. Three months later you can't solve FizzBuzz.

Sensei tracks **when** you solved a problem and **how well** you understood it. Then it tells you exactly what to review — before your brain evicts it from cache.

```
┌──────────────────────────────────────────────────────────────┐
│  Your brain has a cache. This is the invalidation policy.   │
└──────────────────────────────────────────────────────────────┘
```

**Zero config. Zero cloud. Zero bullshit.** Your solutions are just `.py` files in a folder — git-friendly, portable, no lock-in.

---

## ⚡ What It Does

| Command | Vibe |
|---------|------|
| `sensei revisit` | "Here's what you're forgetting" — color-coded review queue |
| `sensei status` | JSON snapshot for you or your AI agent |
| `sensei hint <problem>` | Get the problem URL + deets **without the answer** (for quizzing) |
| `sensei show <problem>` | Full problem + your saved solution (for review) |
| `sensei mark <problem> --rating g` | "Good" → next review in 7 days (with load smoothing) |
| `sensei new <num> <slug> <cat>` | Scaffold a fresh problem in 0.3 seconds |
| `sensei open <problem>` | Jump into the code + LeetCode page |
| `sensei rebalance` | Spread review clusters across empty days |
| `sensei revisit --export` | Dump everything to CSV or Markdown |

---

## 📅 Daily Loop

```bash
# 1. What's rotting in my brain today?
sensei revisit

# 2. Quiz me on this one (agent, don't spoil it)
sensei hint 217

# 3. Let me code, then compare
sensei show 217

# 4. How'd I do?
sensei mark 217 --rating g    # good → 7 days
```

That's it. Four commands. Whole loop takes 2 seconds of typing.

---

## 🧠 Spaced Repetition — The Smart Part

Rate yourself after each solve. Intervals are hardcoded — no adaptive math, no history weighting:

| Rating | Flag | Next Review |
|--------|------|-------------|
| Trivial 🏆 | `--rating t` | 90 days |
| Easy 🟢 | `--rating e` | 30 days |
| Good 🔵 | `--rating g` | 7 days |
| Hard 🟡 | `--rating h` | 3 days |
| Struggled 🔴 | `--rating s` | 1 day |

**The schedule is the curriculum.** Every rating directly sets the next review — no surprises.

### 📈 New-Problem Progression Gate

New problems are gated through a 1 → 3 → 7 → 30 day ladder before entering full SRS. No matter how well you solve a brand-new problem, it can't skip ahead:

| Review # | Max interval |
|----------|-------------|
| 1st solve | 1 day |
| 2nd solve | 3 days |
| 3rd solve | 7 days |
| 4th solve | 30 days |
| 5th+ | Full SRS (no cap) |

Rating `e` on your first solve → capped at 1 day. Rating `s` on your 4th solve → 1 day (under cap). The gate only fires when the rating would exceed the cap.

### ⚖️ Load Smoothing

`sensei mark` automatically spreads reviews across nearby days to avoid spikes. Instead of 6 problems all landing on the same day, the scheduler finds the least-loaded day within a window:

| Rating | Base | Spread range |
|--------|------|-------------|
| `s` | 1d | fixed |
| `h` | 3d | 2–4 days |
| `g` | 7d | 5–14 days |
| `e` | 30d | 15–45 days |
| `t` | 90d | 45–90 days |

Problems reviewed 5+ times are biased toward the **later** end of their window (stable memory, safe to defer). Newer problems stay at the **earlier** end (fragile memory, keep close).

Disable with `--no-spread` to get exact base intervals.

---

## 🤖 AI-Agent Native

Every command returns clean JSON. Plug it into Cline, Claude Code, ChatGPT, or your own agent:

```bash
sensei status                     # → {"total":22,"overdue":0,...}
sensei revisit --json             # → Full review data with dates
sensei hint 217                   # → Problem URL + status, no solution
sensei show 217                   # → Metadata + saved solution
sensei mark 217 --rating e        # → Update schedule, no prompts
```

See **[`AGENTS.md`](AGENTS.md)** for the complete agent integration guide.

---

## 📦 Setup

```bash
pip install leetcode-sensei
sensei init                      # Creates problems/ directory
sensei new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set
code problems/                   # Start solving
```

### Dependencies

- Python ≥ 3.10
- That's it. No npm. No Docker. No cloud.

---

## 📖 Commands

### `sensei revisit` — what to review

```bash
sensei revisit                    # Overdue + due today + upcoming 7 days
sensei revisit --all              # Everything
sensei revisit --topic trees      # Filter by topic
sensei revisit --json             # Agent-friendly JSON
sensei revisit --export           # → export.csv
sensei revisit --export-md        # → export.md
```

Colored terminal output:

```
📅  LeetCode Sensei Revisit — Tuesday, May 26 2026

🟢  UPCOMING (7 days)
──────────────────────────────────────────────────────────────────────────
  in 3d          [hard  ]   124. Binary Tree Maximum Path Sum      (trees)
  in 4d          [medium]   853. Car Fleet                         (stack, monotonic-stack)
```

### `sensei show <problem>` — inspect + solution

```bash
sensei show 217
sensei show contains-duplicate
```

Returns JSON: label, number, title, filepath, metadata (last_solved, revisit_in_days, difficulty, topic_tags, due_date), and **your saved solution code**.

### `sensei hint <problem>` — inspect, NO solution

```bash
sensei hint 217
sensei hint contains-duplicate
```

Same as `show` but **no `solution` field**. Returns `times_reviewed` so the agent knows review history without seeing the answer. Perfect for agents that want to quiz without spoiling.

### `sensei mark <problem>` — rate your session

```bash
sensei mark 217                         # Interactive prompt
sensei mark 217 --rating e              # Non-interactive (agent-friendly)
sensei mark 217 --rating g --no-spread  # Exact base interval, no smoothing
```

Automatically increments `times_reviewed` and applies the progression gate and load smoothing.

### `sensei rebalance` — flatten review spikes

```bash
sensei rebalance              # Dry run — preview moves, no writes
sensei rebalance --apply      # Write changes to disk
sensei rebalance --cap 2      # Flag days with more than 2 reviews
```

Finds days exceeding the review cap and displaces the most-reviewed problems (most stable memory) to nearby low-load dates within ±50% of their current interval. Always preview before applying.

### `sensei new <num> <slug> <cat>` — scaffold

```bash
sensei new 217 contains-duplicate 1-arrays-and-hashing -d easy -t arrays hash-set
```

### `sensei open <problem>` — jump in

```bash
sensei open 217                    # Editor + browser
sensei open 217 --no-browser       # Editor only
```

### `sensei status` — quick pulse

```bash
sensei status
```

Returns `{total, overdue, due_today, upcoming, future, problems[]}` — one-liner for agents. Schema matches `sensei revisit --json` counts.

---

## 🔧 Fuzzy Matching

Every command that takes a problem accepts:

```bash
sensei show 217                    # Problem number
sensei show contains-duplicate     # URL slug
sensei show "valid anagram"        # Title words
```

It matches the first unique result. No tab-complete needed (but we have it anyway — see [completions](src/completions)).

---

## 🐚 Zsh Completions

```zsh
fpath=(/path/to/leetcode-sensei/src/completions $fpath)
autoload -Uz compinit && compinit
```

---

## 📄 License

PolyForm Noncommercial License 1.0.0 — free for personal and non-commercial use.

Full license in [`LICENSE`](LICENSE).

---

<div align="center">
  <img src="assets/overkill-labs.png" height="48" alt="OverKill Labs" />
  <br/>
  <sub>Built with precision by <strong>OverKill Labs</strong></sub>
</div>
