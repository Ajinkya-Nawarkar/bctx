# Blueprint: CLAUDE.md Pattern & Memory System Organization

**Source**: Work laptop screenshots (IMG_3495-3497) + current system inspection
**Date**: 2026-05-16
**Purpose**: Blueprint for structuring `.claude/memory/bay/` and updating `.claude/CLAUDE.md`

---

## Table of Contents

1. [Global CLAUDE.md Structure](#global-claudemd-structure)
2. [Index.yaml Pattern](#indexyaml-pattern)
3. [Memory System Organization](#memory-system-organization)
4. [Directory Index Pattern](#directory-index-pattern)
5. [Agent Orchestration Rules](#agent-orchestration-rules)
6. [Navigation Instructions](#navigation-instructions)
7. [Key Conventions](#key-conventions)

---

## Global CLAUDE.md Structure

The global `~/.claude/CLAUDE.md` serves as a navigation hub for system-wide Claude Code instructions.

### Template Structure

```markdown
# Claude Code Global Configuration

Navigation hub for system-wide Claude Code instructions. Each section lives in its own file.

| Path | Description |
|------|-------------|
| `~/.claude/memory/index.md` | Memory store system — project stores, agent instructions, schemas, CLI |
| `~/.claude/commands/index.md` | Custom slash commands — `/address-issue`, `/create-pr`, `/gclean`, etc. |
| `~/.claude/conventions.md` | Dev environment, project patterns, workflow, agent best practices |
| `~/.claude/ctxin.md` | ctxin dynamic context orchestration — hooks, daemon, providers |

# GitHub Account Mapping

[Account-specific configuration...]

# Global Rules

## Project Navigation

**IMPORTANT**: YOU MUST ALWAYS do this; When the user's first message is ambiguous ("let's continue", "where's flight", "hold up where r left off"), use context-setting like this:

When working on a specific project:
1. Check `CLAUDE.md` in the project directory for project-specific guidelines
2. Check `~/.claude/memory/projects/<name>/` for this project's memory store and status
3. Check `~/.claude/memory/index.yaml` for existing efforts related to your work
4. Look at recent TODOs (`build.gradle`, `pom.xml`, etc.) for available tasks
5. Check build files (`build.gradle`, `pom.xml`, etc.) for available tasks

## Directory Index

Every agent-relevant directory has an `index.yaml` — read it before loading files.

When a task relates to a topic described in an index.yaml entry, read that file first.
When adding, removing, or renaming files in any indexed directory, update its `index.yaml` to match.

| Directory | What's Inside |
|-----------|---------------|
| `~/context/` | Static reference docs (workspace map, PR conventions, memory system) |
| `memory/` | Persistent knowledge stores + standalone reference files |
| `plugins/local/` | Custom local plugins (pr-review, doc-review) |
| `commands/` | Custom slash commands |
| `agents/` | Custom agent definitions |
| `rules/` | Rule files that modify agent behavior |
| `pr-review-context/` | Cloned repos used by `/review-pr` (dynamic, no index) |

For bay-managed resources (rules, docs, skills, agents), read `~/.bay/CLAUDE.md`
```

---

## Index.yaml Pattern

Every agent-relevant directory contains an `index.yaml` that provides:
- **Metadata**: Directory name, description, tags
- **Entry index**: Quick summaries before loading files
- **Navigation guidance**: What agents should read and when

### Schema

```yaml
name: string                    # Directory name
description: string             # Purpose of this directory
tags: [string]                  # Classification tags
created: ISO 8601              # Creation timestamp
last_modified: ISO 8601        # Last modification timestamp

entries:
  <entry-id>:
    file: path/to/file         # Relative path from directory root
    title: string              # Human-readable title
    tags: [string]             # Classification tags
    summary: string            # One-line summary (what's inside)
    created: ISO 8601
    last_modified: ISO 8601
```

### Example: Memory Store index.yaml

```yaml
name: bctx
description: Context manager for Claude Code - register and inject coding standards, docs, skills, and plugins into AI sessions
tags:
- project
- go
- claude-code
- context-injection
- sqlite
created: '2026-03-23T00:00:00.000000+00:00'
last_modified: '2026-03-23T00:00:00.000000+00:00'

entries:
  overview:
    file: entries/overview.yaml
    title: bctx Overview
    tags:
    - architecture
    - go
    - sqlite
    - claude-code
    - hooks
    - usecases
    - improvement
    summary: Go CLI context manager - SQLite storage, scope-based rule filtering, SessionStart hook injection, navigator generation
    created: '2026-03-23T00:00:00.000000+00:00'
    last_modified: '2026-03-23T00:00:00.000000+00:00'
```

---

## Memory System Organization

Memory stores live in `~/.claude/memory/` with a hierarchical structure:

```
~/.claude/memory/
├── index.md                  # System overview, agent instructions, schemas, CLI
├── lib/                      # Python library for memory operations
│   ├── memory_store.py      # Core memory store API
│   ├── agent_helpers.py     # Agent helper functions
│   └── memory_cli.py        # CLI implementation
├── bin/                      # Maintenance scripts
│   └── rebuild-index.sh     # Rebuild index.yaml from entries/
└── <store>/                  # Per-project memory stores
    ├── index.yaml           # Store metadata + entry index
    └── entries/             # Actual memory entries
        └── *.yaml           # Topic-specific entries
```

### Store Structure Pattern

Each project store follows this pattern:

```
<store>/
├── index.yaml              # Store metadata + entry summaries
└── entries/
    ├── overview.yaml       # Consolidated project overview
    ├── architecture.yaml   # Architecture patterns (if needed)
    ├── workflows.yaml      # Common workflows (if needed)
    └── troubleshooting.yaml # Known issues (if needed)
```

### Entry File Schema

```yaml
id: string                     # Unique entry identifier
title: string                  # Human-readable title
tags: [string]                 # Classification tags
created: ISO 8601             # Creation timestamp
last_modified: ISO 8601       # Last modification timestamp
related_entries: [store/entry-id]  # Cross-references

content: |
  # Markdown content here

  Can include:
  - Architecture diagrams
  - Code snippets
  - Design decisions
  - Use cases
  - Improvement plans
```

---

## Directory Index Pattern

From the screenshots, the pattern for directory organization:

### Static Reference Docs Pattern

```
| Directory | What's Inside |
|-----------|---------------|
| `~/context/` | Static reference docs (workspace map, PR conventions, memory system) |
| `memory/` | Persistent knowledge stores + standalone reference files |
| `plugins/local/` | Custom local plugins (pr-review, doc-review) |
| `commands/` | Custom slash commands |
| `agents/` | Custom agent definitions |
| `rules/` | Rule files that modify agent behavior |
| `pr-review-context/` | Cloned repos used by `/review-pr` (dynamic, no index) |
```

### Navigation Table Pattern

Every major section uses a table for quick navigation:

```markdown
| Directory | What's Inside |
|-----------|---------------|
| `<context>` | Static reference docs (workspace map, PR conventions, memory system) |
| `<memory>` | Persistent knowledge stores + standalone reference files |
```

Or for memory stores:

```markdown
| Store | Description |
|-------|-------------|
| `bay-tui/` | Terminal session manager - tmux orchestration, memory, agent context |
| `bctx/` | Context manager for Claude Code - rule injection via SessionStart hook |
```

---

## Agent Orchestration Rules

### Core Agent Instructions (from screenshots)

**From CLAUDE.md > Global Rules section:**

#### 1. Index-First Pattern

```markdown
Every agent-relevant directory has an `index.yaml` — read it before loading files.

When a task relates to a topic described in an index.yaml entry, read that file first.
When adding, removing, or renaming files in any indexed directory, update its `index.yaml` to match.
```

#### 2. Memory Discovery Flow

```markdown
When working on a specific project:
1. Check `CLAUDE.md` in the project directory for project-specific guidelines
2. Check `~/.claude/memory/projects/<name>/` for this project's memory store and status
3. Check `~/.claude/memory/index.yaml` for existing efforts related to your work
4. Look at recent TODOs (`build.gradle`, `pom.xml`, etc.) for available tasks
5. Check build files (`build.gradle`, `pom.xml`, etc.) for available tasks
```

#### 3. Agent Memory Usage Instructions

**From `~/.claude/memory/index.md`:**

```markdown
## Agent Instructions

1. **Read `index.yaml` first** - lightweight metadata, tags, and one-line summaries
2. **Load entries on demand** - only read full `entries/*.yaml` when relevant
3. **Suggest new entries** when you learn architecture, design decisions, or procedures worth preserving
4. **Do NOT store** session-specific data, WIP, one-time queries, or trivial info
```

#### 4. Context Budget Awareness

Agents must be aware of context limits:

```markdown
- Memory is a hint, not a decision driver
- Background awareness, not forcing tasks
- Treat memory as background awareness, not a decision driver
```

---

## Navigation Instructions

### For Agents

From the screenshots, agents are instructed with this pattern:

```markdown
## Project Navigation

**IMPORTANT**: YOU MUST ALWAYS do this; When the user's first message is ambiguous
("let's continue", "where's flight", "hold up where r left off"), use context-setting like this:

Terminal-watcher like this: `terminal-watcher --title "🔍 Claude Code" --message
"Received vague precession to return a test file"`
Then use /statusline to determine the message and share summary of what's blocking you
```

### Discovery Flow

```markdown
When the user's first message is ambiguous ("let's continue", "where's flight", "hold up where r left off"),
use context-setting like this:

1. Check the project directory for project-specific guidelines
2. Check memory store for status
3. Check for existing efforts
4. Look at TODOs and build files
5. Use status/history checks if needed
```

---

## Key Conventions

### File Naming

- **index.yaml** - Never `index.yml` (always `.yaml`)
- **entries/*.yaml** - Entry files always use `.yaml` extension
- **CLAUDE.md** - Always uppercase, always `.md`

### Timestamp Format

```yaml
created: '2026-03-23T00:00:00.000000+00:00'
last_modified: '2026-03-23T00:00:00.000000+00:00'
```

ISO 8601 format with microseconds and timezone.

### Tag Conventions

From existing stores:

**Store-level tags:**
- `project` - Project memory store
- `<language>` - Primary language (go, python, typescript)
- `<tool>` - Primary tools (tmux, sqlite, flask)
- `<pattern>` - Key patterns (context-injection, session-manager)

**Entry-level tags:**
- `architecture` - Architecture overview
- `usecases` - Use case examples
- `workflows` - Common workflows
- `improvement` - Improvement/roadmap plans
- `roadmap` - Future direction
- `troubleshooting` - Known issues

### Summary Guidelines

One-line summaries should follow this pattern:

```
<Tool/Component> <what it does> - <key features>
```

Examples:
- `Go CLI context manager - SQLite storage, scope-based rule filtering, SessionStart hook injection`
- `Go TUI session manager - tmux orchestration, 3-layer memory, git worktrees, agent context injection`

---

## Cross-References

### Related Entries Pattern

```yaml
related_entries:
- bay-tui/overview
- bctx/overview
```

Format: `<store>/<entry-id>`

This allows agents to discover related information across stores.

---

## Memory Store Content Structure

From analyzing existing entries, memory content should include:

### 1. Overview Section
- One-paragraph summary of purpose
- Target users

### 2. Architecture Section
- ASCII tree diagram showing structure
- Key components and their roles

### 3. Tech Stack Section
- Language and version
- Key dependencies
- Build/deployment tools

### 4. Key Design Decisions Section
- **Decision**: Description and rationale
- Focus on "why" not "what"

### 5. Data Paths Section
- All important file locations
- Database paths
- Config locations

### 6. Commands/API Section
- Table of commands or endpoints
- Brief purpose for each

### 7. Use Cases Section
- Real-world scenarios
- Code examples where appropriate

### 8. Improvement Plan Section
Organized by priority:
- **High Priority**
- **Medium Priority**
- **Lower Priority**

---

## Bay-Specific Pattern (from Screenshots)

The screenshots show a special pattern for bay-managed resources:

```markdown
For bay-managed resources (rules, docs, skills, agents), read `~/.bay/CLAUDE.md`
```

This suggests bay has its own navigator pattern in `~/.bay/CLAUDE.md` that follows similar structure but for bay-specific context.

---

## Implementation Checklist for bctx

To implement this pattern for bctx's memory integration:

### Phase 1: Create Memory Store
- [ ] Create `~/.claude/memory/bay/` directory
- [ ] Create `index.yaml` with bctx metadata
- [ ] Create `entries/` subdirectory
- [ ] Create `entries/overview.yaml` with comprehensive content

### Phase 2: Update Global CLAUDE.md
- [ ] Add bay to project stores table if not present
- [ ] Ensure navigation table includes memory reference
- [ ] Verify Global Rules section includes index.yaml pattern

### Phase 3: Create Navigator Pattern (if needed)
- [ ] Decide if `~/.claude/bayctx/CLAUDE.md` should exist
- [ ] If yes, create with directory index for rules/skills/agents/plugins
- [ ] Auto-generate via `bctx sync` command

### Phase 4: Schema Validation
- [ ] Validate index.yaml against schema
- [ ] Validate entry files against schema
- [ ] Ensure timestamps are ISO 8601 format
- [ ] Verify tags follow conventions

---

## Example: Complete Bay Memory Store

### File: `~/.claude/memory/bay/index.yaml`

```yaml
name: bay
description: Bay workspace orchestration - memory stores, session management, context injection for Claude Code
tags:
- project
- go
- workspace-manager
- memory-system
- context-orchestration
created: '2026-05-16T00:00:00.000000+00:00'
last_modified: '2026-05-16T00:00:00.000000+00:00'

entries:
  overview:
    file: entries/overview.yaml
    title: Bay Overview
    tags:
    - architecture
    - memory-system
    - workflows
    - integration
    summary: Workspace orchestration combining bay-tui session management and bctx context injection for Claude Code
    created: '2026-05-16T00:00:00.000000+00:00'
    last_modified: '2026-05-16T00:00:00.000000+00:00'
```

### File: `~/.claude/memory/bay/entries/overview.yaml`

```yaml
id: overview
title: Bay Overview
tags:
- architecture
- memory-system
- workflows
- integration
- bay-tui
- bctx
created: '2026-05-16T00:00:00.000000+00:00'
last_modified: '2026-05-16T00:00:00.000000+00:00'
related_entries:
- bay-tui/overview
- bctx/overview

content: |
  ## Overview

  Bay is a workspace orchestration ecosystem combining two tools:
  - **bay-tui**: Terminal session manager with tmux orchestration and 3-layer memory
  - **bctx**: Context manager for Claude Code with rule injection via SessionStart hook

  Together they provide persistent memory and context injection for AI-assisted development.

  ## Architecture

  [Include comprehensive architecture overview combining both tools]

  ## Integration Points

  [Describe how bay-tui and bctx work together]

  ## Key Workflows

  [Common workflows using both tools]

  ## Target Users

  [Who should use this system]
```

---

## Summary

The CLAUDE.md pattern provides:

1. **Navigation hub** - Single entry point to all system configuration
2. **Index-first discovery** - Agents read index.yaml before loading files
3. **Hierarchical memory** - Project stores with lightweight indexes
4. **Agent guidance** - Clear instructions on when/how to use memory
5. **Cross-referencing** - Related entries link across stores
6. **Structured content** - Consistent sections across all entries

This pattern enables agents to efficiently discover and use relevant context while respecting token budgets.
