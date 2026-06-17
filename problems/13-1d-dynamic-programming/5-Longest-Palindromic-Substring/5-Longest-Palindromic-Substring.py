'''
https://leetcode.com/problems/longest-palindromic-substring/
'''

last_solved     = "2026-06-16"
revisit_in_days = 3
difficulty      = "medium"
topic_tags      = ["dynamic-programming", "strings"]
times_reviewed  = 1

'''
Space: O(N^2)
Time: O(1) if output is not considered, O(N) if output is considered
'''
class Solution:
    def longestPalindrome(self, s: str) -> str:
        def is_palindrome(l_c, r_c):
            left, right = l_c, r_c
            length = -1 if l_c == r_c else 0
            while left >= 0 and right < len(s) and s[left] == s[right]:
                length += 2
                left -= 1
                right += 1
            return length, left + 1, right - 1
        
        max_pal_substr = 1
        max_substr = s[0]

        for i in range(0, len(s)):
                curr, l, r = is_palindrome(i, i)
                if curr > max_pal_substr:
                    max_pal_substr = curr
                    max_substr = s[l:r+1]
                n_curr, n_l, n_r = is_palindrome(i, i + 1)
                if n_curr > max_pal_substr:
                    max_pal_substr = n_curr
                    max_substr = s[n_l:n_r+1]
        
        return max_substr
