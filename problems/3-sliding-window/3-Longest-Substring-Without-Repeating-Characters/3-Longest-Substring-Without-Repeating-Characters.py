'''
https://leetcode.com/problems/longest-substring-without-repeating-characters/
'''

last_solved     = "2026-05-27"
revisit_in_days = 61
difficulty      = "medium"
topic_tags      = ["sliding-window", "hash-set"]
times_reviewed  = 1

from typing import List, Optional


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        lookup = set()
        max_len = 0

        left, right = 0, 0
        while right < len(s):
            while s[right] in lookup:
                lookup.remove(s[left])
                left += 1
            lookup.add(s[right])
            max_len = max(max_len, right - left + 1)
            right += 1
        
        return max_len
