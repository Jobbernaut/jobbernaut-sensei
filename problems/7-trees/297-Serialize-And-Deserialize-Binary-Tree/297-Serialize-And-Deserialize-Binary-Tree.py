'''
https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
'''

last_solved     = "2026-06-26"
revisit_in_days = 3
difficulty      = "hard"
topic_tags      = ["trees"]

class Codec:
    def serialize(self, root):
        self.serialized_tree = []

        def preorder(node):
            if not node:
                self.serialized_tree.append("N")
                return
            
            self.serialized_tree.append(str(node.val))
            preorder(node.left)
            preorder(node.right)
        
        preorder(root)

        return ",".join(self.serialized_tree)
        

    def deserialize(self, data):
        self.deserialized_tree = list(data.split(","))
        self.global_index = -1

        def preorder():
            self.global_index += 1

            if self.deserialized_tree[self.global_index] == "N":
                return None
            
            node = TreeNode(int(self.deserialized_tree[self.global_index]))

            node.left = preorder()
            node.right = preorder()

            return node
        
        return preorder()