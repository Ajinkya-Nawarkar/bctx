package cmd

import (
	"fmt"

	bctxctx "bctx/internal/context"
)

// Rm removes a context file by name.
func Rm(name string) error {
	if err := bctxctx.Remove(name); err != nil {
		return fmt.Errorf("removing context file: %w", err)
	}
	fmt.Printf("Removed '%s'\n", name)
	regenerate()
	return nil
}
