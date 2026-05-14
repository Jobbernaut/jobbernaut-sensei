'''
https://leetcode.com/problems/contains-duplicate/
'''

last_solved = "4/May/2026"
revisit_in_days = "3"

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        return not len(set(nums)) == len(nums)