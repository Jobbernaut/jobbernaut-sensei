'''
https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
'''

last_solved     = "2026-07-16"
revisit_in_days = 37
difficulty      = "medium"
topic_tags      = ["trees", "bst"]
times_reviewed  = 6

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        def recurse(node):
            if not node:
                return None
            
            if node.val > max(p.val, q.val):
                return recurse(node.left)
            elif node.val < min(p.val, q.val):
                return recurse(node.right)
            else:
                return node
        
        return recurse(root)
