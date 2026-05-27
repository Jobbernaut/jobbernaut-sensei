'''
https://leetcode.com/problems/last-stone-weight/description/
'''

last_solved     = "2026-05-23"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["heap"]

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        heap = [-stone for stone in stones]

        heapq.heapify(heap)

        while len(heap) > 1:
            stone_1 = -heapq.heappop(heap)
            stone_2 = -heapq.heappop(heap)

            if stone_1 > stone_2:
                heapq.heappush(heap, stone_2 - stone_1)
        
        return -heap[0] if len(heap) else 0