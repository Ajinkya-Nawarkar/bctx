"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path
import pytest

from bctx.core.database import Database, reset_db


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def memory_db():
    """Create an in-memory SQLite database for testing."""
    # Reset singleton before each test
    reset_db()

    # Create in-memory database
    db = Database(Path(":memory:"))
    db.connect()

    yield db

    # Cleanup
    db.close()
    reset_db()


@pytest.fixture
def test_db_path(temp_dir):
    """Create a test database file path."""
    db_path = temp_dir / "test.db"
    yield db_path

    # Cleanup
    reset_db()
