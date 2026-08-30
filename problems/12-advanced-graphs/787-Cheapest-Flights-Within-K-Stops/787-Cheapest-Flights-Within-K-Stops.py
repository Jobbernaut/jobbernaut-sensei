'''
https://leetcode.com/problems/cheapest-flights-within-k-stops/
'''

last_solved     = "2026-08-30"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["dynamic-programming", "depth-first-search", "breadth-first-search", "graph", "heap-priority-queue", "shortest-path"]

class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        dist = [float('inf')] * n
        dist[src] = 0

        for i in range(k + 1):
            copy = dist[:]

            for u, v, price in flights:
                dist[v] = min(dist[v], copy[u] + price)

        return dist[dst] if dist[dst] != float('inf') else -1
