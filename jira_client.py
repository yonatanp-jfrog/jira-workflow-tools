"""Jira API client for fetching ticket information."""

import requests
from typing import Dict, Any, Optional
from config import config


class JiraClient:
    """Client for interacting with Jira API."""
    
    def __init__(self):
        self.base_url = config.jira_api_base
        self.headers = config.auth_headers
    
    def get_issue(self, issue_key: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a Jira issue by its key (e.g., 'RTDEV-55950').
        
        Args:
            issue_key: The Jira issue key
            
        Returns:
            Dictionary containing issue data, or None if not found
        """
        url = f"{self.base_url}/issue/{issue_key}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"❌ Issue {issue_key} not found")
                return None
            elif response.status_code == 401:
                print("❌ Authentication failed. Please check your credentials.")
                return None
            elif response.status_code == 403:
                print("❌ Access denied. You don't have permission to view this issue.")
                return None
            else:
                print(f"❌ HTTP Error {response.status_code}: {e}")
                return None
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return None
    
    def get_issue_url(self, issue_key: str) -> str:
        """Get the web URL for a Jira issue."""
        return f"{config.jira_base_url}/browse/{issue_key}"
