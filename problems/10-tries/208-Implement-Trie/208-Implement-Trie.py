'''
https://leetcode.com/problems/implement-trie-prefix-tree/
'''

last_solved     = "2026-07-07"
revisit_in_days = 45
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["trie"]

class TrieNode:
    def __init__(self):
        self.children  = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.trie = TrieNode()
    
    def traverse(self, string: str, insert_mode: bool=False) -> None:
        curr = self.trie

        for character in string:
            if character not in curr.children:
                if insert_mode:
                    curr.children[character] = TrieNode()
                else:
                    return None
            curr = curr.children[character]

        if insert_mode:
            curr.is_end_of_word = True

        return curr

    def insert(self, word: str) -> None:
        self.traverse(word, True)

    def search(self, word: str) -> bool:
        res = self.traverse(word)
        return res is not None and res.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        return self.traverse(prefix) is not None
