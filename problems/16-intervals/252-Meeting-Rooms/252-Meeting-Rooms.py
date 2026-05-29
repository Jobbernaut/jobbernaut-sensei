'''
https://leetcode.com/problems/meeting-rooms/
'''

last_solved     = "2026-05-29"
revisit_in_days = 3
difficulty      = "easy"
topic_tags      = ["intervals"]
times_reviewed  = 0

class Solution:
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        intervals.sort()

        for idx in range(0, len(intervals) - 1):
            if intervals[idx][1] > intervals[idx + 1][0]:
                return False
        
        return True