'''
https://leetcode.com/problems/combination-sum/
'''

last_solved     = "2026-08-26"
revisit_in_days = 43
times_reviewed  = 9
difficulty      = "medium"
topic_tags      = ["backtracking", "recursion"]

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        self.output = []

        def backtrack(idx, curr_arr, curr_sum):
            if idx >= len(candidates) or curr_sum > target:
                return 
            elif curr_sum == target:
                self.output.append(list(curr_arr))
                return
            
            curr_arr.append(candidates[idx])
            curr_sum += candidates[idx]

            backtrack(idx, curr_arr, curr_sum)

            curr_sum -= curr_arr.pop()

            backtrack(idx + 1, curr_arr, curr_sum)
        
        backtrack(0, [], 0)

        return self.output
