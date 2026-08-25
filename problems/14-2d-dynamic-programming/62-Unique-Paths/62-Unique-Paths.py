'''
https://leetcode.com/problems/unique-paths/
'''

last_solved     = "2026-08-24"
revisit_in_days = 1
times_reviewed  = 4
difficulty      = "medium"
topic_tags      = ["math", "dynamic-programming", "combinatorics"]

# Note that the dp array holds the values from
# the previous iterations before its value
# is updated in place.
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        dp = [0] * n

        for i in range(m):
            for j in range(n):
                if i == 0 or j == 0:
                    dp[j] = 1
                else:
                    dp[j] += dp[j - 1]

        return dp[-1]
