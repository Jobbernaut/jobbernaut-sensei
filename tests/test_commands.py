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
from mark import (
    compute_interval,
    update_metadata,
    compute_spread_interval,
    SMOOTH_OVERLOAD_CAP,
    RATING_ESCALATION,
)


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
        assert "future" in data  # future count must be present
    
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
        assert "future" in data  # future count must match revisit --json schema
    
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
        assert "solution" not in data        # hint shouldn't show solution
        assert "times_reviewed" in data      # coaching metadata must be present
    
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
    """Test hardcoded SRS interval computation."""

    def test_trivial(self):
        """Trivial → 90 days."""
        assert compute_interval("t") == 90

    def test_easy(self):
        """Easy → 30 days."""
        assert compute_interval("e") == 30

    def test_good(self):
        """Good → 7 days."""
        assert compute_interval("g") == 7

    def test_hard(self):
        """Hard → 3 days."""
        assert compute_interval("h") == 3

    def test_struggled(self):
        """Struggled → 1 day."""
        assert compute_interval("s") == 1


class TestUpdateMetadata:
    """Test metadata update logic."""

    def test_update_changes_date(self):
        """Test that last_solved date is updated."""
        source = '''
last_solved = "2026-05-01"
revisit_in_days = 7
difficulty = "easy"
topic_tags = ["arrays"]

class Solution:
    pass
'''
        updated, days = update_metadata(source, "2026-06-02", "g")
        assert 'last_solved     = "2026-06-02"' in updated

    def test_update_sets_interval_trivial(self):
        """Test revisit_in_days is set to 90 for trivial."""
        source = '''
last_solved = "2026-05-01"
revisit_in_days = 3
difficulty = "easy"
topic_tags = ["arrays"]

class Solution:
    pass
'''
        updated, days = update_metadata(source, "2026-06-02", "t")
        assert days == 90
        assert "revisit_in_days = 90" in updated

    def test_update_sets_interval_easy(self):
        """Test revisit_in_days is set to 30 for easy."""
        source = '''
last_solved = "2026-05-01"
revisit_in_days = 3
difficulty = "easy"
topic_tags = ["arrays"]

class Solution:
    pass
'''
        updated, days = update_metadata(source, "2026-06-02", "e")
        assert days == 30
        assert "revisit_in_days = 30" in updated

    def test_update_sets_interval_good(self):
        """Test revisit_in_days is set to 7 for good."""
        source = '''
last_solved = "2026-05-01"
revisit_in_days = 30
difficulty = "easy"
topic_tags = ["arrays"]

class Solution:
    pass
'''
        updated, days = update_metadata(source, "2026-06-02", "g")
        assert days == 7
        assert "revisit_in_days = 7" in updated

    def test_update_sets_interval_hard(self):
        """Test revisit_in_days is set to 3 for hard."""
        source = '''
last_solved = "2026-05-01"
revisit_in_days = 7
difficulty = "easy"
topic_tags = ["arrays"]

class Solution:
    pass
'''
        updated, days = update_metadata(source, "2026-06-02", "h")
        assert days == 3
        assert "revisit_in_days = 3" in updated

    def test_update_sets_interval_struggled(self):
        """Test revisit_in_days is set to 1 for struggled."""
        source = '''
last_solved = "2026-05-01"
revisit_in_days = 7
difficulty = "easy"
topic_tags = ["arrays"]

class Solution:
    pass
'''
        updated, days = update_metadata(source, "2026-06-02", "s")
        assert days == 1
        assert "revisit_in_days = 1" in updated

    def test_update_does_not_touch_times_reviewed(self):
        """Test that times_reviewed is not modified (field is no longer managed)."""
        source = '''
last_solved = "2026-05-01"
revisit_in_days = 7
difficulty = "easy"
topic_tags = ["arrays"]

class Solution:
    pass
'''
        updated, _ = update_metadata(source, "2026-06-02", "e")
        assert "times_reviewed" not in updated


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
        # New problems must start with times_reviewed = 0
        assert "times_reviewed  = 0" in content
        # New problems must start at revisit_in_days = 1 (progression gate)
        assert "revisit_in_days = 1" in content


class TestProgressionGate:
    """Test new-problem progression cap enforcement."""

    def test_first_solve_capped_at_1(self):
        """Rating e on first solve should be capped at 1 day."""
        from mark import get_progression_cap, compute_interval
        cap = get_progression_cap(0)  # times_reviewed = 0
        base = compute_interval("e")   # 30 days
        assert cap == 1
        assert base > cap

    def test_second_solve_capped_at_3(self):
        """times_reviewed = 1 → max 3 days."""
        from mark import get_progression_cap
        assert get_progression_cap(1) == 3

    def test_third_solve_capped_at_7(self):
        """times_reviewed = 2 → max 7 days."""
        from mark import get_progression_cap
        assert get_progression_cap(2) == 7

    def test_fourth_solve_capped_at_30(self):
        """times_reviewed = 3 → max 30 days."""
        from mark import get_progression_cap
        assert get_progression_cap(3) == 30

    def test_fifth_solve_uncapped(self):
        """times_reviewed = 4 → no cap (full SRS)."""
        from mark import get_progression_cap
        assert get_progression_cap(4) is None

    def test_rating_under_cap_not_affected(self):
        """Rating s (1 day) on review #3 stays 1 day — under 30-day cap."""
        from mark import get_progression_cap, compute_interval
        cap = get_progression_cap(3)
        base = compute_interval("s")
        assert base <= cap  # no capping needed


class TestTimesReviewedField:
    """Test times_reviewed tracking in update_metadata."""

    def test_times_reviewed_inserted_if_absent(self):
        """If times_reviewed absent, it should be inserted after revisit_in_days."""
        source = '''last_solved     = "2026-05-01"
revisit_in_days = 7
difficulty      = "easy"
topic_tags      = ["arrays"]
'''
        updated, _ = update_metadata(source, "2026-06-01", "g",
                                     new_times_reviewed=1)
        assert "times_reviewed  = 1" in updated

    def test_times_reviewed_updated_if_present(self):
        """If times_reviewed already exists, it should be updated in-place."""
        source = '''last_solved     = "2026-05-01"
revisit_in_days = 7
times_reviewed  = 3
difficulty      = "easy"
topic_tags      = ["arrays"]
'''
        updated, _ = update_metadata(source, "2026-06-01", "g",
                                     new_times_reviewed=4)
        assert "times_reviewed  = 4" in updated
        assert "times_reviewed  = 3" not in updated

    def test_times_reviewed_not_touched_if_none(self):
        """If new_times_reviewed is None, existing field should be untouched."""
        source = '''last_solved     = "2026-05-01"
revisit_in_days = 7
times_reviewed  = 5
difficulty      = "easy"
topic_tags      = ["arrays"]
'''
        updated, _ = update_metadata(source, "2026-06-01", "g")
        assert "times_reviewed  = 5" in updated


class TestComputeSpreadIntervalEscalation:
    """Test auto-escalation in compute_spread_interval when all nearby days are overloaded."""

    def _make_due_dates(self, target_date, count):
        """Return a list of `count` copies of target_date to simulate an overloaded day."""
        return [target_date] * count

    def test_no_escalation_when_free_day_exists(self):
        """If a free day is available in the spread window, no escalation happens."""
        from datetime import date, timedelta
        today = date(2026, 6, 1)
        # No competing due dates — plenty of room
        days, effective = compute_spread_interval(1, "s", today, [], times_reviewed=0)
        assert effective == "s"
        assert days >= 1

    def test_escalation_chain_is_correct(self):
        """RATING_ESCALATION must follow s→h→g→e→t→None."""
        assert RATING_ESCALATION["s"] == "h"
        assert RATING_ESCALATION["h"] == "g"
        assert RATING_ESCALATION["g"] == "e"
        assert RATING_ESCALATION["e"] == "t"
        assert RATING_ESCALATION["t"] is None

    def test_smooth_overload_cap_constant(self):
        """SMOOTH_OVERLOAD_CAP must equal DAILY_LOAD_CAP from config."""
        from config import DAILY_LOAD_CAP
        assert SMOOTH_OVERLOAD_CAP == DAILY_LOAD_CAP

    def test_escalation_triggered_when_all_days_overloaded(self):
        """When every day in the 'g' window is loaded >= SMOOTH_OVERLOAD_CAP, escalate to 'e'."""
        from datetime import date, timedelta
        today = date(2026, 6, 1)
        # 'g' base=7d, spread (-2,+7) → days 5–14
        # Note: 's' is explicitly exempt from escalation — use 'g' to test this behaviour
        overloaded_dates = []
        for delta in range(5, 15):
            overloaded_dates.extend([today + timedelta(days=delta)] * SMOOTH_OVERLOAD_CAP)
        days, effective = compute_spread_interval(7, "g", today, overloaded_dates, times_reviewed=0)
        assert effective != "g", "expected escalation away from 'g'"
        assert days > 7, "escalated interval should be larger than the base 7 days"

    def test_escalation_stops_at_trivial(self):
        """Escalation never goes beyond 't' (top of chain)."""
        from datetime import date, timedelta
        today = date(2026, 6, 1)
        # Flood every day 1–99 to force escalation through g→e→t
        overloaded_dates = []
        for delta in range(1, 100):
            overloaded_dates.extend([today + timedelta(days=delta)] * SMOOTH_OVERLOAD_CAP)
        days, effective = compute_spread_interval(7, "g", today, overloaded_dates, times_reviewed=0)
        assert effective == "t"
        assert days >= 1

    def test_returned_days_use_escalated_tier_base(self):
        """Days returned after escalation are computed from the escalated tier's base, not original."""
        from datetime import date, timedelta
        today = date(2026, 6, 1)
        # Flood 'g' window (days 5–14) to force escalation to 'e'
        overloaded_dates = []
        for delta in range(5, 15):
            overloaded_dates.extend([today + timedelta(days=delta)] * SMOOTH_OVERLOAD_CAP)
        days, effective = compute_spread_interval(7, "g", today, overloaded_dates, times_reviewed=0)
        # e base is 30 days; spread window (-15,+15) → should land in 15–45 day range
        assert effective == "e"
        assert 15 <= days <= 45

