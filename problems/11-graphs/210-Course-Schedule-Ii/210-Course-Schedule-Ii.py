'''
https://leetcode.com/problems/course-schedule-ii/
'''

last_solved     = "2026-09-01"
revisit_in_days = 14
times_reviewed  = 6
difficulty      = "medium"
topic_tags      = ["graphs", "topological-sort", "dfs"]

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        output = []

        indegree = [0] * numCourses
        adj_list = defaultdict(list)
        queue = deque()

        for subseq, prereq in prerequisites:
            adj_list[prereq].append(subseq)
            indegree[subseq] += 1

        for idx, degree in enumerate(indegree):
            if not degree:
                queue.append(idx)

        while queue:
            prereq = queue.popleft()
            output.append(prereq)

            for subseq in adj_list[prereq]:
                indegree[subseq] -= 1

                if not indegree[subseq]:
                    queue.append(subseq)

        if len(output) < numCourses:
            return []

        return output
