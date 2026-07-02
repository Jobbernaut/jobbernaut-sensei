'''
https://leetcode.com/problems/maximum-depth-of-binary-tree/
'''

last_solved     = "2026-05-29"
revisit_in_days = 66
difficulty      = "easy"
topic_tags      = ["trees"]
times_reviewed  = 1

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def depth(node):
            if not node:
                return 0
            elif not node.left and node.right:
                return 1 + depth(node.right)
            elif node.left and not node.right:
                return 1 + depth(node.left)
            else:
                return 1 + max(depth(node.left), depth(node.right))
        
        return depth(root)