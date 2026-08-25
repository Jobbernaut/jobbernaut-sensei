'''
https://leetcode.com/problems/insert-interval/
'''

last_solved     = "2026-08-24"
revisit_in_days = 34
times_reviewed  = 4
difficulty      = "medium"
topic_tags      = ["array"]

class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        output = []

        new_lower, new_upper = newInterval

        for idx, interval in enumerate(intervals):
            lower, upper = interval

            if max(lower, new_lower) <= min(upper, new_upper):
                new_lower = min(lower, new_lower)
                new_upper = max(upper, new_upper)
            elif new_upper < lower:
                output.append([new_lower, new_upper])
                output.extend(intervals[idx:])
                return output
            else:
                output.append([lower, upper])
        
        output.append([new_lower, new_upper])

        return output