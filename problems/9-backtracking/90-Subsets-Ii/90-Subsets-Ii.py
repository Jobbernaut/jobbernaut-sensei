'''
https://leetcode.com/problems/subsets-ii/
'''

last_solved     = "2026-06-21"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["backtracking", "recursion"]

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()

        self.output = []

        def backtrack(idx, curr):
            if idx == len(nums):
                self.output.append(list(curr))
                return
            
            curr.append(nums[idx])
            backtrack(idx + 1, curr)
            curr.pop()

            while idx < len(nums) - 1 and nums[idx] == nums[idx + 1]:
                idx += 1
            backtrack(idx + 1, curr)

        backtrack(0, [])

        return self.output 
