'''
https://leetcode.com/problems/min-cost-climbing-stairs/
'''

last_solved     = "2026-06-03"
revisit_in_days = 3
difficulty      = "easy"
topic_tags      = ["dynamic-programming"]
times_reviewed  = 1

class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        # f(i) = cost[i] + min(f(i-1), f(i-2))
        # base cases: f(0) = cost[0], f(1) = cost[1]
        # answer: min(f(n-1), f(n-2)) — can reach top from either last stair
        prev2 = cost[0]   # f(i-2): two steps back
        prev1 = cost[1]   # f(i-1): one step back

        for i in range(2, len(cost)):
            curr = cost[i] + min(prev1, prev2)
            prev2 = prev1   # slide: 2-back becomes 1-back
            prev1 = curr    # slide: 1-back becomes current

        return min(prev1, prev2)
