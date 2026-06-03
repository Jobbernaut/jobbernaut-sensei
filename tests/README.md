# Jobbernaut Sensei Test Suite

Comprehensive test suite for the Jobbernaut Sensei CLI application.

## Overview

The test suite validates all functionality across multiple platforms and Python versions:

- **Platforms:** Linux, macOS, Windows
- **Python Versions:** 3.10, 3.11, 3.12, 3.13
- **Total Test Configurations:** 12 (3 OS × 4 Python versions)

## Test Structure

```
tests/
├── __init__.py           # Package marker
├── conftest.py           # Shared pytest fixtures
├── test_utils.py         # Unit tests for utils.py
├── test_commands.py      # Integration tests for all CLI commands
└── README.md             # This file
```

## Running Tests Locally

### Install Test Dependencies

```bash
pip install -e ".[test]"
```

Or manually:
```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
pytest tests/
```

### Run With Coverage

```bash
pytest tests/ --cov=src --cov-report=term --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_utils.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_commands.py::TestSenseiInit -v
```

### Run Specific Test

```bash
pytest tests/test_commands.py::TestSenseiInit::test_init_creates_directory -v
```

## Test Categories

### Unit Tests (`test_utils.py`)
Tests for utility functions:
- Metadata parsing
- File finding
- String normalization
- Fuzzy matching
- URL extraction

**Test Count:** ~25 tests

### Command Tests (`test_commands.py`)
Integration tests for all CLI commands:
- `sensei init` - Directory initialization
- `sensei new` - Problem scaffolding
- `sensei mark` - Marking problems as solved
- `sensei hint` - Getting problem hints
- `sensei show` - Showing problem details
- `sensei open` - Opening in browser
- `sensei status` - Getting status summary
- `sensei revisit` - Reviewing due problems

**Test Count:** ~30 tests

### SRS Algorithm Tests
Tests for spaced repetition logic:
- Bootstrap phase intervals (3 days → 7 days)
- Rating-based intervals (easy/good/hard/struggled)
- Exponential growth for mastered problems
- Metadata update logic

**Test Count:** ~15 tests

## Fixtures

### `temp_workspace`
Creates a temporary directory and changes to it.

### `initialized_workspace`
Creates a workspace with `problems/` directory.

### `sample_problem_file`
Creates a single sample problem for testing.

### `multiple_problems`
Creates multiple problems with different due dates (overdue, due today, future).

### `non_numbered_problem`
Creates a problem without a number prefix (for edge case testing).

## CI/CD Integration

Tests run automatically on:
- **Push to main branch**
- **Pull requests**
- **Manual workflow dispatch**

See `.github/workflows/test.yml` for CI configuration.

### GitHub Actions Matrix

```yaml
matrix:
  os: [ubuntu-latest, macos-latest, windows-latest]
  python-version: ["3.10", "3.11", "3.12", "3.13"]
```

## Coverage

Coverage reports are generated and uploaded to Codecov for the primary configuration (Ubuntu + Python 3.12).

Target coverage: **>85%**

## Writing New Tests

### Example: Testing a New Command

```python
def test_new_command(initialized_workspace):
    """Test new command functionality."""
    result = subprocess.run(
        [sys.executable, "-m", "sensei", "new", "arg1", "arg2"],
        capture_output=True,
        text=True,
        cwd=str(initialized_workspace)
    )
    
    assert result.returncode == 0
    assert "expected output" in result.stdout
```

### Example: Testing Utility Function

```python
def test_utility_function():
    """Test a utility function."""
    from utils import my_function
    result = my_function("input")
    assert result == "expected"
```

## Known Test Limitations

1. **Browser opening tests** - Cannot fully test actual browser launching, only command construction
2. **Interactive prompts** - Tests use `--rating` flag to bypass interactive input
3. **Time-dependent tests** - Some tests depend on current date (handled with fixtures)

## Troubleshooting

### Tests fail with "ModuleNotFoundError"
- Ensure you've installed the package: `pip install -e .`
- Or add src to PYTHONPATH: `export PYTHONPATH=src:$PYTHONPATH`

### Tests fail on Windows
- Check that paths use `Path` objects for cross-platform compatibility
- Verify subprocess commands work on Windows

### Coverage too low
- Check that all new code has corresponding tests
- Use `pytest --cov-report=html` to see which lines are untested

## Contributing

When adding new features:
1. Write tests first (TDD approach recommended)
2. Ensure tests pass on your platform
3. Add fixtures if needed for common setup
4. Document any platform-specific behavior
5. Aim for >85% code coverage

## Questions?

See the main [README.md](../README.md) or open an issue on GitHub.
