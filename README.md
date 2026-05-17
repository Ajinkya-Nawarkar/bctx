# bctx

**Claude Code Context Manager & Agent Harness**

Transform Claude Code into a self-learning autonomous assistant with memory, observation, reflection, and multi-agent coordination capabilities.

## Features

- **Context Management**: Register rules, skills, docs, and plugins for Claude Code sessions
- **Memory System**: Short-term, long-term, and episodic memory stores
- **Observation Layer**: Automatic action logging and pattern detection
- **Verification Framework**: Pre-action checks to prevent errors
- **Reflection System**: Learning from successes and failures
- **Multi-Agent Coordination**: Executor, observer, and coordinator agents

## Install

Install via pip:

```bash
pip install bctx
```

Or install from source:

```bash
git clone https://github.com/Ajinkya-Nawarkar/bctx.git
cd bctx
pip install -e .
```

## Quick Start

### 1. Install the Agent Harness

```bash
bctx install
```

This creates:
- `~/.claude/settings/bay/` - Configuration and rules
- `~/.claude/hooks/` - Lifecycle hook scripts
- `~/.claude/memory/bay/` - Memory store
- `~/.claude/CLAUDE.md` - Resource navigator

### 2. Register Context Files

```bash
# Register a coding standards doc
bctx add go-standards ~/docs/go-standards.md

# Register a repo-specific design doc
bctx add api-design ~/work/api/DESIGN.md --scope repo:api-service

# See what's registered
bctx files

# Test what gets injected
bctx inject
```

### 3. Configure Claude Code Hooks

Add bctx to Claude Code's SessionStart hook in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [{ "type": "command", "command": "bctx inject" }]
      }
    ]
  }
}
```

## Commands

### Context Management

```bash
bctx                          # Show status (registered files, active rules)
bctx inject                   # Output active rules for SessionStart hook
bctx files                    # List all registered context files
bctx add <name> <path>        # Register a context file
                              #   --scope global|repo:<name>
                              #   --type rules|skills|agents|plugins
                              #   --category <cat>  --desc <description>
bctx rm <name>                # Remove a context file
bctx toggle <name>            # Enable/disable a context file
bctx sync                     # Regenerate CLAUDE.md navigator + indexes
bctx cleanup                  # Remove entries pointing to deleted files
bctx config                   # Show feature settings
bctx config <key> on|off      # Toggle: context_injection, context_budget
```

### Installation & Management

```bash
bctx install                  # Install agent harness
bctx uninstall                # Remove agent harness (--keep-data to preserve data)
bctx upgrade                  # Upgrade to new version
```

### Agent Operations

```bash
bctx observe [event]          # Trigger observation hooks
bctx reflect                  # Trigger reflection and learning
bctx memory <cmd>             # Memory operations (add, show, search, list)
bctx validate                 # Validate schemas and configuration
```

## How It Works

bctx stores registered context files in a SQLite database at `~/.claude/settings/bay/bctx.db`. Each file has a name, path, scope (global or per-repo), type, and category.

On `bctx inject`, it finds all enabled files matching the current repo (global scope + repo-specific scope), reads their content, and outputs it as markdown for Claude to consume.

bctx also generates:
- `~/.claude/CLAUDE.md` — Resource navigator (entry point for agents)
- `~/.claude/settings/bay/{type}/index.yaml` — Catalogs per resource type
- `~/.claude/memory/bay/index.yaml` — Memory entry catalog

## Resource Types

| Type | Directory | Purpose |
|------|-----------|---------|
| rules | `~/.claude/settings/bay/rules/` | Coding standards, conventions, constraints |
| skills | `~/.claude/settings/bay/skills/` | Reusable agent capabilities |
| agents | `~/.claude/settings/bay/agents/` | Agent configurations |
| plugins | `~/.claude/settings/bay/plugins/` | Extensions and integrations |

## Agent Harness Architecture

### Memory System (Phase 2)

- **Short-term memory (STM)**: Session-scoped, in-memory tracking
- **Long-term memory (LTM)**: Persistent patterns and learnings
- **Episodic memory**: Historical archive in JSONL format

Memory stores use an index-first discovery pattern:
1. Read `index.yaml` for entry summaries
2. Load specific entries on demand
3. Verify recalled information (memory = hint, check reality)

### Observation Layer (Phase 3)

- Automatic logging of all actions via lifecycle hooks
- Pattern detection (sequences, frequencies, anti-patterns)
- Learning from failures and successes

### Verification Framework (Phase 4)

Pre-action checks to prevent common errors:
- **Edit without Read**: Blocks Edit tool calls without prior Read in session
- **Git account mismatch**: Verifies correct GitHub account before push
- **Unquoted spaces**: Warns about paths with spaces in Bash commands

### Reflection System (Phase 5)

Triggered on:
- Task completion (success or failure)
- Error thresholds (3+ failures)
- User corrections

Generates insights and stores learnings to LTM for future use.

### Multi-Agent Coordination (Phase 6)

- **Executor Agent**: Performs primary tasks
- **Observer Agent**: Monitors and logs actions
- **Coordinator Agent**: Orchestrates workflows

Communication via message protocol with correlation IDs.

## Configuration

Configuration lives in `~/.claude/settings/bay/config.yaml`:

```yaml
version: "2.0.0"
context_injection: true
context_budget: 50000

agents:
  executor:
    enabled: true
    max_concurrent_tasks: 5
    timeout_seconds: 300
  observer:
    enabled: true
    log_level: info

memory:
  short_term:
    max_size: 1000
    ttl_seconds: 3600
  long_term:
    path: ~/.claude/memory/bay
    retrieval:
      strategy: hybrid
      recency_weight: 0.3
      relevance_weight: 0.7

hooks:
  pre_session:
    enabled: true
  post_command:
    enabled: true
  pre_tool_call:
    enabled: true
  post_tool_call:
    enabled: true
  on_error:
    enabled: true
```

## Migration from Go Version

If you previously used the Go-based bctx (`~/.claude/bayctx/`), the Python version will automatically detect and migrate your configuration and database on first install.

A backup is created at `~/.claude.backup.<timestamp>/` before migration.

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/Ajinkya-Nawarkar/bctx.git
cd bctx

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=bctx --cov-report=term-missing

# Run specific test file
pytest tests/test_context.py -v
```

### Code Quality

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/
```

## Design Document

See [DESIGN.md](DESIGN.md) for the complete architecture vision and implementation roadmap.

## License

MIT

## Contributing

Contributions welcome! Please open an issue or PR.

## Acknowledgments

Built with:
- [Click](https://click.palletsprojects.com/) - CLI framework
- [PyYAML](https://pyyaml.org/) - YAML parser
- SQLite - Embedded database
