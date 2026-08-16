'''
https://leetcode.com/problems/happy-number/
'''

last_solved     = "2026-08-16"
revisit_in_days = 5
difficulty      = "easy"
topic_tags      = ["math"]
times_reviewed  = 7

class Solution:
    def isHappy(self, n: int) -> bool:
        def make_happy(n):
            happy = 0
            while n:
                happy += (n % 10)**2
                n //= 10
            return happy
        
        slow = fast = n

        while True:
            slow = make_happy(slow)
            fast = make_happy(make_happy(fast))

            if slow == 1 or fast == 1:
                return True

            if slow == fast:
                return False
