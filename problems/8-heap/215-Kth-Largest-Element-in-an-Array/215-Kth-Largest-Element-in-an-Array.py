'''
https://leetcode.com/problems/kth-largest-element-in-an-array/description/
'''

last_solved     = "2026-08-31"
revisit_in_days = 90
times_reviewed  = 9
difficulty      = "medium"
topic_tags      = ["heap"]

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []

        for num in nums:
            heapq.heappush(heap, num)

            if len(heap) > k:
                heapq.heappop(heap)
        
        return heap[0]