"""
Custom exceptions for Jira Workflow Tools.

Provides specific exception types for different error conditions,
making error handling more precise and user-friendly.
"""


class JiraToolsError(Exception):
    """Base exception for all Jira Workflow Tools errors."""
    pass


class ConfigurationError(JiraToolsError):
    """Raised when configuration is invalid or missing."""
    pass


class TemplateError(JiraToolsError):
    """Raised when template operations fail."""
    pass


class ValidationError(JiraToolsError):
    """Raised when data validation fails."""
    pass


class AuthenticationError(JiraToolsError):
    """Raised when Jira authentication fails."""
    pass


class PermissionError(JiraToolsError):
    """Raised when user lacks required permissions."""
    pass


class NetworkError(JiraToolsError):
    """Raised when network operations fail."""
    pass


class PrivateModeError(JiraToolsError):
    """Raised when private mode operations fail."""
    pass


class StagingError(JiraToolsError):
    """Raised when staging operations fail."""
    pass
