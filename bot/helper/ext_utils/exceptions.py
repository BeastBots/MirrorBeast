"""
Custom exceptions for standardized error handling across the codebase.
"""

class MirrorBeastException(Exception):
    """Base exception class for all Mirror Beast specific exceptions."""
    
    def __init__(self, message="An error occurred in Mirror Beast", user_msg=None):
        self.message = message
        self.user_msg = user_msg or message
        super().__init__(self.message)


# Download exceptions
class DownloadException(MirrorBeastException):
    """Base class for all download-related exceptions."""
    pass


class DirectDownloadLinkException(DownloadException):
    """Exception when extracting direct download link from HTTP link fails."""
    
    def __init__(self, message="Failed to extract direct download link", user_msg=None):
        super().__init__(message, user_msg)


class TorrentDownloadException(DownloadException):
    """Exception for torrent download failures."""
    
    def __init__(self, message="Torrent download failed", user_msg=None):
        super().__init__(message, user_msg)


class NzbDownloadException(DownloadException):
    """Exception for NZB download failures."""
    
    def __init__(self, message="NZB download failed", user_msg=None):
        super().__init__(message, user_msg)


# Upload exceptions
class UploadException(MirrorBeastException):
    """Base class for all upload-related exceptions."""
    pass


class DriveUploadException(UploadException):
    """Exception for Google Drive upload failures."""
    
    def __init__(self, message="Failed to upload to Google Drive", user_msg=None):
        super().__init__(message, user_msg)


class TelegramUploadException(UploadException):
    """Exception for Telegram upload failures."""
    
    def __init__(self, message="Failed to upload to Telegram", user_msg=None):
        super().__init__(message, user_msg)


class RcloneUploadException(UploadException):
    """Exception for Rclone upload failures."""
    
    def __init__(self, message="Failed to upload with Rclone", user_msg=None):
        super().__init__(message, user_msg)


# Processing exceptions
class ProcessingException(MirrorBeastException):
    """Base class for all processing-related exceptions."""
    pass


class NotSupportedExtractionArchive(ProcessingException):
    """Exception when the archive format is not supported for extraction."""
    
    def __init__(self, message="Archive format not supported for extraction", user_msg=None):
        super().__init__(message, user_msg)


class CompressionException(ProcessingException):
    """Exception for compression failures."""
    
    def __init__(self, message="Failed to compress files", user_msg=None):
        super().__init__(message, user_msg)


# Authentication exceptions
class AuthException(MirrorBeastException):
    """Base class for all authentication-related exceptions."""
    pass


class UnauthorizedUserException(AuthException):
    """Exception when an unauthorized user attempts to use the bot."""
    
    def __init__(self, message="User not authorized to use this feature", user_msg=None):
        super().__init__(message, user_msg)


class RateLimitException(AuthException):
    """Exception when a user exceeds rate limits."""
    
    def __init__(self, message="Rate limit exceeded", user_msg=None):
        super().__init__(message, user_msg)


# API exceptions
class ApiException(MirrorBeastException):
    """Base class for all API-related exceptions."""
    pass


class TgLinkException(ApiException):
    """Exception when access is not granted for a Telegram chat."""
    
    def __init__(self, message="No access granted for this chat", user_msg=None):
        super().__init__(message, user_msg)


class DriveApiException(ApiException):
    """Exception for Google Drive API failures."""
    
    def __init__(self, message="Google Drive API error", user_msg=None):
        super().__init__(message, user_msg)


# External integration exceptions
class ExternalServiceException(MirrorBeastException):
    """Base class for all external service-related exceptions."""
    pass


class JDownloaderException(ExternalServiceException):
    """Exception for JDownloader failures."""
    
    def __init__(self, message="JDownloader operation failed", user_msg=None):
        super().__init__(message, user_msg)


class QBittorrentException(ExternalServiceException):
    """Exception for qBittorrent failures."""
    
    def __init__(self, message="qBittorrent operation failed", user_msg=None):
        super().__init__(message, user_msg)


# System exceptions
class SystemException(MirrorBeastException):
    """Base class for all system-related exceptions."""
    pass


class ConfigException(SystemException):
    """Exception for configuration errors."""
    
    def __init__(self, message="Configuration error", user_msg=None):
        super().__init__(message, user_msg)


class DatabaseException(SystemException):
    """Exception for database errors."""
    
    def __init__(self, message="Database operation failed", user_msg=None):
        super().__init__(message, user_msg)


class RssShutdownException(SystemException):
    """Exception raised when shutdown is called to stop the RSS monitor."""
    
    def __init__(self, message="RSS monitor shutdown requested", user_msg=None):
        super().__init__(message, user_msg) 