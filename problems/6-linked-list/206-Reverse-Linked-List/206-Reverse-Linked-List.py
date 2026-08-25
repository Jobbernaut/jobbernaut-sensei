'''
https://leetcode.com/problems/reverse-linked-list/
'''

last_solved     = "2026-05-27"
revisit_in_days = 130
difficulty      = "easy"
topic_tags      = ["linked-list", "recursion"]
times_reviewed  = 5

from typing import List, Optional


# Definition for singly-linked list node
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Reverse a singly linked list iteratively.
        
        Algorithm:
        1. Keep track of previous node (initially None)
        2. Walk through the list with current pointer
        3. Before changing current.next, save the next node
        4. Flip current.next to point to previous
        5. Move pointers forward
        6. Return prev (new head)
        
        Time: O(n), Space: O(1)
        """
        prev = None
        current = head
        
        while current:
            nxt = current.next      # Save the next node before we lose it
            current.next = prev     # Flip the pointer
            prev = current          # Move prev forward
            current = nxt           # Move current forward
        
        return prev
