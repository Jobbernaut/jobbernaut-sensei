'''
https://leetcode.com/problems/evaluate-reverse-polish-notation/description/
'''

last_solved     = "2026-06-10"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["stack"]

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []

        for token in tokens:
            if token == "+":
                op_2 = int(stack.pop())
                op_1 = int(stack.pop())
                stack.append(str(op_1 + op_2))
            elif token == '-':
                op_2 = int(stack.pop())
                op_1 = int(stack.pop())
                stack.append(str(op_1 - op_2))
            elif token == "*":
                op_2 = int(stack.pop())
                op_1 = int(stack.pop())
                stack.append(str(op_1 * op_2))
            elif token == "/":
                op_2 = int(stack.pop())
                op_1 = int(stack.pop())
                stack.append(str(int(op_1 / op_2)))
            else:
                stack.append(token)
        
        return int(stack[0])
