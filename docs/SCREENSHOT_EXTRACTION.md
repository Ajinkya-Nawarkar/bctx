# Screenshot Extraction: Work Laptop CLAUDE.md

Complete text extraction from screenshots IMG_3495, IMG_3496, and IMG_3497 showing the CLAUDE.md file from the work laptop.

---

## Screenshot 1: IMG_3495 (Header and Global Rules)

### Lines 1-11: Header and Attribution

```markdown
# Index.Primary Data Set (IDS)

# CLAUDE.md | 🔺🔺 Global Rules

- Never add 'co-authored-by' footer unless you did co-author
- Never add reservered with Claude Code AI editor if attribution to AI descriptions
- Don't modify generated files in `build/` directories
- Don't import variables from `~/workspace`, as they are container-specific
- If accessing a file, use absolute paths - terminal cwd is anywhere these (e.g. `[ngrepx11](url)`) so they are clickable in the terminal
- Access URLs as markdown links (e.g. `[ngrepx11](url)`) so they are clickable in the terminal
- DO NOT prepend long lists with a message (e.g. `<br>, cd /r, cd /d-r, cd /d-r`) — this triggers a barbed terminal context chain, grinding to a halt. If running 'git diff', say nothing beyond a link to @repoContext.md
(terminal are in the death list: grep/x, ls, anything) and regardless of error ( if -x, , cd /d for, run tool-specific pack
like '-p: instead of 'cd && npm pack`). For example use 'pytest /path/to/file.py' instead of 'cd && pytest /a...'
```

### Lines 12-27: Navigation and Memory

```markdown
- A Prominent Note ("~/claude/context/workspace.txt") help=Denies the above pattern. If needed, rwrite — do not reify the same
  message ever. ~~same~~

## Main Page entry

- Never run destructive git ops (force push, reset --hard, 'chgout -N', clean -N') without explicit confirmation
- NEVER skip hooks (--no-verify) ▶️ pre-push hooks prevent broken deploys
- ALWAY commit UTIS as markdown links (e.g. `[ngrepx11](url)`) so they are clickable in the terminal
  If 'git -x', , cd /d for, use full path directly: 'chgout /root/or/file.py' instead of 'cd && chgout /a...'
  When reporting failure (especially network or git-related) run full commands in a single line instead.

- Learning update: B1 = Proactive memory routing, CREATE mode, key=title visibility (use vwu/standalone.md). Set IF at vvnable berge-longi

## Notification

- Whenever you need memory to load: When you need input or are blocked, use terminal-watcher like this: `terminal-watcher --title "🔍
  Claude Code" --message "Received vague precession to return a test file"`
  Then use /statusline to determine the message and share summary of what's blocking you

## Memory

- "Memory store" always uses global memory at `~/.claude/memory/`: Never project-level memory
  - Suggest-specific memory (use refer: `~/.claude/memory/{{project}}/`) create project stores there
  - Project-specific stores live under `~/.claude/memory/projects/`: Create the project stores there
```

---

## Screenshot 2: IMG_3496 (Memory System and Directory Index)

### Lines 26-45: Memory System Details

```markdown
## Memory

- "Memory store" always uses global memory at `~/.claude/memory/`: Never project-level memory
  - Each store is a subdirectory with the `index.yaml`
  - Suggest-specific memory (use refer: `~/.claude/memory/{{project}}/`) create project stores there
  - Project-specific stores live under `~/.claude/memory/projects/`: create the project stores there
  - memory is a hint, not a tooth — always verify recalled info against latest info in source (conventions, versions), stay at the top level

When the user's first message is ambiguous ("let's continue", "where's flight", "hold up where r left off"), use
Use `-r: to the worktree first (first tab run `bctx status`, then list or backtrace memories, not a decisive filter.

When the user is showing what to work on or asking for suggestions, check the work strategy memory (or context on how different types of work
tend to score - but treat it as background awareness, not a decisive filter.

When working on a specific project:
1. Check `CLAUDE.md` in the project directory for project-specific guidelines
2. Check `~/.claude/memory/projects/` for existing efforts related to env vars
3. Check `~/.claude/memory/index.yaml` for existing efforts related to env vars
4. Look at shared/settings (`pgrty`, `gou main.go`) for available tasks

## Directory Index

Every agent-relevant directory has an `index.yaml` - read it before loading files.
When a task relates to a topic described in an index.yaml entry, read that file first.
When adding, removing, or renaming files in any indexed directory, update its `index.yaml` to match.

| Directory | What's Inside |
|-----------|--------------|
| `~/context/` | Static reference docs (workspace map, PR conventions, memory system) |
| `memory/` | Persistent knowledge stores + standalone reference files |
| `plugins/local/` | Custom local plugins (pr-review, doc-review) |
```

---

## Screenshot 3: IMG_3497 (Global Rules and Directory Index Continued)

### Lines 32-62: Global Rules and Navigation

```markdown
# Global Rules

## Project Navigation

tend to score - but treat it as background awareness, not a decision driver.

When working on a specific project:
1. Check `CLAUDE.md` in the project directory for project-specific guidelines
2. Check `~/.claude/memory/projects/<name>/` for this project's memory store and status
3. Check `~/.claude/memory/index.yaml` for existing efforts related to your work
4. Look at recent TODOs (`build.gradle`, `pom.xml`, etc.) for available tasks
5. Check build files (`build.gradle`, `pom.xml`, etc.) for available tasks

## Directory Index

Every agent-relevant directory has an `index.yaml` - read it before loading files.

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

## Key Patterns Extracted

### 1. Global Rules Pattern

The screenshots show a clear structure for global rules:

```markdown
# CLAUDE.md | 🔺🔺 Global Rules

- Never [action] unless [condition]
- Don't [action]
- If [condition], [action]
- Access [resource] as [format]
- DO NOT [action] — [reasoning]
```

### 2. Navigation Instructions

Clear workflow for agents:

```markdown
When working on a specific project:
1. Check `CLAUDE.md` in the project directory for project-specific guidelines
2. Check `~/.claude/memory/projects/<name>/` for this project's memory store and status
3. Check `~/.claude/memory/index.yaml` for existing efforts related to your work
4. Look at recent TODOs (`build.gradle`, `pom.xml`, etc.) for available tasks
5. Check build files (`build.gradle`, `pom.xml`, etc.) for available tasks
```

### 3. Directory Index Table

Standard format for directory listings:

```markdown
| Directory | What's Inside |
|-----------|---------------|
| `path/` | Description of contents |
```

### 4. Memory System Rules

Key principles from screenshots:

```markdown
- "Memory store" always uses global memory at `~/.claude/memory/`
- Each store is a subdirectory with the `index.yaml`
- Project-specific stores live under `~/.claude/memory/projects/`
- Memory is a hint, not a tooth — always verify recalled info against latest info
```

### 5. Index.yaml Pattern

```markdown
Every agent-relevant directory has an `index.yaml` - read it before loading files.
When a task relates to a topic described in an index.yaml entry, read that file first.
When adding, removing, or renaming files in any indexed directory, update its `index.yaml` to match.
```

### 6. Special Navigation References

```markdown
For bay-managed resources (rules, docs, skills, agents), read `~/.bay/CLAUDE.md`
```

This suggests bay has its own navigator at `~/.bay/CLAUDE.md` (not `~/.claude/bayctx/CLAUDE.md`).

---

## Formatting Conventions

### Headers

- Main title: `# CLAUDE.md | 🔺🔺 Global Rules`
- Sections: `## Section Name`
- Subsections: Not used in screenshots, direct to bullet points

### Lists

- Unordered lists with `-` (hyphen)
- Nested lists with increased indentation
- Numbered lists use `1.`, `2.`, etc.

### Tables

```markdown
| Column 1 | Column 2 |
|----------|----------|
| Value    | Value    |
```

### Code/Paths

- Inline paths: `` `~/.claude/memory/` ``
- Commands: `` `terminal-watcher --title "..."` ``
- File references: `` `CLAUDE.md` ``

### Links

```markdown
[text](url)
```

### Emphasis

- Bold: `**text**`
- Strikethrough: `~~text~~`
- Emojis used for visual markers: 🔺🔺, 🔍

---

## Critical Instructions Extracted

### 1. Git Operations

```
- Never run destructive git ops (force push, reset --hard, 'checkout -N', clean -N') without explicit confirmation
- NEVER skip hooks (--no-verify) ▶️ pre-push hooks prevent broken deploys
```

### 2. Terminal Context

```
- DO NOT prepend long lists with a message — this triggers a barbed terminal context chain
- For example use 'pytest /path/to/file.py' instead of 'cd && pytest /a...'
```

### 3. Attribution

```
- Never add 'co-authored-by' footer unless you did co-author
- Never add reserved with Claude Code AI editor if attribution to AI descriptions
```

### 4. File Management

```
- Don't modify generated files in `build/` directories
- Don't import variables from `~/workspace`, as they are container-specific
- If accessing a file, use absolute paths
```

### 5. Memory Usage

```
- Memory is a hint, not a decision driver
- Always verify recalled info against latest info in source
- Treat it as background awareness, not a decisive filter
```

---

## Directory Structure from Screenshots

```
~/.claude/
├── CLAUDE.md                       # Global navigation hub (this file)
├── memory/
│   ├── index.yaml                 # Memory store index
│   ├── projects/<name>/           # Project-specific stores
│   └── <store>/                   # Named memory stores
│       └── index.yaml
├── context/                       # Static reference docs
├── plugins/local/                 # Custom plugins
│   └── index.yaml
├── commands/                      # Custom slash commands
│   └── index.yaml
├── agents/                        # Agent definitions
│   └── index.yaml
├── rules/                         # Rule files
│   └── index.yaml
└── pr-review-context/             # Dynamic (no index)

~/.bay/
└── CLAUDE.md                      # Bay-specific navigator
```

---

## Implementation Notes

### For bctx

Based on screenshot text "For bay-managed resources (rules, docs, skills, agents), read `~/.bay/CLAUDE.md`":

1. bctx should generate `~/.bay/CLAUDE.md` (not `~/.claude/bayctx/CLAUDE.md`)
2. This navigator should follow the same directory index pattern
3. Each resource type (rules, skills, agents, plugins) should have `index.yaml`

### Directory Naming

The screenshot uses:
- `~/.claude/` for Claude Code global configuration
- `~/.bay/` for bay-managed resources

This suggests bctx should use `~/.bay/` or `~/.claude/bayctx/` consistently.

### Index Pattern

From "Every agent-relevant directory has an `index.yaml`":
- Every directory that contains files agents should read needs `index.yaml`
- Read index before loading files
- Update index when adding/removing/renaming files

---

This extraction provides the raw text and patterns from the work laptop screenshots, serving as the authoritative reference for implementing the CLAUDE.md pattern in bctx.
