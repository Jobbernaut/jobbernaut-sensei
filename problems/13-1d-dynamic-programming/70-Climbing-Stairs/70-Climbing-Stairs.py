'''
https://leetcode.com/problems/climbing-stairs/
'''

last_solved     = "2026-06-03"
revisit_in_days = 7
difficulty      = "easy"
topic_tags      = ["dynamic-programming", "recursion", "memoization"]
times_reviewed  = 2


'''
Naive Solution
'''
class Solution:
    def climbStairs(self, n: int) -> int:
        def climb(n):
            if n == 1:
                return 1
            elif n == 2:
                return 2
            
            return climb(n - 1) + climb(n - 2)
        
        return climb(n)

'''
Memoized Solution
'''
class Solution:
    def climbStairs(self, n: int) -> int:
        self.cache = {}

        def climb(n):
            if n in self.cache:
                return self.cache[n]
            if n <= 2:
                return n

            self.cache[n] = climb(n - 1) + climb(n - 2)

            return self.cache[n]
        
        return climb(n)

'''
O(1) Optimized Solution
'''
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2:
            return n

        prev2 = 1   # f(1)
        prev1 = 2   # f(2)

        for i in range(3, n + 1):
            curr = prev1 + prev2
            prev2 = prev1   # slide: 2-back becomes 1-back
            prev1 = curr    # slide: 1-back becomes current

        return prev1
