'''
https://leetcode.com/problems/3sum/
'''

last_solved     = "2026-07-01"
revisit_in_days = 89
difficulty      = "medium"
topic_tags      = ["two-pointers", "array"]
times_reviewed  = 5

class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        output = []

        nums.sort()
        for idx, num in enumerate(nums):
            if idx > 0 and nums[idx] == nums[idx - 1]:
                continue
            target = -num
            left, right = idx + 1, len(nums) - 1
            while left < right:
                local = nums[left] + nums[right]
                if local == target:
                    output.append([nums[idx], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    while left < right and nums[right] == nums[right + 1]:
                        right -= 1
                elif local < target:
                    left += 1
                else:
                    right -= 1
        
        return output
