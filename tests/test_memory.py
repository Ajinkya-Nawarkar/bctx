"""Tests for memory system."""

import pytest
from datetime import datetime, timedelta
from pathlib import Path

from bctx.memory import (
    MemoryEntry,
    MemoryIndex,
    create_memory_entry,
    create_memory_index,
    ShortTermMemory,
    LongTermMemory,
    EpisodicMemory,
)


# Schema Tests


def test_create_memory_entry():
    """Test creating a memory entry."""
    entry = create_memory_entry(
        id="test-001",
        title="Test Entry",
        tags=["test", "example"],
        content="# Test\nThis is a test entry.",
        related_entries=["test-002"],
    )

    assert entry.id == "test-001"
    assert entry.title == "Test Entry"
    assert entry.tags == ["test", "example"]
    assert entry.content == "# Test\nThis is a test entry."
    assert entry.related_entries == ["test-002"]
    assert entry.created is not None
    assert entry.last_modified is not None


def test_memory_entry_to_dict():
    """Test converting memory entry to dictionary."""
    entry = create_memory_entry(
        id="test-001", title="Test", tags=["test"], content="Test content"
    )

    data = entry.to_dict()

    assert data["id"] == "test-001"
    assert data["title"] == "Test"
    assert data["tags"] == ["test"]
    assert data["content"] == "Test content"


def test_memory_entry_from_dict():
    """Test creating memory entry from dictionary."""
    data = {
        "id": "test-001",
        "title": "Test Entry",
        "tags": ["test"],
        "content": "Test content",
        "created": "2024-01-01T00:00:00",
        "last_modified": "2024-01-01T00:00:00",
        "related_entries": [],
        "metadata": {},
    }

    entry = MemoryEntry.from_dict(data)

    assert entry.id == "test-001"
    assert entry.title == "Test Entry"
    assert entry.tags == ["test"]


def test_memory_entry_file_io(temp_dir):
    """Test saving and loading memory entry from file."""
    entry = create_memory_entry(
        id="test-001", title="Test", tags=["test"], content="Test content"
    )

    # Save to file
    file_path = temp_dir / "test-entry.yaml"
    entry.to_file(file_path)

    assert file_path.exists()

    # Load from file
    loaded = MemoryEntry.from_file(file_path)

    assert loaded.id == entry.id
    assert loaded.title == entry.title
    assert loaded.tags == entry.tags
    assert loaded.content == entry.content


def test_memory_entry_summary():
    """Test generating entry summary."""
    entry = create_memory_entry(
        id="test-001",
        title="Test Entry",
        tags=["test"],
        content="# Header\n\nThis is the first line of content.",
    )

    summary = entry.summary()

    assert summary["file"] == "entries/test-001.yaml"
    assert summary["title"] == "Test Entry"
    assert summary["tags"] == ["test"]
    assert "summary" in summary
    assert summary["created"] == entry.created


def test_create_memory_index():
    """Test creating a memory index."""
    index = create_memory_index(
        name="test-store", description="Test memory store", tags=["test"]
    )

    assert index.name == "test-store"
    assert index.description == "Test memory store"
    assert index.tags == ["test"]
    assert index.entries == {}
    assert index.created is not None


def test_memory_index_add_entry():
    """Test adding entry to index."""
    index = create_memory_index(name="test", description="Test")
    entry = create_memory_entry(
        id="test-001", title="Test", tags=["test"], content="Test"
    )

    index.add_entry(entry)

    assert "test-001" in index.entries
    assert index.entries["test-001"]["title"] == "Test"


def test_memory_index_remove_entry():
    """Test removing entry from index."""
    index = create_memory_index(name="test", description="Test")
    entry = create_memory_entry(
        id="test-001", title="Test", tags=["test"], content="Test"
    )

    index.add_entry(entry)
    assert "test-001" in index.entries

    index.remove_entry("test-001")
    assert "test-001" not in index.entries


# Short-Term Memory Tests


def test_stm_add_and_get():
    """Test adding and getting entries from STM."""
    stm = ShortTermMemory(max_size=10, ttl_seconds=60)

    entry = create_memory_entry(
        id="test-001", title="Test", tags=["test"], content="Test content"
    )

    stm.add_entry(entry)

    retrieved = stm.get_entry("test-001")
    assert retrieved is not None
    assert retrieved.id == "test-001"
    assert retrieved.title == "Test"


def test_stm_expiration():
    """Test STM entry expiration."""
    stm = ShortTermMemory(max_size=10, ttl_seconds=1)  # 1 second TTL

    entry = create_memory_entry(
        id="test-001", title="Test", tags=["test"], content="Test"
    )

    stm.add_entry(entry)

    # Should be available immediately
    assert stm.get_entry("test-001") is not None

    # Manually expire by setting old access time
    stm._access_times["test-001"] = datetime.now() - timedelta(seconds=2)

    # Should be expired now
    assert stm.get_entry("test-001") is None


def test_stm_max_size():
    """Test STM max size enforcement."""
    stm = ShortTermMemory(max_size=3, ttl_seconds=60)

    # Add 4 entries (exceeds max size)
    for i in range(4):
        entry = create_memory_entry(
            id=f"test-{i:03d}", title=f"Test {i}", tags=["test"], content=f"Test {i}"
        )
        stm.add_entry(entry)

    # Should only have 3 entries (oldest pruned)
    entries = stm.list_entries()
    assert len(entries) == 3


def test_stm_search():
    """Test searching STM."""
    stm = ShortTermMemory()

    # Add entries
    stm.add_entry(
        create_memory_entry(
            id="test-001", title="Python Tutorial", tags=["python"], content="Learn Python"
        )
    )
    stm.add_entry(
        create_memory_entry(
            id="test-002", title="JavaScript Guide", tags=["js"], content="Learn JS"
        )
    )
    stm.add_entry(
        create_memory_entry(
            id="test-003",
            title="Python Advanced",
            tags=["python"],
            content="Advanced Python",
        )
    )

    # Search for "python"
    results = stm.search("python", k=5)

    assert len(results) == 2
    assert all("python" in r.title.lower() or "python" in " ".join(r.tags) for r in results)


def test_stm_clear():
    """Test clearing STM."""
    stm = ShortTermMemory()

    stm.add_entry(create_memory_entry(id="test-001", title="Test", tags=[], content="Test"))

    assert len(stm.list_entries()) == 1

    stm.clear()

    assert len(stm.list_entries()) == 0


# Long-Term Memory Tests


def test_ltm_add_and_get(temp_dir):
    """Test adding and getting entries from LTM."""
    ltm = LongTermMemory(store_path=temp_dir)

    entry = create_memory_entry(
        id="test-001", title="Test Entry", tags=["test"], content="Test content"
    )

    ltm.add_entry(entry)

    # Check entry file exists
    entry_file = temp_dir / "entries" / "test-001.yaml"
    assert entry_file.exists()

    # Check index updated
    assert "test-001" in ltm.index.entries

    # Retrieve entry
    retrieved = ltm.get_entry("test-001")
    assert retrieved is not None
    assert retrieved.id == "test-001"
    assert retrieved.title == "Test Entry"


def test_ltm_search(temp_dir):
    """Test searching LTM."""
    ltm = LongTermMemory(store_path=temp_dir)

    # Add entries
    ltm.add_entry(
        create_memory_entry(
            id="test-001", title="Python Anti-Pattern", tags=["python"], content="Bad code"
        )
    )
    ltm.add_entry(
        create_memory_entry(
            id="test-002", title="JavaScript Pattern", tags=["js"], content="Good code"
        )
    )
    ltm.add_entry(
        create_memory_entry(
            id="test-003", title="Python Best Practice", tags=["python"], content="Good code"
        )
    )

    # Search for "python"
    results = ltm.search("python", k=5)

    assert len(results) == 2
    assert all("python" in r.title.lower() for r in results)


def test_ltm_list_entries(temp_dir):
    """Test listing all LTM entries."""
    ltm = LongTermMemory(store_path=temp_dir)

    # Add entries
    for i in range(3):
        ltm.add_entry(
            create_memory_entry(
                id=f"test-{i:03d}", title=f"Entry {i}", tags=["test"], content=f"Content {i}"
            )
        )

    entries = ltm.list_entries()

    assert len(entries) == 3


def test_ltm_delete_entry(temp_dir):
    """Test deleting entry from LTM."""
    ltm = LongTermMemory(store_path=temp_dir)

    entry = create_memory_entry(
        id="test-001", title="Test", tags=["test"], content="Test"
    )

    ltm.add_entry(entry)

    # Verify exists
    assert ltm.get_entry("test-001") is not None
    assert "test-001" in ltm.index.entries

    # Delete
    ltm.delete_entry("test-001")

    # Verify deleted
    assert ltm.get_entry("test-001") is None
    assert "test-001" not in ltm.index.entries


def test_ltm_update_entry(temp_dir):
    """Test updating entry in LTM."""
    ltm = LongTermMemory(store_path=temp_dir)

    entry = create_memory_entry(
        id="test-001", title="Original Title", tags=["test"], content="Original content"
    )

    ltm.add_entry(entry)

    # Update
    ltm.update_entry("test-001", {"title": "Updated Title", "content": "Updated content"})

    # Verify update
    updated = ltm.get_entry("test-001")
    assert updated.title == "Updated Title"
    assert updated.content == "Updated content"


# Episodic Memory Tests


def test_episodic_add_and_get(temp_dir):
    """Test adding and getting entries from episodic memory."""
    log_path = temp_dir / "episodes.jsonl"
    episodic = EpisodicMemory(log_path=log_path)

    entry = create_memory_entry(
        id="test-001", title="Test Episode", tags=["test"], content="Test content"
    )

    episodic.add_entry(entry)

    # Check log file exists
    assert log_path.exists()

    # Retrieve entry
    retrieved = episodic.get_entry("test-001")
    assert retrieved is not None
    assert retrieved.id == "test-001"


def test_episodic_search(temp_dir):
    """Test searching episodic memory."""
    log_path = temp_dir / "episodes.jsonl"
    episodic = EpisodicMemory(log_path=log_path)

    # Add entries
    episodic.add_entry(
        create_memory_entry(
            id="test-001", title="Error: File not found", tags=["error"], content="Error details"
        )
    )
    episodic.add_entry(
        create_memory_entry(
            id="test-002", title="Success: File created", tags=["success"], content="Success"
        )
    )
    episodic.add_entry(
        create_memory_entry(
            id="test-003", title="Error: Permission denied", tags=["error"], content="Error"
        )
    )

    # Search for "error"
    results = episodic.search("error", k=5)

    assert len(results) == 2
    assert all("error" in r.title.lower() or "error" in " ".join(r.tags) for r in results)


def test_episodic_list_entries(temp_dir):
    """Test listing episodic memory entries."""
    log_path = temp_dir / "episodes.jsonl"
    episodic = EpisodicMemory(log_path=log_path)

    # Add entries
    for i in range(3):
        episodic.add_entry(
            create_memory_entry(
                id=f"test-{i:03d}", title=f"Episode {i}", tags=["test"], content=f"Content {i}"
            )
        )

    entries = episodic.list_entries()

    assert len(entries) == 3
