'''
https://leetcode.com/problems/palindromic-substrings/
'''

last_solved     = "2026-07-19"
revisit_in_days = 13
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["dynamic-programming", "strings"]

class Solution:
    def countSubstrings(self, s: str) -> int:
        def expand(left, right):
            cnt = 1 if right - left == 1 else 0

            while 0 <= left < right < len(s) and s[left] == s[right]:
                cnt += 1
                left -= 1
                right += 1
            
            return cnt
        
        total_cnt = 0
        for idx in range(len(s)):
            total_cnt += (expand(idx, idx + 1) + expand(idx - 1, idx + 1))
        
        return total_cnt
