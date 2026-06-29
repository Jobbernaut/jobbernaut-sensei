'''
https://leetcode.com/problems/search-in-rotated-sorted-array/
'''

last_solved     = "2026-06-29"
revisit_in_days = 3
difficulty      = "medium"
topic_tags      = ["binary-search"]

class Solution:
    def search(self, nums: List[int], target: int) -> int:
            left, right = 0, len(nums) - 1

            while left < right:
                mid = (left + right) // 2

                if nums[mid] <= nums[right]:
                    right = mid
                else:
                    left = mid + 1
            
            def b_search(left, right, target):
                while left <= right:
                    mid = (left + right) // 2

                    if nums[mid] == target:
                        return mid
                    elif nums[mid] > target:
                        right = mid - 1
                    else:
                        left = mid + 1
                
                return -1 

            search_left = b_search(0, left - 1, target)
            search_right = b_search(left, len(nums) - 1, target)

            if search_left == -1 and search_right == -1:
                return -1
            elif search_left != -1:
                return search_left
            else:
                return search_right