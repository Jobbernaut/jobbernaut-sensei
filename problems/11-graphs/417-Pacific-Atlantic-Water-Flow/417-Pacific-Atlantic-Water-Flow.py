'''
https://leetcode.com/problems/pacific-atlantic-water-flow/
'''

last_solved     = "2026-07-21"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["graphs", "dfs"]

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        M, N = len(heights), len(heights[0])
        pacific_set, atlantic_set = set(), set()
        pacific_queue, atlantic_queue = deque(), deque()

        for row in range(M):
            for col in range(N):
                if row == 0 or col == 0:
                    pacific_queue.append((row, col))
                    pacific_set.add((row, col))
                if row == M - 1 or col == N - 1:
                    atlantic_queue.append((row, col))
                    atlantic_set.add((row, col))
        
        while pacific_queue:
            for _ in range(len(pacific_queue)):
                row, col = pacific_queue.popleft()

                directions = [
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1)
                ]

                for row_adj, col_adj in directions:
                    new_row, new_col = row + row_adj, col + col_adj

                    if (
                        0 <= new_row < M and
                        0 <= new_col < N and
                        heights[new_row][new_col] >= heights[row][col] and
                        (new_row, new_col) not in pacific_set
                    ):
                        pacific_queue.append((new_row, new_col))
                        pacific_set.add((new_row, new_col))

        while atlantic_queue:
            for _ in range(len(atlantic_queue)):
                row, col = atlantic_queue.popleft()

                directions = [
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1)
                ]

                for row_adj, col_adj in directions:
                    new_row, new_col = row + row_adj, col + col_adj

                    if (
                        0 <= new_row < M and
                        0 <= new_col < N and
                        heights[new_row][new_col] >= heights[row][col] and
                        (new_row, new_col) not in atlantic_set
                    ):
                        atlantic_queue.append((new_row, new_col))
                        atlantic_set.add((new_row, new_col))
        
        return [[x, y] for x, y in atlantic_set.intersection(pacific_set)]
