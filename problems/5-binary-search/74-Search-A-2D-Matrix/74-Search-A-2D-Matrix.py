'''
https://leetcode.com/problems/search-a-2d-matrix/
'''

last_solved     = "2026-07-08"
revisit_in_days = 57
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["binary-search", "matrix"]

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        M, N = len(matrix), len(matrix[0])

        left, right = 0, M*N - 1

        while left <= right:
            flat_mid = (left + right) // 2
            matrix_mid_x, matrix_mid_y = flat_mid // N, flat_mid % N
            curr = matrix[matrix_mid_x][matrix_mid_y]

            if curr == target:
                return True
            elif curr > target:
                right = flat_mid - 1
            else:
                left = flat_mid + 1
        
        return False
