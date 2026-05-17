"""Memory entry schemas and data models."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path
import yaml


@dataclass
class MemoryEntry:
    """Represents a single memory entry."""

    id: str
    title: str
    tags: List[str]
    content: str
    created: str
    last_modified: str
    related_entries: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryEntry":
        """Create MemoryEntry from dictionary.

        Args:
            data: Memory entry dictionary.

        Returns:
            MemoryEntry instance.
        """
        return cls(
            id=data["id"],
            title=data["title"],
            tags=data.get("tags", []),
            content=data["content"],
            created=data["created"],
            last_modified=data["last_modified"],
            related_entries=data.get("related_entries", []),
            metadata=data.get("metadata", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation.
        """
        return asdict(self)

    @classmethod
    def from_file(cls, path: Path) -> "MemoryEntry":
        """Load memory entry from YAML file.

        Args:
            path: Path to YAML file.

        Returns:
            MemoryEntry instance.

        Raises:
            FileNotFoundError: If file doesn't exist.
            yaml.YAMLError: If YAML is invalid.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data)

    def to_file(self, path: Path) -> None:
        """Save memory entry to YAML file.

        Args:
            path: Path to save to.

        Raises:
            IOError: If file can't be written.
        """
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write to file
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)

    def summary(self) -> Dict[str, Any]:
        """Generate entry summary for index.

        Returns:
            Summary dictionary.
        """
        return {
            "file": f"entries/{self.id}.yaml",
            "title": self.title,
            "tags": self.tags,
            "summary": self._generate_summary(),
            "created": self.created,
            "last_modified": self.last_modified,
        }

    def _generate_summary(self) -> str:
        """Generate a brief summary of content.

        Returns:
            First 200 characters of content or first line.
        """
        lines = self.content.strip().split("\n")
        # Skip markdown headers
        for line in lines:
            if line and not line.startswith("#"):
                # Take first non-header line, limit to 200 chars
                return line[:200] + ("..." if len(line) > 200 else "")

        # Fallback: just take first 200 chars
        return self.content[:200] + ("..." if len(self.content) > 200 else "")


@dataclass
class MemoryIndex:
    """Index for a memory store."""

    name: str
    description: str
    tags: List[str]
    created: str
    last_modified: str
    entries: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryIndex":
        """Create MemoryIndex from dictionary.

        Args:
            data: Index dictionary.

        Returns:
            MemoryIndex instance.
        """
        return cls(
            name=data["name"],
            description=data["description"],
            tags=data.get("tags", []),
            created=data["created"],
            last_modified=data["last_modified"],
            entries=data.get("entries", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary.

        Returns:
            Dictionary representation.
        """
        return asdict(self)

    @classmethod
    def from_file(cls, path: Path) -> "MemoryIndex":
        """Load index from YAML file.

        Args:
            path: Path to index.yaml.

        Returns:
            MemoryIndex instance.

        Raises:
            FileNotFoundError: If file doesn't exist.
            yaml.YAMLError: If YAML is invalid.
        """
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        return cls.from_dict(data)

    def to_file(self, path: Path) -> None:
        """Save index to YAML file.

        Args:
            path: Path to save to.

        Raises:
            IOError: If file can't be written.
        """
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write to file
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)

    def add_entry(self, entry: MemoryEntry) -> None:
        """Add or update an entry in the index.

        Args:
            entry: Memory entry to add.
        """
        self.entries[entry.id] = entry.summary()
        self.last_modified = datetime.now().isoformat()

    def remove_entry(self, entry_id: str) -> None:
        """Remove an entry from the index.

        Args:
            entry_id: ID of entry to remove.
        """
        if entry_id in self.entries:
            del self.entries[entry_id]
            self.last_modified = datetime.now().isoformat()


def create_memory_entry(
    id: str,
    title: str,
    tags: List[str],
    content: str,
    related_entries: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> MemoryEntry:
    """Create a new memory entry with timestamps.

    Args:
        id: Unique identifier.
        title: Entry title.
        tags: List of tags.
        content: Entry content (markdown).
        related_entries: Optional list of related entry IDs.
        metadata: Optional metadata dictionary.

    Returns:
        New MemoryEntry instance.
    """
    now = datetime.now().isoformat()

    return MemoryEntry(
        id=id,
        title=title,
        tags=tags,
        content=content,
        created=now,
        last_modified=now,
        related_entries=related_entries or [],
        metadata=metadata or {},
    )


def create_memory_index(
    name: str, description: str, tags: Optional[List[str]] = None
) -> MemoryIndex:
    """Create a new memory index with timestamps.

    Args:
        name: Store name.
        description: Store description.
        tags: Optional list of tags.

    Returns:
        New MemoryIndex instance.
    """
    now = datetime.now().isoformat()

    return MemoryIndex(
        name=name,
        description=description,
        tags=tags or [],
        created=now,
        last_modified=now,
        entries={},
    )
