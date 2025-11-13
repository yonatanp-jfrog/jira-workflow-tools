"""
Core functionality for Jira Workflow Tools.

This module contains the core classes and functions for:
- Configuration management (environment and private mode)
- Jira API client
- Template processing
- Authentication handling
"""

from .config import ConfigManager
from .client import JiraClient

__all__ = [
    'ConfigManager', 
    'JiraClient',
]
