'''
https://leetcode.com/problems/search-in-rotated-sorted-array/
'''

last_solved     = "2026-07-16"
revisit_in_days = 44
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["binary-search"]

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] > nums[right]:
                if nums[left] <= target < nums[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
            else:
                if nums[mid] < target <= nums[right]:
                    left = mid + 1
                else:
                    right = mid - 1
        
        return -1