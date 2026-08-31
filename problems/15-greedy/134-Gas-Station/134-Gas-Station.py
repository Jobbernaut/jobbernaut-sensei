'''
https://leetcode.com/problems/gas-station/
'''

last_solved     = "2026-08-28"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["array", "greedy"]

class Solution:
    def canCompleteCircuit(self, gas: List[int], cost: List[int]) -> int:
        if sum(gas) < sum(cost):
            return -1
        
        n = len(gas)

        start = 0

        tank = 0
        for i in range(0, n):
            tank += gas[i]
            tank -= cost[i]

            if tank < 0:
                start = i + 1
                tank = 0
        
        return start
    