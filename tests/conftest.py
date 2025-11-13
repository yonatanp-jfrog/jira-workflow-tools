"""
Pytest configuration and shared fixtures for Jira Workflow Tools tests.

This file provides common test fixtures and configuration
for all test modules in the project.
"""

import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import Mock, patch


@pytest.fixture(scope="session")
def project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def test_fixtures_dir(project_root):
    """Get the test fixtures directory."""
    return project_root / "tests" / "fixtures"


@pytest.fixture(scope="session")
def sample_config_data(test_fixtures_dir):
    """Load sample configuration data from fixtures."""
    config_file = test_fixtures_dir / "sample_configs.yaml"
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)


@pytest.fixture
def mock_jira_config(sample_config_data):
    """Provide mock Jira configuration for testing."""
    return sample_config_data['test_configurations']['valid_config']


@pytest.fixture
def mock_rtdev_config(sample_config_data):
    """Provide mock RTDEV project configuration."""
    return sample_config_data['test_configurations']['rtdev_config']


@pytest.fixture
def mock_app_config(sample_config_data):
    """Provide mock APP project configuration."""
    return sample_config_data['test_configurations']['app_config']


@pytest.fixture
def sample_issue_response(sample_config_data):
    """Provide sample issue response data."""
    return sample_config_data['test_responses']['successful_issue']


@pytest.fixture
def template_test_context(sample_config_data):
    """Provide template test context data."""
    return sample_config_data['template_test_data']['epic_context']


@pytest.fixture
def temp_template_dir():
    """Create a temporary directory for template testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)


@pytest.fixture
def mock_requests_get():
    """Mock requests.get for HTTP testing."""
    with patch('requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_requests_post():
    """Mock requests.post for HTTP testing."""
    with patch('requests.post') as mock_post:
        yield mock_post


@pytest.fixture
def mock_successful_jira_response():
    """Mock a successful Jira API response."""
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
    return mock_response


@pytest.fixture
def mock_jira_client_success():
    """Mock JiraClient with successful responses."""
    with patch('jira_tools.core.client.JiraClient') as mock_client:
        client_instance = Mock()
        client_instance.test_connection.return_value = True
        client_instance.get_issue.return_value = {
            'key': 'TEST-123',
            'fields': {'summary': 'Test Issue'}
        }
        client_instance.get_issue_url.return_value = 'https://test.atlassian.net/browse/TEST-123'
        mock_client.return_value = client_instance
        yield client_instance


@pytest.fixture
def valid_epic_template():
    """Provide a valid epic template for testing."""
    return '''
{
  "fields": {
    "project": {
      "id": "{{ project.id }}"
    },
    "summary": "{{ epic.name }}",
    "description": "{{ epic.description | default('TBD') }}",
    "issuetype": {
      "id": "{{ issue_types.epic }}"
    },
    "priority": {
      "id": "{{ priorities[epic.priority] | default(priorities['4 - Normal']) }}"
    }
  }
}
    '''.strip()


@pytest.fixture
def invalid_epic_template():
    """Provide an invalid epic template for testing."""
    return '''
{
  "fields": {
    "summary": "{{ epic.name }}"
  }
}
    '''.strip()


@pytest.fixture
def mock_environment_config():
    """Mock environment variables for configuration testing."""
    env_vars = {
        'JIRA_BASE_URL': 'https://test.atlassian.net',
        'JIRA_AUTH_TOKEN': 'test-token',
        'JIRA_USER_ACCOUNT_ID': 'test-user-id'
    }
    
    with patch.dict('os.environ', env_vars):
        yield env_vars


@pytest.fixture
def clean_environment():
    """Provide a clean environment with no Jira variables set."""
    with patch.dict('os.environ', {}, clear=True):
        yield


# Test markers for categorizing tests
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "template: mark test as a template-related test"
    )
    config.addinivalue_line(
        "markers", "config: mark test as a configuration-related test"
    )
    config.addinivalue_line(
        "markers", "client: mark test as a client-related test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Skip integration tests by default unless explicitly requested
def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle markers."""
    if config.getoption("--integration"):
        # Don't skip anything if --integration is specified
        return
    
    skip_integration = pytest.mark.skip(reason="need --integration option to run")
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--integration",
        action="store_true",
        default=False,
        help="run integration tests"
    )
