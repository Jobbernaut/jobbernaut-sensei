'''
https://leetcode.com/problems/network-delay-time/
'''

last_solved     = "2026-08-30"
revisit_in_days = 36
times_reviewed  = 5
difficulty      = "medium"
topic_tags      = ["depth-first-search", "breadth-first-search", "graph", "heap-priority-queue", "shortest-path", "dijkstra"]

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        adj_list = defaultdict(list)
        final_dist = {}
        heap = []

        for source, destination, weight in times:
            adj_list[source].append([weight, destination])

        heapq.heappush(heap, [0, k])

        while heap:
            curr_dist, curr_node = heapq.heappop(heap)

            if curr_node not in final_dist:
                final_dist[curr_node] = curr_dist

                for neighbor_weight, neighbor_node in adj_list[curr_node]:
                    if neighbor_node not in final_dist:
                        heapq.heappush(heap, [curr_dist + neighbor_weight, neighbor_node])

        if len(final_dist) != n:
            return -1

        return max(final_dist.values())
