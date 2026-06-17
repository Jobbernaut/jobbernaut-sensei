'''
https://leetcode.com/problems/house-robber-ii/
'''

last_solved     = "2026-06-16"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["dynamic-programming"]
times_reviewed  = 0

class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]

        def house_robber(arr):
            prev2 = arr[0]
            prev1 = max(arr[0:2], default=0)

            for idx in range(2, len(arr)):
                curr = max(prev1, arr[idx] + prev2)
                prev2 = prev1
                prev1 = curr

            return max(prev1, prev2)

        return max(house_robber(nums[0:len(nums) - 1]), house_robber(nums[1:len(nums)]))