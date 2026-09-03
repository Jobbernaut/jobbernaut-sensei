'''
https://leetcode.com/problems/word-ladder/
'''

last_solved     = "2026-09-03"
revisit_in_days = 3
times_reviewed  = 2
difficulty      = "hard"
topic_tags      = ["hash-table", "string", "breadth-first-search", "bidirectional-search"]

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        patterns = defaultdict(list)

        for word in wordList:
            for idx in range(len(word)):
                pattern = word[:idx] + "*" + word[idx+1:]
                patterns[pattern].append(word)

        queue = deque()
        visited = set()
        queue.append(beginWord)
        visited.add(beginWord)

        level = 0
        while queue:
            level += 1
            for _ in range(len(queue)):
                word = queue.popleft()

                if word == endWord:
                    return level

                for idx in range(len(word)):
                    pattern = word[:idx] + "*" + word[idx+1:]
                    for neighbor in patterns[pattern]:
                        if neighbor not in visited:
                            queue.append(neighbor)
                            visited.add(neighbor)

        return 0
