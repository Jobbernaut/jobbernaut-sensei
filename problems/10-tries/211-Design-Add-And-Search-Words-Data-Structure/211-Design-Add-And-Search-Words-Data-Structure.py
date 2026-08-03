'''
https://leetcode.com/problems/design-add-and-search-words-data-structure/
'''

last_solved     = "2026-07-21"
revisit_in_days = 18
times_reviewed  = 7
difficulty      = "medium"
topic_tags      = ["trie", "dfs"]

class WordDictionaryNode:
    def __init__(self):
        self.children: dict = {}
        self.is_end: bool = False

class WordDictionary:
    def __init__(self):
        self.word_dictionary: WordDictionaryNode = WordDictionaryNode()

    def addWord(self, word: str) -> None:
        curr = self.word_dictionary

        for c in word:
            if c not in curr.children:
                curr.children[c] = WordDictionaryNode()
            curr = curr.children[c]
        
        curr.is_end = True

    def search(self, word: str) -> bool:
        def traverse(curr: WordDictionaryNode, idx: int, string: str) -> bool:
            if idx == len(string):
                return curr.is_end
            
            if string[idx] != "." and string[idx] not in curr.children:
                return False
            
            if string[idx] != "." and string[idx] in curr.children:
                return traverse(curr.children[string[idx]], idx + 1, string)
            
            if string[idx] == ".":
                return any(traverse(node, idx + 1, string) for node in curr.children.values())

        return traverse(self.word_dictionary, 0, word)