'''
https://leetcode.com/problems/rotate-image/
'''

last_solved     = "2026-09-04"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["array", "math", "matrix"]

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        N = len(matrix)

        for i in range(N):
            for j in range(N):
                if i < j:
                    matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

        for i in range(N):
            for j in range(N):
                if j < N // 2:
                    matrix[i][j], matrix[i][N-j-1] = matrix[i][N-j-1], matrix[i][j]
