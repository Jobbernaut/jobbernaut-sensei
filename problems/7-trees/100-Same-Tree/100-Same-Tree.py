'''
https://leetcode.com/problems/same-tree/
'''

last_solved     = "2026-05-29"
revisit_in_days = 90
difficulty      = "easy"
topic_tags      = ["trees"]
times_reviewed  = 0

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        def same(node1, node2):
            if not node1 and not node2:
                return True
            
            if not node1 and node2 or node1 and not node2 or node1.val != node2.val:
                return False
            
            left_subtree = same(node1.left, node2.left)
            right_subtree = same(node1.right, node2.right)

            return left_subtree and right_subtree
        
        return same(p, q)