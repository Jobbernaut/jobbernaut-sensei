'''
https://leetcode.com/problems/binary-tree-level-order-traversal/
'''

last_solved     = "2026-06-02"
revisit_in_days = 3
difficulty      = "medium"
topic_tags      = ["trees", "bfs"]
times_reviewed  = 1

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        output = []

        if not root:
            return output

        queue = deque()
        queue.append(root)

        while queue:
            level = []
            for _ in range(len(queue)):
                curr = queue.popleft()
                level.append(curr.val)

                if curr.left:
                    queue.append(curr.left)
                if curr.right:
                    queue.append(curr.right)
            output.append(level)
        
        return output
