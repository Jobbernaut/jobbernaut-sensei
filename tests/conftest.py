"""
Shared pytest fixtures for sensei test suite.
"""

import os
import pytest
import tempfile
from pathlib import Path
from datetime import date


@pytest.fixture
def temp_workspace(tmp_path, monkeypatch):
    """
    Create a temporary workspace and change directory to it.
    Returns the temp directory path.
    """
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def initialized_workspace(temp_workspace):
    """
    Create a workspace with problems/ directory initialized.
    """
    problems_dir = temp_workspace / "problems"
    problems_dir.mkdir()
    (problems_dir / ".gitkeep").touch()
    return temp_workspace


@pytest.fixture
def sample_problem_file(initialized_workspace):
    """
    Create a sample problem file with valid metadata.
    """
    problem_dir = initialized_workspace / "problems" / "1-arrays" / "217-Contains-Duplicate"
    problem_dir.mkdir(parents=True)
    
    problem_file = problem_dir / "217-Contains-Duplicate.py"
    content = '''\'\'\'
https://leetcode.com/problems/contains-duplicate/
\'\'\'

last_solved     = "2026-06-01"
revisit_in_days = 3
difficulty      = "easy"
topic_tags      = ["arrays", "hash-set"]

class Solution:
    def containsDuplicate(self, nums):
        return len(nums) != len(set(nums))
'''
    problem_file.write_text(content)
    return problem_file


@pytest.fixture
def multiple_problems(initialized_workspace):
    """
    Create multiple problems with different due dates.
    """
    problems = []
    
    # Overdue problem
    p1_dir = initialized_workspace / "problems" / "1-arrays" / "1-Two-Sum"
    p1_dir.mkdir(parents=True)
    p1 = p1_dir / "1-Two-Sum.py"
    p1.write_text(f'''\'\'\'
https://leetcode.com/problems/two-sum/
\'\'\'

last_solved     = "2026-05-01"
revisit_in_days = 7
difficulty      = "easy"
topic_tags      = ["arrays", "hash-map"]

class Solution:
    def twoSum(self, nums, target):
        pass
''')
    problems.append(p1)
    
    # Due today
    today = date.today().isoformat()
    p2_dir = initialized_workspace / "problems" / "2-pointers" / "125-Valid-Palindrome"
    p2_dir.mkdir(parents=True)
    p2 = p2_dir / "125-Valid-Palindrome.py"
    p2.write_text(f'''\'\'\'
https://leetcode.com/problems/valid-palindrome/
\'\'\'

last_solved     = "{today}"
revisit_in_days = 0
difficulty      = "easy"
topic_tags      = ["two-pointers", "string"]

class Solution:
    def isPalindrome(self, s):
        pass
''')
    problems.append(p2)
    
    # Future problem
    p3_dir = initialized_workspace / "problems" / "3-sliding-window" / "3-Longest-Substring"
    p3_dir.mkdir(parents=True)
    p3 = p3_dir / "3-Longest-Substring.py"
    p3.write_text(f'''\'\'\'
https://leetcode.com/problems/longest-substring-without-repeating-characters/
\'\'\'

last_solved     = "2026-06-01"
revisit_in_days = 30
difficulty      = "medium"
topic_tags      = ["sliding-window", "hash-map"]

class Solution:
    def lengthOfLongestSubstring(self, s):
        pass
''')
    problems.append(p3)
    
    return problems


@pytest.fixture
def non_numbered_problem(initialized_workspace):
    """
    Create a problem without a number prefix.
    """
    problem_dir = initialized_workspace / "problems" / "custom" / "Custom-Problem"
    problem_dir.mkdir(parents=True)
    
    problem_file = problem_dir / "Custom-Problem.py"
    content = '''\'\'\'
https://leetcode.com/problems/custom-problem/
\'\'\'

last_solved     = "2026-06-01"
revisit_in_days = 7
difficulty      = "medium"
topic_tags      = ["custom"]

class Solution:
    def solve(self):
        pass
'''
    problem_file.write_text(content)
    return problem_file
