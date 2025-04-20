"""
Configuration validation utility to ensure proper configuration of the bot.
"""

from typing import Any, Dict, List, Optional, Tuple, Union

from .... import LOGGER
from ..exceptions import ConfigException


class ConfigValidator:
    """
    Utility class for validating configuration values.
    """

    @staticmethod
    def validate_required_fields(config: Dict[str, Any], required_fields: List[str]) -> None:
        """
        Validate that all required fields are present and not None.

        Args:
            config: The configuration dictionary
            required_fields: List of required field names

        Raises:
            ConfigException: If a required field is missing or None
        """
        missing_fields = []
        
        for field in required_fields:
            if field not in config or config[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            raise ConfigException(
                f"Missing required configuration: {', '.join(missing_fields)}",
                f"Bot configuration is incomplete. Contact the bot administrator."
            )

    @staticmethod
    def validate_field_type(
        config: Dict[str, Any], 
        field: str, 
        expected_type: Union[type, Tuple[type, ...]], 
        allow_none: bool = False
    ) -> None:
        """
        Validate that a field has the expected type.

        Args:
            config: The configuration dictionary
            field: The field name to validate
            expected_type: The expected type(s) for the field
            allow_none: Whether to allow None value

        Raises:
            ConfigException: If the field has an incorrect type
        """
        if field not in config:
            return
        
        value = config[field]
        
        if value is None and allow_none:
            return
        
        if value is not None and not isinstance(value, expected_type):
            type_names = (
                ", ".join([t.__name__ for t in expected_type]) 
                if isinstance(expected_type, tuple) 
                else expected_type.__name__
            )
            raise ConfigException(
                f"Configuration '{field}' has incorrect type. Expected {type_names}, got {type(value).__name__}",
                f"Bot configuration error. Contact the bot administrator."
            )

    @staticmethod
    def validate_numeric_range(
        config: Dict[str, Any], 
        field: str, 
        min_val: Optional[float] = None, 
        max_val: Optional[float] = None,
        allow_none: bool = False
    ) -> None:
        """
        Validate that a numeric field is within the specified range.

        Args:
            config: The configuration dictionary
            field: The field name to validate
            min_val: Minimum allowed value (inclusive)
            max_val: Maximum allowed value (inclusive)
            allow_none: Whether to allow None value

        Raises:
            ConfigException: If the field is outside the allowed range
        """
        if field not in config:
            return
        
        value = config[field]
        
        if value is None and allow_none:
            return
        
        if value is not None:
            if not isinstance(value, (int, float)):
                raise ConfigException(
                    f"Configuration '{field}' is not a number",
                    f"Bot configuration error. Contact the bot administrator."
                )
            
            if min_val is not None and value < min_val:
                raise ConfigException(
                    f"Configuration '{field}' is too small. Minimum value is {min_val}",
                    f"Bot configuration error. Contact the bot administrator."
                )
            
            if max_val is not None and value > max_val:
                raise ConfigException(
                    f"Configuration '{field}' is too large. Maximum value is {max_val}",
                    f"Bot configuration error. Contact the bot administrator."
                )

    @staticmethod
    def validate_string_length(
        config: Dict[str, Any], 
        field: str, 
        min_length: Optional[int] = None, 
        max_length: Optional[int] = None,
        allow_none: bool = False
    ) -> None:
        """
        Validate that a string field has the correct length.

        Args:
            config: The configuration dictionary
            field: The field name to validate
            min_length: Minimum allowed length (inclusive)
            max_length: Maximum allowed length (inclusive)
            allow_none: Whether to allow None value

        Raises:
            ConfigException: If the field has an incorrect length
        """
        if field not in config:
            return
        
        value = config[field]
        
        if value is None and allow_none:
            return
        
        if value is not None:
            if not isinstance(value, str):
                raise ConfigException(
                    f"Configuration '{field}' is not a string",
                    f"Bot configuration error. Contact the bot administrator."
                )
            
            if min_length is not None and len(value) < min_length:
                raise ConfigException(
                    f"Configuration '{field}' is too short. Minimum length is {min_length}",
                    f"Bot configuration error. Contact the bot administrator."
                )
            
            if max_length is not None and len(value) > max_length:
                raise ConfigException(
                    f"Configuration '{field}' is too long. Maximum length is {max_length}",
                    f"Bot configuration error. Contact the bot administrator."
                )

    @staticmethod
    def validate_choices(
        config: Dict[str, Any], 
        field: str, 
        choices: List[Any],
        allow_none: bool = False
    ) -> None:
        """
        Validate that a field has one of the allowed values.

        Args:
            config: The configuration dictionary
            field: The field name to validate
            choices: List of allowed values
            allow_none: Whether to allow None value

        Raises:
            ConfigException: If the field has an invalid value
        """
        if field not in config:
            return
        
        value = config[field]
        
        if value is None and allow_none:
            return
        
        if value is not None and value not in choices:
            choices_str = ", ".join([str(c) for c in choices])
            raise ConfigException(
                f"Configuration '{field}' has invalid value. Allowed values: {choices_str}",
                f"Bot configuration error. Contact the bot administrator."
            )

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> None:
        """
        Validate the entire configuration.

        Args:
            config: The configuration dictionary to validate

        Raises:
            ConfigException: If the configuration is invalid
        """
        try:
            # Required fields validation
            required_fields = [
                "BOT_TOKEN", 
                "OWNER_ID", 
                "DOWNLOAD_DIR",
            ]
            ConfigValidator.validate_required_fields(config, required_fields)
            
            # Type validations
            ConfigValidator.validate_field_type(config, "BOT_TOKEN", str)
            ConfigValidator.validate_field_type(config, "OWNER_ID", int)
            ConfigValidator.validate_field_type(config, "AUTHORIZED_USERS", list, allow_none=True)
            ConfigValidator.validate_field_type(config, "AUTHORIZED_CHATS", list, allow_none=True)
            ConfigValidator.validate_field_type(config, "DATABASE_URL", str, allow_none=True)
            ConfigValidator.validate_field_type(config, "DOWNLOAD_DIR", str)
            ConfigValidator.validate_field_type(config, "INCOMPLETE_TASK_NOTIFIER", bool, allow_none=True)
            ConfigValidator.validate_field_type(config, "PARALLEL_TASKS", int, allow_none=True)
            
            # Numeric range validations
            ConfigValidator.validate_numeric_range(config, "PARALLEL_TASKS", 1, 20, allow_none=True)
            ConfigValidator.validate_numeric_range(config, "STATUS_UPDATE_INTERVAL", 1, 60, allow_none=True)
            ConfigValidator.validate_numeric_range(config, "LEECH_SPLIT_SIZE", 1, None, allow_none=True)
            
            # String length validations
            ConfigValidator.validate_string_length(config, "BOT_TOKEN", 30, 100)
            
            LOGGER.info("Configuration validation successful")
        except ConfigException as e:
            LOGGER.error(f"Configuration validation failed: {e.message}")
            raise
        except Exception as e:
            LOGGER.error(f"Unexpected error during configuration validation: {str(e)}")
            raise ConfigException(
                f"Unexpected configuration validation error: {str(e)}",
                "Bot configuration error. Contact the bot administrator."
            ) 