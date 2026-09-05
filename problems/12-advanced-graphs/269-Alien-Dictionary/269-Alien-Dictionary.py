'''
https://leetcode.com/problems/alien-dictionary/
'''

last_solved     = "2026-09-05"
revisit_in_days = 7
times_reviewed  = 3
difficulty      = "hard"
topic_tags      = ["array", "string", "depth-first-search", "breadth-first-search", "graph", "topological-sort", "directed-acyclic-graph"]

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        alien_dictionary = defaultdict(list)
        indegree = defaultdict(int)

        for word in words:
            for c in word:
                alien_dictionary[c], indegree[c]

        for idx in range(0, len(words) - 1):
            prev = words[idx]
            curr = words[idx + 1]

            i, j = 0, 0
            while i < len(prev) and j < len(curr):
                if prev[i] != curr[j]:
                    alien_dictionary[prev[i]].append(curr[j])
                    indegree[curr[j]] += 1
                    break

                i += 1
                j += 1

            if i != len(prev) and j == len(curr):
                return ""

        output = []
        queue = deque()

        for c, deg in indegree.items():
            if not deg:
                queue.append(c)

        while queue:
            c = queue.popleft()
            output.append(c)

            for n_c in alien_dictionary[c]:
                indegree[n_c] -= 1

                if not indegree[n_c]:
                    queue.append(n_c)

        if len(output) != len(indegree):
            return ""

        return "".join(output)
