"""Path constants and version information for bctx."""

import os
from pathlib import Path

__version__ = "2.0.0-alpha"

# Base directories
def home_dir() -> Path:
    """Return user's home directory."""
    return Path.home()


def claude_dir() -> Path:
    """Return ~/.claude directory."""
    return home_dir() / ".claude"


def settings_dir() -> Path:
    """Return ~/.claude/settings/bay directory (new structure)."""
    return claude_dir() / "settings" / "bay"


def hooks_dir() -> Path:
    """Return ~/.claude/hooks directory."""
    return claude_dir() / "hooks"


def memory_dir() -> Path:
    """Return ~/.claude/memory/bay directory."""
    return claude_dir() / "memory" / "bay"


def observations_dir() -> Path:
    """Return ~/.claude/observations directory."""
    return claude_dir() / "observations"


def sessions_dir() -> Path:
    """Return ~/.claude/sessions directory."""
    return claude_dir() / "sessions"


# Legacy directories (for migration from Go version)
def legacy_bctx_dir() -> Path:
    """Return ~/.claude/bayctx directory (Go version location)."""
    return claude_dir() / "bayctx"


# Specific file paths
def config_path() -> Path:
    """Return ~/.claude/settings/bay/config.yaml."""
    return settings_dir() / "config.yaml"


def db_path() -> Path:
    """Return ~/.claude/settings/bay/bctx.db."""
    return settings_dir() / "bctx.db"


def rules_dir() -> Path:
    """Return ~/.claude/settings/bay/rules directory."""
    return settings_dir() / "rules"


def navigator_path() -> Path:
    """Return ~/.claude/CLAUDE.md navigator file."""
    return claude_dir() / "CLAUDE.md"


# Resource types
RESOURCE_TYPES = ["rules", "skills", "agents", "plugins"]


def ensure_dirs() -> None:
    """Create all required directories if they don't exist."""
    dirs = [
        settings_dir(),
        hooks_dir(),
        memory_dir(),
        observations_dir(),
        sessions_dir(),
        rules_dir(),
    ]

    # Create resource type directories
    for resource_type in RESOURCE_TYPES:
        dirs.append(settings_dir() / resource_type)

    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)


def legacy_db_path() -> Path:
    """Return ~/.claude/bayctx/bayctx.db (Go version location)."""
    return legacy_bctx_dir() / "bayctx.db"


def legacy_config_path() -> Path:
    """Return ~/.claude/bayctx/config.yaml (Go version location)."""
    return legacy_bctx_dir() / "config.yaml"
