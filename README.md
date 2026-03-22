# bctx

Context manager for Claude Code. Register rules, skills, docs, and plugins that get injected into every Claude session.

## Install

Download a binary from [Releases](https://github.com/Ajinkya-Nawarkar/bctx/releases) and add it to your PATH:

```bash
tar -xzf bctx-*.tar.gz
mv bctx ~/.local/bin/
```

Or build from source:

```bash
go install github.com/Ajinkya-Nawarkar/bctx@latest
```

## Quick Start

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

## Hook Setup

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

`bctx inject` outputs active rules for the current repo. It never returns a non-zero exit code (safe for hooks).

## Commands

```
bctx                          Show status (registered files, active rules)
bctx inject                   Output active rules for SessionStart hook
bctx files                    List all registered context files
bctx add <name> <path>        Register a context file
                                --scope global|repo:<name>
                                --type rules|skills|agents|plugins
                                --category <cat>  --desc <description>
bctx rm <name>                Remove a context file
bctx toggle <name>            Enable/disable a context file
bctx sync                     Regenerate CLAUDE.md navigator + indexes
bctx cleanup                  Remove entries pointing to deleted files
bctx config                   Show feature settings
bctx config <key> on|off      Toggle: context_injection, context_budget
bctx version                  Show version
```

## How It Works

bctx stores registered context files in a SQLite database at `~/.claude/bayctx/bayctx.db`. Each file has a name, path, scope (global or per-repo), type, and category.

On `bctx inject`, it finds all enabled files matching the current repo (global scope + repo-specific scope), reads their content, and outputs it as markdown for Claude to consume.

bctx also generates:
- `~/.claude/bayctx/CLAUDE.md` — resource navigator (entry point for agents to discover available resources)
- `~/.claude/bayctx/{type}/index.yaml` — catalogs per resource type (rules, skills, agents, plugins)

## Resource Types

| Type | Directory | Purpose |
|------|-----------|---------|
| rules | `~/.claude/bayctx/rules/` | Coding standards, conventions, constraints |
| skills | `~/.claude/bayctx/skills/` | Reusable agent capabilities |
| agents | `~/.claude/bayctx/agents/` | Agent configurations |
| plugins | `~/.claude/bayctx/plugins/` | Extensions and integrations |

## Project Context

bctx creates per-repo project context at `~/.claude/bayctx/projects/<repo>/status.md`. Use this for persistent project state — milestones, what's shipped, known issues. Updated by agents and humans, survives across sessions.

## Migration

If you previously used bay's context management (`bay ctx files/add/rm`), bctx auto-imports your registered files from `~/.bay/bay.db` on first run. No manual migration needed.
