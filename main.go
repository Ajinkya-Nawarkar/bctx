package main

import (
	"fmt"
	"os"

	"bctx/cmd"
)

var Version = "dev"

func main() {
	args := os.Args[1:]

	if len(args) == 0 {
		if err := cmd.Status(); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}
		return
	}

	switch args[0] {
	case "inject":
		if err := cmd.Inject(); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "files":
		if err := cmd.Files(); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "add":
		if err := cmd.Add(args[1:]); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "rm", "remove":
		if len(args) < 2 {
			fmt.Fprintln(os.Stderr, "Usage: bctx rm <name>")
			os.Exit(1)
		}
		if err := cmd.Rm(args[1]); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "toggle":
		if len(args) < 2 {
			fmt.Fprintln(os.Stderr, "Usage: bctx toggle <name>")
			os.Exit(1)
		}
		if err := cmd.Toggle(args[1]); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "sync":
		if err := cmd.Sync(); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "cleanup":
		if err := cmd.Cleanup(); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "config":
		if err := cmd.Config(args[1:]); err != nil {
			fmt.Fprintf(os.Stderr, "Error: %v\n", err)
			os.Exit(1)
		}

	case "version", "--version", "-v":
		fmt.Printf("bctx %s — Claude Code context manager\n", Version)

	case "help", "--help", "-h":
		printHelp()

	default:
		fmt.Fprintf(os.Stderr, "Unknown command: %s\n", args[0])
		printHelp()
		os.Exit(1)
	}
}

func printHelp() {
	fmt.Println(`bctx — Claude Code Context Manager

Manage rules, skills, agents, and plugins injected into Claude Code sessions.

Usage:
  bctx                          Show status (registered files, active rules)
  bctx inject                   Output active rules for SessionStart hook
  bctx files                    List all registered context files
  bctx add <name> <path>        Register a context file
                                  --scope global|repo:<name>
                                  --type rules|skills|agents|plugins
                                  --category <cat>  --desc <description>
  bctx rm <name>                Remove a context file
  bctx toggle <name>            Enable/disable a context file
  bctx sync                     Regenerate CLAUDE.md navigator + indexes
  bctx cleanup                  Remove entries pointing to deleted files
  bctx config                   Show feature settings
  bctx config <key> on|off      Toggle features (context_injection, context_budget)
  bctx version                  Show version
  bctx help                     Show this help`)
}
