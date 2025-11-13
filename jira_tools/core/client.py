"""
Jira API client for secure ticket and epic management.

Provides a clean interface to Jira REST API with proper error handling,
security considerations, and team-focused functionality.
"""

import requests
from typing import Dict, Any, Optional, List
from .config import ConfigManager


class JiraClientError(Exception):
    """Base exception for Jira client errors."""
    pass


class JiraAuthenticationError(JiraClientError):
    """Raised when authentication fails."""
    pass


class JiraPermissionError(JiraClientError):
    """Raised when user lacks permissions."""
    pass


class JiraNotFoundError(JiraClientError):
    """Raised when resource is not found."""
    pass


class JiraClient:
    """
    Secure Jira API client with error handling and team features.
    
    Features:
    - Automatic configuration management
    - Proper error handling and user-friendly messages
    - Security-focused (no credential logging)
    - Team-optimized workflows
    """
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        Initialize Jira client.
        
        Args:
            config_manager: Optional config manager instance.
                          If None, uses global config manager.
        """
        self.config = config_manager or ConfigManager()
        self.session = requests.Session()
        self.session.headers.update(self.config.auth_headers)
    
    def get_issue(self, issue_key: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a Jira issue by its key.
        
        Args:
            issue_key: The Jira issue key (e.g., 'PROJ-123')
            
        Returns:
            Dictionary containing issue data, or None if not found
            
        Raises:
            JiraClientError: For various API errors
        """
        if not issue_key or not issue_key.strip():
            raise ValueError("Issue key cannot be empty")
        
        issue_key = issue_key.strip().upper()
        url = f"{self.config.jira_api_base}/issue/{issue_key}"
        
        try:
            response = self.session.get(url, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                raise JiraNotFoundError(f"Issue {issue_key} not found")
            elif response.status_code == 401:
                raise JiraAuthenticationError(
                    "Authentication failed. Please check your credentials."
                )
            elif response.status_code == 403:
                raise JiraPermissionError(
                    f"Access denied to issue {issue_key}. "
                    "You may not have permission to view this issue."
                )
            else:
                response.raise_for_status()
                
        except requests.exceptions.Timeout:
            raise JiraClientError(f"Timeout while fetching issue {issue_key}")
        except requests.exceptions.ConnectionError:
            raise JiraClientError(
                f"Connection error. Please check your network and Jira URL: "
                f"{self.config.jira_base_url}"
            )
        except requests.exceptions.RequestException as e:
            raise JiraClientError(f"Request failed: {e}")
    
    def create_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new Jira issue.
        
        Args:
            issue_data: Issue creation payload
            
        Returns:
            Dictionary containing created issue information
            
        Raises:
            JiraClientError: For various API errors
        """
        if not issue_data or 'fields' not in issue_data:
            raise ValueError("Invalid issue data: 'fields' key required")
        
        url = f"{self.config.jira_api_base}/issue/"
        
        try:
            response = self.session.post(url, json=issue_data, timeout=30)
            
            if response.status_code == 201:
                result = response.json()
                # Add web URL for convenience
                if 'key' in result:
                    result['web_url'] = self.get_issue_url(result['key'])
                return result
            elif response.status_code == 400:
                error_details = response.json().get('errorMessages', ['Unknown error'])
                raise JiraClientError(f"Invalid issue data: {', '.join(error_details)}")
            elif response.status_code == 401:
                raise JiraAuthenticationError("Authentication failed")
            elif response.status_code == 403:
                raise JiraPermissionError("Insufficient permissions to create issues")
            else:
                response.raise_for_status()
                
        except requests.exceptions.Timeout:
            raise JiraClientError("Timeout while creating issue")
        except requests.exceptions.ConnectionError:
            raise JiraClientError("Connection error while creating issue")
        except requests.exceptions.RequestException as e:
            raise JiraClientError(f"Request failed: {e}")
    
    def get_issue_url(self, issue_key: str) -> str:
        """Get the web URL for a Jira issue."""
        return f"{self.config.jira_base_url}/browse/{issue_key}"
    
    def search_issues(self, jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Search for issues using JQL.
        
        Args:
            jql: JQL query string
            max_results: Maximum number of results to return
            
        Returns:
            List of issue dictionaries
            
        Raises:
            JiraClientError: For various API errors
        """
        if not jql or not jql.strip():
            raise ValueError("JQL query cannot be empty")
        
        url = f"{self.config.jira_api_base}/search"
        params = {
            'jql': jql.strip(),
            'maxResults': max_results,
            'fields': 'key,summary,status,priority,assignee,created,updated'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('issues', [])
            elif response.status_code == 400:
                raise JiraClientError(f"Invalid JQL query: {jql}")
            else:
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            raise JiraClientError(f"Search failed: {e}")
    
    def test_connection(self) -> bool:
        """
        Test the connection to Jira.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            url = f"{self.config.jira_api_base}/myself"
            response = self.session.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_user_info(self) -> Optional[Dict[str, Any]]:
        """
        Get current user information.
        
        Returns:
            User information dictionary or None if failed
        """
        try:
            url = f"{self.config.jira_api_base}/myself"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except requests.exceptions.RequestException:
            return None
    
    def close(self):
        """Close the HTTP session."""
        if self.session:
            self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
