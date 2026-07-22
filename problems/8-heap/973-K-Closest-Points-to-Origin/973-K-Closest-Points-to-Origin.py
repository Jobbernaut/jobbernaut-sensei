'''
https://leetcode.com/problems/k-closest-points-to-origin/description/
'''

last_solved     = "2026-07-22"
revisit_in_days = 45
times_reviewed  = 7
difficulty      = "medium"
topic_tags      = ["heap"]

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        k_closest = []

        for idx, (x_coord, y_coord) in enumerate(points):
            dist = -(x_coord**2 + y_coord**2)
            heapq.heappush(k_closest, (dist, idx))
            if len(k_closest) > k:
                heapq.heappop(k_closest)

        return [points[idx] for _, idx in k_closest]