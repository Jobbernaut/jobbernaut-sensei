'''
https://leetcode.com/problems/find-the-duplicate-number/
'''

last_solved     = "2026-08-07"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["linked-list", "two-pointers"]

class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow, fast = 0, 0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]

            if slow == fast:
                break

        slow = 0
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]

        return slow
