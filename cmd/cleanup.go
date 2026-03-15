package cmd

import (
	"fmt"

	bctxctx "bctx/internal/context"
)

// Cleanup removes context file entries pointing to deleted files.
func Cleanup() error {
	fmt.Println("Removing stale context file entries...")
	cleaned, err := bctxctx.CleanupStaleEntries()
	if err != nil {
		return fmt.Errorf("cleanup failed: %w", err)
	}
	if cleaned == 0 {
		fmt.Println("No stale entries found.")
	} else {
		fmt.Printf("Cleaned %d stale entries.\n", cleaned)
		regenerate()
	}
	return nil
}
