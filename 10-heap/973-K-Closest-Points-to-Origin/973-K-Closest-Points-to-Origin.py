'''
https://leetcode.com/problems/k-closest-points-to-origin/description/
'''

last_solved     = "2026-05-23"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["heap"]

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        import heapq

        heap = []
        heapq.heapify(heap)

        for point in points:
            heapq.heappush(heap, [-1*(point[0]**2 + point[1]**2),point])
            if len(heap) > k:
                heapq.heappop(heap)
        
        return [point[1] for point in heap]