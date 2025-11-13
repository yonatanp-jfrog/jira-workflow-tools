"""
Jira Workflow Tools - Internal Team Version

A secure, team-focused toolkit for Jira epic creation and ticket management
with support for private mode (local-only operation) and team collaboration.

Key Features:
- Private mode operation with encrypted local storage
- Customizable Jira templates
- Team-focused workflows
- Secure credential management
- Local-only staging for sensitive data

Usage:
    python -m jira_tools setup --private    # Set up private mode
    python -m jira_tools epic create "Epic Name"  # Create epic
    python -m jira_tools viewer PROJ-123    # View ticket

For setup help, see README.md
"""

__version__ = "2.0.0-team"
__author__ = "JFrog Internal Team"
__description__ = "Internal Jira workflow tools with private mode support"

# Public API
from .core.config import ConfigManager
from .core.client import JiraClient

__all__ = [
    'ConfigManager',
    'JiraClient',
]
