"""
Enhanced logger utility with standardized formatting and additional features.
"""

import logging
import os
import time
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional, Union

from .... import LOGGER as base_logger


class LoggerManager:
    """
    Enhanced logger manager with additional capabilities.
    """

    # Log levels
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    # ANSI color codes for terminal output
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",   # Green
        "WARNING": "\033[33m", # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[41m\033[37m", # White on Red background
        "RESET": "\033[0m"    # Reset
    }

    _instance = None
    _log_file = "log.txt"
    _max_file_size = 20 * 1024 * 1024  # 20 MB
    _backup_count = 2

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_file: Optional[str] = None, log_level: int = logging.INFO):
        if self._initialized:
            return
        
        self._initialized = True
        self._logger = base_logger
        
        if log_file:
            self._log_file = log_file
        
        # Configure file handler if not already set up
        self._setup_file_handler()
        
        # Set log level
        self._logger.setLevel(log_level)

    def _setup_file_handler(self):
        """Set up rotating file handler for the logger."""
        # Check if log file exists and create directory if needed
        log_dir = os.path.dirname(self._log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            self._log_file,
            maxBytes=self._max_file_size,
            backupCount=self._backup_count
        )
        
        # Set formatter for file handler
        formatter = logging.Formatter(
            "{asctime} - [{levelname}] {name}: {message}",
            datefmt="%Y-%m-%d %H:%M:%S",
            style="{"
        )
        file_handler.setFormatter(formatter)
        
        # Add handler to logger if not already present
        for handler in self._logger.handlers:
            if isinstance(handler, RotatingFileHandler) and handler.baseFilename == os.path.abspath(self._log_file):
                return
        
        self._logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance."""
        return self._logger

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message."""
        self._logger.critical(message, *args, **kwargs)

    def log_exception(self, e: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an exception with optional context information.
        
        Args:
            e: The exception to log
            context: Optional dictionary with context information
        """
        error_type = type(e).__name__
        error_msg = str(e)
        
        log_message = f"{error_type}: {error_msg}"
        
        if context:
            context_str = ", ".join(f"{k}={v}" for k, v in context.items())
            log_message = f"{log_message} | Context: {context_str}"
        
        self._logger.error(log_message, exc_info=True)

    def timed(self, level: int = logging.INFO, prefix: str = ""):
        """
        Decorator to log the execution time of a function.
        
        Args:
            level: The log level to use
            prefix: Optional prefix for the log message
        
        Returns:
            Decorated function that logs execution time
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time
                
                # Create log message
                func_name = func.__name__
                log_message = f"{prefix}Function '{func_name}' executed in {execution_time:.4f} seconds"
                
                # Log at appropriate level
                if level == logging.DEBUG:
                    self.debug(log_message)
                elif level == logging.INFO:
                    self.info(log_message)
                elif level == logging.WARNING:
                    self.warning(log_message)
                elif level == logging.ERROR:
                    self.error(log_message)
                elif level == logging.CRITICAL:
                    self.critical(log_message)
                
                return result
            return wrapper
        return decorator

    async def timed_async(self, level: int = logging.INFO, prefix: str = ""):
        """
        Decorator to log the execution time of an async function.
        
        Args:
            level: The log level to use
            prefix: Optional prefix for the log message
        
        Returns:
            Decorated async function that logs execution time
        """
        def decorator(func):
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                result = await func(*args, **kwargs)
                end_time = time.time()
                execution_time = end_time - start_time
                
                # Create log message
                func_name = func.__name__
                log_message = f"{prefix}Async function '{func_name}' executed in {execution_time:.4f} seconds"
                
                # Log at appropriate level
                if level == logging.DEBUG:
                    self.debug(log_message)
                elif level == logging.INFO:
                    self.info(log_message)
                elif level == logging.WARNING:
                    self.warning(log_message)
                elif level == logging.ERROR:
                    self.error(log_message)
                elif level == logging.CRITICAL:
                    self.critical(log_message)
                
                return result
            return wrapper
        return decorator


# Create a singleton instance for easy import
logger = LoggerManager() 