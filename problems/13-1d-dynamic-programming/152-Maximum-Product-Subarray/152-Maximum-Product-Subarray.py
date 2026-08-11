'''
https://leetcode.com/problems/maximum-product-subarray/
'''

last_solved     = "2026-08-10"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["dynamic-programming"]

class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        curr_min = 1
        curr_max = 1

        global_max = nums[0]

        for num in nums:
            prev_min = curr_min
            prev_max = curr_max

            curr_min = min(prev_min * num, prev_max * num, num)
            curr_max = max(prev_min * num, prev_max * num, num)

            global_max = max(global_max, curr_max)
        
        return global_max