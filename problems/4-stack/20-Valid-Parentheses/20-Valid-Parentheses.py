'''
https://leetcode.com/problems/valid-parentheses/description/
'''

last_solved     = "2026-06-10"
revisit_in_days = 30
difficulty      = "easy"
topic_tags      = ["stack"]

class Solution:
    def isValid(self, s: str) -> bool:
        st = []

        for c in s:
            if c == "(" or c == "[" or c == "{":
                st.append(c)
            elif not st or not(c == ")" and st[-1] == '(' or c == "]" and st[-1] == "[" or c == "}" and st[-1] == "{"):
                return False
            else:
                st.pop()
        
        return not st
