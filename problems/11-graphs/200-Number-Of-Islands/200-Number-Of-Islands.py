'''
https://leetcode.com/problems/number-of-islands/
'''

last_solved     = "2026-05-26"
revisit_in_days = 90
difficulty      = "medium"
topic_tags      = ["graphs", "bfs"]
times_reviewed  = 1

from collections import deque
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        num = 0
        
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == "1":
                    queue = deque()

                    queue.append((row,col))

                    while queue:
                        for _ in range(len(queue)):
                            x, y = queue.popleft()

                            directions = [
                                (0,1),
                                (0,-1),
                                (1,0),
                                (-1,0)
                            ]

                            for x_adj, y_adj in directions:
                                new_x, new_y = x + x_adj, y + y_adj

                                if (
                                    0 <= new_x < len(grid)
                                    and 0 <= new_y < len(grid[0])
                                    and grid[new_x][new_y] == "1"
                                ):
                                    queue.append((new_x,new_y))
                                    grid[new_x][new_y] = "0"
                    num += 1
                
        return num
