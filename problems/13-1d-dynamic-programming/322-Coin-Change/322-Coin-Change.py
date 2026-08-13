'''
https://leetcode.com/problems/coin-change/
'''

last_solved     = "2026-08-13"
revisit_in_days = 7
times_reviewed  = 3
difficulty      = "medium"
topic_tags      = ["dynamic-programming"]

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0

        for amt in range(1, amount + 1):
            min_coins = float('inf')

            for d in coins:
                if d <= amt:
                    min_coins = min(min_coins, 1 + dp[amt - d])
            
            dp[amt] = min_coins
        
        if isinf(dp[amount]):
            return -1
        
        return dp[amount]
