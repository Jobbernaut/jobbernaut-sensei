'''
https://leetcode.com/problems/copy-list-with-random-pointer/
'''

last_solved     = "2026-07-07"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["linked-list", "hash-map"]

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return head

        lookup = {}

        copy = Node(head.val)

        org = head
        curr = copy

        lookup[org] = curr

        while org.next:
            curr.next = Node(org.next.val)
            lookup[org.next] = curr.next

            curr = curr.next
            org = org.next
        
        org = head
        curr = copy

        while org:
            if org.random:
                curr.random = lookup[org.random]
            else:
                curr.random = None

            curr = curr.next
            org = org.next
        
        return copy