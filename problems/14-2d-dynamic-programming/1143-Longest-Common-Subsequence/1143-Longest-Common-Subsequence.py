'''
https://leetcode.com/problems/longest-common-subsequence/
'''

last_solved     = "2026-08-14"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["string", "dynamic-programming", "longest-common-subsequence"]

class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        memo = {}

        def lcs(i, j):
            if (i, j) in memo:
                return memo[(i, j)]
            elif i == len(text1) or j == len(text2):
                memo[(i, j)] = 0
            elif text1[i] == text2[j]:
                memo[(i, j)] = 1 + lcs(i + 1, j + 1)
            else:
                memo[(i, j)] = max(lcs(i + 1, j), lcs(i, j + 1))

            return memo[(i, j)]

        return lcs(0, 0)
