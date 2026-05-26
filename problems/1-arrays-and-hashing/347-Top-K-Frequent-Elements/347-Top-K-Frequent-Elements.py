'''
https://leetcode.com/problems/top-k-frequent-elements/description/
'''

last_solved     = "2026-05-14"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["arrays", "hashing"]

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        frequencies = Counter(nums)

        heap = []
        heapq.heapify(heap)

        for elem, freq in frequencies.items():
            heapq.heappush(heap, (freq, elem))
            if len(heap) > k:
                heapq.heappop(heap)
        
        return [elem for freq, elem in heap]
