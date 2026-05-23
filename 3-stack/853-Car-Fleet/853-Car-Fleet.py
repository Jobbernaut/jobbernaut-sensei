'''
https://leetcode.com/problems/car-fleet/description/
'''

last_solved     = "2026-05-23"
revisit_in_days = 7
difficulty      = "medium"
topic_tags      = ["stack", "monotonic-stack"]

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        stack = []

        pos_spd_sorted = sorted(list(zip(position, speed)), reverse=True)

        for pos, spd in pos_spd_sorted:
            arrival_time = (target - pos) / spd

            if stack and arrival_time <= stack[-1]:
                continue
            
            stack.append(arrival_time)

        return len(stack)