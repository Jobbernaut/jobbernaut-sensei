'''
https://leetcode.com/problems/same-tree/
'''

last_solved     = "2026-08-04"
revisit_in_days = 89
difficulty      = "easy"
topic_tags      = ["trees"]
times_reviewed  = 7

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        def same(p, q):
            if not p and not q:
                return True
            elif not p or not q or p.val != q.val:
                return False
            
            return same(p.left, q.left) and same(p.right, q.right)

        return same(p, q)