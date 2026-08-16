'''
https://leetcode.com/problems/reverse-bits/
'''

last_solved     = "2026-08-16"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "easy"
topic_tags      = ["divide-and-conquer", "bit-manipulation"]

class Solution:
    def reverseBits(self, n: int) -> int:
        rev = 0
        for _ in range(32):
            rev = (rev << 1) | (n & 1)
            n >>= 1
        return rev
