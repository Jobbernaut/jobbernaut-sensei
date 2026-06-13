'''
https://leetcode.com/problems/longest-repeating-character-replacement/
'''

last_solved     = "2026-06-13"
revisit_in_days = 7
difficulty      = "medium"
topic_tags      = ["sliding-window"]
times_reviewed  = 2

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        freq_arr = [0] * 26

        max_len = 0
        max_freq = 0

        left = right = 0
        while left <= right and right < len(s):
            freq_arr[ord(s[right]) - ord('A')] += 1
            max_freq = max(max_freq, freq_arr[ord(s[right]) - ord('A')])

            if (right - left + 1) - max_freq <= k:
                max_len = max(max_len, right - left + 1)

            while left <= right and (right - left + 1) - max_freq > k:
                freq_arr[ord(s[left]) - ord('A')] -= 1
                left += 1
            
            right += 1
        
        return max_len
