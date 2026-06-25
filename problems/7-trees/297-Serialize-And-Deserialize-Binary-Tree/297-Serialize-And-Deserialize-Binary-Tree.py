'''
https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
'''

last_solved     = "2026-06-25"
revisit_in_days = 1
difficulty      = "hard"
topic_tags      = ["trees"]

class Codec:
    def serialize(self, root):
        self.serialized_binary_tree = []

        def preorder(node):
            if not node:
                self.serialized_binary_tree.append("N")
                return None
            
            self.serialized_binary_tree.append(str(node.val))
            preorder(node.left)
            preorder(node.right)
        
        preorder(root)

        data = ",".join(self.serialized_binary_tree)

        return data

    def deserialize(self, data):
        def preorder(tree_nodes):
            if not len(tree_nodes):
                return None
            
            curr = tree_nodes.popleft()

            if curr == "N":
                return None
            else:
                new = TreeNode(curr)

                new.left = preorder(tree_nodes)
                new.right = preorder(tree_nodes)

                return new
        
        return preorder(deque(data.split(",")))