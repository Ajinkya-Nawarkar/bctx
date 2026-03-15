package context

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"

	"bctx/internal/config"
	"bctx/internal/db"
)

const bctxRuleName = "bctx-cli"

const bctxRuleContent = `# bctx — Context Manager for Claude Code

bctx manages context files (rules, skills, agents, plugins) that get injected
into your Claude Code sessions. Resources live in ` + "`~/.claude/bayctx/`" + ` and are
discovered lazily via ` + "`~/.claude/bayctx/CLAUDE.md`" + `.

## Commands

### Context Files — documents injected into every agent session

- ` + "`bctx files`" + ` — list all registered context files and their status.
- ` + "`bctx add <name> <path>`" + ` — register a file for injection (design docs,
  API specs, coding standards). Use --scope repo:<name> to limit to one repo.
- ` + "`bctx rm <name>`" + ` — remove a registered context file.
- ` + "`bctx toggle <name>`" + ` — enable/disable without removing.
- ` + "`bctx sync`" + ` — regenerate resource navigator and indexes.

## Resource Discovery

Resources are organized in ` + "`~/.claude/bayctx/{type}/`" + ` directories (rules, skills, agents, plugins).
Each directory has an ` + "`index.yaml`" + ` catalog. Read ` + "`~/.claude/bayctx/CLAUDE.md`" + ` for the full listing.

## Project Context

Project-specific context lives in ` + "`~/.claude/bayctx/projects/<project-name>/`" + `.

Key file: ` + "`status.md`" + ` — current project state, milestones, what's shipped, known issues.
Read ` + "`status.md`" + ` at the start of work. Update it when you complete meaningful changes.

### status.md format

` + "`status.md`" + ` uses **timestamped, append-style updates**. Do NOT overwrite previous entries.
Add new updates at the top of the ` + "`## Updates`" + ` section with a date heading:

` + "```" + `
## Updates

### YYYY-MM-DD — short description
- what changed
- what shipped

### (previous entries stay below)
` + "```" + `
`

// RulesDir returns the path to ~/.claude/bayctx/rules/
func RulesDir() string {
	return filepath.Join(config.BctxDir(), "rules")
}

// EnsureBuiltinRules writes the bctx rule file and ensures it's registered in the DB.
func EnsureBuiltinRules(d *sql.DB) error {
	if d == nil {
		var err error
		d, err = db.Open()
		if err != nil {
			return fmt.Errorf("opening db: %w", err)
		}
	}

	rulesDir := RulesDir()
	if err := os.MkdirAll(rulesDir, 0755); err != nil {
		return fmt.Errorf("creating rules dir: %w", err)
	}

	rulePath := filepath.Join(rulesDir, bctxRuleName+".md")
	if err := os.WriteFile(rulePath, []byte(bctxRuleContent), 0644); err != nil {
		return fmt.Errorf("writing bctx rule: %w", err)
	}

	var exists bool
	if err := d.QueryRow(`SELECT 1 FROM context_files WHERE name = ? LIMIT 1`, bctxRuleName).Scan(&exists); err == nil && exists {
		return nil
	}

	if err := AddDB(d, bctxRuleName, rulePath, "global", "rules", "rules", "bctx CLI and context management reference"); err != nil {
		return fmt.Errorf("registering bctx rule: %w", err)
	}

	return nil
}
