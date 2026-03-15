package cmd

import (
	"fmt"

	"bctx/internal/config"
	bctxctx "bctx/internal/context"
)

// Sync regenerates the navigator and all indexes.
func Sync() error {
	fmt.Println("Regenerating resource navigator...")
	config.EnsureDirs()
	regenerate()
	fmt.Println("Done.")
	return nil
}

// regenerate refreshes the resource navigator after context file changes.
func regenerate() {
	config.EnsureDirs()
	bctxctx.GenerateNavigator()
	bctxctx.GenerateAllIndexes()
}
