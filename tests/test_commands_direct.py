"""
Direct command tests for code coverage.
These tests import and call main() functions directly instead of using subprocess.
"""

import pytest
import json
import sys
import io
from pathlib import Path
from datetime import date
from unittest.mock import patch, MagicMock

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import sensei
import hint
import mark
import new
import lopen
import revisit


class TestSenseiInitDirect:
    """Direct tests for sensei init."""
    
    def test_init_creates_directory(self, temp_workspace, capsys):
        """Test init creates problems/ directory."""
        sensei.cmd_init()
        
        assert (temp_workspace / "problems").is_dir()
        assert (temp_workspace / "problems" / ".gitkeep").exists()
        
        captured = capsys.readouterr()
        assert "Initialized" in captured.out
    
    def test_init_already_exists(self, initialized_workspace, capsys):
        """Test init when directory exists."""
        sensei.cmd_init()
        
        captured = capsys.readouterr()
        assert "already exists" in captured.out


class TestSenseiStatusDirect:
    """Direct tests for sensei status."""
    
    def test_status_no_problems(self, initialized_workspace, capsys):
        """Test status with no problems."""
        with patch("sys.argv", ["sensei", "status"]):
            sensei.cmd_status()
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["total"] == 0
        assert data["overdue"] == 0
    
    def test_status_with_problems(self, multiple_problems, initialized_workspace, capsys):
        """Test status with multiple problems."""
        with patch("sys.argv", ["sensei", "status"]):
            sensei.cmd_status()
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["total"] == 3
        assert data["overdue"] >= 1
    
    def test_status_missing_directory(self, temp_workspace, capsys):
        """Test status when problems/ missing."""
        with patch("sys.argv", ["sensei", "status"]):
            with pytest.raises(SystemExit) as exc_info:
                sensei.cmd_status()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "error" in data


class TestSenseiHintDirect:
    """Direct tests for sensei hint."""
    
    def test_hint_by_number(self, sample_problem_file, initialized_workspace, capsys):
        """Test hint by problem number."""
        with patch("sys.argv", ["hint", "217"]):
            hint.main()
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["number"] == "217"
        assert "Contains Duplicate" in data["title"]
        assert data["difficulty"] == "easy"
    
    def test_hint_no_match(self, sample_problem_file, initialized_workspace, capsys):
        """Test hint with no match."""
        with patch("sys.argv", ["hint", "999"]):
            with pytest.raises(SystemExit) as exc_info:
                hint.main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "error" in data
    
    def test_hint_missing_directory(self, temp_workspace, capsys):
        """Test hint when problems/ missing."""
        with patch("sys.argv", ["hint", "217"]):
            with pytest.raises(SystemExit) as exc_info:
                hint.main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "error" in data
        assert "not found" in data["error"]


class TestSenseiShowDirect:
    """Direct tests for sensei show."""
    
    def test_show_with_solution(self, sample_problem_file, initialized_workspace, capsys):
        """Test show includes solution."""
        with patch("sys.argv", ["sensei", "show", "217"]):
            sensei.cmd_show()
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "solution" in data
        assert "class Solution" in data["solution"]
    
    def test_show_non_numbered_problem(self, non_numbered_problem, initialized_workspace, capsys):
        """Test show with non-numbered problem."""
        with patch("sys.argv", ["sensei", "show", "custom"]):
            sensei.cmd_show()
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["number"] is None
        assert data["title"] is not None


class TestSenseiMarkDirect:
    """Direct tests for sensei mark."""
    
    def test_mark_with_rating(self, sample_problem_file, initialized_workspace, capsys):
        """Test marking a problem."""
        with patch("sys.argv", ["mark", "217", "--rating", "e"]):
            mark.main()
        
        captured = capsys.readouterr()
        assert "Marked as solved" in captured.out
        
        # Verify file was updated
        content = sample_problem_file.read_text()
        today = date.today().isoformat()
        assert f'last_solved     = "{today}"' in content
    
    def test_mark_no_match(self, sample_problem_file, initialized_workspace, capsys):
        """Test mark with no matching problem."""
        with patch("sys.argv", ["mark", "999", "--rating", "e"]):
            with pytest.raises(SystemExit) as exc_info:
                mark.main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "No match found" in captured.out
    
    def test_mark_missing_directory(self, temp_workspace, capsys):
        """Test mark when problems/ missing."""
        with patch("sys.argv", ["mark", "217", "--rating", "e"]):
            with pytest.raises(SystemExit) as exc_info:
                mark.main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "not found" in captured.out


class TestSenseiRevisitDirect:
    """Direct tests for sensei revisit."""
    
    def test_revisit_json_mode(self, multiple_problems, initialized_workspace, capsys):
        """Test revisit with --json."""
        with patch("sys.argv", ["revisit", "--json"]):
            revisit.main()
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "total_tracked" in data
        assert data["total_tracked"] == 3
    
    def test_revisit_missing_directory_json(self, temp_workspace, capsys):
        """Test revisit when problems/ missing (JSON mode)."""
        with patch("sys.argv", ["revisit", "--json"]):
            with pytest.raises(SystemExit) as exc_info:
                revisit.main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "error" in data
    
    def test_revisit_topic_filter(self, multiple_problems, initialized_workspace, capsys):
        """Test revisit with topic filter."""
        with patch("sys.argv", ["revisit", "--json", "--topic", "arrays"]):
            revisit.main()
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        # Should find problems with "arrays" tag
        assert data["total_tracked"] >= 1
    
    def test_revisit_normal_mode(self, multiple_problems, initialized_workspace, capsys):
        """Test revisit in normal (non-JSON) mode."""
        with patch("sys.argv", ["revisit"]):
            revisit.main()
        
        captured = capsys.readouterr()
        assert "Jobbernaut Sensei Revisit" in captured.out


class TestSenseiNewDirect:
    """Direct tests for sensei new."""
    
    def test_new_creates_problem(self, initialized_workspace, capsys):
        """Test creating a new problem."""
        with patch("sys.argv", ["new", "456", "test-problem", "1-test-category",
                               "-d", "easy", "-t", "arrays", "hash-map"]):
            new.main()
        
        captured = capsys.readouterr()
        assert "Created" in captured.out
        
        # Verify file exists
        problem_path = (initialized_workspace / "problems" / 
                       "1-test-category" / "456-Test-Problem" / "456-Test-Problem.py")
        assert problem_path.exists()
        
        # Verify content
        content = problem_path.read_text()
        assert "https://leetcode.com/problems/test-problem/" in content
        assert 'difficulty      = "easy"' in content
    
    def test_new_already_exists(self, sample_problem_file, initialized_workspace, capsys):
        """Test new when problem already exists."""
        with patch("sys.argv", ["new", "217", "contains-duplicate", "1-arrays",
                               "-d", "easy", "-t", "arrays"]):
            with pytest.raises(SystemExit) as exc_info:
                new.main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Already exists" in captured.out


class TestSenseiLopenDirect:
    """Direct tests for sensei open."""
    
    def test_open_finds_problem(self, sample_problem_file, initialized_workspace, capsys):
        """Test open finds and attempts to open problem."""
        with patch("sys.argv", ["open", "217"]):
            with patch("lopen.open_in_browser") as mock_open:
                lopen.main()
        
        captured = capsys.readouterr()
        assert "Opening" in captured.out
        assert "leetcode.com" in captured.out
    
    def test_open_no_match(self, sample_problem_file, initialized_workspace, capsys):
        """Test open with no match."""
        with patch("sys.argv", ["open", "999"]):
            with pytest.raises(SystemExit) as exc_info:
                lopen.main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "No match found" in captured.out
    
    def test_open_missing_directory(self, temp_workspace, capsys):
        """Test open when problems/ missing."""
        with patch("sys.argv", ["open", "217"]):
            with pytest.raises(SystemExit) as exc_info:
                lopen.main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "not found" in captured.out


class TestSenseiMainDirect:
    """Direct tests for main sensei entry point."""
    
    def test_main_no_command(self, capsys):
        """Test main with no command shows help."""
        with patch("sys.argv", ["sensei"]):
            with pytest.raises(SystemExit) as exc_info:
                sensei.main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Usage: sensei <command>" in captured.out
        assert "init" in captured.out
        assert "mark" in captured.out
    
    def test_main_unknown_command(self, capsys):
        """Test main with unknown command."""
        with patch("sys.argv", ["sensei", "unknown"]):
            with pytest.raises(SystemExit) as exc_info:
                sensei.main()
            assert exc_info.value.code == 1
        
        captured = capsys.readouterr()
        assert "Unknown command" in captured.out
    
    def test_main_init_command(self, temp_workspace, capsys):
        """Test main routing to init command."""
        with patch("sys.argv", ["sensei", "init"]):
            sensei.main()
        
        assert (temp_workspace / "problems").is_dir()
    
    def test_main_status_command(self, initialized_workspace, capsys):
        """Test main routing to status command."""
        with patch("sys.argv", ["sensei", "status"]):
            sensei.main()
        
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "total" in data
