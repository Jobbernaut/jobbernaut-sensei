'''
https://leetcode.com/problems/kth-smallest-element-in-a-bst/
'''

last_solved     = "2026-05-26"
revisit_in_days = 7
difficulty      = "medium"
topic_tags      = ["trees"]

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