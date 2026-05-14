'''
https://leetcode.com/problems/contains-duplicate/
'''

last_solved     = "2026-05-04"
revisit_in_days = 3
difficulty      = "easy"
topic_tags      = ["arrays", "hash-set"]

from typing import List

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return not len(set(nums)) == len(nums)
