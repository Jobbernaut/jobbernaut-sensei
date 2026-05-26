'''
https://leetcode.com/problems/two-sum/description/
'''

last_solved     = "2026-05-04"
revisit_in_days = 30
difficulty      = "easy"
topic_tags      = ["arrays", "hashing"]

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        d = defaultdict(list)

        for idx, num in enumerate(nums):
            d[num].append(idx)

            if target - num in d:
                if num == target - num:
                    if len(d[target - num]) > 1:
                        return d[target - num]
                    else:
                        continue
                else:
                    return [d[target - num][0], idx]
