'''
https://leetcode.com/problems/lru-cache/
'''

last_solved     = "2026-08-10"
revisit_in_days = 3
times_reviewed  = 2
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
        self.head = Node()
        self.tail = Node()

        self.head.next = self.tail
        self.tail.prev = self.head

        self.lookup = {}

        self.capacity = capacity

    def get(self, key: int) -> int:
        if key not in self.lookup:
            return -1
        
        self._move_to_front(self.lookup[key])

        return self.lookup[key].val

    def put(self, key: int, value: int) -> None:
        if key in self.lookup:
            self.lookup[key].val = value
            self._move_to_front(self.lookup[key])
        else:
            self._insert(Node(key, value))

            if len(self.lookup) > self.capacity:
                self._remove(self.tail.prev)
    
    def _remove(self, node_to_remove):
        node_to_remove.prev.next = node_to_remove.next
        node_to_remove.next.prev = node_to_remove.prev

        node_to_remove.prev = None
        node_to_remove.next = None

        del self.lookup[node_to_remove.key]
    
    def _insert(self, node_to_insert):
        self.lookup[node_to_insert.key] = node_to_insert

        node_to_insert.prev = self.head
        node_to_insert.next = self.head.next

        self.head.next = node_to_insert
        node_to_insert.next.prev = node_to_insert
    
    def _move_to_front(self, node_to_move):
        self._remove(node_to_move)
        self._insert(node_to_move)
