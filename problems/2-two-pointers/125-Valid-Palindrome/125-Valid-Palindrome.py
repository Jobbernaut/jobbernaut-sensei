'''
https://leetcode.com/problems/valid-palindrome/
'''

last_solved     = "2026-05-27"
revisit_in_days = 90
difficulty      = "easy"
topic_tags      = ["two-pointers", "string"]
times_reviewed  = 5

class Solution:
    def isPalindrome(self, s: str) -> bool:
        left, right = 0, len(s) - 1

        while left <= right:
            if not s[left].isalnum():
                left += 1
                continue
            if not s[right].isalnum():
                right -= 1
                continue

            if s[left].lower() != s[right].lower():
                return False

            left += 1
            right -= 1
        
        return True