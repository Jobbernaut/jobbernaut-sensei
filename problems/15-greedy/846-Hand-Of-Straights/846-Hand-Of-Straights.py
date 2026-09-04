'''
https://leetcode.com/problems/hand-of-straights/
'''

last_solved     = "2026-09-04"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["array", "hash-table", "greedy", "sorting"]

from collections import Counter

class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize != 0:
            return False

        elems = 0
        counter = Counter(hand)

        mini = float('inf')
        while counter:
            if elems % groupSize == 0:
                mini = min(counter)

            if mini not in counter:
                return False
            else:
                counter[mini] -= 1
                elems -= 1
                if not counter[mini]:
                    del counter[mini]
                mini += 1

        return True
        # Time: O(N^2) — min(counter) called N/groupSize times, each O(K) distinct keys
        # Space: O(N)
