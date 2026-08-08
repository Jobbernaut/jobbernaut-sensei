'''
https://leetcode.com/problems/lru-cache/
'''

last_solved     = "2026-08-08"
revisit_in_days = 1
times_reviewed  = 1
difficulty      = "medium"
topic_tags      = ["linked-list", "hash-map", "design"]

class Node:

    def __init__(self, key=-1, value=-1, prev=None, next=None):
        self.key = key
        self.val = value
        self.prev = prev
        self.next = next

class LRUCache:

    def __init__(self, capacity: int):
        self.node_lookup = {}
        self.capacity = capacity

        self.head = Node()
        self.tail = Node()

        self.head.next = self.tail
        self.tail.prev = self.head

    def get(self, key: int) -> int:
        if key in self.node_lookup:
            self._move_to_front(self.node_lookup[key])
            return self.node_lookup[key].val

        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.node_lookup:
            self.node_lookup[key].val = value
            self._move_to_front(self.node_lookup[key])
        else:
            node_to_add = Node(key, value)
            self._insert(node_to_add)
            self.node_lookup[key] = node_to_add

        if len(self.node_lookup) > self.capacity:
            key_to_remove = self.tail.prev.key
            self._remove(self.tail.prev)
            del self.node_lookup[key_to_remove]

    def _remove(self, node_to_remove):
        node_to_remove.prev.next = node_to_remove.next
        node_to_remove.next.prev = node_to_remove.prev
        node_to_remove.prev = None
        node_to_remove.next = None
        return node_to_remove

    def _insert(self, node_to_insert):
        node_to_insert.next = self.head.next
        node_to_insert.prev = self.head
        self.head.next.prev = node_to_insert
        self.head.next = node_to_insert
        return node_to_insert

    def _move_to_front(self, node):
        self._remove(node)
        self._insert(node)
