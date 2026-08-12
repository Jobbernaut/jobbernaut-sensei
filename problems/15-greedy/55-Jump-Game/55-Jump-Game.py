'''
https://leetcode.com/problems/jump-game/
'''

last_solved     = "2026-08-12"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["greedy"]

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        farthest = 0

        for idx, n in enumerate(nums):
            if idx > farthest:
                return False
            farthest = max(farthest, idx + n)
        
        return farthest >= len(nums) - 1

