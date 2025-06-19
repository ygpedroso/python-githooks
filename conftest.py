import pathlib
import shutil
import pytest

# Use pytest's tmp_path fixture for cleaner test isolation and automatic cleanup
# These module-level constants are no longer the primary way to define test paths.

@pytest.fixture
def workspace_base_path(tmp_path: pathlib.Path) -> pathlib.Path:
    """Provides a base temporary directory for tests."""
    return tmp_path

@pytest.fixture
def workspace_without_git_path(workspace_base_path: pathlib.Path) -> pathlib.Path:
    """Creates a workspace directory without a .git/hooks subdirectory."""
    # workspace_base_path itself can serve as the workspace without git
    # No specific subdirectories needed for this fixture, tmp_path is sufficient
    return workspace_base_path

@pytest.fixture
def workspace_with_git_path(workspace_base_path: pathlib.Path) -> pathlib.Path:
    """Creates a workspace directory with a .git/hooks subdirectory."""
    githooks_dir = workspace_base_path / ".git" / "hooks"
    githooks_dir.mkdir(parents=True, exist_ok=True)
    return workspace_base_path
