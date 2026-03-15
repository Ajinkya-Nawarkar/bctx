package cmd

import (
	"fmt"
	"os"
	"strconv"

	"bctx/internal/config"
)

// Config shows or toggles bctx configuration.
func Config(args []string) error {
	if len(args) == 0 {
		cfg := loadOrDefault()
		fmt.Printf("bctx Configuration:\n")
		fmt.Printf("  context_injection:  %v\n", cfg.ContextInjection)
		fmt.Printf("  context_budget:     %d\n", cfg.ContextBudget)
		return nil
	}

	if len(args) < 2 {
		fmt.Fprintln(os.Stderr, "Usage: bctx config <feature> on|off|<value>")
		return nil
	}

	feature := args[0]
	cfg := loadOrDefault()

	switch feature {
	case "context_injection":
		cfg.ContextInjection = parseBool(args[1])
	case "context_budget":
		v, err := strconv.Atoi(args[1])
		if err != nil {
			return fmt.Errorf("context_budget must be an integer: %w", err)
		}
		cfg.ContextBudget = v
	default:
		return fmt.Errorf("unknown feature: %s", feature)
	}

	if err := config.Save(cfg); err != nil {
		return fmt.Errorf("saving config: %w", err)
	}

	fmt.Printf("%s set\n", feature)
	return nil
}

func loadOrDefault() *config.Config {
	cfg, err := config.Load()
	if err != nil {
		return config.DefaultConfig()
	}
	return cfg
}

func parseBool(s string) bool {
	return s == "on" || s == "true"
}
