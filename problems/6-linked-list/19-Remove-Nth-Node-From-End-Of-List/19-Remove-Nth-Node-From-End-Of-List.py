'''
https://leetcode.com/problems/remove-nth-node-from-end-of-list/
'''

last_solved     = "2026-07-16"
revisit_in_days = 7
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["linked-list", "two-pointers"]

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        left, right = head, head

        N = n + 1

        while right and N:
            right = right.next
            N -= 1
        
        if not right and N:
            return head.next
        
        while right:
            left = left.next
            right = right.next
        
        left.next = left.next.next

        return head
