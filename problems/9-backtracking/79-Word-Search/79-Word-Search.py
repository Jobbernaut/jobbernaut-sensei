'''
https://leetcode.com/problems/word-search/
'''

last_solved     = "2026-08-26"
revisit_in_days = 42
times_reviewed  = 8
difficulty      = "medium"
topic_tags      = ["backtracking", "dfs"]

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        M = len(board)
        N = len(board[0])

        def backtrack(row, col, idx):
            if idx == len(word):
                return True
            elif (
                (not 0 <= row < M) or
                (not 0 <= col < N) or
                board[row][col] != word[idx]
                ):
                return False
            
            temp = board[row][col]
            board[row][col] = "#"
            
            res = (
                backtrack(row + 1, col, idx + 1) or
                backtrack(row - 1, col, idx + 1) or
                backtrack(row, col + 1, idx + 1) or
                backtrack(row, col - 1, idx + 1)
            )

            board[row][col] = temp

            return res
        
        for row in range(M):
            for col in range(N):
                if backtrack(row, col, 0):
                    return True
        
        return False