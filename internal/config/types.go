package config

// Config represents the bctx configuration stored in ~/.claude/bayctx/config.yaml
type Config struct {
	Version          int  `yaml:"version"`
	ContextInjection bool `yaml:"context_injection"`
	ContextBudget    int  `yaml:"context_budget"`
}
