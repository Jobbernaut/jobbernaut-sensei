'''
https://leetcode.com/problems/min-stack/description/
'''

last_solved     = "2026-06-05"
revisit_in_days = 112
difficulty      = "medium"
topic_tags      = ["stack"]
times_reviewed  = 12

class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        popped = self.stack.pop()
        if self.min_stack[-1] == popped:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
