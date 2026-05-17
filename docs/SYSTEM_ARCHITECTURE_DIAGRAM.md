# Bay System Architecture Diagram

Visual representation of the complete Bay ecosystem structure extracted from work laptop screenshots.

---

## Complete System Structure

```
~/.claude/
├── CLAUDE.md                           # Global navigation hub
├── conventions.md                      # Dev environment patterns
├── ctxin.md                           # ctxin orchestration docs
│
├── memory/                            # Memory store system
│   ├── index.md                       # Memory system docs, schemas, CLI
│   ├── lib/                          # Python library
│   │   ├── memory_store.py           # Core API
│   │   ├── agent_helpers.py          # Agent utilities
│   │   └── memory_cli.py             # CLI implementation
│   ├── bin/
│   │   └── rebuild-index.sh          # Maintenance scripts
│   │
│   ├── bay/                          # Bay ecosystem store
│   │   ├── index.yaml                # Bay metadata
│   │   └── entries/
│   │       └── overview.yaml         # Combined bay-tui + bctx overview
│   │
│   ├── bay-tui/                      # Session manager store
│   │   ├── index.yaml                # Store metadata
│   │   └── entries/
│   │       └── overview.yaml         # Architecture, workflows, use cases
│   │
│   ├── bctx/                         # Context manager store
│   │   ├── index.yaml                # Store metadata
│   │   └── entries/
│   │       └── overview.yaml         # Architecture, workflows, use cases
│   │
│   └── [other-projects]/            # Other project stores
│       ├── index.yaml
│       └── entries/*.yaml
│
├── commands/                          # Custom slash commands
│   ├── index.md                      # Command documentation
│   └── [command-files]
│
├── plugins/local/                     # Custom local plugins
│   └── index.yaml                    # Plugin directory index
│
├── agents/                           # Custom agent definitions
│   └── index.yaml                    # Agent directory index
│
└── rules/                            # Rule files
    └── index.yaml                    # Rules directory index
```

---

## Bay Ecosystem Detail

```
Bay Ecosystem
├── bay-tui (Terminal Session Manager)
│   ├── Purpose: Multi-repo workspace orchestration
│   ├── Runtime: tmux windows + Bubbletea TUI
│   ├── Storage: YAML sessions + SQLite memory
│   └── Features:
│       ├── Session management
│       ├── 3-layer memory (episodic, working, tasks)
│       ├── Git worktree management
│       └── Agent context injection
│
└── bctx (Context Manager)
    ├── Purpose: Claude Code context injection
    ├── Runtime: CLI + SQLite database
    ├── Storage: SQLite + referenced markdown files
    └── Features:
        ├── Rule registration (global/repo-scoped)
        ├── SessionStart hook integration
        ├── Navigator generation (CLAUDE.md + index.yaml)
        └── Context budget management
```

---

## Memory Store Pattern

```
Memory Store (<project>/)
│
├── index.yaml ──────────────────┐
│   ├── name                     │  Quick metadata
│   ├── description              │  Tags for discovery
│   ├── tags[]                   │  Entry summaries
│   └── entries{}                │
│       └── <id>                 │
│           ├── file ────────────┼───> entries/<id>.yaml
│           ├── title            │
│           ├── tags[]           │
│           ├── summary          │  One-line description
│           ├── created          │
│           └── last_modified    │
│                                │
└── entries/ ────────────────────┘
    └── <id>.yaml
        ├── id
        ├── title
        ├── tags[]
        ├── created
        ├── last_modified
        ├── related_entries[]  ───> Cross-store references
        └── content (markdown)
            ├── Overview
            ├── Architecture
            ├── Tech Stack
            ├── Key Design Decisions
            ├── Data Paths
            ├── Commands/API
            ├── Use Cases
            └── Improvement Plan
```

---

## Agent Discovery Flow

```
Agent starts working
        │
        ├─> Reads ~/.claude/CLAUDE.md (navigation hub)
        │       │
        │       ├─> memory/index.md          (memory system overview)
        │       ├─> commands/index.md        (custom commands)
        │       ├─> conventions.md           (dev patterns)
        │       └─> ctxin.md                 (context orchestration)
        │
        ├─> Checks project directory
        │       │
        │       └─> Reads CLAUDE.md (project-specific rules)
        │
        ├─> Memory Discovery (if relevant)
        │       │
        │       ├─> ~/.claude/memory/index.md
        │       │       └─> Find relevant stores by tags
        │       │
        │       ├─> Read <store>/index.yaml
        │       │       └─> Scan entry summaries
        │       │
        │       └─> Load entries/<id>.yaml (on demand)
        │               └─> Get full context
        │
        └─> Directory-specific indexes
                │
                ├─> plugins/local/index.yaml
                ├─> commands/index.yaml
                ├─> agents/index.yaml
                └─> rules/index.yaml
```

---

## bctx Context Injection Flow

```
Claude Code Session Starts
        │
        └─> SessionStart Hook
                │
                └─> bctx inject
                        │
                        ├─> Detect current git repo
                        │
                        ├─> Query SQLite database
                        │   WHERE enabled=1
                        │   AND (scope='global' OR scope='repo:<name>')
                        │
                        ├─> Read markdown content from disk
                        │   └─> Respect context budget
                        │
                        └─> Output to stdout
                                │
                                └─> Claude receives context
                                        │
                                        ├─> Global rules (always)
                                        ├─> Project-specific rules
                                        ├─> Skills
                                        ├─> Agents
                                        └─> Plugins
```

---

## bctx Navigator Generation

```
bctx sync command
        │
        ├─> Query all registered context files
        │       │
        │       └─> Group by type: rules, skills, agents, plugins
        │
        ├─> Generate ~/.claude/bayctx/CLAUDE.md
        │       │
        │       └─> Navigation table:
        │           | Directory | What's Inside |
        │           |-----------|---------------|
        │           | rules/    | Coding standards... |
        │           | skills/   | Task capabilities... |
        │           | agents/   | Agent definitions... |
        │           | plugins/  | MCP servers... |
        │
        └─> Generate type-specific index.yaml files
                │
                ├─> ~/.claude/bayctx/rules/index.yaml
                ├─> ~/.claude/bayctx/skills/index.yaml
                ├─> ~/.claude/bayctx/agents/index.yaml
                └─> ~/.claude/bayctx/plugins/index.yaml
```

---

## Memory Store Content Structure

```
entries/overview.yaml
│
└─> content: |
      ## Overview
      ├─ One-paragraph purpose
      └─ Target users

      ## Architecture
      ├─ ASCII tree diagram
      └─ Component descriptions

      ## Tech Stack
      ├─ Language/version
      ├─ Key dependencies
      └─ Build tools

      ## Key Design Decisions
      ├─ Decision 1: Rationale
      ├─ Decision 2: Rationale
      └─ Decision N: Rationale

      ## Data Paths
      ├─ Config locations
      ├─ Database paths
      └─ Storage directories

      ## Commands/API
      └─ Table of commands

      ## Use Cases
      ├─ Scenario 1
      ├─ Scenario 2
      └─ Scenario N

      ## Improvement Plan
      ├─ High Priority
      ├─ Medium Priority
      └─ Lower Priority
```

---

## Index.yaml Reading Pattern

```
Agent Task
    │
    └─> Check if directory has index.yaml
            │
            ├─> YES: Read index.yaml first
            │       │
            │       ├─> Scan entries{} for relevant topics
            │       │   └─> Use summary for quick filtering
            │       │
            │       └─> Load specific entry files on demand
            │           └─> entries/<id>.yaml
            │
            └─> NO: Proceed with direct file access
```

---

## Cross-Store References

```
bay/entries/overview.yaml
    │
    ├─> related_entries:
    │   ├─ bay-tui/overview ─────┐
    │   └─ bctx/overview ────┐   │
    │                         │   │
    │                         │   └─> bay-tui/entries/overview.yaml
    │                         │           └─> Architecture, memory system
    │                         │
    │                         └─> bctx/entries/overview.yaml
    │                                 └─> Context injection, hooks
    │
    └─> Agents follow references
        to build comprehensive understanding
```

---

## Tag-Based Discovery

```
Memory Stores Tagged By:
│
├─ Store-Level Tags
│   ├─ project              (all project stores)
│   ├─ <language>          (go, python, typescript)
│   ├─ <primary-tool>      (tmux, sqlite, flask)
│   └─ <pattern>           (context-injection, session-manager)
│
└─ Entry-Level Tags
    ├─ architecture        (system structure)
    ├─ workflows           (common procedures)
    ├─ usecases            (examples)
    ├─ improvement         (future plans)
    └─ troubleshooting     (known issues)

Agent Query:
    tags=['go', 'sqlite'] ──> Returns bay-tui, bctx stores
    tags=['architecture'] ──> Returns all overview entries
    tags=['workflows']    ──> Returns workflow entries
```

---

## Context Budget Management

```
bctx inject
    │
    ├─> Query enabled rules
    │
    ├─> Read content from disk
    │
    ├─> Calculate total size
    │
    └─> If over budget:
            │
            ├─> Prioritize by:
            │   ├─ Scope (repo-specific > global)
            │   ├─ Recency (newer > older)
            │   └─ Type (rules > skills > plugins)
            │
            └─> Truncate lowest priority
                └─> Always respect context_budget setting
```

---

## Data Flow: bay-tui + bctx Integration

```
Developer Workflow
        │
        ├─> Launch bay-tui
        │       ├─> Creates tmux session
        │       ├─> Loads SQLite memory
        │       ├─> Displays TUI (topbar + panes)
        │       └─> Tracks episodic events
        │
        ├─> Start Claude Code in session
        │       │
        │       └─> SessionStart Hook
        │               │
        │               └─> bctx inject
        │                       │
        │                       ├─> Detects repo from bay session
        │                       ├─> Injects repo-specific rules
        │                       └─> Injects global rules
        │
        ├─> Work on code
        │       │
        │       ├─> bay-tui captures:
        │       │   ├─ Terminal snapshots
        │       │   ├─ Git commits
        │       │   └─ Session events
        │       │
        │       └─> bctx provides:
        │           ├─ Coding standards
        │           ├─ API documentation
        │           └─ Project context
        │
        └─> Context persists
                │
                ├─> bay-tui memory: SQLite (episodic, working, tasks)
                └─> bctx rules: SQLite + referenced markdown files
```

---

## File Organization Conventions

```
Directory Naming:
    ├─ lowercase-with-hyphens    (bay-tui, lasso-proxy)
    └─ single-word preferred     (bctx, edgedyv)

File Extensions:
    ├─ index.yaml (always .yaml, never .yml)
    ├─ CLAUDE.md (always uppercase)
    └─ entries/*.yaml (always .yaml)

Timestamp Format:
    └─ ISO 8601: '2026-03-23T00:00:00.000000+00:00'

Summary Format:
    └─ <Tool> <action> - <key features>
       Example: "Go CLI context manager - SQLite storage, hook injection"
```

---

## System Integration Summary

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Code Session                       │
│                                                              │
│  ┌────────────┐         ┌──────────────┐                   │
│  │  Global    │         │   Project    │                   │
│  │ CLAUDE.md  │────────>│  CLAUDE.md   │                   │
│  └────────────┘         └──────────────┘                   │
│         │                       │                            │
│         v                       v                            │
│  ┌─────────────────────────────────────────┐                │
│  │    Memory Store System                   │                │
│  │    ~/.claude/memory/                     │                │
│  │                                          │                │
│  │  ├─ bay/         (ecosystem overview)   │                │
│  │  ├─ bay-tui/     (session manager)      │                │
│  │  ├─ bctx/        (context manager)      │                │
│  │  └─ [projects]/  (other stores)         │                │
│  └─────────────────────────────────────────┘                │
│         │                       │                            │
│         v                       v                            │
│  ┌────────────┐         ┌──────────────┐                   │
│  │  bctx      │         │   bay-tui    │                   │
│  │  inject    │         │   memory     │                   │
│  │  (rules)   │         │  (context)   │                   │
│  └────────────┘         └──────────────┘                   │
│         │                       │                            │
│         └───────────┬───────────┘                            │
│                     v                                        │
│            ┌─────────────────┐                              │
│            │  Agent Context  │                              │
│            │  - Rules        │                              │
│            │  - Memory       │                              │
│            │  - Tasks        │                              │
│            │  - Project docs │                              │
│            └─────────────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Next Steps for bctx Implementation

1. **Create Memory Store**
   ```bash
   mkdir -p ~/.claude/memory/bay/entries
   # Create index.yaml
   # Create entries/overview.yaml
   ```

2. **Update Global CLAUDE.md**
   ```bash
   # Add bay to memory stores table if missing
   # Verify navigation structure
   ```

3. **Implement Navigator Generation**
   ```bash
   # bctx sync should generate:
   # - ~/.claude/bayctx/CLAUDE.md
   # - ~/.claude/bayctx/rules/index.yaml
   # - ~/.claude/bayctx/skills/index.yaml
   # - ~/.claude/bayctx/agents/index.yaml
   # - ~/.claude/bayctx/plugins/index.yaml
   ```

4. **Validate Schema Compliance**
   ```bash
   # All index.yaml files match schema
   # All entry files match schema
   # Timestamps are ISO 8601
   # Tags follow conventions
   ```

---

This diagram shows the complete system architecture extracted from the work laptop screenshots, providing a blueprint for implementing the memory integration in bctx.
