'''
https://leetcode.com/problems/min-cost-to-connect-all-points/
'''

last_solved     = "2026-08-25"
revisit_in_days = 7
times_reviewed  = 3
difficulty      = "medium"
topic_tags      = ["array", "union-find", "graph", "minimum-spanning-tree", "prims-algorithm", "kruskals-algorithm", "boruvkas-algorithm"]

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        min_cost = 0
        visited = set()
        heap = []

        heapq.heappush(heap, [0, points[0]])

        while heap:
            for _ in range(len(heap)):
                d, point = heapq.heappop(heap)

                x, y = point

                if (x, y) not in visited:
                    visited.add((x, y))

                    min_cost += d

                    for n_x, n_y in points:
                        if (n_x, n_y) not in visited:
                            heapq.heappush(heap, [abs(x - n_x) + abs(y - n_y), [n_x, n_y]])
        
        return min_cost