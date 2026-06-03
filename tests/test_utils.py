"""
Unit tests for utils.py module.
"""

import pytest
from datetime import date
from pathlib import Path
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import (
    parse_metadata,
    find_solution_files,
    normalise,
    find_match,
    extract_url,
)


class TestParseMetadata:
    """Test metadata parsing from solution files."""
    
    def test_parse_valid_metadata(self, sample_problem_file):
        """Test parsing a file with valid metadata."""
        meta = parse_metadata(str(sample_problem_file))
        
        assert meta is not None
        assert meta["last_solved"] == date(2026, 6, 1)
        assert meta["revisit_in_days"] == 3
        assert meta["difficulty"] == "easy"
        assert meta["topic_tags"] == ["arrays", "hash-set"]
    
    def test_parse_missing_file(self, tmp_path):
        """Test parsing a non-existent file."""
        result = parse_metadata(str(tmp_path / "nonexistent.py"))
        assert result is None
    
    def test_parse_invalid_syntax(self, tmp_path):
        """Test parsing a file with syntax errors."""
        bad_file = tmp_path / "bad.py"
        bad_file.write_text("this is not valid python{{{")
        assert parse_metadata(str(bad_file)) is None
    
    def test_parse_missing_required_field(self, tmp_path):
        """Test parsing a file missing required metadata."""
        incomplete = tmp_path / "incomplete.py"
        incomplete.write_text('''
last_solved = "2026-06-01"
difficulty = "easy"
# Missing revisit_in_days and topic_tags
''')
        assert parse_metadata(str(incomplete)) is None
    
    def test_parse_invalid_date_format(self, tmp_path):
        """Test parsing with invalid date format."""
        bad_date = tmp_path / "baddate.py"
        bad_date.write_text('''
last_solved = "not-a-date"
revisit_in_days = 3
difficulty = "easy"
topic_tags = ["arrays"]
''')
        assert parse_metadata(str(bad_date)) is None
    
    def test_parse_single_topic_tag(self, tmp_path):
        """Test that single string topic_tag is converted to list."""
        single_tag = tmp_path / "single.py"
        single_tag.write_text('''
last_solved = "2026-06-01"
revisit_in_days = 3
difficulty = "easy"
topic_tags = "arrays"
''')
        meta = parse_metadata(str(single_tag))
        assert meta is not None
        assert meta["topic_tags"] == ["arrays"]


class TestFindSolutionFiles:
    """Test finding solution files in directory."""
    
    def test_find_in_initialized_workspace(self, sample_problem_file, initialized_workspace):
        """Test finding files in a workspace with one problem."""
        files = find_solution_files(str(initialized_workspace / "problems"))
        assert len(files) == 1
        assert "217-Contains-Duplicate.py" in files[0]
    
    def test_find_multiple_problems(self, multiple_problems, initialized_workspace):
        """Test finding multiple problem files."""
        files = find_solution_files(str(initialized_workspace / "problems"))
        assert len(files) == 3
    
    def test_find_nonexistent_directory(self, tmp_path):
        """Test finding files in non-existent directory."""
        files = find_solution_files(str(tmp_path / "nonexistent"))
        assert files == []
    
    def test_exclude_files(self, initialized_workspace, sample_problem_file):
        """Test excluding specific filenames."""
        # Create an excluded file
        (initialized_workspace / "problems" / "mark.py").write_text("# excluded")
        
        files = find_solution_files(
            str(initialized_workspace / "problems"),
            exclude_files={"mark.py"}
        )
        assert len(files) == 1
        assert "mark.py" not in files[0]


class TestNormalise:
    """Test string normalization for fuzzy matching."""
    
    def test_normalise_lowercase(self):
        """Test lowercase conversion."""
        assert normalise("HELLO") == "hello"
    
    def test_normalise_remove_special_chars(self):
        """Test removal of special characters."""
        assert normalise("hello-world_123") == "helloworld123"
    
    def test_normalise_remove_spaces(self):
        """Test removal of spaces."""
        assert normalise("hello world") == "helloworld"
    
    def test_normalise_complex(self):
        """Test complex normalization."""
        assert normalise("217-Contains-Duplicate") == "217containsduplicate"


class TestFindMatch:
    """Test fuzzy matching of problems."""
    
    def test_match_by_number(self, sample_problem_file, initialized_workspace):
        """Test matching by problem number."""
        files = find_solution_files(str(initialized_workspace / "problems"))
        match = find_match("217", files)
        assert match is not None
        assert "217-Contains-Duplicate.py" in match
    
    def test_match_by_slug(self, sample_problem_file, initialized_workspace):
        """Test matching by slug."""
        files = find_solution_files(str(initialized_workspace / "problems"))
        match = find_match("contains-duplicate", files)
        assert match is not None
        assert "217-Contains-Duplicate.py" in match
    
    def test_match_by_title_words(self, sample_problem_file, initialized_workspace):
        """Test matching by title words."""
        files = find_solution_files(str(initialized_workspace / "problems"))
        match = find_match("contains", files)
        assert match is not None
        assert "217-Contains-Duplicate.py" in match
    
    def test_no_match(self, sample_problem_file, initialized_workspace):
        """Test when no match is found."""
        files = find_solution_files(str(initialized_workspace / "problems"))
        match = find_match("999", files)
        assert match is None
    
    def test_multiple_matches_leftmost(self, multiple_problems, initialized_workspace):
        """Test that leftmost match is preferred."""
        files = find_solution_files(str(initialized_workspace / "problems"))
        # "sum" appears in "Two-Sum" and potentially others
        match = find_match("sum", files)
        assert match is not None


class TestExtractUrl:
    """Test URL extraction from problem files."""
    
    def test_extract_valid_url(self, sample_problem_file):
        """Test extracting valid LeetCode URL."""
        url = extract_url(str(sample_problem_file))
        assert url == "https://leetcode.com/problems/contains-duplicate/"
    
    def test_extract_no_url(self, tmp_path):
        """Test file with no URL."""
        no_url = tmp_path / "nourl.py"
        no_url.write_text("class Solution:\n    pass")
        assert extract_url(str(no_url)) is None
    
    def test_extract_skip_template_url(self, tmp_path):
        """Test that template placeholder URLs are skipped."""
        template = tmp_path / "template.py"
        template.write_text('''
\'\'\'
https://leetcode.com/problems/PROBLEM-SLUG/
\'\'\'
class Solution:
    pass
''')
        assert extract_url(str(template)) is None
    
    def test_extract_nonexistent_file(self, tmp_path):
        """Test extracting from non-existent file."""
        assert extract_url(str(tmp_path / "missing.py")) is None
