'''
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
'''

last_solved     = "2026-06-25"
revisit_in_days = 1
difficulty      = "medium"
topic_tags      = ["trees"]

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        
        self.inorder_lookup = {}
        for idx, val in enumerate(inorder): self.inorder_lookup[val] = idx

        def build(preorder_left, preorder_right, inorder_left, inorder_right):
            if (
                preorder_left > preorder_right or
                preorder_left > len(preorder) - 1 or
                preorder_right < 0
                ):
                return None

            root_preorder_val = preorder[preorder_left]
            root_inorder_idx = self.inorder_lookup[root_preorder_val]

            left_children_size = root_inorder_idx - inorder_left

            tree = TreeNode(root_preorder_val)

            tree.left = build(
                preorder_left + 1,
                preorder_left + left_children_size,
                inorder_left,
                root_inorder_idx - 1,
                )

            tree.right = build(
                preorder_left + left_children_size + 1,
                preorder_right,
                root_inorder_idx + 1,
                inorder_right,
                )

            return tree
        
        return build(
            0,
            len(preorder) - 1,
            0,
            len(inorder) - 1,
            )