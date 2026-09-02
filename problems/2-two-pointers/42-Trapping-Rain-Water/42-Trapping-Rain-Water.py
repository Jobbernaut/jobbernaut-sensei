'''
https://leetcode.com/problems/trapping-rain-water/
'''

last_solved     = "2026-09-02"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "hard"
topic_tags      = ["array", "two-pointers", "dynamic-programming", "stack", "monotonic-stack"]

class Solution:
    def trap(self, height: List[int]) -> int:
        rain_water = 0
        left, right = 0, len(height) - 1
        max_left, max_right = float('-inf'), float('-inf')

        while left <= right:
            max_left, max_right = max(max_left, height[left]), max(max_right, height[right])

            if max_left < max_right:
                rain_water += (max_left - height[left])
                left += 1
            else:
                rain_water += (max_right - height[right])
                right -= 1

        return rain_water
