'''
https://leetcode.com/problems/unique-paths/
'''

last_solved     = "2026-08-14"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["math", "dynamic-programming", "combinatorics"]

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [1] * n

        for row in range(1, m):
            for col in range(1, n):
                dp[col] += dp[col - 1]
        
        return dp[-1]
