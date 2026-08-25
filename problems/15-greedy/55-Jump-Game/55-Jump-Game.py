'''
https://leetcode.com/problems/jump-game/
'''

last_solved     = "2026-08-24"
revisit_in_days = 30
times_reviewed  = 4
difficulty      = "medium"
topic_tags      = ["greedy"]

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        max_idx = 0

        for idx, num in enumerate(nums):
            if max_idx >= len(nums) - 1:
                return True
            
            max_idx = max(max_idx, idx + nums[idx])

            if idx == max_idx:
                return False
        
        return True

