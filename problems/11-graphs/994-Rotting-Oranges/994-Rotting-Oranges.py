'''
https://leetcode.com/problems/rotting-oranges/
'''

last_solved     = "2026-05-26"
revisit_in_days = 90
difficulty      = "medium"
topic_tags      = ["graphs", "bfs"]
times_reviewed  = 1

from collections import deque
from typing import List


class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        rotten = deque()

        no_rotten = 0
        no_fresh = 0

        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == 2:
                    rotten.append((row,col))
                    no_rotten += 1
                elif grid[row][col] == 1:
                    no_fresh += 1
        
        if not no_rotten and no_fresh:
            return -1
        
        minutes = -1
        while rotten:
            minutes += 1
            for _ in range(len(rotten)):
                x, y = rotten.popleft()

                directions = [
                    (0,1),
                    (0,-1),
                    (-1,0),
                    (1,0)
                ]

                for x_adj, y_adj in directions:
                    new_x, new_y = x + x_adj, y + y_adj

                    if (
                        0 <= new_x < len(grid)
                        and 0 <= new_y < len(grid[0])
                        and grid[new_x][new_y] == 1
                    ):
                        grid[new_x][new_y] = 2
                        rotten.append((new_x, new_y))
                        no_fresh -= 1
        
        if not no_rotten:
            return 0

        if not no_fresh:
            return minutes
        
        return -1
