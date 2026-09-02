'''
https://leetcode.com/problems/permutations/
'''

last_solved     = "2026-09-02"
revisit_in_days = 43
times_reviewed  = 8
difficulty      = "medium"
topic_tags      = ["backtracking", "recursion"]

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        output = []

        def backtrack(curr, pending):
            if len(curr) == len(nums):
                output.append(list(curr))
                return

            for num in list(pending):
                curr.append(num)
                pending.remove(num)
                backtrack(curr, pending)
                pending.add(curr.pop())

        backtrack([], set(nums))

        return output
