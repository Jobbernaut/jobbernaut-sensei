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
A timed mock interview flow: pick N random problems (optionally filtered by topic/difficulty), hide topic tags, enforce a time limit per problem, no hints. Generates a score at the end. Intentionally bypasses SRS scheduling — interview readiness, not memory maintenance.
