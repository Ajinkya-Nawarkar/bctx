"""Command-line interface for bctx."""

import sys
import subprocess
from pathlib import Path
from typing import Optional
import click

from .core.paths import __version__, claude_dir
from .core import config as cfg_module
from .context import manager as ctx_manager
from .context.builtin import ensure_builtin_rules


def detect_repo() -> str:
    """Detect current git repository name.

    Returns:
        Repository name, or "(not in a git repo)" if not in a repo.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
            timeout=2
        )
        repo_path = Path(result.stdout.strip())
        return repo_path.name
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return "(not in a git repo)"


@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version=__version__, prog_name="bctx")
def cli(ctx):
    """bctx - Claude Code Context Manager & Agent Harness

    Manage rules, skills, agents, and plugins injected into Claude Code sessions.
    """
    # If no subcommand provided, show status
    if ctx.invoked_subcommand is None:
        ctx.invoke(status)


@cli.command()
def status():
    """Show status (registered files, active rules)."""
    try:
        files = ctx_manager.list_all()
        repo_name = detect_repo()

        enabled_count = sum(1 for f in files if f.enabled)

        click.echo("bctx — context manager & agent harness\n")
        click.echo(f"  Repo:     {repo_name}")
        click.echo(f"  Files:    {len(files)} registered, {enabled_count} enabled")

        if repo_name and repo_name != "(not in a git repo)":
            active = ctx_manager.active_rules(repo_name)
            click.echo(f"  Active:   {len(active)} rules for this repo")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def inject():
    """Output active rules for SessionStart hook."""
    # Must never fail - non-zero exit breaks Claude startup
    try:
        # Check if context injection is enabled
        try:
            config = cfg_module.load()
            if not config.context_injection:
                return
        except FileNotFoundError:
            # No config yet, skip injection
            return

        repo_name = detect_repo()
        if not repo_name or repo_name == "(not in a git repo)":
            return

        active = ctx_manager.active_rules(repo_name)
        if not active:
            return

        # Output context rules
        click.echo("# Context Rules\n")

        for f in active:
            try:
                content = ctx_manager.read_content(f)
                click.echo(f"> {f.name} ({f.scope})")
                click.echo(content)
                click.echo()
            except Exception:
                # Skip files that can't be read
                continue

    except Exception:
        # Silently fail to avoid breaking Claude
        pass


@cli.command()
def files():
    """List all registered context files."""
    try:
        all_files = ctx_manager.list_all()

        if not all_files:
            click.echo("No context files registered.")
            return

        click.echo("Registered context files:\n")

        for f in all_files:
            status_icon = "✓" if f.enabled else "✗"
            click.echo(f"  {status_icon} {f.name}")
            click.echo(f"      Path:     {f.path}")
            click.echo(f"      Scope:    {f.scope}")
            click.echo(f"      Type:     {f.type}")
            click.echo(f"      Category: {f.category}")
            if f.description:
                click.echo(f"      Desc:     {f.description}")
            click.echo()

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("name")
@click.argument("path", type=click.Path(exists=True))
@click.option("--scope", default="global", help="Scope: global or repo:<name>")
@click.option("--type", "typ", default="rules", help="Type: rules, skills, agents, plugins")
@click.option("--category", default="rules", help="Category (e.g., rules, docs, standards)")
@click.option("--desc", "description", default="", help="Description of the context file")
def add(name: str, path: str, scope: str, typ: str, category: str, description: str):
    """Register a context file.

    NAME: Unique name for the context file
    PATH: File path
    """
    try:
        ctx_manager.add(
            name=name,
            path=path,
            scope=scope,
            category=category,
            typ=typ,
            description=description
        )
        click.echo(f"✓ Registered '{name}' → {path}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("name")
def rm(name: str):
    """Remove a context file.

    NAME: Name of the context file to remove
    """
    try:
        # Check if exists
        existing = ctx_manager.get_by_name(name)
        if not existing:
            click.echo(f"Error: Context file '{name}' not found.", err=True)
            sys.exit(1)

        ctx_manager.remove(name)
        click.echo(f"✓ Removed '{name}'")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("name")
def toggle(name: str):
    """Enable/disable a context file.

    NAME: Name of the context file to toggle
    """
    try:
        # Check if exists
        existing = ctx_manager.get_by_name(name)
        if not existing:
            click.echo(f"Error: Context file '{name}' not found.", err=True)
            sys.exit(1)

        ctx_manager.toggle(name)

        # Get updated state
        updated = ctx_manager.get_by_name(name)
        state = "enabled" if updated and updated.enabled else "disabled"
        click.echo(f"✓ Toggled '{name}' → {state}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def sync():
    """Regenerate CLAUDE.md navigator + indexes."""
    try:
        from .context.navigator import generate_navigator

        # Ensure builtin rules are registered
        ensure_builtin_rules()

        # Generate navigator
        generate_navigator()

        click.echo("✓ Regenerated CLAUDE.md navigator")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def cleanup():
    """Remove entries pointing to deleted files."""
    try:
        all_files = ctx_manager.list_all()
        removed_count = 0

        for f in all_files:
            if not Path(f.path).exists():
                ctx_manager.remove(f.name)
                click.echo(f"  Removed '{f.name}' (file not found: {f.path})")
                removed_count += 1

        if removed_count == 0:
            click.echo("No stale entries found.")
        else:
            click.echo(f"\n✓ Removed {removed_count} stale entries")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("key", required=False)
@click.argument("value", required=False)
def config(key: Optional[str], value: Optional[str]):
    """Show or set configuration.

    With no arguments, shows current configuration.
    With KEY, shows that setting's value.
    With KEY VALUE, sets that setting (VALUE should be 'on' or 'off').
    """
    try:
        # Load or create default config
        try:
            current_config = cfg_module.load()
        except FileNotFoundError:
            current_config = cfg_module.default_config()
            cfg_module.save(current_config)

        # Show all settings
        if key is None:
            click.echo("bctx configuration:\n")
            click.echo(f"  version:            {current_config.version}")
            click.echo(f"  context_injection:  {'on' if current_config.context_injection else 'off'}")
            click.echo(f"  context_budget:     {current_config.context_budget}")
            return

        # Show specific setting
        if value is None:
            if key == "context_injection":
                state = "on" if current_config.context_injection else "off"
                click.echo(f"{key}: {state}")
            elif key == "context_budget":
                click.echo(f"{key}: {current_config.context_budget}")
            else:
                click.echo(f"Error: Unknown setting '{key}'", err=True)
                sys.exit(1)
            return

        # Set setting
        if key == "context_injection":
            if value.lower() in ("on", "true", "1"):
                current_config.context_injection = True
            elif value.lower() in ("off", "false", "0"):
                current_config.context_injection = False
            else:
                click.echo(f"Error: Value must be 'on' or 'off'", err=True)
                sys.exit(1)

            cfg_module.save(current_config)
            state = "on" if current_config.context_injection else "off"
            click.echo(f"✓ Set {key} → {state}")

        elif key == "context_budget":
            try:
                budget = int(value)
                current_config.context_budget = budget
                cfg_module.save(current_config)
                click.echo(f"✓ Set {key} → {budget}")
            except ValueError:
                click.echo(f"Error: context_budget must be a number", err=True)
                sys.exit(1)

        else:
            click.echo(f"Error: Unknown setting '{key}'", err=True)
            sys.exit(1)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


# NEW commands for agent harness

@cli.command()
@click.option("--force", is_flag=True, help="Force reinstall over existing installation")
def install(force: bool):
    """Install agent harness (directories, hooks, configs)."""
    try:
        from .hooks.installer import install as do_install

        do_install(force=force)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--keep-data", is_flag=True, help="Keep data directories (memory, observations, sessions)")
@click.confirmation_option(prompt="Are you sure you want to uninstall bctx?")
def uninstall(keep_data: bool):
    """Remove agent harness."""
    try:
        from .hooks.installer import uninstall as do_uninstall

        do_uninstall(keep_data=keep_data)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def upgrade():
    """Upgrade to new version."""
    try:
        from .hooks.installer import upgrade as do_upgrade

        do_upgrade()

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("event", required=False)
def observe(event: Optional[str]):
    """Trigger observation hooks."""
    click.echo(f"TODO: Implement observe command (Phase 3)")
    if event:
        click.echo(f"Event: {event}")


@cli.command()
def reflect():
    """Trigger reflection and learning."""
    click.echo("TODO: Implement reflect command (Phase 5)")


@cli.group()
def memory():
    """Memory operations (add, show, search, list)."""
    pass


@memory.command()
@click.argument("title")
@click.argument("content")
@click.option("--tags", help="Comma-separated tags")
@click.option("--id", "entry_id", help="Custom entry ID (auto-generated if not provided)")
def add_memory(title: str, content: str, tags: Optional[str], entry_id: Optional[str]):
    """Add a memory entry.

    TITLE: Entry title
    CONTENT: Entry content (markdown)
    """
    try:
        from .memory import LongTermMemory, create_memory_entry
        from datetime import datetime

        # Parse tags
        tag_list = [t.strip() for t in tags.split(",")] if tags else []

        # Generate ID if not provided
        if not entry_id:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            entry_id = f"entry-{timestamp}"

        # Create entry
        entry = create_memory_entry(
            id=entry_id,
            title=title,
            tags=tag_list,
            content=content,
        )

        # Add to LTM
        ltm = LongTermMemory()
        ltm.add_entry(entry)

        click.echo(f"✓ Added memory entry: {entry_id}")
        click.echo(f"  Title: {title}")
        click.echo(f"  Tags: {', '.join(tag_list) if tag_list else '(none)'}")

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@memory.command()
@click.argument("entry_id")
def show(entry_id: str):
    """Show a memory entry by ID.

    ENTRY_ID: ID of the entry to show
    """
    try:
        from .memory import LongTermMemory

        ltm = LongTermMemory()
        entry = ltm.get_entry(entry_id)

        if not entry:
            click.echo(f"Error: Entry '{entry_id}' not found.", err=True)
            sys.exit(1)

        # Display entry
        click.echo(f"\n{'=' * 60}")
        click.echo(f"ID: {entry.id}")
        click.echo(f"Title: {entry.title}")
        click.echo(f"Tags: {', '.join(entry.tags) if entry.tags else '(none)'}")
        click.echo(f"Created: {entry.created}")
        click.echo(f"Modified: {entry.last_modified}")
        if entry.related_entries:
            click.echo(f"Related: {', '.join(entry.related_entries)}")
        click.echo(f"{'=' * 60}\n")
        click.echo(entry.content)
        click.echo()

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@memory.command()
@click.argument("query")
@click.option("--limit", "-n", default=5, help="Number of results to return")
def search(query: str, limit: int):
    """Search memory entries.

    QUERY: Search query (matches title, tags, content)
    """
    try:
        from .memory import LongTermMemory

        ltm = LongTermMemory()
        results = ltm.search(query, k=limit)

        if not results:
            click.echo(f"No results found for '{query}'")
            return

        click.echo(f"\nFound {len(results)} result(s) for '{query}':\n")

        for i, entry in enumerate(results, 1):
            click.echo(f"{i}. {entry.id} - {entry.title}")
            click.echo(f"   Tags: {', '.join(entry.tags) if entry.tags else '(none)'}")
            click.echo(f"   Modified: {entry.last_modified}")
            # Show first line of content
            first_line = entry.content.strip().split("\n")[0]
            click.echo(f"   {first_line[:80]}...")
            click.echo()

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@memory.command()
def list_memory():
    """List all memory entries."""
    try:
        from .memory import LongTermMemory

        ltm = LongTermMemory()
        index = ltm.get_index()

        if not index.entries:
            click.echo("No memory entries found.")
            return

        click.echo(f"\nMemory Store: {index.name}")
        click.echo(f"Description: {index.description}")
        click.echo(f"Total entries: {len(index.entries)}\n")

        # Sort by last_modified
        sorted_entries = sorted(
            index.entries.items(),
            key=lambda x: x[1].get("last_modified", ""),
            reverse=True,
        )

        for entry_id, entry_summary in sorted_entries:
            title = entry_summary.get("title", "")
            tags = entry_summary.get("tags", [])
            modified = entry_summary.get("last_modified", "")

            click.echo(f"• {entry_id} - {title}")
            click.echo(f"  Tags: {', '.join(tags) if tags else '(none)'}")
            click.echo(f"  Modified: {modified}")
            click.echo()

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def validate():
    """Validate schemas and configuration."""
    click.echo("TODO: Implement validate command (Phase 4)")


def main():
    """Entry point for CLI."""
    cli()


if __name__ == "__main__":
    main()
