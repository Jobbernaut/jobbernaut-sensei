'''
https://leetcode.com/problems/min-cost-to-connect-all-points/
'''

last_solved     = "2026-09-05"
revisit_in_days = 35
times_reviewed  = 5
difficulty      = "medium"
topic_tags      = ["array", "union-find", "graph", "minimum-spanning-tree", "prims-algorithm", "kruskals-algorithm", "boruvkas-algorithm"]

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        min_cost = 0
        heap = []
        final = {}

        heapq.heappush(heap, [0, tuple(points[0])])
        while heap:
            cost, coords = heapq.heappop(heap)
            x, y = coords

            if coords not in final:
                final[coords] = cost
                min_cost += cost

                for point in points:
                    if tuple(point) not in final:
                        heapq.heappush(heap, [abs(point[0] - x) + abs(point[1] - y), tuple(point)])

        return min_cost