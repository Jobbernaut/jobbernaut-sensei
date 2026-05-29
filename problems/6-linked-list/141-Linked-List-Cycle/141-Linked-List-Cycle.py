'''
https://leetcode.com/problems/linked-list-cycle/
'''

last_solved     = "2026-05-29"
revisit_in_days = 90
difficulty      = "easy"
topic_tags      = ["linked-list"]
times_reviewed  = 0

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow, fast = head, head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True
        
        return False