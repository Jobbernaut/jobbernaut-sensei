'''
https://leetcode.com/problems/add-two-numbers/
'''

last_solved     = "2026-08-05"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["linked-list"]

class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        output = ListNode()

        curr = output
        carry = 0
        while l1 or l2 or carry:
            new = 0

            if l1:
                new += l1.val
                l1 = l1.next
            
            if l2:
                new += l2.val
                l2 = l2.next
            
            if carry:
                new += carry

            carry = new // 10
            new = new % 10

            curr.next = ListNode(new)
            curr = curr.next
        
        return output.next