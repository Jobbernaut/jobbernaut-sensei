'''
https://leetcode.com/problems/course-schedule-ii/
'''

last_solved     = "2026-08-08"
revisit_in_days = 7
times_reviewed  = 3
difficulty      = "medium"
topic_tags      = ["graphs", "topological-sort", "dfs"]

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
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

        if len(output) < numCourses:
            return []
        
        return output
