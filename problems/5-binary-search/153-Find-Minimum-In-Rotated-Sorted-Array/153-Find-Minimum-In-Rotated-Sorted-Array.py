'''
https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
'''

last_solved     = "2026-06-29"
revisit_in_days = 3
difficulty      = "medium"
topic_tags      = ["binary-search"]
times_reviewed  = 2

class Solution:
    def findMin(self, nums: List[int]) -> int:
        left, right = 0, len(nums) - 1

        while left < right:
            mid = (left + right) // 2

            if nums[mid] > nums[right]:
                left = mid + 1
            else:
                right = mid
        
        return nums[left]
