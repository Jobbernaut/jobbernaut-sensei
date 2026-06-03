'''
https://leetcode.com/problems/house-robber/
'''

last_solved     = "2026-06-03"
revisit_in_days = 3
difficulty      = "medium"
topic_tags      = ["dynamic-programming"]
times_reviewed  = 1

class Solution:
    def rob(self, nums: List[int]) -> int:
        # f(i) = max(f(i-1), nums[i] + f(i-2))
        # Choice: skip house i → keep f(i-1), OR rob house i → nums[i] + f(i-2)
        # Base: f(0) = nums[0], f(1) = max(nums[0], nums[1])
        prev2 = nums[0]
        prev1 = max(nums[0:2], default=0)

        for idx in range(2, len(nums)):
            curr = max(prev1, nums[idx] + prev2)
            prev2 = prev1   # slide: 2-back becomes 1-back
            prev1 = curr    # slide: 1-back becomes current

        return prev1
