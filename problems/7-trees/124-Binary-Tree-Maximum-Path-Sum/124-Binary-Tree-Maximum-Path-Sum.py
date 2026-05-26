'''
https://leetcode.com/problems/binary-tree-maximum-path-sum/
'''

last_solved     = "2026-05-26"
revisit_in_days = 3
difficulty      = "hard"
topic_tags      = ["trees"]

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_sum = float('-inf')

        def max_path_sum(node):
            if not node:
                return 0

            left = max(max_path_sum(node.left), 0)
            right = max(max_path_sum(node.right), 0)
            
            curr_sum = left + node.val + right
            self.max_sum = max(self.max_sum, curr_sum)

            return node.val + max(left, right)
        
        max_path_sum(root)

        return self.max_sum