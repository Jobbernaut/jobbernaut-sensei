'''
https://leetcode.com/problems/longest-common-subsequence/
'''

last_solved     = "2026-08-19"
revisit_in_days = 2
times_reviewed  = 3
difficulty      = "medium"
topic_tags      = ["string", "dynamic-programming", "longest-common-subsequence"]

class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def lcs(i, j):
            if i == len(text1) or j == len(text2):
                return 0
            elif text1[i] == text2[j]:
                return 1 + lcs(i+1, j+1)
            else:
                return max(lcs(i+1, j), lcs(i, j+1))
        
        return lcs(0, 0)
