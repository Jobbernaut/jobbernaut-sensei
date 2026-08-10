'''
https://leetcode.com/problems/invert-binary-tree/
'''

last_solved     = "2026-08-10"
revisit_in_days = 45
difficulty      = "easy"
topic_tags      = ["tree"]
times_reviewed  = 6

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def invert(node):
            if not node:
                return
            
            invert(node.left)
            invert(node.right)

            node.left, node.right = node.right, node.left
        
        invert(root)

        return root
