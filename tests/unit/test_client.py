"""
Unit tests for Jira client.

Tests the JiraClient class functionality with mocked responses
to avoid requiring actual Jira connections.
"""

import pytest
import json
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path

# Import the modules we're testing
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from jira_tools.core.client import JiraClient, JiraClientError, JiraAuthenticationError, JiraPermissionError, JiraNotFoundError
from jira_tools.core.config import ConfigManager


class TestJiraClient:
    """Test cases for JiraClient."""
    
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_client_initialization(self):
        """Test that JiraClient can be initialized."""
        config = ConfigManager()
        client = JiraClient(config)
        
        assert client is not None
        assert client.config == config
        assert client.session is not None
    
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_client_initialization_default_config(self):
        """Test client initialization with default config."""
        client = JiraClient()
        
        assert client is not None
        assert client.config is not None
    
    @patch('jira_tools.core.client.requests.Session.get')
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_get_issue_success(self, mock_get):
        """Test successful issue retrieval."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'key': 'TEST-123',
            'fields': {
                'summary': 'Test Issue',
                'status': {'name': 'Open'},
                'issuetype': {'name': 'Epic'}
            }
        }
        mock_get.return_value = mock_response
        
        client = JiraClient()
        result = client.get_issue('TEST-123')
        
        assert result is not None
        assert result['key'] == 'TEST-123'
        assert result['fields']['summary'] == 'Test Issue'
    
    @patch('jira_tools.core.client.requests.Session.get')
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_get_issue_not_found(self, mock_get):
        """Test issue not found error."""
        # Mock 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404")
        mock_get.return_value = mock_response
        
        client = JiraClient()
        
        with pytest.raises(JiraNotFoundError, match="not found"):
            client.get_issue('NONEXISTENT-123')
    
    @patch('jira_tools.core.client.requests.Session.get')
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_get_issue_authentication_error(self, mock_get):
        """Test authentication error."""
        # Mock 401 response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = Exception("401")
        mock_get.return_value = mock_response
        
        client = JiraClient()
        
        with pytest.raises(JiraAuthenticationError, match="Authentication failed"):
            client.get_issue('TEST-123')
    
    @patch('jira_tools.core.client.requests.Session.get')
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_get_issue_permission_error(self, mock_get):
        """Test permission error."""
        # Mock 403 response
        mock_response = Mock()
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = Exception("403")
        mock_get.return_value = mock_response
        
        client = JiraClient()
        
        with pytest.raises(JiraPermissionError, match="Access denied"):
            client.get_issue('TEST-123')
    
    @patch('jira_tools.core.client.requests.Session.post')
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_create_issue_success(self, mock_post):
        """Test successful issue creation."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            'key': 'TEST-124',
            'id': '12345'
        }
        mock_post.return_value = mock_response
        
        client = JiraClient()
        
        issue_data = {
            'fields': {
                'project': {'id': '10001'},
                'summary': 'New Test Issue',
                'issuetype': {'id': '10000'}
            }
        }
        
        result = client.create_issue(issue_data)
        
        assert result is not None
        assert result['key'] == 'TEST-124'
        assert 'web_url' in result
        assert 'TEST-124' in result['web_url']
    
    @patch('jira_tools.core.client.requests.Session.post')
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_create_issue_validation_error(self, mock_post):
        """Test issue creation with validation error."""
        # Mock 400 response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'errorMessages': ['Summary is required']
        }
        mock_response.raise_for_status.side_effect = Exception("400")
        mock_post.return_value = mock_response
        
        client = JiraClient()
        
        issue_data = {
            'fields': {
                'project': {'id': '10001'},
                'issuetype': {'id': '10000'}
                # Missing required summary
            }
        }
        
        with pytest.raises(JiraClientError, match="Invalid issue data"):
            client.create_issue(issue_data)
    
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_get_issue_url(self):
        """Test issue URL generation."""
        client = JiraClient()
        
        url = client.get_issue_url('TEST-123')
        
        assert url == 'https://test.atlassian.net/browse/TEST-123'
    
    @patch('jira_tools.core.client.requests.Session.get')
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_search_issues(self, mock_get):
        """Test JQL search functionality."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'issues': [
                {
                    'key': 'TEST-123',
                    'fields': {'summary': 'Test Issue 1'}
                },
                {
                    'key': 'TEST-124', 
                    'fields': {'summary': 'Test Issue 2'}
                }
            ]
        }
        mock_get.return_value = mock_response
        
        client = JiraClient()
        
        results = client.search_issues('project = TEST')
        
        assert len(results) == 2
        assert results[0]['key'] == 'TEST-123'
        assert results[1]['key'] == 'TEST-124'
    
    @patch('jira_tools.core.client.requests.Session.get')
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_test_connection_success(self, mock_get):
        """Test successful connection test."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        client = JiraClient()
        
        result = client.test_connection()
        
        assert result is True
    
    @patch('jira_tools.core.client.requests.Session.get')
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_test_connection_failure(self, mock_get):
        """Test failed connection test."""
        # Mock failed response
        mock_get.side_effect = Exception("Connection failed")
        
        client = JiraClient()
        
        result = client.test_connection()
        
        assert result is False
    
    @patch('jira_tools.core.client.requests.Session.get')
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_get_user_info(self, mock_get):
        """Test user info retrieval."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'accountId': 'test-user-id',
            'displayName': 'Test User',
            'emailAddress': 'test@example.com'
        }
        mock_get.return_value = mock_response
        
        client = JiraClient()
        
        user_info = client.get_user_info()
        
        assert user_info is not None
        assert user_info['accountId'] == 'test-user-id'
        assert user_info['displayName'] == 'Test User'
    
    def test_input_validation(self):
        """Test input validation for client methods."""
        with patch.dict('os.environ', {
            'JIRA_BASE_URL': 'https://test.atlassian.net',
            'JIRA_AUTH_TOKEN': 'test-token'
        }):
            client = JiraClient()
            
            # Empty issue key
            with pytest.raises(ValueError, match="Issue key cannot be empty"):
                client.get_issue('')
            
            # Invalid issue data
            with pytest.raises(ValueError, match="Invalid issue data"):
                client.create_issue({})
            
            with pytest.raises(ValueError, match="Invalid issue data"):
                client.create_issue({'invalid': 'data'})
            
            # Empty JQL
            with pytest.raises(ValueError, match="JQL query cannot be empty"):
                client.search_issues('')
    
    @patch.dict('os.environ', {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_context_manager(self):
        """Test client as context manager."""
        with JiraClient() as client:
            assert client is not None
            assert client.session is not None
        
        # Session should be closed after context exit
        # (We can't easily test this without inspecting session internals)


if __name__ == '__main__':
    # Allow running tests directly
    pytest.main([__file__])
