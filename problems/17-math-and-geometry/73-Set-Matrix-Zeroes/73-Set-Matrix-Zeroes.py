'''
https://leetcode.com/problems/set-matrix-zeroes/description/
'''

last_solved     = "2026-06-26"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["math","geometry"]
times_reviewed  = 5

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        is_first_row_zero = False
        is_first_col_zero = False

        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if not matrix[row][col]:
                    if not is_first_row_zero and not row:
                        is_first_row_zero = True
                    if not is_first_col_zero and not col:
                        is_first_col_zero = True
                    if row > 0 and col > 0:
                        matrix[row][0] = 0
                        matrix[0][col] = 0
        
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if row > 0 and col > 0:
                    if not matrix[row][0] or not matrix[0][col]:
                        matrix[row][col] = 0
        
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if (not row and is_first_row_zero) or (not col and is_first_col_zero):
                    matrix[row][col] = 0