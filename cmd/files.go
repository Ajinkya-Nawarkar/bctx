package cmd

import (
	"fmt"

	bctxctx "bctx/internal/context"
)

// Files lists all registered context files with status.
func Files() error {
	list, err := bctxctx.List()
	if err != nil {
		return fmt.Errorf("listing context files: %w", err)
	}

	if len(list) == 0 {
		fmt.Println("No context files registered.")
		return nil
	}

	fmt.Printf("%-20s %-10s %-8s %-8s %-15s %-30s %s\n", "NAME", "TYPE", "CATEGORY", "STATUS", "SCOPE", "DESCRIPTION", "PATH")
	for _, f := range list {
		status := "on"
		if !f.Enabled {
			status = "off"
		}
		cat := f.Category
		if cat == "" {
			cat = "rules"
		}
		typ := f.Type
		if typ == "" {
			typ = "rules"
		}
		desc := f.Description
		if len(desc) > 28 {
			desc = desc[:25] + "..."
		}
		fmt.Printf("%-20s %-10s %-8s %-8s %-15s %-30s %s\n", f.Name, typ, cat, status, f.Scope, desc, f.Path)
	}
	return nil
}
