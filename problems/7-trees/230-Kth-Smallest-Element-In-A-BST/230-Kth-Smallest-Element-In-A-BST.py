'''
https://leetcode.com/problems/kth-smallest-element-in-a-bst/
'''

last_solved     = "2026-07-16"
revisit_in_days = 42
difficulty      = "medium"
topic_tags      = ["trees"]
times_reviewed  = 6

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        self.count = k
        self.result = None

        def inorder(node):
            if not node or self.result is not None:
                return
            
            inorder(node.left)
            
            self.count -= 1
            if self.count == 0:
                self.result = node.val
                return
            
            inorder(node.right)

        inorder(root)
        return self.result