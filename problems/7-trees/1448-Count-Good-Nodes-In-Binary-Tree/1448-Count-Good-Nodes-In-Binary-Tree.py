'''
https://leetcode.com/problems/count-good-nodes-in-binary-tree/
'''

last_solved     = "2026-08-07"
revisit_in_days = 42
times_reviewed  = 8
difficulty      = "medium"
topic_tags      = ["trees", "dfs"]

class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        self.good = 0
        
        def traverse(node, hi):
            if not node:
                return
            
            if node.val >= hi:
                self.good += 1
                hi = node.val
            
            traverse(node.left, hi)
            traverse(node.right, hi)
        
        traverse(root, root.val)

        return self.good