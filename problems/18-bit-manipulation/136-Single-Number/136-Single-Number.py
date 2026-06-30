'''
https://leetcode.com/problems/single-number/
'''

last_solved     = "2026-06-30"
revisit_in_days = 7
difficulty      = "easy"
topic_tags      = ["bit-manipulation"]

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        res = 0
        for num in nums: res ^= num
        return res

# Time:  O(N) — single pass through the array
# Space: O(1) — one extra variable
# Key insight: a ^ a = 0, a ^ 0 = a → all duplicates cancel, lone element survives
