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
    from ..memory import LongTermMemory, create_memory_entry

    # Initialize LTM (creates directory structure and index)
    ltm = LongTermMemory()

    # Create initial anti-pattern entries
    initial_entries = [
        create_memory_entry(
            id="edit-requires-read",
            title="Edit Requires Prior Read",
            tags=["anti-pattern", "file-operations", "verification"],
            content="""# Anti-Pattern: Edit Without Read

## Pattern
Calling the Edit tool without first reading the file in the current session
results in failure 82% of the time.

## Why It Fails
The Edit tool requires file contents to be in the agent's working context to
make accurate string replacements. Without a prior Read, the agent lacks the
context needed for precise edits.

## Solution
Always Read the file before Edit:
1. Check if file is in session STM (short-term memory)
2. If not, call Read to load contents
3. Then proceed with Edit using exact strings from the Read output

## Examples

✅ **Good Pattern**:
1. Read(config.yaml)
2. Edit(config.yaml, old_string="port: 8080", new_string="port: 9000")

❌ **Bad Pattern**:
1. Edit(config.yaml, old_string="port: 8080", new_string="port: 9000")
   → FAILS: File not in context

## Verification
This pattern is enforced by the pre_tool_call hook's EditRequiresReadCheck.
""",
        ),
        create_memory_entry(
            id="git-account-verification",
            title="Git Account Verification",
            tags=["anti-pattern", "git", "verification"],
            content="""# Anti-Pattern: Git Push to Wrong Account

## Pattern
Pushing to a repository using the wrong GitHub account leads to authentication
failures or commits attributed to the wrong user.

## Why It Happens
Multiple GitHub accounts configured via `gh auth` can cause confusion about
which account is active.

## Solution
Always verify active account before git operations:
1. Run `gh auth status` to check active account
2. If wrong account, run `gh auth switch --user <correct-user>`
3. Then proceed with git push

## Account Mapping

| Account | Repos |
|---------|-------|
| Ajinkya-Nawarkar | bay-tui, bctx |
| lasso-dev | edgedyv, claude-config, lasso_proxy, portfoliodyv, ctxin |

## Verification
This pattern is enforced by the pre_tool_call hook's GitAccountCheck.
""",
        ),
        create_memory_entry(
            id="bash-quote-spaces",
            title="Bash Paths with Spaces Require Quotes",
            tags=["anti-pattern", "bash", "verification"],
            content="""# Anti-Pattern: Unquoted Paths with Spaces

## Pattern
Using paths containing spaces in Bash commands without quotes causes the path
to be split into multiple arguments, leading to "file not found" errors.

## Why It Fails
Bash uses spaces as argument delimiters. Without quotes, "My Documents/file.txt"
becomes two arguments: "My" and "Documents/file.txt".

## Solution
Always quote paths with spaces:
- Use double quotes: `cd "My Documents"`
- Or escape spaces: `cd My\\ Documents`

## Examples

✅ **Good Pattern**:
```bash
cd "/Users/name/My Documents"
python "/path/with spaces/script.py"
```

❌ **Bad Pattern**:
```bash
cd /Users/name/My Documents        # FAILS
python /path/with spaces/script.py  # FAILS
```

## Verification
This pattern generates a warning from the pre_tool_call hook's BashQuoteSpacesCheck.
""",
        ),
        create_memory_entry(
            id="index-first-discovery",
            title="Index-First Discovery Pattern",
            tags=["pattern", "memory", "best-practice"],
            content="""# Pattern: Index-First Discovery

## Pattern
Always read index.yaml before loading individual entries from a resource
directory or memory store.

## Why It Matters
Index files provide:
1. Entry summaries without loading full content
2. Metadata (tags, timestamps, descriptions)
3. Fast discovery of relevant entries
4. Reduced context usage

## Implementation
1. Read `<store>/index.yaml` first
2. Scan summaries for relevant entries
3. Load only the specific entries needed
4. Verify information (memory = hint, check reality)

## Examples

✅ **Good Pattern**:
```python
# 1. Read index
index = read_yaml("~/.claude/memory/bay/index.yaml")

# 2. Find relevant entries
relevant = [e for e in index.entries if "anti-pattern" in e.tags]

# 3. Load specific entries
for entry_id in relevant[:3]:
    entry = read_yaml(f"~/.claude/memory/bay/entries/{entry_id}.yaml")
```

❌ **Bad Pattern**:
```python
# Load all entries without checking index first
entries = glob("~/.claude/memory/bay/entries/*.yaml")
all_data = [read_yaml(e) for e in entries]  # Loads everything!
```

## Application
- Memory stores (`~/.claude/memory/bay/`)
- Context resources (`~/.claude/settings/bay/{type}/`)
- Project contexts (`~/.claude/settings/bay/projects/`)
""",
        ),
    ]

    # Add entries to LTM
    for entry in initial_entries:
        ltm.add_entry(entry)


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
