package cmd

import (
	"fmt"
	"os/exec"
	"path/filepath"
	"strings"

	bctxctx "bctx/internal/context"
)

// Status shows a summary of registered context files and active rules.
func Status() error {
	files, err := bctxctx.List()
	if err != nil {
		return fmt.Errorf("listing context files: %w", err)
	}

	repoName := detectRepo()

	enabled := 0
	for _, f := range files {
		if f.Enabled {
			enabled++
		}
	}

	fmt.Printf("bctx — context manager\n\n")
	fmt.Printf("  Repo:     %s\n", repoName)
	fmt.Printf("  Files:    %d registered, %d enabled\n", len(files), enabled)

	if repoName != "" {
		active, _ := bctxctx.ActiveRules(repoName)
		fmt.Printf("  Active:   %d rules for this repo\n", len(active))
	}

	return nil
}

// detectRepo returns the current repo name from CWD.
func detectRepo() string {
	out, err := exec.Command("git", "rev-parse", "--show-toplevel").Output()
	if err != nil {
		return "(not in a git repo)"
	}
	return filepath.Base(strings.TrimSpace(string(out)))
}
