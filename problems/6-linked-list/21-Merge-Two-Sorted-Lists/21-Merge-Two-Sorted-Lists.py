'''
https://leetcode.com/problems/merge-two-sorted-lists/
'''

last_solved     = "2026-05-29"
revisit_in_days = 90
difficulty      = "easy"
topic_tags      = ["linked-list"]
times_reviewed  = 5

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        tail = dummy

        while list1 and list2:
            if list1.val < list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next
            tail = tail.next
        
        tail.next = list1 or list2
        
        return dummy.next