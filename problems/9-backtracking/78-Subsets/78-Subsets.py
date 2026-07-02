'''
https://leetcode.com/problems/subsets/
'''

last_solved     = "2026-07-01"
revisit_in_days = 90
difficulty      = "medium"
topic_tags      = ["backtracking"]
times_reviewed  = 1

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        self.res = []

        def backtrack(index, curr):
            if index == len(nums):
                self.res.append(list(curr))
                return
            
            curr.append(nums[index])
            backtrack(index + 1, curr)
            curr.pop()
            backtrack(index + 1, curr)
        
        backtrack(0, [])

        return self.res