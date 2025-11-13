"""
Configuration management for Jira Workflow Tools.

Supports multiple configuration modes:
- Environment variables (for CI/CD and simple setups)
- Private mode (encrypted local storage)
- Mixed mode (environment + local overrides)
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from rich.console import Console

# Load environment variables from .env file if it exists
load_dotenv()

console = Console()


class ConfigManager:
    """
    Centralized configuration management.
    
    Determines configuration source and provides unified access to settings.
    """
    
    def __init__(self):
        self.config_source = self._determine_config_source()
        self._jira_base_url = None
        self._jira_auth_token = None
        self._user_account_id = None
        
        # Load configuration based on source
        self._load_configuration()
    
    def _determine_config_source(self) -> str:
        """Determine which configuration source to use."""
        
        # Check private mode first (prioritize over environment)
        private_config_dir = Path.home() / '.jira-private'
        private_config_file = private_config_dir / 'config.json'
        private_secrets_file = private_config_dir / 'secrets.enc'
        
        # Private mode is available if both config and encrypted secrets exist
        # and JIRA_PRIVATE_MODE is not explicitly disabled
        private_mode_disabled = os.getenv('JIRA_PRIVATE_MODE', 'true').lower() == 'false'
        
        if (not private_mode_disabled and 
            private_config_file.exists() and 
            private_secrets_file.exists()):
            return 'private'
        elif os.getenv('JIRA_AUTH_TOKEN') and os.getenv('JIRA_BASE_URL'):
            return 'environment'
        else:
            return 'missing'
    
    def _load_configuration(self):
        """Load configuration from the determined source."""
        
        if self.config_source == 'private':
            self._load_private_config()
        elif self.config_source == 'environment':
            self._load_environment_config()
        else:
            # Configuration is missing - will raise error when accessed
            pass
    
    def _load_environment_config(self):
        """Load configuration from environment variables."""
        self._jira_base_url = os.getenv('JIRA_BASE_URL')
        self._jira_auth_token = os.getenv('JIRA_AUTH_TOKEN')
        self._user_account_id = os.getenv('JIRA_USER_ACCOUNT_ID', '')
    
    def _load_private_config(self):
        """Load configuration from private mode."""
        try:
            from ..private_mode import private_mode_manager
            
            if not private_mode_manager.is_configured():
                # Fall back to environment if private mode isn't fully configured
                self._load_environment_config()
                return
            
            config_data = private_mode_manager.get_jira_config()
            self._jira_base_url = config_data.get('jira_base_url')
            self._jira_auth_token = config_data.get('jira_auth_token')
            self._user_account_id = config_data.get('user_account_id', '')
            
        except Exception as e:
            console.print(f"⚠️  Private mode error: {e}")
            console.print("Falling back to environment configuration...")
            self._load_environment_config()
    
    @property
    def jira_base_url(self) -> str:
        """Get Jira base URL."""
        if not self._jira_base_url:
            raise ValueError(
                "JIRA_BASE_URL not configured. Please:\n"
                "1. Set JIRA_BASE_URL environment variable, or\n"
                "2. Use private mode: python -m jira_tools setup --private"
            )
        return self._jira_base_url
    
    @property
    def jira_auth_token(self) -> str:
        """Get Jira authentication token."""
        if not self._jira_auth_token:
            raise ValueError(
                "JIRA_AUTH_TOKEN not configured. Please:\n"
                "1. Set JIRA_AUTH_TOKEN environment variable, or\n"
                "2. Use private mode: python -m jira_tools setup --private"
            )
        return self._jira_auth_token
    
    @property
    def user_account_id(self) -> str:
        """Get user account ID."""
        return self._user_account_id or ''
    
    @property
    def jira_api_base(self) -> str:
        """Get the base URL for Jira API calls."""
        return f"{self.jira_base_url}/rest/api/2"
    
    @property
    def auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for API requests."""
        return {
            "Authorization": f"Basic {self.jira_auth_token}",
            "Content-Type": "application/json"
        }
    
    def validate_config(self) -> bool:
        """Validate current configuration."""
        try:
            # Try to access all required properties
            _ = self.jira_base_url
            _ = self.jira_auth_token
            return True
        except ValueError:
            return False
    
    def get_config_info(self) -> Dict[str, Any]:
        """Get configuration information for display."""
        return {
            'source': self.config_source,
            'jira_url': self.jira_base_url if self._jira_base_url else 'Not configured',
            'has_token': bool(self._jira_auth_token),
            'has_user_id': bool(self._user_account_id),
            'valid': self.validate_config()
        }


# Legacy compatibility - maintain the old Config class interface
class Config:
    """Legacy Config class for backward compatibility."""
    
    def __init__(self):
        self._config_manager = ConfigManager()
    
    @property
    def jira_base_url(self) -> str:
        return self._config_manager.jira_base_url
    
    @property
    def jira_auth_token(self) -> str:
        return self._config_manager.jira_auth_token
    
    @property
    def jira_api_base(self) -> str:
        return self._config_manager.jira_api_base
    
    @property
    def auth_headers(self) -> Dict[str, str]:
        return self._config_manager.auth_headers


# Global instances for backward compatibility
config_manager = ConfigManager()
config = Config()
