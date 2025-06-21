import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

import yaml

from .errors import ConfigurationError
from .logging_utils import setup_logger


class ConfigManager:
    def __init__(
        self,
        config_dir: Optional[str] = None,
        config_file: str = 'config.yaml',
        env_prefix: str = 'BOSSKIT_',
        logger: Optional[logging.Logger] = None
    ):
        """Initialize the configuration manager.

        Args:
            config_dir: Configuration directory
            config_file: Configuration file name
            env_prefix: Environment variable prefix
            logger: Logger instance
        """
        self.config_dir = Path(config_dir or os.path.expanduser('~/.bosskit'))
        self.config_file = Path(config_file)
        self.config_path = self.config_dir / self.config_file
        self.env_prefix = env_prefix
        self.logger = logger or setup_logger('bosskit.config')

        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Load initial configuration
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file.

        Returns:
            Configuration dictionary
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            return {}
        except Exception as e:
            self.logger.error(f"Error loading config: {str(e)}")
            return {}

    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self._config, f)
            self.logger.info("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving config: {str(e)}")
            raise ConfigurationError(f"Failed to save configuration: {str(e)}")

    def _get_env_var(self, key: str) -> Optional[str]:
        """Get environment variable with prefix.

        Args:
            key: Environment variable name

        Returns:
            Environment variable value or None
        """
        return os.getenv(f"{self.env_prefix}{key.upper()}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: Configuration key
            default: Default value if key not found

        Returns:
            Configuration value
        """
        # Check environment variables first
        env_value = self._get_env_var(key)
        if env_value is not None:
            return env_value

        # Check configuration file
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
        self._save_config()

    def delete(self, key: str) -> None:
        """Delete a configuration value.

        Args:
            key: Configuration key
        """
        if key in self._config:
            del self._config[key]
            self._save_config()

    def update(self, config: Dict[str, Any]) -> None:
        """Update multiple configuration values.

        Args:
            config: Dictionary of configuration values
        """
        self._config.update(config)
        self._save_config()

    def load_from_file(self, path: Union[str, Path]) -> None:
        """Load configuration from a file.

        Args:
            path: Path to configuration file
        """
        try:
            with open(path, 'r') as f:
                new_config = yaml.safe_load(f) or {}
            self.update(new_config)
        except Exception as e:
            self.logger.error(f"Error loading config from file: {str(e)}")
            raise ConfigurationError(f"Failed to load configuration: {str(e)}")

    def validate(self, schema: Dict[str, Any]) -> bool:
        """Validate configuration against a schema.

        Args:
            schema: Validation schema

        Returns:
            True if valid, False otherwise
        """
        for key, value in schema.items():
            if key not in self._config:
                if 'required' in value and value['required']:
                    self.logger.error(f"Missing required configuration: {key}")
                    return False
            else:
                if 'type' in value:
                    if not isinstance(self._config[key], value['type']):
                        self.logger.error(
                            f"Invalid type for {key}: {type(self._config[key])}"
                        )
                        return False
        return True

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values.

        Returns:
            Dictionary of all configuration values
        """
        return self._config.copy()

    def reset(self) -> None:
        """Reset configuration to default values."""
        self._config = {}
        self._save_config()

def get_config_manager(
    config_dir: Optional[str] = None,
    config_file: str = 'config.yaml',
    env_prefix: str = 'BOSSKIT_',
    logger: Optional[logging.Logger] = None
) -> ConfigManager:
    """Get a configuration manager instance.

    Args:
        config_dir: Configuration directory
        config_file: Configuration file name
        env_prefix: Environment variable prefix
        logger: Logger instance

    Returns:
        ConfigManager instance
    """
    return ConfigManager(
        config_dir=config_dir,
        config_file=config_file,
        env_prefix=env_prefix,
        logger=logger
    )
