'''
https://leetcode.com/problems/koko-eating-bananas/
'''

last_solved     = "2026-07-07"
revisit_in_days = 55
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["binary-search"]

from math import ceil
from typing import List

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        def cost(k):
            return sum(ceil(pile / k) for pile in piles)

        left, right = 1, max(piles)

        final_k = 0

        while left <= right:
            local_k = (left + right) // 2

            valid_k = cost(local_k)

            if valid_k <= h:
                final_k = local_k
                right = local_k - 1
            else:
                left = local_k + 1
        
        return final_k
