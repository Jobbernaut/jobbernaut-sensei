'''
https://leetcode.com/problems/longest-palindromic-substring/
'''

last_solved     = "2026-07-27"
revisit_in_days = 89
difficulty      = "medium"
topic_tags      = ["dynamic-programming", "strings"]
times_reviewed  = 6

class Solution:
    def longestPalindrome(self, s: str) -> str:
        def expand(left, right):
            while 0 <= left <= right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            
            return s[left+1:right]
        
        max_str = s[0]
        for idx in range(len(s)):
            odd_str, even_str = expand(idx, idx), expand(idx, idx + 1)
            max_str = max(max_str, odd_str, even_str, key=len)
        
        return max_str