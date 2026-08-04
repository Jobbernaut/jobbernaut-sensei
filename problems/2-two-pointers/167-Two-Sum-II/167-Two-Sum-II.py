'''
https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/
'''

last_solved     = "2026-05-28"
revisit_in_days = 117
difficulty      = "medium"
topic_tags      = ["two-pointers", "array"]
times_reviewed  = 5

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left, right = 0, len(numbers) - 1

        while left < right:
            local = numbers[left] + numbers[right]

            if local == target:
                return [left + 1, right + 1]
            elif local < target:
                left += 1
            else:
                right -= 1
