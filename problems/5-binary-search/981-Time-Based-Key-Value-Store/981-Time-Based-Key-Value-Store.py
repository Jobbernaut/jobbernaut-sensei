'''
https://leetcode.com/problems/time-based-key-value-store/
'''

last_solved     = "2026-06-26"
revisit_in_days = 9
difficulty      = "medium"
topic_tags      = ["binary-search", "hash-map"]

from collections import defaultdict

class TimeMap:
    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((timestamp, value))

    def get(self, key: str, timestamp: int) -> str:
        search = self.store[key]

        left, right = 0, len(search) - 1

        last_known = ""

        while left <= right:
            mid = (left + right) // 2

            if search[mid][0] <= timestamp:
                last_known = search[mid][1]
                left = mid + 1
            else:
                right = mid - 1
        
        return last_known
