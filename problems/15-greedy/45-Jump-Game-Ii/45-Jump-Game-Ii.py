'''
https://leetcode.com/problems/jump-game-ii/
'''

last_solved     = "2026-08-13"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["array", "dynamic-programming", "greedy"]

class Solution:
    def jump(self, nums: List[int]) -> int:
        current_end = 0
        farthest = nums[0]
        jumps = 0

        for idx in range(0, len(nums) - 1):
            farthest = max(farthest, idx + nums[idx])

            if idx == current_end:
                jumps += 1
                current_end = farthest
        
        return jumps
