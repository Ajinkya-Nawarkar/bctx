"""Installation and uninstallation logic for bctx agent harness."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import List
import os

from ..core.paths import (
    claude_dir,
    settings_dir,
    hooks_dir,
    memory_dir,
    observations_dir,
    sessions_dir,
    rules_dir,
    config_path,
    navigator_path,
    legacy_bctx_dir,
    ensure_dirs,
)
from ..core.config import default_config, save, migrate_from_legacy
from ..core.database import get_db
from ..context.builtin import ensure_builtin_rules
from ..context.navigator import generate_navigator


HOOK_NAMES = [
    "pre_session",
    "post_command",
    "pre_tool_call",
    "post_tool_call",
    "on_error",
]


def install(force: bool = False) -> None:
    """Install the bctx agent harness.

    Creates directory structure, installs hooks, configs, and default rules.

    Args:
        force: If True, overwrite existing installation without prompting.

    Raises:
        RuntimeError: If installation fails.
    """
    # Check if already installed
    if config_path().exists() and not force:
        raise RuntimeError(
            "bctx is already installed. Use --force to reinstall, "
            "or run 'bctx upgrade' to update."
        )

    # Create backup of existing installation
    if claude_dir().exists():
        backup_path = _create_backup()
        print(f"✓ Created backup: {backup_path}")

    # Create directory structure
    ensure_dirs()
    print("✓ Created directory structure")

    # Migrate from legacy installation if exists
    migrated_config = None
    if legacy_bctx_dir().exists():
        migrated_config = migrate_from_legacy()
        if migrated_config:
            print(f"✓ Migrated configuration from {legacy_bctx_dir()}")

    # Install configuration
    config = migrated_config or default_config()
    save(config)
    print(f"✓ Installed configuration: {config_path()}")

    # Initialize database
    db = get_db()
    db.connect()
    print(f"✓ Initialized database")

    # Install hook scripts
    _install_hooks()
    print(f"✓ Installed hook scripts: {hooks_dir()}")

    # Copy default rules from package to ~/.claude/settings/bay/rules/
    _copy_default_rules()
    print(f"✓ Copied default rules to {rules_dir()}")

    # Ensure builtin rules are registered
    ensure_builtin_rules()
    print("✓ Registered built-in rules")

    # Create initial memory entries
    _create_initial_memory()
    print(f"✓ Created initial memory entries: {memory_dir()}")

    # Generate navigator
    generate_navigator()
    print(f"✓ Generated navigator: {navigator_path()}")

    print("\n✓ Installation complete!")
    print("\nNext steps:")
    print("  1. Review configuration: bctx config")
    print("  2. Check installed files: bctx files")
    print("  3. View navigator: cat ~/.claude/CLAUDE.md")


def uninstall(keep_data: bool = False) -> None:
    """Uninstall the bctx agent harness.

    Args:
        keep_data: If True, keep data directories (memory, observations, sessions).

    Raises:
        RuntimeError: If uninstallation fails.
    """
    # Create backup before uninstalling
    if claude_dir().exists():
        backup_path = _create_backup()
        print(f"✓ Created backup: {backup_path}")

    # Remove hook scripts
    for hook_name in HOOK_NAMES:
        hook_path = hooks_dir() / hook_name
        if hook_path.exists():
            hook_path.unlink()

    print(f"✓ Removed hook scripts")

    # Remove settings directory
    if settings_dir().exists():
        shutil.rmtree(settings_dir())
        print(f"✓ Removed settings: {settings_dir()}")

    # Remove navigator
    if navigator_path().exists():
        navigator_path().unlink()
        print(f"✓ Removed navigator: {navigator_path()}")

    # Optionally remove data directories
    if not keep_data:
        if memory_dir().exists():
            shutil.rmtree(memory_dir())
            print(f"✓ Removed memory: {memory_dir()}")

        if observations_dir().exists():
            shutil.rmtree(observations_dir())
            print(f"✓ Removed observations: {observations_dir()}")

        if sessions_dir().exists():
            shutil.rmtree(sessions_dir())
            print(f"✓ Removed sessions: {sessions_dir()}")
    else:
        print("✓ Kept data directories (--keep-data)")

    print("\n✓ Uninstallation complete!")
    if keep_data:
        print(f"\nData preserved in backup: {backup_path}")


def _create_backup() -> Path:
    """Create a backup of the ~/.claude directory.

    Returns:
        Path to backup directory.

    Raises:
        RuntimeError: If backup creation fails.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = claude_dir().parent / f".claude.backup.{timestamp}"

    try:
        shutil.copytree(claude_dir(), backup_path, symlinks=True)
        return backup_path
    except Exception as e:
        raise RuntimeError(f"Failed to create backup: {e}")


def _install_hooks() -> None:
    """Install hook scripts to ~/.claude/hooks/.

    Copies hook templates from package to hooks directory and makes them executable.

    Raises:
        RuntimeError: If hook installation fails.
    """
    # Get templates directory from package
    templates_dir = Path(__file__).parent / "templates"

    if not templates_dir.exists():
        raise RuntimeError(f"Hook templates not found: {templates_dir}")

    # Ensure hooks directory exists
    hooks_dir().mkdir(parents=True, exist_ok=True)

    # Copy and make executable
    for hook_name in HOOK_NAMES:
        template_path = templates_dir / hook_name
        if not template_path.exists():
            continue

        hook_path = hooks_dir() / hook_name

        # Copy file
        shutil.copy2(template_path, hook_path)

        # Make executable
        os.chmod(hook_path, 0o755)


def _copy_default_rules() -> None:
    """Copy default rules from package to ~/.claude/settings/bay/rules/.

    Raises:
        RuntimeError: If rule copying fails.
    """
    # Find package root (traverse up from this file)
    package_root = Path(__file__).parent.parent.parent.parent

    # Rules are in the rules/ directory at package root
    source_rules_dir = package_root / "rules"

    if not source_rules_dir.exists():
        # Try alternate location (for development)
        source_rules_dir = Path.cwd() / "rules"

    if not source_rules_dir.exists():
        print(f"⚠ Warning: Default rules not found at {source_rules_dir}")
        return

    # Ensure destination exists
    dest_rules = rules_dir()
    dest_rules.mkdir(parents=True, exist_ok=True)

    # Copy all .md files
    for rule_file in source_rules_dir.glob("*.md"):
        dest_file = dest_rules / rule_file.name
        shutil.copy2(rule_file, dest_file)


def _create_initial_memory() -> None:
    """Create initial memory entries and index.

    Raises:
        RuntimeError: If memory creation fails.
    """
    # Ensure memory directory exists
    memory_path = memory_dir()
    memory_path.mkdir(parents=True, exist_ok=True)

    # Create entries directory
    entries_dir = memory_path / "entries"
    entries_dir.mkdir(parents=True, exist_ok=True)

    # Create initial index.yaml
    import yaml

    index_data = {
        "name": "bay",
        "description": "Bay agent memory store - patterns, learnings, and insights",
        "tags": ["agent", "learning", "patterns"],
        "created": datetime.now().isoformat(),
        "last_modified": datetime.now().isoformat(),
        "entries": {},
    }

    index_path = memory_path / "index.yaml"
    with open(index_path, "w", encoding="utf-8") as f:
        yaml.dump(index_data, f, default_flow_style=False, sort_keys=False)


def upgrade() -> None:
    """Upgrade bctx to the latest version.

    Preserves existing configuration and data while updating code and hooks.

    Raises:
        RuntimeError: If upgrade fails.
    """
    print("Upgrading bctx...")

    # Create backup
    if claude_dir().exists():
        backup_path = _create_backup()
        print(f"✓ Created backup: {backup_path}")

    # Reinstall hooks (may have been updated)
    _install_hooks()
    print("✓ Updated hook scripts")

    # Regenerate navigator (may have new features)
    generate_navigator()
    print(f"✓ Regenerated navigator: {navigator_path()}")

    # Ensure builtin rules are up to date
    ensure_builtin_rules()
    print("✓ Updated built-in rules")

    print("\n✓ Upgrade complete!")
