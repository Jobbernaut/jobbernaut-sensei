'''
https://leetcode.com/problems/course-schedule/
'''

last_solved     = "2026-08-14"
revisit_in_days = 9999
times_reviewed  = 5
difficulty      = "medium"
topic_tags      = ["depth-first-search", "breadth-first-search", "graph", "topological-sort", "directed-acyclic-graph"]

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        adj_lst = defaultdict(set)
        indegree_lst = [0] * numCourses

        for course, prereq in prerequisites:
            adj_lst[prereq].add(course)
            indegree_lst[course] += 1

        output = []

        q = deque()

        for course_no, indegree in enumerate(indegree_lst):
            if indegree == 0:
                q.append(course_no)

        while q:
            for _ in range(len(q)):
                curr = q.popleft()

                output.append(curr)

                for each_course in adj_lst[curr]:
                    indegree_lst[each_course] -= 1

                    if indegree_lst[each_course] == 0:
                        q.append(each_course)

        return len(output) == numCourses
