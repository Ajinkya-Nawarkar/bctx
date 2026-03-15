package cmd

import (
	"bctx/internal/config"
	"bctx/internal/context"
)

func init() {
	// Ensure dirs + builtin rules + migration on first use
	config.EnsureDirs()
	context.EnsureBuiltinRules(nil)
	context.MigrateFromBay()
}
