'''
https://leetcode.com/problems/two-sum/description/
'''

last_solved     = "2026-06-03"
revisit_in_days = 3
difficulty      = "easy"
topic_tags      = ["arrays", "hashing"]
times_reviewed  = 1

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashmap = {}
        for idx, num in enumerate(nums):
            if target - num in hashmap:
                return [idx, hashmap[target - num]]
            hashmap[num] = idx
