# Implementation Guide: bctx Memory Integration

Practical step-by-step guide for implementing the CLAUDE.md pattern and memory system integration for bctx.

---

## Phase 1: Create Bay Memory Store

### Step 1.1: Create Directory Structure

```bash
mkdir -p ~/.claude/memory/bay/entries
```

### Step 1.2: Create `index.yaml`

**File**: `~/.claude/memory/bay/index.yaml`

```yaml
name: bay
description: Bay workspace orchestration - combines bay-tui session management and bctx context injection for Claude Code
tags:
- ecosystem
- workspace-manager
- memory-system
- context-orchestration
- go
created: '2026-05-16T00:00:00.000000+00:00'
last_modified: '2026-05-16T00:00:00.000000+00:00'
entries:
  overview:
    file: entries/overview.yaml
    title: Bay Ecosystem Overview
    tags:
    - architecture
    - integration
    - memory-system
    - workflows
    summary: Workspace orchestration combining bay-tui session management and bctx context injection for Claude Code
    created: '2026-05-16T00:00:00.000000+00:00'
    last_modified: '2026-05-16T00:00:00.000000+00:00'
```

### Step 1.3: Create `entries/overview.yaml`

**File**: `~/.claude/memory/bay/entries/overview.yaml`

```yaml
id: overview
title: Bay Ecosystem Overview
tags:
- architecture
- integration
- memory-system
- workflows
- bay-tui
- bctx
- claude-code
created: '2026-05-16T00:00:00.000000+00:00'
last_modified: '2026-05-16T00:00:00.000000+00:00'
related_entries:
- bay-tui/overview
- bctx/overview

content: |
  ## Overview

  Bay is a workspace orchestration ecosystem for developers using Claude Code. It combines two complementary tools:

  - **bay-tui**: Terminal session manager with tmux orchestration, 3-layer memory, and git worktree management
  - **bctx**: Context manager that injects coding standards, documentation, and project context into Claude Code sessions

  Together they provide persistent memory and intelligent context injection for AI-assisted development workflows.

  ## Architecture

  ```
  Bay Ecosystem
  │
  ├─ bay-tui (Session Layer)
  │   ├─ Runtime: tmux session + Bubbletea TUI
  │   ├─ Storage: YAML sessions (~/.bay/sessions/) + SQLite memory (~/.bay/bay.db)
  │   ├─ Purpose: Multi-repo workspace orchestration
  │   └─ Features:
  │       ├─ Session management (create, switch, delete)
  │       ├─ 3-layer memory (episodic log, working state, tasks)
  │       ├─ Git worktree isolation (~/.bay/worktrees/)
  │       ├─ Context capture (terminal snapshots, git commits)
  │       └─ Agent context injection via hooks
  │
  └─ bctx (Context Layer)
      ├─ Runtime: CLI + SessionStart hook
      ├─ Storage: SQLite database (~/.claude/bayctx/bayctx.db) + referenced markdown
      ├─ Purpose: Intelligent context injection into Claude Code
      └─ Features:
          ├─ Rule registration (global/repo-scoped)
          ├─ Context filtering (scope, type, category)
          ├─ SessionStart hook integration
          ├─ Navigator generation (CLAUDE.md + index.yaml catalogs)
          └─ Context budget management
  ```

  ## Integration Points

  ### 1. Session Detection
  bay-tui sets current working directory → bctx detects git repo → injects repo-specific rules

  ### 2. Memory Context
  bay-tui captures episodic events → stores in SQLite → available for agent context queries

  ### 3. Task Tracking
  bay-tui task system → tasks visible to agents via context injection

  ### 4. Navigator Pattern
  Both tools generate CLAUDE.md navigators:
  - `~/.claude/CLAUDE.md` - Global navigation hub
  - `~/.claude/bayctx/CLAUDE.md` - bctx resource catalog (auto-generated)
  - Project-specific CLAUDE.md files - Project guidelines

  ## Data Flow

  ```
  Developer Session
          │
          ├─> Launch bay-tui
          │       ├─ Attach to tmux session "bay"
          │       ├─ Load session YAML (~/.bay/sessions/{name}.yaml)
          │       ├─ Connect to SQLite (~/.bay/bay.db)
          │       ├─ Display TUI (topbar + active pane)
          │       └─ Begin capturing events
          │
          ├─> Start Claude Code
          │       │
          │       └─> SessionStart Hook
          │               │
          │               └─> bctx inject
          │                       ├─ Detect git repo from cwd
          │                       ├─ Query: WHERE enabled=1 AND (scope='global' OR scope='repo:name')
          │                       ├─ Read markdown content from disk
          │                       ├─ Apply context budget constraints
          │                       └─ Output to stdout → Claude receives context
          │
          ├─> Work on code
          │       │
          │       ├─> bay-tui captures:
          │       │   ├─ Terminal snapshots (every 5s, debounced)
          │       │   ├─ Git commits (via hooks)
          │       │   ├─ Session switches
          │       │   └─ Task updates
          │       │
          │       └─> bctx provides:
          │           ├─ Global coding standards
          │           ├─ Repo-specific API docs
          │           ├─ Skills and agent definitions
          │           └─ MCP plugin configurations
          │
          └─> Context persists across sessions
                  │
                  ├─> bay-tui: SQLite memory (episodic, working_state, tasks)
                  └─> bctx: SQLite registrations + file references
  ```

  ## Key Design Decisions

  ### Complementary Roles
  - **bay-tui**: Captures what happened (memory layer)
  - **bctx**: Provides what agents need (context layer)

  ### Shared Storage Pattern
  - Both use SQLite with WAL mode for concurrent access
  - Both support per-repo scoping
  - Both expose CLI for management

  ### Navigator Pattern
  - Global `~/.claude/CLAUDE.md` as single entry point
  - Auto-generated catalogs reduce manual maintenance
  - index.yaml files provide lightweight discovery

  ### Context Budget
  - bctx respects configurable budget (default 12K chars)
  - Prioritizes repo-specific over global rules
  - Enables truncation of lowest-priority content

  ### Hook-Based Injection
  - SessionStart hook ensures context always available
  - Graceful failure (silent no-op) never breaks Claude Code startup
  - Single command (`bctx inject`) handles all logic

  ## Data Paths

  ### bay-tui
  - `~/.bay/` - Root directory
  - `~/.bay/config.yaml` - Configuration
  - `~/.bay/bay.db` - SQLite memory database
  - `~/.bay/sessions/{name}.yaml` - Session files
  - `~/.bay/worktrees/{repo}/{branch}/` - Git worktrees
  - `~/.bay/.active-session` - Active session marker

  ### bctx
  - `~/.claude/bayctx/` - Root directory
  - `~/.claude/bayctx/config.yaml` - Configuration
  - `~/.claude/bayctx/bayctx.db` - SQLite registration database
  - `~/.claude/bayctx/CLAUDE.md` - Auto-generated navigator
  - `~/.claude/bayctx/{rules,skills,agents,plugins}/index.yaml` - Resource catalogs
  - `~/.claude/bayctx/projects/{repo}/status.md` - Per-project state

  ### Shared
  - `~/.claude/CLAUDE.md` - Global navigation hub
  - `~/.claude/memory/bay/` - Ecosystem memory store
  - `~/.claude/memory/bay-tui/` - bay-tui memory store
  - `~/.claude/memory/bctx/` - bctx memory store

  ## Commands

  ### bay-tui
  | Command | Purpose |
  |---------|---------|
  | `bay` | Launch TUI (attach to tmux) |
  | `bay -f` | Fresh start (kill existing, relaunch) |
  | `bay session ls` | List all sessions |
  | `bay session kill <name>` | Delete session |
  | `bay task create "desc"` | Create task |
  | `bay task done <id>` | Mark task complete |
  | `bay ctx search "query"` | Search memory (FTS5) |

  ### bctx
  | Command | Purpose |
  |---------|---------|
  | `bctx` | Show status (counts, active rules) |
  | `bctx inject` | Output active rules (hook use) |
  | `bctx add <name> <path>` | Register context file |
  | `bctx rm <name>` | Remove registration |
  | `bctx toggle <name>` | Enable/disable file |
  | `bctx files` | List registrations |
  | `bctx sync` | Rebuild navigator & indexes |
  | `bctx cleanup` | Remove stale entries |

  ## Use Cases

  ### Multi-Repo Development
  ```bash
  # Create sessions for different repos
  bay  # Launch TUI, press 'n' to create session
  # Arrow keys to navigate repos
  # Enter to activate session
  ```

  ### Persistent Coding Standards
  ```bash
  # Register global Go standards
  bctx add go-standards ~/docs/go-standards.md --scope global --type rules

  # Register repo-specific API docs
  bctx add api-spec ~/projects/myapp/api.md --scope repo:myapp --type rules

  # Every Claude Code session in myapp gets both
  ```

  ### Context-Aware Agent
  ```bash
  # Start bay session
  bay

  # Navigate to project
  # Arrow keys → select repo → Enter

  # Start Claude Code
  # SessionStart hook → bctx inject
  # Agent receives:
  #   - Global rules (coding standards)
  #   - Repo rules (API docs)
  #   - Recent bay-tui tasks
  #   - Session context
  ```

  ### Task-Driven Development
  ```bash
  # Create task in bay
  bay task "Implement user authentication"

  # Task visible in topbar
  # Task injected into agent context
  # Agent can reference task in suggestions
  ```

  ### Memory Search
  ```bash
  # Search across all captured context
  bay ctx search "authentication flow"

  # FTS5 search across:
  #   - Terminal snapshots
  #   - Git commits
  #   - Session notes
  ```

  ## Target Users

  ### Individual Developers
  - Working on multiple repos simultaneously
  - Want persistent context across sessions
  - Need intelligent AI agent assistance

  ### Small Teams
  - Share coding standards via bctx rules
  - Standardize project documentation patterns
  - Consistent Claude Code experience

  ### Power Users
  - Heavy tmux users wanting better orchestration
  - AI-assisted development workflows
  - Complex multi-repo/multi-branch scenarios

  ## Improvement Plan

  ### High Priority (Q2 2026)
  - **Team sharing**: Git-based rule repositories for synchronized context
  - **Context ranking**: Intelligent priority system for budget management
  - **Integration depth**: Deeper bay-tui ↔ bctx communication

  ### Medium Priority (Q3 2026)
  - **Conditional rules**: File-pattern and branch-based scoping
  - **Layout persistence**: Full pane tree serialization in bay-tui
  - **Remote sessions**: SSH-based forwarding for distributed teams

  ### Lower Priority (Q4 2026)
  - **Plugin system**: Extensible context providers and pane types
  - **PreCompact hook**: Mid-session context refresh
  - **Content transformation**: Smart truncation and summarization

  ## Related Documentation

  - `~/.claude/memory/bay-tui/entries/overview.yaml` - bay-tui deep dive
  - `~/.claude/memory/bctx/entries/overview.yaml` - bctx deep dive
  - `~/.claude/CLAUDE.md` - Global navigation hub
  - `~/.claude/memory/index.md` - Memory system documentation
```

---

## Phase 2: Update Global CLAUDE.md

### Step 2.1: Check Current Memory Table

Verify that the memory stores table in `~/.claude/CLAUDE.md` includes bay:

```markdown
| Store | Description |
|-------|-------------|
| `bay/` | Bay workspace orchestration - bay-tui + bctx ecosystem |
| `bay-tui/` | Terminal session manager - tmux orchestration, memory, agent context |
| `bctx/` | Context manager for Claude Code - rule injection via SessionStart hook |
```

### Step 2.2: Verify Global Rules Section

Ensure the Global Rules section includes index.yaml pattern:

```markdown
# Global Rules

## Directory Index

Every agent-relevant directory has an `index.yaml` — read it before loading files.

When a task relates to a topic described in an index.yaml entry, read that file first.
When adding, removing, or renaming files in any indexed directory, update its `index.yaml` to match.
```

---

## Phase 3: Implement Navigator Generation

### Step 3.1: Update `bctx sync` Command

The `bctx sync` command should generate:

1. `~/.claude/bayctx/CLAUDE.md` - Main navigator
2. `~/.claude/bayctx/rules/index.yaml` - Rules catalog
3. `~/.claude/bayctx/skills/index.yaml` - Skills catalog
4. `~/.claude/bayctx/agents/index.yaml` - Agents catalog
5. `~/.claude/bayctx/plugins/index.yaml` - Plugins catalog

### Step 3.2: Navigator Template

**File**: `~/.claude/bayctx/CLAUDE.md` (auto-generated)

```markdown
# bctx Navigator

Auto-generated resource catalog for bctx-managed context. Last updated: {{TIMESTAMP}}

## Directory Index

Every directory below has an `index.yaml` — read it before loading files.

| Directory | What's Inside |
|-----------|---------------|
| `rules/` | Coding standards, API docs, design patterns |
| `skills/` | Task-specific capabilities for agents |
| `agents/` | Custom agent definitions and configurations |
| `plugins/` | MCP server configurations and plugins |

## Agent Instructions

1. **Read index.yaml first** - Each directory has metadata and entry summaries
2. **Load on demand** - Only read full files when relevant to current task
3. **Respect scope** - Global vs repo-specific context
4. **Context budget** - Prioritize based on relevance and recency

## Quick Access

- **List all rules**: Check `rules/index.yaml`
- **List all skills**: Check `skills/index.yaml`
- **List all agents**: Check `agents/index.yaml`
- **List all plugins**: Check `plugins/index.yaml`

## Configuration

- **Database**: `~/.claude/bayctx/bayctx.db`
- **Config**: `~/.claude/bayctx/config.yaml`
- **CLI**: Run `bctx` for status, `bctx files` to list all registrations

## Management

```bash
bctx add <name> <path>    # Register new context
bctx rm <name>            # Remove registration
bctx toggle <name>        # Enable/disable
bctx sync                 # Regenerate this navigator
```
```

### Step 3.3: Index Template for Type Catalogs

**File**: `~/.claude/bayctx/rules/index.yaml` (auto-generated)

```yaml
name: rules
description: Coding standards, API documentation, and design patterns
tags:
- rules
- coding-standards
- documentation
created: '{{TIMESTAMP}}'
last_modified: '{{TIMESTAMP}}'
entries:
  # Generated from database query:
  # SELECT name, path, scope, description FROM context_files WHERE type='rules' AND enabled=1
  {{ENTRY_ID}}:
    file: {{PATH}}
    title: {{NAME}}
    tags:
    - {{TYPE}}
    - {{CATEGORY}}
    summary: {{DESCRIPTION}}
    scope: {{SCOPE}}
    created: '{{CREATED}}'
    last_modified: '{{LAST_MODIFIED}}'
```

---

## Phase 4: Schema Validation

### Step 4.1: Validation Checklist

- [ ] All `index.yaml` files use `.yaml` extension (not `.yml`)
- [ ] Timestamps are ISO 8601 format with timezone
- [ ] Tags follow lowercase-with-hyphens convention
- [ ] Summaries are single-line, actionable descriptions
- [ ] related_entries use `store/entry-id` format
- [ ] File paths in entries{} are relative to store root

### Step 4.2: Validation Script

Create a validation tool:

```bash
#!/bin/bash
# validate-memory-store.sh

STORE_PATH="$1"

if [ ! -f "$STORE_PATH/index.yaml" ]; then
    echo "ERROR: No index.yaml found at $STORE_PATH"
    exit 1
fi

# Check for .yml (should be .yaml)
if find "$STORE_PATH" -name "*.yml" | grep -q .; then
    echo "WARNING: Found .yml files (should be .yaml)"
fi

# Validate YAML syntax
if ! python3 -c "import yaml; yaml.safe_load(open('$STORE_PATH/index.yaml'))" 2>/dev/null; then
    echo "ERROR: Invalid YAML syntax in index.yaml"
    exit 1
fi

# Check entry files exist
python3 << EOF
import yaml
with open('$STORE_PATH/index.yaml') as f:
    data = yaml.safe_load(f)
    for entry_id, entry in data.get('entries', {}).items():
        file_path = '$STORE_PATH/' + entry['file']
        if not __import__('os').path.exists(file_path):
            print(f"ERROR: Entry file not found: {file_path}")
            exit(1)
EOF

echo "✓ Store validation passed"
```

---

## Phase 5: Testing

### Step 5.1: Manual Testing

```bash
# 1. Create memory store
mkdir -p ~/.claude/memory/bay/entries

# 2. Create files (use templates above)
# ...

# 3. Validate structure
find ~/.claude/memory/bay -type f

# Expected output:
# ~/.claude/memory/bay/index.yaml
# ~/.claude/memory/bay/entries/overview.yaml

# 4. Test memory CLI
memory show bay

# Expected output: Display index.yaml content

memory get bay overview

# Expected output: Display full entry content

# 5. Test agent discovery
# Start Claude Code session and verify:
# - Global CLAUDE.md includes bay in memory table
# - Agent can discover bay memory store
# - Agent can read entry content
```

### Step 5.2: Integration Testing

```bash
# 1. Register test context file
echo "# Test Rule" > /tmp/test-rule.md
bctx add test-rule /tmp/test-rule.md --scope global --type rules

# 2. Sync navigator
bctx sync

# 3. Verify generation
ls ~/.claude/bayctx/
# Expected:
# CLAUDE.md
# rules/index.yaml
# skills/index.yaml
# agents/index.yaml
# plugins/index.yaml

# 4. Check navigator content
cat ~/.claude/bayctx/CLAUDE.md
cat ~/.claude/bayctx/rules/index.yaml

# 5. Test injection
bctx inject
# Should output test-rule.md content

# 6. Cleanup
bctx rm test-rule
rm /tmp/test-rule.md
```

---

## Phase 6: Documentation

### Step 6.1: Update Project README

Add section about memory integration:

```markdown
## Memory Integration

bctx integrates with the Claude Code memory system:

- **Memory store**: `~/.claude/memory/bay/` - Ecosystem overview
- **Navigator**: `~/.claude/bayctx/CLAUDE.md` - Auto-generated catalog
- **Indexes**: Type-specific catalogs (rules, skills, agents, plugins)

### For Agents

When working with bctx:
1. Check `~/.claude/memory/bay/index.yaml` for ecosystem overview
2. Read `~/.claude/bayctx/CLAUDE.md` for resource catalog
3. Load `{rules,skills,agents,plugins}/index.yaml` for specific resources

### For Developers

Memory stores provide persistent knowledge across sessions:
```bash
memory show bay           # View ecosystem overview
memory get bay overview   # Read full entry
```
```

### Step 6.2: Add to Installation Instructions

```markdown
## Post-Installation

After installing bctx:

1. **Create memory store** (optional but recommended):
   ```bash
   # Memory store provides persistent knowledge for Claude Code agents
   mkdir -p ~/.claude/memory/bay/entries
   # Copy templates from docs/memory-templates/
   ```

2. **Sync navigator**:
   ```bash
   bctx sync
   # Generates ~/.claude/bayctx/CLAUDE.md and index files
   ```

3. **Verify integration**:
   ```bash
   memory show bay
   cat ~/.claude/bayctx/CLAUDE.md
   ```
```

---

## Phase 7: Maintenance

### Step 7.1: Automated Sync

Add post-registration hook to auto-sync:

```go
// In internal/context/context.go

func (c *ContextManager) Add(...) error {
    // ... existing add logic ...

    // Auto-sync navigator after registration
    if err := c.SyncNavigator(); err != nil {
        // Log but don't fail - sync is best-effort
        log.Printf("Warning: Failed to sync navigator: %v", err)
    }

    return nil
}
```

### Step 7.2: Timestamp Management

Helper function for consistent timestamps:

```go
func nowISO8601() string {
    return time.Now().UTC().Format("2006-01-02T15:04:05.000000-07:00")
}
```

### Step 7.3: Index Rebuilding

Support rebuilding index from existing registrations:

```bash
bctx sync --rebuild
# Scans database and regenerates all index.yaml files
```

---

## Success Criteria

Integration is complete when:

- [ ] `~/.claude/memory/bay/` exists with index.yaml and overview.yaml
- [ ] Global `~/.claude/CLAUDE.md` includes bay in memory stores table
- [ ] `bctx sync` generates `~/.claude/bayctx/CLAUDE.md`
- [ ] Type-specific index.yaml files are auto-generated
- [ ] All schemas validate correctly
- [ ] Memory CLI can read bay store
- [ ] Claude Code agents can discover and use bay memory
- [ ] Navigator updates automatically on context changes

---

## Troubleshooting

### Issue: index.yaml validation fails

```bash
# Check YAML syntax
python3 -c "import yaml; print(yaml.safe_load(open('~/.claude/memory/bay/index.yaml')))"

# Common issues:
# - Using .yml instead of .yaml
# - Inconsistent indentation
# - Missing quotes around timestamps
```

### Issue: Navigator not generating

```bash
# Check bctx sync output
bctx sync -v

# Verify database connectivity
sqlite3 ~/.claude/bayctx/bayctx.db "SELECT COUNT(*) FROM context_files;"

# Check directory permissions
ls -la ~/.claude/bayctx/
```

### Issue: Memory CLI can't find store

```bash
# Check store location
ls ~/.claude/memory/bay/

# Verify index.md includes bay
grep "bay" ~/.claude/memory/index.md

# Test directly
memory list
```

---

This implementation guide provides concrete steps, templates, and validation tools for integrating bctx with the Claude Code memory system following the established patterns from the work laptop.
