'''
https://leetcode.com/problems/implement-trie-prefix-tree/
'''

last_solved     = "2026-06-24"
revisit_in_days = 3
difficulty      = "medium"
topic_tags      = ["trie"]

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.trie = TrieNode()

    def insert(self, word: str) -> None:
        node = self.trie

        for character in word:
            if character not in node.children:
                node.children[character] = TrieNode()
            node = node.children[character]

        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self.trie

        for character in word:
            if character not in node.children:
                return False
            node = node.children[character]
        
        return node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        node = self.trie

        for character in prefix:
            if character not in node.children:
                return False
            node = node.children[character]
        
        return True
