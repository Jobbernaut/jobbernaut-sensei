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
import progress


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
        assert "LeetCode Sensei Revisit" in captured.out


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

    def test_main_progress_command(self, initialized_workspace, capsys):
        """Test main routing to progress command."""
        (initialized_workspace / "problems" / "NEETCODE150.md").write_text(
            "# NeetCode 150\n\nTotal: **0 / 150**\n\n## 1. Arrays\n- [ ] 1. Problem (Easy)\n"
        )
        with patch("sys.argv", ["sensei", "progress"]):
            progress.main()
        captured = capsys.readouterr()
        assert "NeetCode 150" in captured.out


class TestSenseiNewUrlMode:
    """Tests for sensei new URL mode."""

    def test_slug_extracted_from_url(self, initialized_workspace, capsys):
        """URL mode derives slug from URL and scaffolds correctly."""
        mock_meta = {
            "number": "217",
            "difficulty": "easy",
            "tags": ["arrays", "hash-set"],
        }
        with patch("new.fetch_leetcode_metadata", return_value=mock_meta):
            with patch("sys.argv", ["new", "https://leetcode.com/problems/contains-duplicate/",
                                    "1-arrays-and-hashing"]):
                new.main()

        captured = capsys.readouterr()
        assert "Created" in captured.out
        path = (initialized_workspace / "problems" / "1-arrays-and-hashing"
                / "217-Contains-Duplicate" / "217-Contains-Duplicate.py")
        assert path.exists()
        content = path.read_text()
        assert 'difficulty      = "easy"' in content
        assert "contains-duplicate" in content

    def test_api_metadata_used_for_difficulty_and_tags(self, initialized_workspace, capsys):
        """Difficulty and tags from API are written into the scaffolded file."""
        mock_meta = {
            "number": "139",
            "difficulty": "medium",
            "tags": ["dynamic-programming", "trie"],
        }
        with patch("new.fetch_leetcode_metadata", return_value=mock_meta):
            with patch("sys.argv", ["new", "https://leetcode.com/problems/word-break/",
                                    "13-1d-dynamic-programming"]):
                new.main()

        path = (initialized_workspace / "problems" / "13-1d-dynamic-programming"
                / "139-Word-Break" / "139-Word-Break.py")
        content = path.read_text()
        assert 'difficulty      = "medium"' in content
        assert "dynamic-programming" in content

    def test_fallback_when_api_unavailable(self, initialized_workspace, capsys):
        """Falls back to manual flags when API returns None."""
        with patch("new.fetch_leetcode_metadata", return_value=None):
            with patch("sys.argv", ["new", "https://leetcode.com/problems/word-break/",
                                    "13-1d-dynamic-programming",
                                    "-d", "medium", "-t", "dynamic-programming"]):
                new.main()

        captured = capsys.readouterr()
        assert "warn" in captured.out
        path = (initialized_workspace / "problems" / "13-1d-dynamic-programming"
                / "0-Word-Break" / "0-Word-Break.py")
        assert path.exists()

    def test_fallback_without_manual_flags_exits(self, initialized_workspace, capsys):
        """Falls back and exits when API unavailable and no -d/-t flags provided."""
        with patch("new.fetch_leetcode_metadata", return_value=None):
            with patch("sys.argv", ["new", "https://leetcode.com/problems/word-break/",
                                    "13-1d-dynamic-programming"]):
                with pytest.raises(SystemExit) as exc_info:
                    new.main()
                assert exc_info.value.code == 1

    def test_invalid_url_exits(self, initialized_workspace, capsys):
        """Non-LeetCode URL exits with error."""
        with patch("sys.argv", ["new", "https://example.com/not-leetcode/",
                                "1-arrays-and-hashing"]):
            with pytest.raises(SystemExit) as exc_info:
                new.main()
            assert exc_info.value.code == 1

    def test_legacy_mode_unchanged(self, initialized_workspace, capsys):
        """Legacy positional form still works."""
        with patch("sys.argv", ["new", "999", "legacy-problem", "1-arrays-and-hashing",
                                "-d", "hard", "-t", "graphs"]):
            new.main()

        path = (initialized_workspace / "problems" / "1-arrays-and-hashing"
                / "999-Legacy-Problem" / "999-Legacy-Problem.py")
        assert path.exists()
        assert 'difficulty      = "hard"' in path.read_text()


class TestProgressDashboard:
    """Tests for sensei progress command."""

    SAMPLE_MD = """\
# NeetCode 150 Progress Tracker

Total Completed: **2 / 4**

## 1. Arrays & Hashing
- [x] 217. Contains Duplicate (Easy)
- [ ] 49. Group Anagrams (Medium)

## 2. Two Pointers
- [x] 125. Valid Palindrome (Easy)
- [ ] 42. Trapping Rain Water (Hard)
"""

    @pytest.fixture
    def progress_workspace(self, initialized_workspace):
        (initialized_workspace / "problems" / "NEETCODE150.md").write_text(self.SAMPLE_MD)
        return initialized_workspace

    def test_parse_neetcode150_sections(self, progress_workspace):
        md = progress_workspace / "problems" / "NEETCODE150.md"
        sections = progress._parse_neetcode150(str(md))
        assert len(sections) == 2
        assert sections[0]["topic"] == "Arrays & Hashing"
        assert len(sections[0]["problems"]) == 2
        assert sections[0]["problems"][0]["number"] == 217
        assert sections[0]["problems"][0]["difficulty"] == "easy"

    def test_terminal_output_shows_dashboard(self, progress_workspace, capsys):
        with patch("sys.argv", ["sensei", "progress"]):
            progress.main()
        out = capsys.readouterr().out
        assert "NeetCode 150" in out
        assert "Completed" in out
        assert "By Topic" in out
        assert "Velocity" in out

    def test_json_output_structure(self, progress_workspace, capsys):
        with patch("sys.argv", ["sensei", "progress", "--json"]):
            progress.main()
        data = json.loads(capsys.readouterr().out)
        assert "completed" in data
        assert "total" in data
        assert "by_difficulty" in data
        assert "by_topic" in data
        assert "velocity_per_week" in data
        assert len(data["by_topic"]) == 2

    def test_json_topic_counts_match_filesystem(self, progress_workspace, capsys):
        """Solved count is driven by filesystem, not .md checkboxes."""
        p_dir = progress_workspace / "problems" / "1-arrays-and-hashing" / "217-Contains-Duplicate"
        p_dir.mkdir(parents=True)
        (p_dir / "217-Contains-Duplicate.py").write_text(
            '\'\'\'https://leetcode.com/problems/contains-duplicate/\'\'\'\n'
            'last_solved = "2026-08-10"\nrevisit_in_days = 30\n'
            'difficulty = "easy"\ntopic_tags = ["arrays"]\n'
        )
        with patch("sys.argv", ["sensei", "progress", "--json"]):
            progress.main()
        data = json.loads(capsys.readouterr().out)
        assert data["completed"] == 1
        arrays_topic = next(t for t in data["by_topic"] if t["topic"] == "Arrays & Hashing")
        assert arrays_topic["done"] == 1
        assert arrays_topic["total"] == 2

    def test_missing_problems_dir_exits(self, temp_workspace, capsys):
        with patch("sys.argv", ["sensei", "progress"]):
            with pytest.raises(SystemExit) as exc_info:
                progress.main()
            assert exc_info.value.code == 1

    def test_missing_neetcode_md_exits(self, initialized_workspace, capsys):
        with patch("sys.argv", ["sensei", "progress"]):
            with pytest.raises(SystemExit) as exc_info:
                progress.main()
            assert exc_info.value.code == 1
