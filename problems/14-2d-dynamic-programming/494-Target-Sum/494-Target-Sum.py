'''
https://leetcode.com/problems/target-sum/
'''

last_solved     = "2026-08-20"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["array", "dynamic-programming", "backtracking", "knapsack-problem", "0-1-knapsack"]

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        min_cost = 0

        visited = set()

        heap = []

        heapq.heappush(heap, (0, points[0][0], points[0][1]))

        while heap:
            for _ in range(len(heap)):
                cost, x, y = heapq.heappop(heap)

                if (x, y) not in visited:
                    visited.add((x, y))

                    min_cost += cost

                    for n_x, n_y in points:
                        if (n_x, n_y) not in visited:
                            heapq.heappush(heap, (abs(x - n_x) + abs(y - n_y), n_x, n_y))
        
        return min_cost
