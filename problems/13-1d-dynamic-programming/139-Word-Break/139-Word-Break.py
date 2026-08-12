'''
https://leetcode.com/problems/word-break/
'''

last_solved     = "2026-08-12"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["dynamic-programming"]

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        dp = [False] * (len(s) + 1)
        dp[0] = True

        lookup = set(wordDict)

        for i in range(1, len(s) + 1):
            for j in range(i - 1, -1, -1):
                if dp[j] and s[j:i] in lookup:
                    dp[i] = True
                    break
        
        return dp[-1]
