'''
https://leetcode.com/problems/reorder-list/
'''

last_solved     = "2026-07-16"
revisit_in_days = 43
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["linked-list", "two-pointers"]

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        # Phase 1: Find the middle point
        slow, fast = head, head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        
        # Phase 2: Reverse from middle of the list
        prev = None
        curr = slow.next

        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        
        slow.next = None
        
        # Phase 3: Splice head and prev together
        lst_1 = head
        lst_2 = prev

        while lst_1 and lst_2:
            lst_1_nxt = lst_1.next
            lst_2_nxt = lst_2.next

            lst_1.next = lst_2
            lst_2.next = lst_1_nxt

            lst_1 = lst_1_nxt
            lst_2 = lst_2_nxt
        
        return head