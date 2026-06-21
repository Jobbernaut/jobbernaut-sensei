'''
https://leetcode.com/problems/longest-palindromic-substring/
'''

last_solved     = "2026-06-19"
revisit_in_days = 7
difficulty      = "medium"
topic_tags      = ["dynamic-programming", "strings"]
times_reviewed  = 1

'''
Time: O(N^2) — outer loop O(N) * expand O(N) worst case
Space: O(1) — only pointers tracked, output string excluded
'''
class Solution:
    def longestPalindrome(self, s: str) -> str:
        def expand(left, right):
            while 0 <= left < right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1

            valid_str = s[left+1:right]
            valid_len = right - left - 1

            return valid_str, valid_len
        
        max_len = 1
        max_str = s[0]
        
        for idx in range(len(s) - 1):
            odd_valid_str, odd_valid_len = expand(idx-1, idx+1)
            even_valid_str, even_valid_len = expand(idx, idx + 1)

            if odd_valid_len > max_len:
                max_len = odd_valid_len
                max_str = odd_valid_str
            
            if even_valid_len > max_len:
                max_len = even_valid_len
                max_str = even_valid_str
        
        return max_str
