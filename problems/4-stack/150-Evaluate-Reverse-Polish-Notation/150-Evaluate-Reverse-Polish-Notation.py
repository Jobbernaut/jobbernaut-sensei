'''
https://leetcode.com/problems/evaluate-reverse-polish-notation/description/
'''

last_solved     = "2026-07-27"
revisit_in_days = 87
times_reviewed  = 7
difficulty      = "medium"
topic_tags      = ["stack"]

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []

        for token in tokens:
            try:
                stack.append(int(token))
            except ValueError:
                op2 = stack.pop()
                op1 = stack.pop()
                if token == "+":
                    stack.append(op1 + op2)
                elif token == '-':
                    stack.append(op1 - op2)
                elif token == "*":
                    stack.append(op1 * op2)
                else:
                    stack.append(int(op1 / op2))
        
        return stack[0]
