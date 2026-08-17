'''
https://leetcode.com/problems/counting-bits/
'''

last_solved     = "2026-08-17"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "easy"
topic_tags      = ["dynamic-programming", "bit-manipulation"]

class Solution:
    def countBits(self, n: int) -> List[int]:
        dp = [0] * (n + 1)

        for i in range(1, n + 1):
            dp[i] = dp[i & (i - 1)] + 1

        return dp
