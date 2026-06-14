'''
https://leetcode.com/problems/permutations/
'''

last_solved     = "2026-06-14"
revisit_in_days = 1
difficulty      = "medium"
topic_tags      = ["backtracking", "recursion"]

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        self.output = []

        def backtrack(curr, available):
            if not len(available):
                self.output.append(list(curr))
                return
            
            for each_elem in list(available):
                curr.append(each_elem)
                available.remove(each_elem)
                backtrack(curr, available)
                available.add(curr.pop())
        
        backtrack([], set(nums))

        return self.output
