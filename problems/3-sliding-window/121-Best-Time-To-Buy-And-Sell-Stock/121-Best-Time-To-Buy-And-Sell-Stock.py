'''
https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
'''

last_solved     = "2026-05-29"
revisit_in_days = 90
difficulty      = "easy"
topic_tags      = ["sliding-window", "stock"]
times_reviewed  = 1

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        left, right = 0, 0

        max_profit = 0

        while left <= right and right < len(prices):
            if prices[right] - prices[left] > 0:
                max_profit = max(max_profit, prices[right] - prices[left])
            else:
                left = right
            right += 1
        
        return max_profit
