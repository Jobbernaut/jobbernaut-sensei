'''
https://leetcode.com/problems/product-of-array-except-self/description/
'''

last_solved     = "2026-06-15"
revisit_in_days = 103
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["arrays", "hashing"]

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        output = []

        prod = 1
        for idx in range(len(nums)):
            output.append(prod)
            prod *= nums[idx]
        
        prod = 1
        for idx in range(len(nums) - 1, -1, -1):
            output[idx] *= prod
            prod *= nums[idx]

        return output
