'''
https://leetcode.com/problems/merge-intervals/
'''

last_solved     = "2026-08-19"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["array", "sorting", "quicksort"]

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort()
        
        output = []

        curr_start, curr_end = intervals[0][0], intervals[0][1]
        for next_start, next_end in intervals[1:]:
            if max(curr_start, next_start) <= min(curr_end, next_end):
                curr_start = min(curr_start, next_start)
                curr_end = max(curr_end, next_end)
            else:
                output.append([curr_start, curr_end])
                curr_start, curr_end = next_start, next_end
        
        output.append([curr_start, curr_end])

        return output

