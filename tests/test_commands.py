"""
Tests for CLI commands.
"""

import pytest
import json
import subprocess
import sys
import io
from pathlib import Path
from datetime import date
from unittest.mock import patch

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import sensei
import hint
import mark
import new
import lopen
import revisit
from mark import compute_interval, update_metadata


class TestSenseiInit:
    """Test sensei init command."""
    
    def test_init_creates_directory(self, temp_workspace):
        """Test that init creates problems/ directory."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "init"],
            capture_output=True,
            text=True,
            cwd=str(temp_workspace)
        )
        
        assert result.returncode == 0
        assert (temp_workspace / "problems").is_dir()
        assert (temp_workspace / "problems" / ".gitkeep").exists()
    
    def test_init_already_exists(self, initialized_workspace):
        """Test init when directory already exists."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "init"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 0
        assert "already exists" in result.stdout


class TestSenseiStatus:
    """Test sensei status command."""
    
    def test_status_no_problems(self, initialized_workspace):
        """Test status with no problems."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "status"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["total"] == 0
        assert data["overdue"] == 0
        assert data["due_today"] == 0
    
    def test_status_with_problems(self, multiple_problems, initialized_workspace):
        """Test status with multiple problems."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "status"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["total"] == 3
        assert data["overdue"] >= 1  # At least one overdue
        assert len(data["problems"]) >= 2  # overdue + due_today
    
    def test_status_missing_directory(self, temp_workspace):
        """Test status when problems/ doesn't exist."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "status"],
            capture_output=True,
            text=True,
            cwd=str(temp_workspace)
        )
        
        assert result.returncode == 1
        data = json.loads(result.stdout)
        assert "error" in data
        assert "not found" in data["error"]


class TestSenseiHint:
    """Test sensei hint command."""
    
    def test_hint_by_number(self, sample_problem_file, initialized_workspace):
        """Test hint using problem number."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "hint", "217"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["number"] == "217"
        assert "Contains Duplicate" in data["title"]
        assert data["difficulty"] == "easy"
        assert "url" in data
        assert "solution" not in data  # hint shouldn't show solution
    
    def test_hint_no_match(self, sample_problem_file, initialized_workspace):
        """Test hint with no matching problem."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "hint", "999"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 1
        data = json.loads(result.stdout)
        assert "error" in data
        assert "No match found" in data["error"]
    
    def test_hint_non_numbered_problem(self, non_numbered_problem, initialized_workspace):
        """Test hint with non-numbered problem (bug fix verification)."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "hint", "custom"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["number"] is None
        assert data["title"] is not None  # Should not crash


class TestSenseiShow:
    """Test sensei show command."""
    
    def test_show_with_solution(self, sample_problem_file, initialized_workspace):
        """Test show includes solution code."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "show", "217"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "solution" in data
        assert "class Solution" in data["solution"]
    
    def test_show_non_numbered_problem(self, non_numbered_problem, initialized_workspace):
        """Test show with non-numbered problem (bug fix verification)."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "show", "custom"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert data["number"] is None
        assert data["title"] is not None
        assert "solution" in data


class TestSenseiMark:
    """Test sensei mark command."""
    
    def test_mark_with_rating(self, sample_problem_file, initialized_workspace):
        """Test marking a problem with specific rating."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "mark", "217", "--rating", "e"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 0
        assert "Marked as solved" in result.stdout
        
        # Verify file was updated
        content = sample_problem_file.read_text()
        today = date.today().isoformat()
        assert f'last_solved     = "{today}"' in content
    
    def test_mark_missing_directory(self, temp_workspace):
        """Test mark when problems/ doesn't exist."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "mark", "217", "--rating", "e"],
            capture_output=True,
            text=True,
            cwd=str(temp_workspace)
        )
        
        assert result.returncode == 1
        assert "not found" in result.stdout


class TestComputeInterval:
    """Test SRS interval computation logic."""
    
    def test_bootstrap_phase_first_attempt(self):
        """Test bootstrap: first attempt -> 3 days."""
        assert compute_interval("e", times_reviewed=0, prev_interval=0) == 3
        assert compute_interval("g", times_reviewed=0, prev_interval=0) == 3
        assert compute_interval("h", times_reviewed=0, prev_interval=0) == 3
        assert compute_interval("s", times_reviewed=0, prev_interval=0) == 3
    
    def test_bootstrap_phase_first_review(self):
        """Test bootstrap: first review -> 7 days."""
        assert compute_interval("e", times_reviewed=1, prev_interval=3) == 7
        assert compute_interval("g", times_reviewed=1, prev_interval=3) == 7
        assert compute_interval("h", times_reviewed=1, prev_interval=3) == 7
        assert compute_interval("s", times_reviewed=1, prev_interval=3) == 7
    
    def test_full_srs_easy(self):
        """Test full SRS: easy rating."""
        assert compute_interval("e", times_reviewed=2, prev_interval=7) == 90
    
    def test_full_srs_easy_repeated(self):
        """Test full SRS: easy always returns 90 days (no exponential growth)."""
        assert compute_interval("e", times_reviewed=3, prev_interval=90) == 90
        assert compute_interval("e", times_reviewed=5, prev_interval=90) == 90
    
    def test_full_srs_good(self):
        """Test full SRS: good rating."""
        assert compute_interval("g", times_reviewed=2, prev_interval=7) == 30
        assert compute_interval("g", times_reviewed=5, prev_interval=30) == 30
    
    def test_full_srs_hard(self):
        """Test full SRS: hard rating → always 7 days."""
        assert compute_interval("h", times_reviewed=2, prev_interval=7) == 7
        assert compute_interval("h", times_reviewed=3, prev_interval=7) == 7
    
    def test_full_srs_struggled(self):
        """Test full SRS: struggled rating."""
        assert compute_interval("s", times_reviewed=2, prev_interval=7) == 3
        assert compute_interval("s", times_reviewed=10, prev_interval=3) == 3


class TestUpdateMetadata:
    """Test metadata update logic."""
    
    def test_update_increments_times_reviewed(self):
        """Test that times_reviewed is incremented."""
        source = '''
last_solved = "2026-05-01"
revisit_in_days = 7
difficulty = "easy"
topic_tags = ["arrays"]
times_reviewed = 2

class Solution:
    pass
'''
        updated, days = update_metadata(source, "2026-06-02", "e")
        assert 'times_reviewed  = 3' in updated
        assert days == 90
    
    def test_update_adds_times_reviewed_if_missing(self):
        """Test that times_reviewed is added if not present."""
        source = '''
last_solved = "2026-05-01"
revisit_in_days = 7
difficulty = "easy"
topic_tags = ["arrays"]

class Solution:
    pass
'''
        updated, days = update_metadata(source, "2026-06-02", "e")
        assert 'times_reviewed  = 1' in updated
    
    def test_update_changes_date(self):
        """Test that last_solved date is updated."""
        source = '''
last_solved = "2026-05-01"
revisit_in_days = 7
difficulty = "easy"
topic_tags = ["arrays"]
times_reviewed = 0

class Solution:
    pass
'''
        updated, days = update_metadata(source, "2026-06-02", "g")
        assert 'last_solved     = "2026-06-02"' in updated


class TestSenseiRevisit:
    """Test sensei revisit command."""
    
    def test_revisit_json_mode(self, multiple_problems, initialized_workspace):
        """Test revisit with --json flag."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "revisit", "--json"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "total_tracked" in data
        assert "problems" in data
        assert len(data["problems"]) == 3
    
    def test_revisit_missing_directory(self, temp_workspace):
        """Test revisit when problems/ doesn't exist."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "revisit", "--json"],
            capture_output=True,
            text=True,
            cwd=str(temp_workspace)
        )
        
        assert result.returncode == 1
        data = json.loads(result.stdout)
        assert "error" in data


class TestSenseiNew:
    """Test sensei new command."""
    
    def test_new_creates_problem(self, initialized_workspace):
        """Test creating a new problem."""
        result = subprocess.run(
            [sys.executable, "-m", "sensei", "new", 
             "123", "test-problem", "1-test-category",
             "-d", "easy", "-t", "arrays", "hash-map"],
            capture_output=True,
            text=True,
            cwd=str(initialized_workspace)
        )
        
        assert result.returncode == 0
        assert "Created" in result.stdout
        
        # Verify file exists
        problem_path = (initialized_workspace / "problems" / 
                       "1-test-category" / "123-Test-Problem" / "123-Test-Problem.py")
        assert problem_path.exists()
        
        # Verify content
        content = problem_path.read_text()
        assert "https://leetcode.com/problems/test-problem/" in content
        assert 'difficulty      = "easy"' in content
        assert '"arrays"' in content
        assert '"hash-map"' in content
