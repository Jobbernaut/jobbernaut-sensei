'''
https://leetcode.com/problems/task-scheduler/
'''

last_solved     = "2026-07-22"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["heap", "greedy"]

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        count_max = 0

        counter = Counter(tasks)
        f = max(counter.values())

        for task, value in counter.items():
            if value == f:
                count_max += 1

        return max(len(tasks), (n+1)*(f-1) + count_max) 
