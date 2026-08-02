'''
https://leetcode.com/problems/word-search/
'''

last_solved     = "2026-07-28"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["backtracking", "dfs"]

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        self.M = len(board)
        self.N = len(board[0])

        def dfs(row, col, idx):
            if idx == len(word):
                return True

            if (
                not (0 <= row < self.M and 0 <= col < self.N) or
                board[row][col] == "#" or
                board[row][col] != word[idx]
            ):
                return False
            
            temp = board[row][col]

            board[row][col] = "#"

            word_exists = any([
                dfs(row + 1, col, idx + 1),
                dfs(row - 1, col, idx + 1),
                dfs(row, col + 1, idx + 1),
                dfs(row, col - 1, idx + 1),
            ])

            board[row][col] = temp

            return word_exists
        
        return any([dfs(row, col, 0) for row in range(self.M) for col in range(self.N)])