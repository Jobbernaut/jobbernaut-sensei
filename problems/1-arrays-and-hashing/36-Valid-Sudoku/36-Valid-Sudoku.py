'''
https://leetcode.com/problems/valid-sudoku/description/
'''

last_solved     = "2026-07-16"
revisit_in_days = 2
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["arrays", "hashing"]

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        rows = defaultdict(set)
        cols = defaultdict(set)
        grids = defaultdict(set)

        for row in range(9):
            for col in range(9):
                val = board[row][col]

                if val == ".":
                    continue
                elif val in rows[row] or val in cols[col]  or val in grids[(row // 3, col // 3)]:
                    return False
                
                rows[row].add(val)
                cols[col].add(val)
                grids[(row // 3, col // 3)].add(val)
        
        return True
