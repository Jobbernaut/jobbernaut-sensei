'''
https://leetcode.com/problems/gas-station/
'''

last_solved     = "2026-09-04"
revisit_in_days = 7
times_reviewed  = 3
difficulty      = "medium"
topic_tags      = ["array", "greedy"]

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        if sum(gas) < sum(cost): return -1

        start, tank = 0, 0

        for idx in range(len(gas)):
            tank += (gas[idx] - cost[idx])

            if tank < 0:
                start = idx + 1
                tank = 0

        return start
    