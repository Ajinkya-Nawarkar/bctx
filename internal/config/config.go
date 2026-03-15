package config

import (
	"os"
	"path/filepath"

	"gopkg.in/yaml.v3"
)

// BctxDir returns the path to ~/.claude/bayctx/
func BctxDir() string {
	home, _ := os.UserHomeDir()
	return filepath.Join(home, ".claude", "bayctx")
}

// ConfigPath returns the path to ~/.claude/bayctx/config.yaml
func ConfigPath() string {
	return filepath.Join(BctxDir(), "config.yaml")
}

// DBPath returns the path to ~/.claude/bayctx/bayctx.db
func DBPath() string {
	return filepath.Join(BctxDir(), "bayctx.db")
}

// ProjectsDir returns the path to ~/.claude/bayctx/projects/
func ProjectsDir() string {
	return filepath.Join(BctxDir(), "projects")
}

// ResourceTypes lists the supported resource directory types.
var ResourceTypes = []string{"rules", "skills", "agents", "plugins"}

// EnsureDirs creates the bctx directory structure.
func EnsureDirs() error {
	dirs := []string{
		BctxDir(),
		ProjectsDir(),
	}
	for _, t := range ResourceTypes {
		dirs = append(dirs, filepath.Join(BctxDir(), t))
	}
	for _, d := range dirs {
		if err := os.MkdirAll(d, 0755); err != nil {
			return err
		}
	}
	return nil
}

// Exists returns true if the config file exists.
func Exists() bool {
	_, err := os.Stat(ConfigPath())
	return err == nil
}

// Load reads and parses config.yaml.
func Load() (*Config, error) {
	data, err := os.ReadFile(ConfigPath())
	if err != nil {
		return nil, err
	}
	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, err
	}
	return &cfg, nil
}

// Save writes the config to config.yaml.
func Save(cfg *Config) error {
	if err := EnsureDirs(); err != nil {
		return err
	}
	data, err := yaml.Marshal(cfg)
	if err != nil {
		return err
	}
	return os.WriteFile(ConfigPath(), data, 0644)
}

// DefaultConfig returns a config with sensible defaults.
func DefaultConfig() *Config {
	return &Config{
		Version:          1,
		ContextInjection: true,
		ContextBudget:    12000,
	}
}
