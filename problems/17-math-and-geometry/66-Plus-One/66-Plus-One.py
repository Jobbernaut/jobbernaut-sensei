'''
https://leetcode.com/problems/plus-one/
'''

last_solved     = "2026-05-29"
revisit_in_days = 3
difficulty      = "easy"
topic_tags      = ["math"]
times_reviewed  = 0

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        carry = 0

        for idx in range(len(digits) - 1, -1, -1):
            if digits[idx] == 9:
                digits[idx] = 0
                carry = 1
            else:
                digits[idx] += 1
                carry = 0
                break
            if not carry:
                break
        
        if not carry:
            return digits
        else:
            return [1] + digits