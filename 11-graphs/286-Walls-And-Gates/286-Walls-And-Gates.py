'''
https://leetcode.com/problems/walls-and-gates/description/
'''

last_solved     = "2026-05-18"
revisit_in_days = 3
difficulty      = "medium"
topic_tags      = ["graphs"]

class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """
        Do not return anything, modify rooms in-place instead.
        """
        m = len(rooms)
        n = len(rooms[0])
        INF = 2147483647

        queue = deque()
        
        for x in range(m):
            for y in range(n):
                if rooms[x][y] == 0:
                    queue.append([x,y])
        
        distance = 0
        while queue:
            distance += 1
            for _ in range(len(queue)):
                curr_x, curr_y = queue.popleft()

                directions = [
                    (0, 1),
                    (0, -1),
                    (1, 0),
                    (-1, 0)
                ]

                for x_adj, y_adj in directions:
                    new_x, new_y = curr_x + x_adj, curr_y + y_adj

                    if (
                        0 <= new_x < m
                        and 0 <= new_y < n
                        and rooms[new_x][new_y] == INF
                    ):
                        rooms[new_x][new_y] = distance
                        queue.append([new_x, new_y])