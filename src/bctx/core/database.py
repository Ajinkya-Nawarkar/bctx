"""Database layer for bctx - SQLite connection and migrations."""

import sqlite3
from pathlib import Path
from typing import Optional
import threading

from .paths import db_path, ensure_dirs


# Thread-local storage for singleton connection
_thread_local = threading.local()


class Database:
    """SQLite database wrapper with connection pooling and migrations."""

    def __init__(self, path: Optional[Path] = None):
        """Initialize database connection.

        Args:
            path: Path to database file. If None, uses default path.
        """
        self.path = path or db_path()
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        """Get or create database connection.

        Returns:
            SQLite connection with WAL mode and busy timeout configured.
        """
        if self._conn is None:
            # Ensure parent directory exists
            ensure_dirs()

            # Create connection
            self._conn = sqlite3.connect(
                str(self.path),
                check_same_thread=False,
                timeout=5.0
            )

            # Configure connection
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA busy_timeout=5000")
            self._conn.row_factory = sqlite3.Row

            # Run migrations
            self._migrate()

        return self._conn

    def _migrate(self) -> None:
        """Run database migrations."""
        conn = self._conn
        if conn is None:
            raise RuntimeError("Cannot migrate without connection")

        # Migration statements
        migrations = [
            # Original context_files table
            """
            CREATE TABLE IF NOT EXISTS context_files (
                name TEXT PRIMARY KEY,
                path TEXT NOT NULL,
                scope TEXT DEFAULT 'global',
                enabled BOOLEAN DEFAULT 1,
                category TEXT DEFAULT 'rules',
                type TEXT DEFAULT 'rules',
                description TEXT DEFAULT ''
            )
            """,

            # Memory entries (Phase 2)
            """
            CREATE TABLE IF NOT EXISTS memory_entries (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT,
                relevance_score REAL
            )
            """,

            # Observations (Phase 3)
            """
            CREATE TABLE IF NOT EXISTS observations (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                session_id TEXT,
                action_type TEXT,
                tool_name TEXT,
                success BOOLEAN,
                error TEXT,
                context TEXT
            )
            """,

            # Reflections (Phase 5)
            """
            CREATE TABLE IF NOT EXISTS reflections (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                trigger TEXT,
                insights TEXT,
                learnings TEXT
            )
            """,
        ]

        # Execute migrations
        cursor = conn.cursor()
        for migration in migrations:
            cursor.execute(migration)

        conn.commit()

    def close(self) -> None:
        """Close database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Singleton instance
_db_instance: Optional[Database] = None
_db_lock = threading.Lock()


def get_db(path: Optional[Path] = None) -> Database:
    """Get singleton database instance.

    Args:
        path: Optional custom database path (mainly for testing).

    Returns:
        Database instance.
    """
    global _db_instance

    with _db_lock:
        if _db_instance is None or (path and path != _db_instance.path):
            _db_instance = Database(path)
            _db_instance.connect()

        return _db_instance


def reset_db() -> None:
    """Reset singleton database instance (for testing)."""
    global _db_instance

    with _db_lock:
        if _db_instance:
            _db_instance.close()
            _db_instance = None


def execute_query(query: str, params: tuple = (), path: Optional[Path] = None):
    """Execute a query and return results.

    Args:
        query: SQL query string.
        params: Query parameters.
        path: Optional database path.

    Returns:
        Query results as list of Row objects.
    """
    db = get_db(path)
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()


def execute_update(query: str, params: tuple = (), path: Optional[Path] = None) -> int:
    """Execute an update/insert/delete query.

    Args:
        query: SQL query string.
        params: Query parameters.
        path: Optional database path.

    Returns:
        Number of affected rows.
    """
    db = get_db(path)
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    return cursor.rowcount
