from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def get_project_root() -> Path:
    """Find and cache the project root directory."""
    current_path = Path(__file__).resolve()

    # Look for project markers
    markers = [".git", "pyproject.toml", "setup.py", "requirements.txt"]

    for parent in [current_path, *list(current_path.parents)]:
        if any((parent / marker).exists() for marker in markers):
            return parent

    # Fallback
    return current_path.parent


DB_PATH = get_project_root() / "quantiq.db"
