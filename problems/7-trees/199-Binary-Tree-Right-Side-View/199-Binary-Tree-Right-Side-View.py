'''
https://leetcode.com/problems/binary-tree-right-side-view/
'''

last_solved     = "2026-06-21"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["trees", "bfs"]
times_reviewed  = 2

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        output = []

        if not root:
            return output
        
        queue = deque()
        queue.append(root)

        while queue:
            rightmost = None
            for _ in range(len(queue)):
                rightmost = queue.popleft()
                if rightmost.left:
                    queue.append(rightmost.left)
                if rightmost.right:
                    queue.append(rightmost.right)
            output.append(rightmost.val)
        
        return output
