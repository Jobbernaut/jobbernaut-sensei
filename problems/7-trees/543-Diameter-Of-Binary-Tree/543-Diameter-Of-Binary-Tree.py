'''
https://leetcode.com/problems/diameter-of-binary-tree/
'''

last_solved     = "2026-06-01"
revisit_in_days = 30
difficulty      = "easy"
topic_tags      = ["trees"]
times_reviewed  = 1

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.diameter = 0

        def depth(node):
            if not node:
                return 0
            
            left = depth(node.left)
            right = depth(node.right)

            self.diameter = max(self.diameter, left + right)

            return 1 + max(left, right)
        
        depth(root)

        return self.diameter