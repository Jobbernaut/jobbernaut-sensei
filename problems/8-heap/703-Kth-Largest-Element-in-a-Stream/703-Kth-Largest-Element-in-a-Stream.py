'''
https://leetcode.com/problems/kth-largest-element-in-a-stream/description/
'''

last_solved     = "2026-06-22"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["heap"]

class KthLargest:

    def __init__(self, k: int, nums: List[int]):
        self.heap = nums
        heapq.heapify(self.heap)
        self.k = k

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        while len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]