package cmd

import (
	"fmt"
	"os"
	"path/filepath"

	bctxctx "bctx/internal/context"
)

// Add registers a context file.
func Add(args []string) error {
	if len(args) < 2 {
		fmt.Fprintln(os.Stderr, "Usage: bctx add <name> <path> [--scope S] [--category C] [--type T] [--desc D]")
		return nil
	}

	name := args[0]
	path := args[1]
	scope := "global"
	category := "rules"
	typ := "rules"
	description := ""

	absPath, err := filepath.Abs(path)
	if err == nil {
		path = absPath
	}

	if _, err := os.Stat(path); os.IsNotExist(err) {
		return fmt.Errorf("file not found: %s", path)
	}

	for i := 2; i < len(args); i++ {
		if args[i] == "--scope" && i+1 < len(args) {
			scope = args[i+1]
			i++
		}
		if args[i] == "--category" && i+1 < len(args) {
			category = args[i+1]
			i++
		}
		if args[i] == "--type" && i+1 < len(args) {
			typ = args[i+1]
			i++
		}
		if args[i] == "--desc" && i+1 < len(args) {
			description = args[i+1]
			i++
		}
	}

	if err := bctxctx.Add(name, path, scope, category, typ, description); err != nil {
		return fmt.Errorf("adding context file: %w", err)
	}

	fmt.Printf("Added '%s' (%s, %s) → %s\n", name, category, scope, path)
	regenerate()
	return nil
}
