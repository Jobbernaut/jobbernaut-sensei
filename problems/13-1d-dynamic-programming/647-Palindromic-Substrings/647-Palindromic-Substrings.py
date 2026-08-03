'''
https://leetcode.com/problems/palindromic-substrings/
'''

last_solved     = "2026-08-03"
revisit_in_days = 45
times_reviewed  = 8
difficulty      = "medium"
topic_tags      = ["dynamic-programming", "strings"]

class Solution:
    def countSubstrings(self, s: str) -> int:
        def expand(left, right):
            cnt = 0

            while 0 <= left <= right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
                cnt += 1
            
            return cnt
        
        cnt = 0
        for idx in range(len(s)):
            cnt += (expand(idx, idx) + expand(idx, idx + 1))
        
        return cnt
