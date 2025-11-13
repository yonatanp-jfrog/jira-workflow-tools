"""Configuration management for Jira ticket viewer."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for Jira API settings."""
    
    def __init__(self):
        self.jira_base_url = os.getenv('JIRA_BASE_URL')
        self.jira_auth_token = os.getenv('JIRA_AUTH_TOKEN')
        
        # Validate required environment variables
        missing_vars = []
        if not self.jira_base_url:
            missing_vars.append('JIRA_BASE_URL')
        if not self.jira_auth_token:
            missing_vars.append('JIRA_AUTH_TOKEN')
        
        if missing_vars:
            raise ValueError(
                f"Required environment variables missing: {', '.join(missing_vars)}. "
                "Please set them in your .env file or environment."
            )
    
    @property
    def jira_api_base(self):
        """Get the base URL for Jira API calls."""
        return f"{self.jira_base_url}/rest/api/2"
    
    @property
    def auth_headers(self):
        """Get authentication headers for API requests."""
        return {
            "Authorization": f"Basic {self.jira_auth_token}",
            "Content-Type": "application/json"
        }

# Global config instance
config = Config()
