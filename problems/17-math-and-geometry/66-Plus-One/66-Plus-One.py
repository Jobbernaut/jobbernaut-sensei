'''
https://leetcode.com/problems/plus-one/
'''

last_solved     = "2026-06-01"
revisit_in_days = 90
difficulty      = "easy"
topic_tags      = ["math"]
times_reviewed  = 1

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        for idx in range(len(digits) - 1, -1, -1):
            if digits[idx] == 9:
                digits[idx] = 0
            else:
                digits[idx] += 1
                break
        
        if digits[0] == 0:
            return [1] + digits
        
        return digits
