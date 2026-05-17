"""Tests for context management."""

import pytest
from pathlib import Path

from bctx.context.manager import (
    add,
    remove,
    list_all,
    toggle,
    active_rules,
    read_content,
    get_by_name,
    ContextFile,
)


def test_add_and_list(memory_db):
    """Test adding and listing context files."""
    db_path = memory_db.path

    # Add two context files
    add(
        name="go-standards",
        path="/home/user/docs/go-standards.md",
        scope="global",
        category="rules",
        typ="rules",
        description="Go coding standards",
        db_path=db_path,
    )

    add(
        name="bay-conv",
        path="/home/user/docs/DESIGN.md",
        scope="repo:bay",
        category="docs",
        typ="rules",
        description="Bay design doc",
        db_path=db_path,
    )

    # List all files
    files = list_all(db_path)

    assert len(files) == 2
    assert files[0].name == "bay-conv"  # Alphabetical order
    assert files[1].name == "go-standards"


def test_remove(memory_db):
    """Test removing a context file."""
    db_path = memory_db.path

    # Add a file
    add(name="test-rule", path="/tmp/test.md", db_path=db_path)

    # Verify it exists
    files = list_all(db_path)
    assert len(files) == 1

    # Remove it
    remove("test-rule", db_path)

    # Verify it's gone
    files = list_all(db_path)
    assert len(files) == 0


def test_toggle(memory_db):
    """Test toggling enabled state."""
    db_path = memory_db.path

    # Add a file
    add(name="test-rule", path="/tmp/test.md", db_path=db_path)

    # Initially enabled
    files = list_all(db_path)
    assert files[0].enabled is True

    # Toggle to disabled
    toggle("test-rule", db_path)
    files = list_all(db_path)
    assert files[0].enabled is False

    # Toggle back to enabled
    toggle("test-rule", db_path)
    files = list_all(db_path)
    assert files[0].enabled is True


def test_active_rules(memory_db):
    """Test fetching active rules for a repository."""
    db_path = memory_db.path

    # Add various rules
    add(name="global-rule", path="/tmp/global.md", scope="global", db_path=db_path)
    add(name="bay-rule", path="/tmp/bay.md", scope="repo:bay", db_path=db_path)
    add(
        name="other-rule",
        path="/tmp/other.md",
        scope="repo:other-project",
        db_path=db_path,
    )
    add(name="disabled-global", path="/tmp/disabled.md", scope="global", db_path=db_path)
    toggle("disabled-global", db_path)  # Disable it

    # Get active rules for 'bay'
    active = active_rules("bay", db_path)

    # Should get global-rule and bay-rule, but not other-rule or disabled-global
    assert len(active) == 2

    names = {f.name for f in active}
    assert "global-rule" in names
    assert "bay-rule" in names
    assert "other-rule" not in names
    assert "disabled-global" not in names


def test_read_content(temp_dir):
    """Test reading content from a context file."""
    # Create a test file
    test_file = temp_dir / "test.md"
    content = "# Test Rule\nThis is a test rule."
    test_file.write_text(content, encoding="utf-8")

    # Create ContextFile object
    ctx_file = ContextFile(name="test", path=str(test_file))

    # Read content
    read_result = read_content(ctx_file)

    assert read_result == content


def test_read_content_missing_file():
    """Test reading content from a non-existent file."""
    ctx_file = ContextFile(name="test", path="/nonexistent/file.md")

    with pytest.raises(FileNotFoundError):
        read_content(ctx_file)


def test_upsert(memory_db):
    """Test upserting a context file (update on conflict)."""
    db_path = memory_db.path

    # Add initial version
    add(
        name="test",
        path="/path/v1.md",
        scope="global",
        category="rules",
        typ="rules",
        description="v1 desc",
        db_path=db_path,
    )

    # Add again with different values (should update)
    add(
        name="test",
        path="/path/v2.md",
        scope="repo:bay",
        category="docs",
        typ="skills",
        description="v2 desc",
        db_path=db_path,
    )

    # Should have only one entry with updated values
    files = list_all(db_path)
    assert len(files) == 1
    assert files[0].path == "/path/v2.md"
    assert files[0].type == "skills"
    assert files[0].description == "v2 desc"


def test_get_by_name(memory_db):
    """Test fetching a context file by name."""
    db_path = memory_db.path

    # Add a file
    add(name="test-rule", path="/tmp/test.md", description="Test", db_path=db_path)

    # Get by name
    ctx_file = get_by_name("test-rule", db_path)

    assert ctx_file is not None
    assert ctx_file.name == "test-rule"
    assert ctx_file.path == "/tmp/test.md"
    assert ctx_file.description == "Test"


def test_get_by_name_not_found(memory_db):
    """Test fetching a non-existent context file."""
    db_path = memory_db.path

    ctx_file = get_by_name("nonexistent", db_path)

    assert ctx_file is None
