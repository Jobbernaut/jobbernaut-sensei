'''
https://leetcode.com/problems/car-fleet/description/
'''

last_solved     = "2026-05-05"
revisit_in_days = 3
difficulty      = "medium"
topic_tags      = ["stack", "monotonic-stack"]

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        pairs = sorted(zip(position, speed), reverse=True)
        stack = []

        for pos, spd in pairs:
            time = (target - pos) / spd
            if not stack or time > stack[-1]:
                stack.append(time)

        return len(stack)
