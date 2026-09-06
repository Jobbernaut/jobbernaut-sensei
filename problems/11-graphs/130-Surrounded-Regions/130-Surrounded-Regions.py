'''
https://leetcode.com/problems/surrounded-regions/
'''

last_solved     = "2026-09-06"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["array", "depth-first-search", "breadth-first-search", "union-find", "matrix"]

class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        M, N = len(board), len(board[0])

        queue = deque()

        for i in range(M):
            for j in range(N):
                if i == 0 or j == 0 or i == M - 1 or j == N - 1:
                    if board[i][j] == "O":
                        board[i][j] = "S"
                        queue.append((i, j))

        while queue:
            i, j = queue.popleft()

            directions = [
                (1, 0),
                (-1, 0),
                (0, 1),
                (0, -1)
            ]

            for i_adj, j_adj in directions:
                if 0 <= i+i_adj < M and 0 <= j+j_adj < N and board[i+i_adj][j+j_adj] == "O":
                    board[i+i_adj][j+j_adj] = "S"
                    queue.append((i+i_adj, j+j_adj))

        for i in range(M):
            for j in range(N):
                if board[i][j] == "S":
                    board[i][j] = "O"
                elif board[i][j] == "O":
                    board[i][j] = "X"
