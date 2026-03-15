package cmd

import (
	"fmt"

	bctxctx "bctx/internal/context"
)

// Toggle enables/disables a context file.
func Toggle(name string) error {
	if err := bctxctx.Toggle(name); err != nil {
		return fmt.Errorf("toggling context file: %w", err)
	}

	list, _ := bctxctx.List()
	for _, f := range list {
		if f.Name == name {
			state := "enabled"
			if !f.Enabled {
				state = "disabled"
			}
			fmt.Printf("'%s' is now %s\n", name, state)
			break
		}
	}

	regenerate()
	return nil
}
