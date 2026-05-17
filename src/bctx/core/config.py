"""Configuration management for bctx."""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

from .paths import config_path, ensure_dirs, legacy_config_path


@dataclass
class AgentConfig:
    """Agent configuration."""
    enabled: bool = True
    max_concurrent_tasks: int = 5
    timeout_seconds: int = 300


@dataclass
class ObserverConfig:
    """Observer agent configuration."""
    enabled: bool = True
    log_level: str = "info"


@dataclass
class AgentsConfig:
    """All agents configuration."""
    executor: AgentConfig = field(default_factory=AgentConfig)
    observer: ObserverConfig = field(default_factory=ObserverConfig)


@dataclass
class ShortTermMemoryConfig:
    """Short-term memory configuration."""
    max_size: int = 1000
    ttl_seconds: int = 3600


@dataclass
class RetrievalConfig:
    """Memory retrieval configuration."""
    strategy: str = "hybrid"
    recency_weight: float = 0.3
    relevance_weight: float = 0.7


@dataclass
class LongTermMemoryConfig:
    """Long-term memory configuration."""
    path: str = "~/.claude/memory/bay"
    retrieval: RetrievalConfig = field(default_factory=RetrievalConfig)


@dataclass
class MemoryConfig:
    """Memory system configuration."""
    short_term: ShortTermMemoryConfig = field(default_factory=ShortTermMemoryConfig)
    long_term: LongTermMemoryConfig = field(default_factory=LongTermMemoryConfig)


@dataclass
class HookConfig:
    """Individual hook configuration."""
    enabled: bool = True


@dataclass
class HooksConfig:
    """All hooks configuration."""
    pre_session: HookConfig = field(default_factory=HookConfig)
    post_command: HookConfig = field(default_factory=HookConfig)
    pre_tool_call: HookConfig = field(default_factory=HookConfig)
    post_tool_call: HookConfig = field(default_factory=HookConfig)
    on_error: HookConfig = field(default_factory=HookConfig)


@dataclass
class Config:
    """Main bctx configuration."""
    version: str = "2.0.0"
    context_injection: bool = True
    context_budget: int = 50000

    # Agent system configuration (Phase 1+)
    agents: AgentsConfig = field(default_factory=AgentsConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    hooks: HooksConfig = field(default_factory=HooksConfig)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Create Config from dictionary.

        Args:
            data: Configuration dictionary.

        Returns:
            Config instance.
        """
        # Handle nested structures
        agents_data = data.get("agents", {})
        memory_data = data.get("memory", {})
        hooks_data = data.get("hooks", {})

        # Create agent configs
        executor_cfg = AgentConfig(**agents_data.get("executor", {}))
        observer_cfg = ObserverConfig(**agents_data.get("observer", {}))
        agents = AgentsConfig(executor=executor_cfg, observer=observer_cfg)

        # Create memory configs
        stm_cfg = ShortTermMemoryConfig(**memory_data.get("short_term", {}))
        retrieval_cfg = RetrievalConfig(**memory_data.get("long_term", {}).get("retrieval", {}))
        ltm_cfg = LongTermMemoryConfig(
            path=memory_data.get("long_term", {}).get("path", "~/.claude/memory/bay"),
            retrieval=retrieval_cfg
        )
        memory = MemoryConfig(short_term=stm_cfg, long_term=ltm_cfg)

        # Create hooks configs
        hooks = HooksConfig(
            pre_session=HookConfig(**hooks_data.get("pre_session", {})),
            post_command=HookConfig(**hooks_data.get("post_command", {})),
            pre_tool_call=HookConfig(**hooks_data.get("pre_tool_call", {})),
            post_tool_call=HookConfig(**hooks_data.get("post_tool_call", {})),
            on_error=HookConfig(**hooks_data.get("on_error", {})),
        )

        return cls(
            version=data.get("version", "2.0.0"),
            context_injection=data.get("context_injection", True),
            context_budget=data.get("context_budget", 50000),
            agents=agents,
            memory=memory,
            hooks=hooks
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert Config to dictionary.

        Returns:
            Configuration as dictionary.
        """
        return asdict(self)


def exists() -> bool:
    """Check if config file exists.

    Returns:
        True if config exists, False otherwise.
    """
    return config_path().exists()


def load(path: Optional[Path] = None) -> Config:
    """Load configuration from file.

    Args:
        path: Optional custom config path (mainly for testing).

    Returns:
        Config instance.

    Raises:
        FileNotFoundError: If config file doesn't exist.
        yaml.YAMLError: If config file is invalid YAML.
    """
    cfg_path = path or config_path()

    if not cfg_path.exists():
        raise FileNotFoundError(f"Config file not found: {cfg_path}")

    with open(cfg_path, "r") as f:
        data = yaml.safe_load(f) or {}

    return Config.from_dict(data)


def save(config: Config, path: Optional[Path] = None) -> None:
    """Save configuration to file.

    Args:
        config: Config instance to save.
        path: Optional custom config path (mainly for testing).
    """
    cfg_path = path or config_path()

    # Ensure directory exists
    ensure_dirs()

    # Convert to dict and save
    data = config.to_dict()
    with open(cfg_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def default_config() -> Config:
    """Create default configuration.

    Returns:
        Config with default values.
    """
    return Config()


def migrate_from_legacy() -> Optional[Config]:
    """Migrate configuration from Go version location.

    Returns:
        Migrated Config if legacy exists, None otherwise.
    """
    legacy_path = legacy_config_path()

    if not legacy_path.exists():
        return None

    # Load legacy config
    with open(legacy_path, "r") as f:
        legacy_data = yaml.safe_load(f) or {}

    # Create new config with legacy values
    config = Config(
        version="2.0.0",
        context_injection=legacy_data.get("context_injection", True),
        context_budget=legacy_data.get("context_budget", 50000),
    )

    return config
