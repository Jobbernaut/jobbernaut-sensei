'''
https://leetcode.com/problems/contains-duplicate/description/
'''

last_solved     = "2026-05-04"
revisit_in_days = 90
difficulty      = "easy"
topic_tags      = ["arrays", "hashing"]

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return not len(set(nums)) == len(nums)
