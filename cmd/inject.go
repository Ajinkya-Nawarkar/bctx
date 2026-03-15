package cmd

import (
	"fmt"
	"strings"

	"bctx/internal/config"
	bctxctx "bctx/internal/context"
)

// Inject outputs active rules content for the SessionStart hook.
// Must never return an error — non-zero exit breaks Claude startup.
func Inject() error {
	cfg, _ := config.Load()
	if cfg != nil && !cfg.ContextInjection {
		return nil
	}

	repoName := detectRepo()
	if repoName == "" || repoName == "(not in a git repo)" {
		return nil
	}

	active, err := bctxctx.ActiveRules(repoName)
	if err != nil {
		return nil
	}

	if len(active) == 0 {
		return nil
	}

	var b strings.Builder
	b.WriteString("# Context Rules\n")

	for _, f := range active {
		content, err := bctxctx.ReadContent(f)
		if err != nil {
			continue
		}
		b.WriteString(fmt.Sprintf("> %s (%s)\n", f.Name, f.Scope))
		b.WriteString(content)
		b.WriteString("\n")
	}

	fmt.Print(b.String())
	return nil
}
