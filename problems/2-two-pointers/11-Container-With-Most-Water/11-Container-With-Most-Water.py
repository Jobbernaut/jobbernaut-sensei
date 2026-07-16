'''
https://leetcode.com/problems/container-with-most-water/
'''

last_solved     = "2026-06-17"
revisit_in_days = 30
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["two-pointers"]

class Solution:
    def maxArea(self, height: List[int]) -> int:
        left, right = 0, len(height) - 1
        maxi = float('-inf')

        while left < right:
            maxi = max(maxi, min(height[left], height[right]) * (right - left))

            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        
        return maxi
