'''
https://leetcode.com/problems/permutation-in-string/
'''

last_solved     = "2026-06-05"
revisit_in_days = 7
difficulty      = "medium"
topic_tags      = ["sliding-window", "hash-map"]
times_reviewed  = 2

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        s1_sig = [0] * 26
        s2_sig = [0] * 26

        for c in s1:
            s1_sig[ord(c) - ord('a')] += 1
        
        left = right = 0
        while left <= right and right < len(s2):
            s2_sig[ord(s2[right]) - ord('a')] += 1

            if right - left + 1 > len(s1):
                s2_sig[ord(s2[left]) - ord('a')] -= 1
                left += 1
            if right - left + 1 == len(s1):
                if s1_sig == s2_sig:
                    return True

            right += 1
        
        return False
