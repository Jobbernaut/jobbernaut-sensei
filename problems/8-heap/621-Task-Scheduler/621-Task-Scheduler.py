'''
https://leetcode.com/problems/task-scheduler/
'''

last_solved     = "2026-08-03"
revisit_in_days = 15
times_reviewed  = 4
difficulty      = "medium"
topic_tags      = ["heap", "greedy"]

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        counter = Counter(tasks)
        max_freq = max(counter.values())
        no_max_freq = len([key for key, value in counter.items() if value == max_freq])

        return max(len(tasks), (max_freq - 1) * (n + 1) + no_max_freq)
