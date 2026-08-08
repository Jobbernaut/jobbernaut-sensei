'''
https://leetcode.com/problems/decode-ways/
'''

last_solved     = "2026-08-08"
revisit_in_days = 7
times_reviewed  = 3
difficulty      = "medium"
topic_tags      = ["dynamic-programming"]

class Solution:
    def numDecodings(self, s: str) -> int:
        prev_2 = 1
        prev_1 = 0 if s[0] == "0" else 1

        for idx in range(1, len(s)):
            curr = (prev_2 if 10 <= int(s[idx-1:idx+1]) <= 26 else 0) + (prev_1 if 1 <= int(s[idx]) <= 9 else 0)
            prev_2 = prev_1
            prev_1 = curr
        
        return prev_1
