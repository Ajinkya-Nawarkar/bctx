"""Context file management - CRUD operations."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import sqlite3

from ..core.database import get_db, execute_query, execute_update


@dataclass
class ContextFile:
    """Represents a registered context file entry."""
    name: str
    path: str
    scope: str = "global"  # "global" or "repo:{name}"
    enabled: bool = True
    category: str = "rules"  # "rules", "docs", "standards", etc.
    type: str = "rules"  # "rules", "skills", "agents", "plugins"
    description: str = ""

    @classmethod
    def from_row(cls, row: sqlite3.Row) -> "ContextFile":
        """Create ContextFile from database row.

        Args:
            row: SQLite row object.

        Returns:
            ContextFile instance.
        """
        return cls(
            name=row["name"],
            path=row["path"],
            scope=row["scope"] or "global",
            enabled=bool(row["enabled"]),
            category=row["category"] or "rules",
            type=row["type"] or "rules",
            description=row["description"] or ""
        )


def add(
    name: str,
    path: str,
    scope: str = "global",
    category: str = "rules",
    typ: str = "rules",
    description: str = "",
    db_path: Optional[Path] = None
) -> None:
    """Register a context file.

    Args:
        name: Unique name for the context file.
        path: File path.
        scope: Scope ("global" or "repo:{name}").
        category: Category (e.g., "rules", "docs").
        typ: Type (e.g., "rules", "skills", "agents", "plugins").
        description: Description of the context file.
        db_path: Optional database path (mainly for testing).

    Raises:
        sqlite3.Error: If database operation fails.
    """
    # Set defaults
    scope = scope or "global"
    category = category or "rules"
    typ = typ or "rules"

    # Upsert into database
    query = """
        INSERT INTO context_files (name, path, scope, enabled, category, type, description)
        VALUES (?, ?, ?, 1, ?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
            path = excluded.path,
            scope = excluded.scope,
            category = excluded.category,
            type = excluded.type,
            description = excluded.description
    """

    execute_update(query, (name, path, scope, category, typ, description), db_path)


def remove(name: str, db_path: Optional[Path] = None) -> None:
    """Remove a context file by name.

    Args:
        name: Name of the context file to remove.
        db_path: Optional database path (mainly for testing).

    Raises:
        sqlite3.Error: If database operation fails.
    """
    query = "DELETE FROM context_files WHERE name = ?"
    execute_update(query, (name,), db_path)


def list_all(db_path: Optional[Path] = None) -> List[ContextFile]:
    """List all registered context files.

    Args:
        db_path: Optional database path (mainly for testing).

    Returns:
        List of ContextFile objects.

    Raises:
        sqlite3.Error: If database operation fails.
    """
    query = """
        SELECT name, path, scope, enabled, category,
               COALESCE(type, 'rules') as type,
               COALESCE(description, '') as description
        FROM context_files
        ORDER BY name
    """

    rows = execute_query(query, (), db_path)
    return [ContextFile.from_row(row) for row in rows]


def toggle(name: str, db_path: Optional[Path] = None) -> None:
    """Toggle the enabled flag for a context file.

    Args:
        name: Name of the context file to toggle.
        db_path: Optional database path (mainly for testing).

    Raises:
        sqlite3.Error: If database operation fails.
    """
    query = "UPDATE context_files SET enabled = NOT enabled WHERE name = ?"
    execute_update(query, (name,), db_path)


def active_rules(repo_name: str = "", db_path: Optional[Path] = None) -> List[ContextFile]:
    """Get enabled context files matching global + repo scope.

    Args:
        repo_name: Name of the repository (for repo-scoped rules).
        db_path: Optional database path (mainly for testing).

    Returns:
        List of enabled ContextFile objects.

    Raises:
        sqlite3.Error: If database operation fails.
    """
    repo_scope = f"repo:{repo_name}" if repo_name else ""

    query = """
        SELECT name, path, scope, enabled, category,
               COALESCE(type, 'rules') as type,
               COALESCE(description, '') as description
        FROM context_files
        WHERE enabled = 1 AND (scope = 'global' OR scope = ?)
        ORDER BY name
    """

    rows = execute_query(query, (repo_scope,), db_path)
    return [ContextFile.from_row(row) for row in rows]


def read_content(context_file: ContextFile) -> str:
    """Read the markdown content from a context file's path.

    Args:
        context_file: ContextFile to read.

    Returns:
        File contents as string.

    Raises:
        FileNotFoundError: If file doesn't exist.
        IOError: If file can't be read.
    """
    path = Path(context_file.path)

    if not path.exists():
        raise FileNotFoundError(f"Context file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_by_name(name: str, db_path: Optional[Path] = None) -> Optional[ContextFile]:
    """Get a context file by name.

    Args:
        name: Name of the context file.
        db_path: Optional database path (mainly for testing).

    Returns:
        ContextFile if found, None otherwise.

    Raises:
        sqlite3.Error: If database operation fails.
    """
    query = """
        SELECT name, path, scope, enabled, category,
               COALESCE(type, 'rules') as type,
               COALESCE(description, '') as description
        FROM context_files
        WHERE name = ?
    """

    rows = execute_query(query, (name,), db_path)
    if rows:
        return ContextFile.from_row(rows[0])
    return None
