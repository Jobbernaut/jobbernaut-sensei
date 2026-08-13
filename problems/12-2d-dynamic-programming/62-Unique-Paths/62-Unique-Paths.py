'''
https://leetcode.com/problems/unique-paths/
'''

last_solved     = "2026-08-13"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["math", "dynamic-programming", "combinatorics"]

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [[0] * n for _ in range(m)]
        
        for row in range(m):
            for col in range(n):
                if row > 0 and col > 0:
                    dp[row][col] = dp[row - 1][col] + dp[row][col - 1]
                else:
                    dp[row][col] = 1
        
        return dp[m - 1][n - 1]
