'''
https://leetcode.com/problems/number-of-1-bits/
'''

last_solved     = "2026-08-17"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "easy"
topic_tags      = ["divide-and-conquer", "bit-manipulation"]

class Solution:
    def hammingWeight(self, n: int) -> int:
        def divide(n):
            cnt = 0
            while n:
                r = n % 2
                if r:
                    cnt += 1
                n = n // 2
            return cnt

        def bit_flip(n):
            cnt = 0
            while n:
                n = n & (n - 1)
                cnt += 1
            return cnt
        
        return bit_flip(n)
