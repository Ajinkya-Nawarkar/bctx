"""Memory store implementations - STM, LTM, Episodic."""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any
import json

from .schema import MemoryEntry, MemoryIndex, create_memory_index
from ..core.paths import memory_dir, observations_dir


class MemoryStore(ABC):
    """Base class for memory stores."""

    @abstractmethod
    def add_entry(self, entry: MemoryEntry) -> str:
        """Add a memory entry.

        Args:
            entry: Memory entry to add.

        Returns:
            Entry ID.
        """
        pass

    @abstractmethod
    def get_entry(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get a memory entry by ID.

        Args:
            entry_id: Entry ID.

        Returns:
            MemoryEntry if found, None otherwise.
        """
        pass

    @abstractmethod
    def search(self, query: str, k: int = 5) -> List[MemoryEntry]:
        """Search for memory entries.

        Args:
            query: Search query.
            k: Number of results to return.

        Returns:
            List of matching MemoryEntry objects.
        """
        pass

    @abstractmethod
    def list_entries(self) -> List[MemoryEntry]:
        """List all entries in the store.

        Returns:
            List of all MemoryEntry objects.
        """
        pass

    def update_entry(self, entry_id: str, updates: Dict[str, Any]) -> None:
        """Update a memory entry.

        Args:
            entry_id: Entry ID.
            updates: Dictionary of fields to update.

        Raises:
            ValueError: If entry not found.
        """
        entry = self.get_entry(entry_id)
        if not entry:
            raise ValueError(f"Entry {entry_id} not found")

        # Apply updates
        for key, value in updates.items():
            if hasattr(entry, key):
                setattr(entry, key, value)

        # Update timestamp
        entry.last_modified = datetime.now().isoformat()

        # Re-add to store
        self.add_entry(entry)

    def delete_entry(self, entry_id: str) -> None:
        """Delete a memory entry.

        Args:
            entry_id: Entry ID.
        """
        raise NotImplementedError("Delete not implemented for this store")


class ShortTermMemory(MemoryStore):
    """Session-scoped in-memory store.

    Stores temporary information for the current session. Data is lost
    when the session ends.
    """

    def __init__(self, max_size: int = 1000, ttl_seconds: int = 3600):
        """Initialize short-term memory.

        Args:
            max_size: Maximum number of entries to store.
            ttl_seconds: Time-to-live for entries in seconds.
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self._entries: Dict[str, MemoryEntry] = {}
        self._access_times: Dict[str, datetime] = {}

    def add_entry(self, entry: MemoryEntry) -> str:
        """Add entry to short-term memory.

        Args:
            entry: Memory entry to add.

        Returns:
            Entry ID.
        """
        # Prune old entries if at max size
        if len(self._entries) >= self.max_size:
            self._prune_oldest()

        # Add entry
        self._entries[entry.id] = entry
        self._access_times[entry.id] = datetime.now()

        return entry.id

    def get_entry(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get entry from short-term memory.

        Args:
            entry_id: Entry ID.

        Returns:
            MemoryEntry if found and not expired, None otherwise.
        """
        if entry_id not in self._entries:
            return None

        # Check if expired
        if self._is_expired(entry_id):
            del self._entries[entry_id]
            del self._access_times[entry_id]
            return None

        # Update access time
        self._access_times[entry_id] = datetime.now()

        return self._entries[entry_id]

    def search(self, query: str, k: int = 5) -> List[MemoryEntry]:
        """Search short-term memory.

        Args:
            query: Search query.
            k: Number of results to return.

        Returns:
            List of matching entries.
        """
        query_lower = query.lower()
        matches = []

        for entry_id, entry in self._entries.items():
            # Skip expired entries
            if self._is_expired(entry_id):
                continue

            # Simple keyword matching
            if (
                query_lower in entry.title.lower()
                or query_lower in entry.content.lower()
                or any(query_lower in tag.lower() for tag in entry.tags)
            ):
                matches.append(entry)

        # Sort by recency (access time)
        matches.sort(
            key=lambda e: self._access_times.get(e.id, datetime.min), reverse=True
        )

        return matches[:k]

    def list_entries(self) -> List[MemoryEntry]:
        """List all entries in short-term memory.

        Returns:
            List of all non-expired entries.
        """
        # Remove expired entries
        expired = [eid for eid in self._entries if self._is_expired(eid)]
        for eid in expired:
            del self._entries[eid]
            del self._access_times[eid]

        return list(self._entries.values())

    def _is_expired(self, entry_id: str) -> bool:
        """Check if entry has expired.

        Args:
            entry_id: Entry ID.

        Returns:
            True if expired, False otherwise.
        """
        if entry_id not in self._access_times:
            return True

        age = datetime.now() - self._access_times[entry_id]
        return age.total_seconds() > self.ttl_seconds

    def _prune_oldest(self) -> None:
        """Remove oldest accessed entry."""
        if not self._access_times:
            return

        oldest_id = min(self._access_times, key=self._access_times.get)
        del self._entries[oldest_id]
        del self._access_times[oldest_id]

    def clear(self) -> None:
        """Clear all entries."""
        self._entries.clear()
        self._access_times.clear()


class LongTermMemory(MemoryStore):
    """Persistent filesystem-based memory store.

    Stores entries as YAML files with an index for discovery.
    """

    def __init__(self, store_path: Optional[Path] = None):
        """Initialize long-term memory.

        Args:
            store_path: Path to memory store directory. Defaults to ~/.claude/memory/bay.
        """
        self.store_path = store_path or memory_dir()
        self.entries_dir = self.store_path / "entries"
        self.index_path = self.store_path / "index.yaml"

        # Ensure directories exist
        self.entries_dir.mkdir(parents=True, exist_ok=True)

        # Load or create index
        self._load_index()

    def _load_index(self) -> None:
        """Load or create memory index."""
        if self.index_path.exists():
            self.index = MemoryIndex.from_file(self.index_path)
        else:
            self.index = create_memory_index(
                name="bay",
                description="Bay agent memory store - patterns, learnings, and insights",
                tags=["agent", "learning", "patterns"],
            )
            self.index.to_file(self.index_path)

    def add_entry(self, entry: MemoryEntry) -> str:
        """Add entry to long-term memory.

        Args:
            entry: Memory entry to add.

        Returns:
            Entry ID.
        """
        # Save entry to file
        entry_path = self.entries_dir / f"{entry.id}.yaml"
        entry.to_file(entry_path)

        # Update index
        self.index.add_entry(entry)
        self.index.to_file(self.index_path)

        return entry.id

    def get_entry(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get entry from long-term memory.

        Args:
            entry_id: Entry ID.

        Returns:
            MemoryEntry if found, None otherwise.
        """
        entry_path = self.entries_dir / f"{entry_id}.yaml"

        if not entry_path.exists():
            return None

        return MemoryEntry.from_file(entry_path)

    def search(self, query: str, k: int = 5) -> List[MemoryEntry]:
        """Search long-term memory.

        Args:
            query: Search query.
            k: Number of results to return.

        Returns:
            List of matching entries.
        """
        query_lower = query.lower()
        matches = []

        # Search index first (faster)
        for entry_id, entry_summary in self.index.entries.items():
            title = entry_summary.get("title", "")
            tags = entry_summary.get("tags", [])
            summary = entry_summary.get("summary", "")

            if (
                query_lower in title.lower()
                or query_lower in summary.lower()
                or any(query_lower in tag.lower() for tag in tags)
            ):
                # Load full entry
                entry = self.get_entry(entry_id)
                if entry:
                    matches.append(entry)

        # Sort by relevance and recency
        # For now, just sort by last_modified (recency)
        matches.sort(
            key=lambda e: datetime.fromisoformat(e.last_modified), reverse=True
        )

        return matches[:k]

    def list_entries(self) -> List[MemoryEntry]:
        """List all entries in long-term memory.

        Returns:
            List of all entries.
        """
        entries = []

        for entry_id in self.index.entries.keys():
            entry = self.get_entry(entry_id)
            if entry:
                entries.append(entry)

        return entries

    def delete_entry(self, entry_id: str) -> None:
        """Delete entry from long-term memory.

        Args:
            entry_id: Entry ID.
        """
        # Remove file
        entry_path = self.entries_dir / f"{entry_id}.yaml"
        if entry_path.exists():
            entry_path.unlink()

        # Update index
        self.index.remove_entry(entry_id)
        self.index.to_file(self.index_path)

    def get_index(self) -> MemoryIndex:
        """Get memory index.

        Returns:
            MemoryIndex object.
        """
        return self.index


class EpisodicMemory(MemoryStore):
    """Historical archive in JSONL format.

    Stores observations and events as append-only log.
    """

    def __init__(self, log_path: Optional[Path] = None):
        """Initialize episodic memory.

        Args:
            log_path: Path to log file. Defaults to ~/.claude/observations/episodes.jsonl.
        """
        self.log_path = log_path or (observations_dir() / "episodes.jsonl")

        # Ensure directory exists
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

        # Create log file if it doesn't exist
        if not self.log_path.exists():
            self.log_path.touch()

    def add_entry(self, entry: MemoryEntry) -> str:
        """Add entry to episodic memory (append to log).

        Args:
            entry: Memory entry to add.

        Returns:
            Entry ID.
        """
        # Append to JSONL
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry.to_dict()) + "\n")

        return entry.id

    def get_entry(self, entry_id: str) -> Optional[MemoryEntry]:
        """Get entry from episodic memory.

        Args:
            entry_id: Entry ID.

        Returns:
            MemoryEntry if found, None otherwise.
        """
        # Linear search through log (inefficient for large logs)
        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                if data.get("id") == entry_id:
                    return MemoryEntry.from_dict(data)

        return None

    def search(self, query: str, k: int = 5) -> List[MemoryEntry]:
        """Search episodic memory.

        Args:
            query: Search query.
            k: Number of results to return.

        Returns:
            List of matching entries.
        """
        query_lower = query.lower()
        matches = []

        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                entry = MemoryEntry.from_dict(data)

                if (
                    query_lower in entry.title.lower()
                    or query_lower in entry.content.lower()
                    or any(query_lower in tag.lower() for tag in entry.tags)
                ):
                    matches.append(entry)

        # Sort by recency
        matches.sort(
            key=lambda e: datetime.fromisoformat(e.created), reverse=True
        )

        return matches[:k]

    def list_entries(self) -> List[MemoryEntry]:
        """List all entries in episodic memory.

        Returns:
            List of all entries.
        """
        entries = []

        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                entries.append(MemoryEntry.from_dict(data))

        return entries
