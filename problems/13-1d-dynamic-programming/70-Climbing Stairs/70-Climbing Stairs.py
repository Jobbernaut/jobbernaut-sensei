'''
https://leetcode.com/problems/climbing-stairs/
'''

last_solved     = "2026-05-27"
revisit_in_days = 7
difficulty      = "easy"
topic_tags      = ["dynamic-programming", "recursion", "memoization"]
times_reviewed  = 1

class Solution:
    def climbStairs(self, n: int) -> int:
        """
        Find number of ways to climb n stairs when you can take 1 or 2 steps at a time.
        
        DP PATTERN:
        ways(n) = ways(n-1) + ways(n-2)
        
        Why? To reach stair n, you must come from either:
        - stair (n-1): take 1 step → all ways to reach (n-1)
        - stair (n-2): take 2 steps → all ways to reach (n-2)
        Total = ways(n-1) + ways(n-2)
        
        EXAMPLES:
        n=1: 1 way → (1)
        n=2: 2 ways → (1+1), (2)
        n=3: 3 ways → (1+1+1), (1+2), (2+1) = ways(2) + ways(1) = 2+1 = 3
        n=4: 5 ways → ways(3) + ways(2) = 3+2 = 5
        
        MEMOIZATION:
        - self.dp[k] stores the answer for ways(k)
        - Before recalculating ways(k), check if self.dp[k] already has it
        - If yes: return immediately (O(1) lookup)
        - If no: calculate, store, then return
        
        Time: O(n), Space: O(n) for dp array + recursion stack
        """
        self.dp = [0] * (n + 1)

        def ways(k):
            # Base cases
            if k == 0:
                return 0
            elif k == 1:
                return 1
            elif k == 2:
                return 2
            
            # Memoization check: if we already computed ways(k), return it
            if self.dp[k]:
                return self.dp[k]
            
            # Recursive case: ways(k) = ways(k-1) + ways(k-2)
            res = ways(k - 1) + ways(k - 2)

            # Store result so we don't recalculate it later
            self.dp[k] = res

            return res
        
        return ways(n)
