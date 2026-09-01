'''
https://leetcode.com/problems/gas-station/
'''

last_solved     = "2026-09-01"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["array", "greedy"]

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        if sum(gas) < sum(cost): return -1

        start = 0
        tank = 0
        for idx in range(len(gas)):
            g, c = gas[idx], cost[idx]
            tank += (g - c)

            if tank < 0:
                start = idx + 1
                tank = 0

        return start
    