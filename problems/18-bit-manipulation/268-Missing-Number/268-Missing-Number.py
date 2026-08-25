'''
https://leetcode.com/problems/missing-number/
'''

last_solved     = "2026-08-20"
revisit_in_days = 43
times_reviewed  = 3
difficulty      = "easy"
topic_tags      = ["array", "hash-table", "math", "binary-search", "bit-manipulation", "sorting"]

class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        return (len(nums) * (len(nums) + 1) // 2) - sum(nums)
