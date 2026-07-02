'''
https://leetcode.com/problems/last-stone-weight/description/
'''

last_solved     = "2026-06-22"
revisit_in_days = 27
difficulty      = "medium"
topic_tags      = ["heap"]

class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        stones_heap = [-stone for stone in stones]
        heapq.heapify(stones_heap)

        while len(stones_heap) > 1:
            smashed_weight = heapq.heappop(stones_heap) - heapq.heappop(stones_heap)

            if smashed_weight:
                heapq.heappush(stones_heap, smashed_weight)
        
        if len(stones_heap):
            return -stones_heap[0]
        
        return 0