'''
https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
'''

last_solved     = "2026-09-02"
revisit_in_days = 7
times_reviewed  = 3
difficulty      = "medium"
topic_tags      = ["array", "dynamic-programming"]

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        hold, sold, cooldown = -prices[0], float('-inf'), 0

        for price in prices:
            prev_hold, prev_sold, prev_cooldown = hold, sold, cooldown

            hold = max(prev_hold, prev_cooldown - price)
            sold = prev_hold + price
            cooldown = max(prev_sold, prev_cooldown)

        return max(sold, cooldown)
