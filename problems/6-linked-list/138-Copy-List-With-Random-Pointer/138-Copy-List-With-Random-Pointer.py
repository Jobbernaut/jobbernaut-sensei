'''
https://leetcode.com/problems/copy-list-with-random-pointer/
'''

last_solved     = "2026-07-08"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "medium"
topic_tags      = ["linked-list", "hash-map"]

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        if not head:
            return head
            
        orig_copy_d = {}

        copy_list = Node(head.val)
        orig_copy_d[head] = copy_list

        orig = head
        copy = copy_list

        while orig:
            copy.val = orig.val

            orig_copy_d[orig] = copy

            if orig.next is None:
                copy.next = None
            else:
                if orig.next in orig_copy_d:
                    copy.next = orig_copy_d[orig.next]
                else:
                    copy.next = Node(orig.next.val)
                    orig_copy_d[orig.next] = copy.next
            
            if orig.random is None:
                copy.random = None
            else:
                if orig.random in orig_copy_d:
                    copy.random = orig_copy_d[orig.random]
                else:
                    copy.random = Node(orig.random.val)
                    orig_copy_d[orig.random] = copy.random
            
            orig = orig.next
            copy = copy.next

        return copy_list