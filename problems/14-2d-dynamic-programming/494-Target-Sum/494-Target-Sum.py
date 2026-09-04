'''
https://leetcode.com/problems/target-sum/
'''

last_solved     = "2026-09-04"
revisit_in_days = 7
times_reviewed  = 4
difficulty      = "medium"
topic_tags      = ["array", "dynamic-programming", "backtracking", "knapsack-problem", "0-1-knapsack"]

from functools import lru_cache

class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        @lru_cache(maxsize=None)
        def target_sum(curr_sum, idx):
            if idx == len(nums):
                return 1 if curr_sum == target else 0

            return target_sum(curr_sum - nums[idx], idx + 1) + target_sum(curr_sum + nums[idx], idx + 1)

        return target_sum(0, 0)
