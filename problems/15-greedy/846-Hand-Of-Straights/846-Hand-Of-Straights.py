'''
https://leetcode.com/problems/hand-of-straights/
'''

last_solved     = "2026-09-05"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["array", "hash-table", "greedy", "sorting"]

class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        if len(hand) % groupSize != 0:
            return False

        counter = Counter(hand)
        min_heap = list(counter.items())
        heapq.heapify(min_heap)

        while counter:
            curr_min, _ = heapq.heappop(min_heap)
            curr_cnt = counter[curr_min] - 1

            if curr_cnt >= 0:
                heapq.heappush(min_heap, (curr_min, curr_cnt))

                for num in range(curr_min, curr_min + groupSize):
                    if num not in counter:
                        return False
                    counter[num] -= 1
                    if not counter[num]:
                        del counter[num]

        return True
        # Time: O(N log N) — heap operations over unique keys
        # Space: O(N)
