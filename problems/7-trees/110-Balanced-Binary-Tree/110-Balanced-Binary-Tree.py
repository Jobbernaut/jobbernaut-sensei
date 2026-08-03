'''
https://leetcode.com/problems/balanced-binary-tree/
'''

last_solved     = "2026-08-02"
revisit_in_days = 1
difficulty      = "easy"
topic_tags      = ["trees"]
times_reviewed  = 6

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        self.balanced = True

        def depth(node):
            if not node:
                return 0
            
            left = depth(node.left)
            right = depth(node.right)

            if abs(left - right) > 1:
                self.balanced = False
            
            return 1 + max(left, right)
        
        depth(root)

        return self.balanced