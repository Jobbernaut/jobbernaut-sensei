'''
https://leetcode.com/problems/maximum-depth-of-binary-tree/
'''

last_solved     = "2026-08-12"
revisit_in_days = 90
difficulty      = "easy"
topic_tags      = ["trees"]
times_reviewed  = 7

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def max_depth(node):
            if not node: return 0

            return 1 + max(max_depth(node.left), max_depth(node.right))
        
        return max_depth(root)