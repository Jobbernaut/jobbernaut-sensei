'''
https://leetcode.com/problems/coin-change/
'''

last_solved     = "2026-08-20"
revisit_in_days = 30
times_reviewed  = 4
difficulty      = "medium"
topic_tags      = ["dynamic-programming"]

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for d in coins:
            for amt in range(1, amount + 1):
                if d <= amt:
                    dp[amt] = min(dp[amt], 1 + dp[amt - d])
        
        if isinf(dp[amount]):
            return -1

        return dp[amount]
