"""
Centralized error handling utility to standardize error management across the application.
"""

import traceback
from functools import wraps
from typing import Callable, Optional, Type, Union

from .... import LOGGER
from ...telegram_helper.message_utils import send_message
from ..exceptions import MirrorBeastException


class ErrorHandler:
    """
    Utility class for handling errors in a standardized way.
    """

    @staticmethod
    async def handle_error(
        error: Exception,
        message=None,
        reply_to=None,
        edit=False,
        delete=False,
        silent=False,
        log_level: str = "error",
    ) -> None:
        """
        Handle an exception with standardized logging and user notification.

        Args:
            error: The exception to handle
            message: The message object for sending error notifications
            reply_to: Message to reply to when sending error message
            edit: Whether to edit the original message
            delete: Whether to delete the original message
            silent: Whether to suppress user-facing error messages
            log_level: The logging level to use (default: error)
        """
        # Get error details
        err_type = type(error).__name__
        err_msg = str(error)
        trace = traceback.format_exc()
        
        # Log the error
        if log_level.lower() == "debug":
            LOGGER.debug(f"{err_type}: {err_msg}\n{trace}")
        elif log_level.lower() == "info":
            LOGGER.info(f"{err_type}: {err_msg}")
        elif log_level.lower() == "warning":
            LOGGER.warning(f"{err_type}: {err_msg}")
        else:
            LOGGER.error(f"{err_type}: {err_msg}\n{trace}")
        
        # Send user-friendly error message if needed
        if not silent and message:
            if isinstance(error, MirrorBeastException):
                user_msg = error.user_msg
            else:
                user_msg = f"<b>Error:</b> {err_msg}"
            
            await send_message(message, user_msg, reply_to=reply_to, edit=edit, delete=delete)

    @staticmethod
    def exception_handler(
        error_types: Optional[Union[Type[Exception], tuple[Type[Exception], ...]]] = None,
        message_arg_name: str = "message",
        silent: bool = False,
        log_level: str = "error",
    ) -> Callable:
        """
        Decorator for handling exceptions in async functions.

        Args:
            error_types: Specific exception types to catch (defaults to Exception)
            message_arg_name: Name of the message argument in the decorated function
            silent: Whether to suppress user-facing error messages
            log_level: The logging level to use

        Returns:
            Decorated function with error handling
        """
        if error_types is None:
            error_types = Exception

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except error_types as e:
                    # Get the message object if it exists in args or kwargs
                    message = None
                    if message_arg_name in kwargs:
                        message = kwargs[message_arg_name]
                    
                    # Handle the error
                    await ErrorHandler.handle_error(
                        error=e,
                        message=message,
                        silent=silent,
                        log_level=log_level
                    )
                    
                    # Re-raise if it's a critical error
                    if not isinstance(e, MirrorBeastException):
                        raise
            
            return wrapper
        
        return decorator 