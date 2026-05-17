"""Tests for database layer."""

import pytest
from pathlib import Path

from bctx.core.database import Database, get_db, reset_db


def test_database_creation_in_memory():
    """Test creating an in-memory database."""
    db = Database(Path(":memory:"))
    conn = db.connect()

    # Check that context_files table exists
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name = 'context_files'"
    )
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == "context_files"

    db.close()


def test_database_migration(memory_db):
    """Test that all tables are created during migration."""
    conn = memory_db.connect()
    cursor = conn.cursor()

    # Check for all expected tables
    expected_tables = ["context_files", "memory_entries", "observations", "reflections"]

    for table_name in expected_tables:
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name = '{table_name}'"
        )
        result = cursor.fetchone()
        assert result is not None, f"Table {table_name} not found"


def test_database_context_manager(temp_dir):
    """Test database context manager."""
    db_path = temp_dir / "test.db"

    with Database(db_path) as db:
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result[0] == 1

    # Verify file was created
    assert db_path.exists()


def test_singleton_database():
    """Test singleton database instance."""
    reset_db()

    db1 = get_db(Path(":memory:"))
    db2 = get_db()

    assert db1 is db2

    reset_db()
