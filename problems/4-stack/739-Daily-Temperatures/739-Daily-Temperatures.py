'''
https://leetcode.com/problems/daily-temperatures/description/
'''

last_solved     = "2026-06-28"
revisit_in_days = 30
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["stack", "monotonic-stack"]

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        n = len(temperatures)
        answer = [0] * n
        stack = []
        
        for curr_day, curr_temp in enumerate(temperatures):
            while stack and temperatures[stack[-1]] < curr_temp:
                prev_day = stack.pop()
                answer[prev_day] = curr_day - prev_day
            stack.append(curr_day)
        
        return answer
