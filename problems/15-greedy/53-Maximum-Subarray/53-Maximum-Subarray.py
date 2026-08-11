'''
https://leetcode.com/problems/maximum-subarray/
'''

last_solved     = "2026-08-11"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["dynamic-programming", "greedy"]

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        curr_max = 0
        global_max = min(nums)

        for n in nums:
            curr_max += n
            
            global_max = max(global_max, curr_max)

            if curr_max < 0:
                curr_max = 0
        
        return global_max
