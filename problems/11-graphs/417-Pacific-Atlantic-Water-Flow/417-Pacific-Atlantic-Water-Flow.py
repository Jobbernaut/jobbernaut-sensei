'''
https://leetcode.com/problems/pacific-atlantic-water-flow/
'''

last_solved     = "2026-08-02"
revisit_in_days = 1
times_reviewed  = 4
difficulty      = "medium"
topic_tags      = ["graphs", "dfs"]

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        def bfs(coord_set, coord_queue):
            while coord_queue:
                for _ in range(len(coord_queue)):
                    row, col = coord_queue.popleft()

                    directions = [
                        (0, 1),
                        (0, -1),
                        (1, 0),
                        (-1, 0)
                    ]

                    for row_adj, col_adj in directions:
                        new_row, new_col = row + row_adj, col + col_adj

                        if (
                            0 <= new_row < M and
                            0 <= new_col < N and
                            (new_row, new_col) not in coord_set and
                            heights[new_row][new_col] >= heights[row][col]
                        ):
                            coord_set.add((new_row, new_col))
                            coord_queue.append((new_row, new_col))
            
            return coord_set

        M, N = len(heights), len(heights[0])
        p_s, a_s = set(), set()
        p_q, a_q = deque(), deque()

        for row in range(M):
            for col in range(N):
                if row == 0 or col == 0:
                    p_s.add((row,col))
                    p_q.append((row,col))
                if row == M - 1 or col == N - 1:
                    a_s.add((row,col))
                    a_q.append((row,col))
        
        return [[row, col] for row, col in bfs(p_s, p_q).intersection(bfs(a_s, a_q))]