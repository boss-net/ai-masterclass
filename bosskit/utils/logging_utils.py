import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Union


class BossKitLogger:
    def __init__(
        self,
        name: str = 'bosskit',
        level: Union[str, int] = 'INFO',
        log_dir: Optional[str] = None,
        log_to_file: bool = True,
        log_to_console: bool = True
    ):
        """Initialize the logger.

        Args:
            name: Logger name
            level: Logging level (str or int)
            log_dir: Directory for log files
            log_to_file: Whether to log to file
            log_to_console: Whether to log to console
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Remove existing handlers
        self.logger.handlers.clear()

        # Create log directory if needed
        if log_to_file:
            if log_dir:
                Path(log_dir).mkdir(parents=True, exist_ok=True)
            else:
                log_dir = Path.home() / '.bosskit' / 'logs'
                log_dir.mkdir(parents=True, exist_ok=True)

            # Create file handler
            log_file = log_dir / f'bosskit_{datetime.now().strftime("%Y%m%d")}.log'
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(self._get_formatter())
            self.logger.addHandler(file_handler)

        # Create console handler
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(self._get_formatter())
            self.logger.addHandler(console_handler)

    def _get_formatter(self) -> logging.Formatter:
        """Get logging formatter."""
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def get_logger(self) -> logging.Logger:
        """Get the configured logger."""
        return self.logger

def setup_logger(
    name: str = 'bosskit',
    level: Union[str, int] = 'INFO',
    log_dir: Optional[str] = None,
    log_to_file: bool = True,
    log_to_console: bool = True
) -> logging.Logger:
    """Setup and get a logger.

    Args:
        name: Logger name
        level: Logging level (str or int)
        log_dir: Directory for log files
        log_to_file: Whether to log to file
        log_to_console: Whether to log to console

    Returns:
        Configured logger instance
    """
    return BossKitLogger(
        name=name,
        level=level,
        log_dir=log_dir,
        log_to_file=log_to_file,
        log_to_console=log_to_console
    ).get_logger()

def log_json(data: dict, logger: logging.Logger, level: str = 'info'):
    """Log data as JSON.

    Args:
        data: Dictionary to log
        logger: Logger instance
        level: Logging level
    """
    log_func = getattr(logger, level.lower())
    log_func(json.dumps(data, indent=2))

def log_request(
    method: str,
    url: str,
    data: Optional[dict] = None,
    logger: Optional[logging.Logger] = None
):
    """Log an API request.

    Args:
        method: HTTP method
        url: Request URL
        data: Request data
        logger: Logger instance
    """
    if not logger:
        logger = logging.getLogger('bosskit.requests')

    logger.info(
        f"API Request - Method: {method}, URL: {url}, Data: {json.dumps(data, indent=2) if data else 'None'}"
    )

def log_response(
    status_code: int,
    response: dict,
    logger: Optional[logging.Logger] = None
):
    """Log an API response.

    Args:
        status_code: HTTP status code
        response: Response data
        logger: Logger instance
    """
    if not logger:
        logger = logging.getLogger('bosskit.responses')

    logger.info(
        f"API Response - Status: {status_code}, Data: {json.dumps(response, indent=2)}"
    )

def log_error(
    error: Exception,
    context: Optional[dict] = None,
    logger: Optional[logging.Logger] = None
):
    """Log an error with context.

    Args:
        error: Exception instance
        context: Additional context information
        logger: Logger instance
    """
    if not logger:
        logger = logging.getLogger('bosskit.errors')

    logger.error(
        f"Error: {str(error)}\nContext: {json.dumps(context, indent=2) if context else 'None'}"
    )
