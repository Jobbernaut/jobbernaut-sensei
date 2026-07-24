'''
https://leetcode.com/problems/remove-nth-node-from-end-of-list/
'''

last_solved     = "2026-07-24"
revisit_in_days = 44
times_reviewed  = 7
difficulty      = "medium"
topic_tags      = ["linked-list", "two-pointers"]

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        dummy = ListNode()
        dummy.next = head

        first, second = dummy, dummy

        while n + 1:
            second = second.next
            n -= 1
        
        while second:
            first = first.next
            second = second.next
        
        first.next = first.next.next

        return dummy.next
