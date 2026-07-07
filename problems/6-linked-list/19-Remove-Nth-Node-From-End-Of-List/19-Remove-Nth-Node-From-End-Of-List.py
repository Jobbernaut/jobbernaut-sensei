'''
https://leetcode.com/problems/remove-nth-node-from-end-of-list/
'''

last_solved     = "2026-07-07"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["linked-list", "two-pointers"]

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        left, right = head, head
        move = n + 1

        while move and right:
            right = right.next
            move -= 1
        
        if move and not right:
            return head.next

        while right:
            left = left.next
            right = right.next
        
        left.next = left.next.next

        return head
