'''
https://leetcode.com/problems/network-delay-time/
'''

last_solved     = "2026-08-15"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["depth-first-search", "breadth-first-search", "graph", "heap-priority-queue", "shortest-path", "dijkstra"]

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        adj_list = defaultdict(list)

        for source, target, weight in times:
            adj_list[source].append((weight, target))

        queue = []
        visited = set()
        min_dist = defaultdict(lambda: float('inf'))

        heapq.heappush(queue, (0, k))
        min_dist[k] = 0

        while queue:
            curr_weight, curr_node = heapq.heappop(queue)

            if curr_node in visited:
                continue
            visited.add(curr_node)
            min_dist[curr_node] = curr_weight

            for neighbor_weight, neighbor_node in adj_list[curr_node]:
                if neighbor_node not in visited:
                    heapq.heappush(queue, (curr_weight + neighbor_weight, neighbor_node))

        if len(visited) < n:
            return -1

        return max(min_dist.values())
