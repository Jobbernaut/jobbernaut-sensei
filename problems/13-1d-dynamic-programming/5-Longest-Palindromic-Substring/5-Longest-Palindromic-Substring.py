'''
https://leetcode.com/problems/longest-palindromic-substring/
'''

last_solved     = "2026-06-26"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["dynamic-programming", "strings"]
times_reviewed  = 5

class Solution:
    def longestPalindrome(self, s: str) -> str:
        def expand(left, right):
            while 0 <= left < right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            
            return (right - left - 1, s[left+1:right])

        max_len = 1
        max_s = s[0]

        for idx in range(0, len(s) - 1):
            local_len, local_s = None, None

            odd_len, odd_s = expand(idx - 1, idx + 1)
            even_len, even_s = expand(idx, idx + 1)

            if odd_len >= even_len:
                local_len = odd_len
                local_s = odd_s
            else:
                local_len = even_len
                local_s = even_s
            
            if local_len >= max_len:
                max_len = local_len
                max_s = local_s
        
        return max_s
