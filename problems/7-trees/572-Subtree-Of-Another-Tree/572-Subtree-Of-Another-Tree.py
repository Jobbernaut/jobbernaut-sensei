'''
https://leetcode.com/problems/subtree-of-another-tree/
'''

last_solved     = "2026-06-15"
revisit_in_days = 53
difficulty      = "easy"
topic_tags      = ["trees"]
times_reviewed  = 5

class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def is_same(node1, node2):
            if not node1 and not node2:
                return True
            if not node1 or not node2 or node1.val != node2.val:
                return False
            return is_same(node1.left, node2.left) and is_same(node1.right, node2.right)

        def traverse(node):
            if not node:
                return False
            
            if is_same(node, subRoot):
                return True

            return traverse(node.left) or traverse(node.right)

        return traverse(root)