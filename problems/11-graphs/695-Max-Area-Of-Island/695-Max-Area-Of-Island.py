'''
https://leetcode.com/problems/max-area-of-island/
'''

last_solved     = "2026-06-30"
revisit_in_days = 7
difficulty      = "medium"
topic_tags      = ["graphs", "dfs", "bfs"]

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        def dfs(row, col):
            if (
                row < 0 or
                col < 0 or
                row > len(grid) - 1 or
                col > len(grid[row]) - 1 or
                not grid[row][col]
            ):
                return 0

            grid[row][col] = 0

            return 1 + dfs(row + 1, col) + dfs(row - 1, col) + dfs(row, col + 1) + dfs(row, col - 1)

        max_area = 0

        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col]:
                    max_area = max(max_area, dfs(row, col))

        return max_area

# Time:  O(M x N) — each cell visited at most once
# Space: O(A) — recursive call stack depth bounded by largest island area
