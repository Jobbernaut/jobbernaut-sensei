'''
https://leetcode.com/problems/combination-sum-ii/
'''

last_solved     = "2026-08-02"
revisit_in_days = 6
times_reviewed  = 7
difficulty      = "medium"
topic_tags      = ["backtracking", "recursion"]

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        freq_arr = [[candidate, freq] for candidate, freq in Counter(candidates).items()]

        self.output = []

        def backtrack(idx, curr_arr, curr_sum):
            if curr_sum >= target or idx == len(freq_arr):
                if curr_sum == target:
                    self.output.append(list(curr_arr))
                return
            
            if freq_arr[idx][1] > 0:
                curr_arr.append(freq_arr[idx][0])
                curr_sum += freq_arr[idx][0]
                freq_arr[idx][1] -= 1
                backtrack(idx, curr_arr, curr_sum)
                curr_sum -= curr_arr.pop()
                freq_arr[idx][1] += 1
            
            backtrack(idx + 1, curr_arr, curr_sum)
        
        backtrack(0, [], 0)

        return self.output