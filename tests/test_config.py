"""Tests for configuration management."""

import pytest
from pathlib import Path

from bctx.core.config import (
    Config,
    load,
    save,
    default_config,
    exists,
)


def test_default_config():
    """Test creating a default configuration."""
    config = default_config()

    assert config.version == "2.0.0"
    assert config.context_injection is True
    assert config.context_budget == 50000


def test_config_to_dict():
    """Test converting config to dictionary."""
    config = default_config()
    data = config.to_dict()

    assert data["version"] == "2.0.0"
    assert data["context_injection"] is True
    assert data["context_budget"] == 50000
    assert "agents" in data
    assert "memory" in data
    assert "hooks" in data


def test_config_from_dict():
    """Test creating config from dictionary."""
    data = {
        "version": "2.0.0",
        "context_injection": False,
        "context_budget": 30000,
        "agents": {
            "executor": {"enabled": False, "max_concurrent_tasks": 3},
            "observer": {"enabled": True, "log_level": "debug"},
        },
        "memory": {
            "short_term": {"max_size": 500, "ttl_seconds": 1800},
            "long_term": {
                "path": "~/.claude/memory/custom",
                "retrieval": {"strategy": "recency", "recency_weight": 0.5},
            },
        },
        "hooks": {
            "pre_session": {"enabled": False},
            "post_command": {"enabled": True},
        },
    }

    config = Config.from_dict(data)

    assert config.version == "2.0.0"
    assert config.context_injection is False
    assert config.context_budget == 30000
    assert config.agents.executor.enabled is False
    assert config.agents.executor.max_concurrent_tasks == 3
    assert config.agents.observer.log_level == "debug"
    assert config.memory.short_term.max_size == 500
    assert config.memory.long_term.path == "~/.claude/memory/custom"
    assert config.hooks.pre_session.enabled is False


def test_save_and_load(temp_dir):
    """Test saving and loading configuration."""
    config_path = temp_dir / "config.yaml"

    # Create and save config
    config = default_config()
    config.context_budget = 40000
    save(config, config_path)

    # Load it back
    loaded = load(config_path)

    assert loaded.version == config.version
    assert loaded.context_budget == 40000


def test_load_missing_file(temp_dir):
    """Test loading a non-existent config file."""
    config_path = temp_dir / "nonexistent.yaml"

    with pytest.raises(FileNotFoundError):
        load(config_path)


def test_exists(temp_dir):
    """Test checking if config exists."""
    config_path = temp_dir / "config.yaml"

    # Initially doesn't exist
    assert not config_path.exists()

    # Save config
    config = default_config()
    save(config, config_path)

    # Now it exists
    assert config_path.exists()
