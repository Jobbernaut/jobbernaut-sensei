'''
https://leetcode.com/problems/valid-anagram/description/
'''

last_solved     = "2026-05-04"
revisit_in_days = 90
times_reviewed  = 6
difficulty      = "easy"
topic_tags      = ["arrays", "hashing"]

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        return Counter(s) == Counter(t)
