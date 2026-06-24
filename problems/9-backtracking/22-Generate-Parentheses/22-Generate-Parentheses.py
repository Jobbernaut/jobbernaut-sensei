'''
https://leetcode.com/problems/generate-parentheses/
'''

last_solved     = "2026-06-24"
revisit_in_days = 7
difficulty      = "medium"
topic_tags      = ["backtracking", "recursion"]

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        self.output = []

        def gen_par(open, close, par):
            if open == n and close == n:
                self.output.append("".join(par))
                return
            
            if open < n:
                par.append("(")
                gen_par(open + 1, close, par)
                par.pop()
            
            if close < open:
                par.append(")")
                gen_par(open, close + 1, par)
                par.pop()

        gen_par(0, 0, [])

        return self.output
