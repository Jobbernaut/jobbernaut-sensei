'''
https://leetcode.com/problems/two-sum/description/
'''

last_solved     = "2026-08-05"
revisit_in_days = 45
difficulty      = "easy"
topic_tags      = ["arrays", "hashing"]
times_reviewed  = 6

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        hashmap = {}
        for idx, num in enumerate(nums):
            if target - num in hashmap:
                return [idx, hashmap[target - num]]
            hashmap[num] = idx

'''
target = 12
0,1 | 3,3 | 5,1 | 8,4 | 10,2
[12, 3, 7]
'''
