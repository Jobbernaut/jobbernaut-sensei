'''
https://leetcode.com/problems/longest-consecutive-sequence/description/
'''

last_solved     = "2026-05-14"
revisit_in_days = 90
difficulty      = "medium"
topic_tags      = ["arrays", "hashing"]

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        lookup_set = set(nums)

        longest = 0

        for num in lookup_set:
            local = 0
            temp = num
            if temp - 1 not in lookup_set:
                local += 1
                while temp + 1 in lookup_set:
                    local += 1
                    temp += 1

            longest = max(longest, local)
        
        return longest
