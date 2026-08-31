'''
https://leetcode.com/problems/merge-intervals/
'''

last_solved     = "2026-08-31"
revisit_in_days = 30
times_reviewed  = 4
difficulty      = "medium"
topic_tags      = ["array", "sorting", "quicksort"]

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        output = []

        intervals.sort()

        l, u = intervals[0]

        for idx in range(1, len(intervals)):
            n_l, n_u = intervals[idx]

            if u >= n_l:
                u = max(u, n_u)
            else:
                output.append([l, u])
                l, u = n_l, n_u

        output.append([l, u])

        return output

