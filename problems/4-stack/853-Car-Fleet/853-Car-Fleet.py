'''
https://leetcode.com/problems/car-fleet/description/
'''

last_solved     = "2026-06-15"
revisit_in_days = 55
difficulty      = "medium"
topic_tags      = ["stack", "monotonic-stack"]
times_reviewed  = 5

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        stack = []
        zipped = sorted(list(zip(position, speed)), reverse=True)
        
        for pos, spd in zipped:
            time_to_target = (target - pos) / spd

            if not stack or stack[-1] < time_to_target:
                stack.append(time_to_target)

        return len(stack)