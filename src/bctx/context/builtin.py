"""Built-in context rules registration."""

from pathlib import Path
from typing import Optional

from ..core.paths import rules_dir
from .manager import add, get_by_name


BCTX_RULE_NAME = "bctx-cli"

BCTX_RULE_CONTENT = """# bctx — Context Manager & Agent Harness for Claude Code

bctx is a Python-based agent harness system that manages context files (rules,
skills, agents, plugins) and provides memory, observation, reflection, and
multi-agent coordination capabilities for Claude Code.

Resources live in `~/.claude/settings/bay/` and are discovered via
`~/.claude/CLAUDE.md` navigator.

## Commands

### Context Files — documents injected into every agent session

- `bctx files` — list all registered context files and their status.
- `bctx add <name> <path>` — register a file for injection (design docs,
  API specs, coding standards). Use --scope repo:<name> to limit to one repo.
- `bctx rm <name>` — remove a registered context file.
- `bctx toggle <name>` — enable/disable without removing.
- `bctx sync` — regenerate resource navigator and indexes.

### Installation & Management

- `bctx install` — install agent harness (creates directories, hooks, configs).
- `bctx uninstall` — remove agent harness.
- `bctx upgrade` — upgrade to new version.

### Agent Operations

- `bctx observe [event]` — trigger observation hooks.
- `bctx reflect` — trigger reflection and learning.
- `bctx memory <cmd>` — memory operations (add, show, search, list).
- `bctx validate` — validate schemas and configuration.

## Resource Discovery

Resources are organized in `~/.claude/settings/bay/{type}/` directories
(rules, skills, agents, plugins). Each type has its own directory.

Read `~/.claude/CLAUDE.md` for the full resource navigator.

## Memory System

Bay memory store lives in `~/.claude/memory/bay/`:
- Always read `index.yaml` FIRST (entry summaries)
- Load specific entries on demand
- Verify recalled information (memory = hint, check reality)

## Agent Harness Features

### Memory (Phase 2)
- Short-term memory (STM): Session-scoped, in-memory
- Long-term memory (LTM): Persistent, indexed patterns
- Episodic memory: Historical archive

### Observation (Phase 3)
- Automatic action logging
- Pattern detection (sequences, frequencies, anti-patterns)
- Learning from failures

### Verification (Phase 4)
- Pre-action checks prevent errors
- Examples: Edit requires Read, Git account verification

### Reflection (Phase 5)
- Triggered on task completion, errors, user correction
- Generates insights and learnings
- Stores to LTM for future use

### Multi-Agent Coordination (Phase 6)
- Executor, Observer, Coordinator agents
- Message-based communication
- Coordination patterns (master-worker, pipeline, peer-to-peer)
"""


def ensure_builtin_rules(db_path: Optional[Path] = None) -> None:
    """Write the bctx rule file and ensure it's registered in the database.

    Args:
        db_path: Optional database path (mainly for testing).

    Raises:
        IOError: If rule file can't be written.
        sqlite3.Error: If database operation fails.
    """
    # Ensure rules directory exists
    rules_path = rules_dir()
    rules_path.mkdir(parents=True, exist_ok=True)

    # Write rule file
    rule_file_path = rules_path / f"{BCTX_RULE_NAME}.md"
    rule_file_path.write_text(BCTX_RULE_CONTENT, encoding="utf-8")

    # Check if already registered
    existing = get_by_name(BCTX_RULE_NAME, db_path)
    if existing:
        # Already registered, skip
        return

    # Register in database
    add(
        name=BCTX_RULE_NAME,
        path=str(rule_file_path),
        scope="global",
        category="rules",
        typ="rules",
        description="bctx CLI and agent harness reference",
        db_path=db_path
    )
