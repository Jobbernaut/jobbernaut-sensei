'''
https://leetcode.com/problems/interleaving-string/
'''

last_solved     = "2026-09-01"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["string", "dynamic-programming"]

class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:

        if len(s3) != len(s1) + len(s2):
            return False

        dp = []
        for i in range(len(s1)+1):
            row = []
            for j in range(len(s2)+1):
                if not i and not j:
                    row.append(True)
                elif not i and j:
                    if row[j-1] and s2[j-1] == s3[j-1]:
                        row.append(True)
                    else:
                        row.append(False)
                elif i and not j:
                    if dp[i-1][j] and s1[i-1] == s3[i-1]:
                        row.append(True)
                    else:
                        row.append(False)
                else:
                    if (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or (row[j-1] and s2[j-1] == s3[i+j-1]):
                        row.append(True)
                    else:
                        row.append(False)
            dp.append(row)

        return dp[-1][-1]
