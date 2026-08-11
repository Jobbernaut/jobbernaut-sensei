# Roadmap

## Released

### v0.6.0
- `sensei progress` — NeetCode 150 dashboard with topic breakdown, difficulty split, velocity, and projected completion date
- `sensei new <url>` — scaffold from a LeetCode URL; auto-fetches number, difficulty, and tags via GraphQL

---

## Planned

### Performance History
Store a per-review history on each problem file (timestamp + rating) instead of only tracking `last_solved` and `times_reviewed`. This unlocks smarter SRS: recent performance is weighted more heavily, so a problem that was `e` five times but came back `h` twice recently gets a tighter interval. Foundation for confidence decay detection.

### Confidence Decay Detection
If a problem keeps returning as `h` or `s` after multiple review cycles, flag it for deliberate pattern study rather than re-queuing it on the standard SRS ladder. Surface these in `sensei status` as a separate "struggling" bucket.

### Weak Topic Detection
Auto-surface topic imbalances at session start based on recent performance history — e.g. "you've hit `h` or `s` on 4 of your last 6 DP problems." Currently requires a manual `sensei revisit --topic` call.

### Session Summaries
After each session, write a structured log entry (date, problems attempted, ratings given) to a local file. Use it to show monthly trends: recall improvement, topic mastery over time, average rating per topic.

### Interview Mode
A dedicated high-pressure coaching mode that bypasses normal SRS pacing and applies a strict interview simulation protocol. Distinct from daily review in every way:

**Coaching behavior:**
- Adversarial interviewer stance — not a tutor
- Probe every edge case unprompted: empty input, single element, all negatives, duplicates, max constraints
- Force manual traces: "walk me through exactly what happens with `[2, -3, 1, -1]` — state at each step"
- Ask follow-up questions after every answer — never let a correct answer be the end of the exchange
- Deliberately mislead to test conviction: propose wrong complexity, suggest incorrect simplifications, claim the solution might fail on a case (even if it doesn't). If the user pushes back correctly and explains why you're wrong, that's the best signal. If they capitulate without reasoning, that reveals shallow understanding
- Pre-submission code review mandatory: agent reads code line by line, traces dangerous inputs with the user, and must explicitly clear the submission before LeetCode is opened
- LeetCode rejection → automatic `s`, no exceptions
- Mistake caught during pre-submission review → downgrade final rating one level

**CLI design (planned):**
- `sensei interview` — enter interview mode, pick N problems
- Optional filters: `--topic graphs`, `--difficulty medium`, `--timed 30m`
- Topic tags hidden by default
- Score report at the end: problems attempted, ratings, time per problem
