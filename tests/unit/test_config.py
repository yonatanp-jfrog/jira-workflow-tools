"""
Unit tests for configuration management.

Tests the ConfigManager class and related functionality
without requiring actual Jira credentials.
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the modules we're testing
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from jira_tools.core.config import ConfigManager
from jira_tools.utils.exceptions import ConfigurationError


class TestConfigManager:
    """Test cases for ConfigManager."""
    
    def test_config_manager_initialization(self):
        """Test that ConfigManager can be initialized."""
        # This might fail if no config is available, which is expected
        try:
            config = ConfigManager()
            assert config is not None
            assert hasattr(config, 'config_source')
        except ValueError:
            # Expected if no configuration is available
            pass
    
    @patch.dict(os.environ, {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token',
        'JIRA_USER_ACCOUNT_ID': 'test-user-id'
    })
    def test_environment_configuration(self):
        """Test configuration from environment variables."""
        config = ConfigManager()
        
        assert config.config_source == 'environment'
        assert config.jira_base_url == 'https://test.atlassian.net'
        assert config.jira_auth_token == 'test-token'
        assert config.user_account_id == 'test-user-id'
        assert config.jira_api_base == 'https://test.atlassian.net/rest/api/2'
    
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_configuration(self):
        """Test behavior when configuration is missing."""
        config = ConfigManager()
        
        assert config.config_source == 'missing'
        
        # Should raise ValueError when trying to access properties
        with pytest.raises(ValueError, match="JIRA_BASE_URL not configured"):
            _ = config.jira_base_url
        
        with pytest.raises(ValueError, match="JIRA_AUTH_TOKEN not configured"):
            _ = config.jira_auth_token
    
    @patch.dict(os.environ, {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_auth_headers(self):
        """Test authentication headers generation."""
        config = ConfigManager()
        
        headers = config.auth_headers
        
        assert 'Authorization' in headers
        assert headers['Authorization'] == 'Basic test-token'
        assert headers['Content-Type'] == 'application/json'
    
    @patch.dict(os.environ, {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token'
    })
    def test_validate_config_success(self):
        """Test config validation with valid configuration."""
        config = ConfigManager()
        
        assert config.validate_config() is True
    
    @patch.dict(os.environ, {}, clear=True)
    def test_validate_config_failure(self):
        """Test config validation with invalid configuration."""
        config = ConfigManager()
        
        assert config.validate_config() is False
    
    @patch.dict(os.environ, {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token',
        'JIRA_USER_ACCOUNT_ID': 'test-user'
    })
    def test_get_config_info(self):
        """Test config information retrieval."""
        config = ConfigManager()
        
        info = config.get_config_info()
        
        assert info['source'] == 'environment'
        assert info['jira_url'] == 'https://test.atlassian.net'
        assert info['has_token'] is True
        assert info['has_user_id'] is True
        assert info['valid'] is True
    
    def test_legacy_config_compatibility(self):
        """Test that legacy Config class still works."""
        from jira_tools.core.config import Config
        
        # This might fail if no config is available, which is expected
        try:
            config = Config()
            assert config is not None
            assert hasattr(config, 'jira_base_url')
            assert hasattr(config, 'jira_auth_token')
        except ValueError:
            # Expected if no configuration is available
            pass


class TestConfigurationSources:
    """Test different configuration source detection."""
    
    def test_private_mode_detection(self):
        """Test private mode detection (will be expanded in Phase 4)."""
        # For now, just test that the detection doesn't crash
        config = ConfigManager()
        
        # Private mode isn't implemented yet, so should not be detected
        assert config.config_source != 'private'
    
    @patch.dict(os.environ, {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token',
        'JIRA_PRIVATE_MODE': 'false'
    })
    def test_environment_mode_explicit(self):
        """Test explicit environment mode selection."""
        config = ConfigManager()
        
        assert config.config_source == 'environment'


if __name__ == '__main__':
    # Allow running tests directly
    pytest.main([__file__])
