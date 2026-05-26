'''
https://leetcode.com/problems/walls-and-gates/description/
'''

last_solved     = "2026-05-21"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["graphs"]

class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        INF = 2147483647
        M = len(rooms)
        N = len(rooms[0])

        queue = deque()

        for row in range(M):
            for col in range(N):
                if not rooms[row][col]:
                    queue.append([row,col])
        
        distance = 0
        while queue:
            distance += 1
            for _ in range(len(queue)):
                curr_x, curr_y = queue.popleft()

                directions = [
                    (1, 0),
                    (-1, 0),
                    (0, 1),
                    (0, -1),
                ]

                for x_adj, y_adj in directions:
                    new_x, new_y = curr_x + x_adj, curr_y + y_adj

                    if (
                        0 <= new_x < M
                        and 0 <= new_y < N
                        and rooms[new_x][new_y] == INF
                    ):
                        rooms[new_x][new_y] = distance
                        queue.append([new_x, new_y])