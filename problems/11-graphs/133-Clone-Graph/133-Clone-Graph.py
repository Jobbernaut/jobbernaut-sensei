'''
https://leetcode.com/problems/clone-graph/
'''

last_solved     = "2026-07-01"
revisit_in_days = 38
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["graphs", "dfs", "bfs", "hash-map"]

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return node

        deep_copy_graph = Node(node.val)

        orig = node
        clone = deep_copy_graph

        visited = {}
        visited[orig] = clone

        queue = deque()
        queue.append((orig, clone))

        while queue:
            for _ in range(len(queue)):
                curr_orig, curr_clone = queue.popleft()

                for each_node in curr_orig.neighbors:
                    new = Node()
                
                    new.val = each_node.val

                    if each_node in visited:
                        curr_clone.neighbors.append(visited[each_node])
                    else:
                        curr_clone.neighbors.append(new)
                        visited[each_node] = new
                        queue.append((each_node, new))
        
        return deep_copy_graph