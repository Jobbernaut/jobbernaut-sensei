'''
https://leetcode.com/problems/group-anagrams/description/
'''

last_solved     = "2026-05-04"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["arrays", "hashing"]

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        def build(string):
            arr = [0] * 26
            for char in string:
                arr[ord(char) - ord('a')] += 1
            return tuple(arr)
        
        lookup_table = defaultdict(list)
        for string in strs:
            lookup_table[build(string)].append(string)
        
        return [word_lst for word_lst in lookup_table.values()]
