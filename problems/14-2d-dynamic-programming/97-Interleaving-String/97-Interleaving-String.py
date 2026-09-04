'''
https://leetcode.com/problems/interleaving-string/
'''

last_solved     = "2026-09-04"
revisit_in_days = 7
times_reviewed  = 3
difficulty      = "medium"
topic_tags      = ["string", "dynamic-programming"]

class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:

        if len(s3) != len(s1) + len(s2):
            return False

        prev = []
        row = []

        for i in range(len(s1) + 1):
            prev = row
            row = []

            for j in range(len(s2) + 1):
                if not i and not j:
                    row.append(True)
                elif not i and j:
                    if row[j-1] and s2[j-1] == s3[j-1]:
                        row.append(True)
                    else:
                        row.append(False)
                elif i and not j:
                    if prev[j] and s1[i-1] == s3[i-1]:
                        row.append(True)
                    else:
                        row.append(False)
                else:
                    if prev[j] and s1[i-1] == s3[i+j-1]:
                        row.append(True)
                    elif row[j-1] and s2[j-1] == s3[i+j-1]:
                        row.append(True)
                    else:
                        row.append(False)

        return row[-1]
