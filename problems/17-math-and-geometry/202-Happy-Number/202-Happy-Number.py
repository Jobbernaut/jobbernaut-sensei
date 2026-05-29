'''
https://leetcode.com/problems/happy-number/
'''

last_solved     = "2026-05-29"
revisit_in_days = 3
difficulty      = "easy"
topic_tags      = ["math"]
times_reviewed  = 0

class Solution:
    def isHappy(self, n: int) -> bool:
        def sum_of_squares(n):
            sumi = 0
            while n:
                sumi += (n % 10) ** 2
                n = n // 10
            return sumi
        
        lookup_set = set()

        while n not in lookup_set:
            lookup_set.add(n)

            if n == 1:
                return True
            
            n = sum_of_squares(n)
        
        return False