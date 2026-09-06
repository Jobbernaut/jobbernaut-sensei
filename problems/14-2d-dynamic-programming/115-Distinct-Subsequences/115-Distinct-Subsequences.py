'''
https://leetcode.com/problems/distinct-subsequences/
'''

last_solved     = "2026-09-06"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "hard"
topic_tags      = ["string", "dynamic-programming"]

class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        from functools import lru_cache

        @lru_cache(maxsize=None)
        def dp(s_idx, t_idx):
            if s_idx == len(s) or t_idx == len(t):
                if t_idx == len(t):
                    return 1
                return 0

            if s[s_idx] == t[t_idx]:
                return dp(s_idx + 1, t_idx + 1) + dp(s_idx + 1, t_idx)

            return dp(s_idx + 1, t_idx)

        return dp(0, 0)
