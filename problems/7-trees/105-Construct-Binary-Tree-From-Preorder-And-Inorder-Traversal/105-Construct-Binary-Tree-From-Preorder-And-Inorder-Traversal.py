'''
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
'''

last_solved     = "2026-08-25"
revisit_in_days = 45
times_reviewed  = 10
difficulty      = "medium"
topic_tags      = ["trees"]

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        self.in_lookup = {}

        for idx, elem in enumerate(inorder):
            self.in_lookup[elem] = idx

        def build(pre_left, pre_right, in_left, in_right):
            if pre_left > pre_right:
                return None

            pre_root_val = preorder[pre_left]
            in_root_idx = self.in_lookup[pre_root_val]

            left_subtree_len = in_root_idx - in_left
            right_subtree_len = in_right - in_root_idx

            node = TreeNode(pre_root_val)

            node.left = build(
                pre_left + 1,
                pre_left + left_subtree_len,
                in_left,
                in_root_idx - 1
                )

            node.right = build(
                pre_right - right_subtree_len + 1,
                pre_right,
                in_root_idx + 1,
                in_right
            )

            return node
        
        return build(
            0,
            len(preorder) - 1,
            0,
            len(inorder) - 1
        )