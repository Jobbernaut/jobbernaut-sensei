'''
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
'''

last_solved     = "2026-08-29"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["array", "dynamic-programming"]

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        holding = -prices[0]
        sold = 0
        cooldown = 0

        for idx in range(1, len(prices)):
            prev_holding, prev_sold, prev_cooldown = holding, sold, cooldown

            holding = max(prev_holding, prev_cooldown - prices[idx])
            sold = prev_holding + prices[idx]
            cooldown = max(prev_cooldown, prev_sold)

        return max(sold, cooldown)
