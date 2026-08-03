'''
https://leetcode.com/problems/valid-anagram/description/
'''

last_solved     = "2026-08-02"
revisit_in_days = 2
times_reviewed  = 7
difficulty      = "easy"
topic_tags      = ["arrays", "hashing"]

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
