'''
https://leetcode.com/problems/binary-tree-maximum-path-sum/
'''

last_solved     = "2026-06-25"
revisit_in_days = 30
difficulty      = "hard"
topic_tags      = ["trees"]
times_reviewed  = 5

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        self.max_path_sum = float('-inf')

        def postorder(node):
            if not node:
                return 0
            
            left = max(0, postorder(node.left))
            right = max(0, postorder(node.right))

            curr = left + node.val + right

            self.max_path_sum = max(self.max_path_sum, curr)

            return node.val + max(left, right)
        
        postorder(root)

        return self.max_path_sum