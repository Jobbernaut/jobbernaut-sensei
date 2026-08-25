'''
https://leetcode.com/problems/reverse-bits/
'''

last_solved     = "2026-08-22"
revisit_in_days = 3
times_reviewed  = 5
difficulty      = "easy"
topic_tags      = ["divide-and-conquer", "bit-manipulation"]

class Solution:
    def reverseBits(self, n: int) -> int:
        r = 0

        for _ in range(32):
            bit = n & 1
            r = (r << 1) | bit
            n >>= 1
        
        return r
