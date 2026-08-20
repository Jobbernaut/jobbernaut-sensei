'''
https://leetcode.com/problems/lru-cache/
'''

last_solved     = "2026-08-20"
revisit_in_days = 30
times_reviewed  = 4
difficulty      = "medium"
topic_tags      = ["linked-list", "hash-map", "design"]

class Node:

    def __init__(self, key=None, val=None, prev=None, next=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next

class LRUCache:

    def __init__(self, capacity: int):
        self.lookup = {}

        self.head = Node()
        self.tail = Node()

        self.head.next = self.tail
        self.tail.prev = self.head

        self.capacity = capacity

    def get(self, key: int) -> int:
        if key in self.lookup:
            self._add_to_front(key, self.lookup[key].val)
            return self.lookup[key].val

        return -1

    def put(self, key: int, value: int) -> None:
        self._add_to_front(key, value)

        if len(self.lookup) > self.capacity:
            self._remove(self.tail.prev.key)
    
    def _insert(self, key, val):
        node_to_insert = Node(key, val)

        node_to_insert.next = self.head.next
        node_to_insert.prev = self.head

        self.head.next.prev = node_to_insert
        self.head.next = node_to_insert

        self.lookup[key] = node_to_insert
    
    def _remove(self, key):
        node_to_remove = self.lookup[key]

        node_to_remove.prev.next = node_to_remove.next
        node_to_remove.next.prev = node_to_remove.prev

        del self.lookup[key]
    
    def _add_to_front(self, key, val):
        if key in self.lookup:
            self._remove(key)
        self._insert(key, val)