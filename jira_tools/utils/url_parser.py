"""
URL parsing utilities for Jira issue keys.

This module provides functionality to extract Jira issue keys from various
input formats including direct keys and full Jira URLs.
"""

import re
from typing import Optional


def extract_issue_key(input_str: str) -> str:
    """
    Extract issue key from either a direct key or a full Jira URL.
    
    This function handles multiple input formats:
    - Direct issue key: 'RTDEV-55950'
    - Full Jira URL: 'https://company.atlassian.net/browse/RTDEV-55950'
    - Browse URL: '/browse/RTDEV-55950'
    - Any text containing an issue key pattern
    
    Args:
        input_str: Either an issue key (e.g., 'RTDEV-55950') or full URL
        
    Returns:
        The extracted issue key
        
    Raises:
        ValueError: If no valid issue key can be extracted
        
    Examples:
        >>> extract_issue_key('RTDEV-55950')
        'RTDEV-55950'
        >>> extract_issue_key('https://company.atlassian.net/browse/APP-12345')
        'APP-12345'
        >>> extract_issue_key('/browse/TEST-999')
        'TEST-999'
    """
    if not input_str or not isinstance(input_str, str):
        raise ValueError("Input must be a non-empty string")
    
    # Clean up the input string
    input_str = input_str.strip()
    
    # If it's already just an issue key, return it
    direct_key_match = re.match(r'^[A-Z]+-\d+$', input_str)
    if direct_key_match:
        return input_str
    
    # Try to extract from URL (most specific to least specific)
    
    # 1. Full Jira URL pattern
    url_patterns = [
        r'/browse/([A-Z]+-\d+)',  # /browse/ISSUE-123
        r'selectedIssue=([A-Z]+-\d+)',  # ?selectedIssue=ISSUE-123
        r'issuekey=([A-Z]+-\d+)',  # ?issuekey=ISSUE-123
        r'/([A-Z]+-\d+)(?:/|$)',  # /ISSUE-123/ or /ISSUE-123 at end
    ]
    
    for pattern in url_patterns:
        match = re.search(pattern, input_str)
        if match:
            return match.group(1)
    
    # 2. General issue key pattern anywhere in the string
    key_pattern = r'([A-Z]+-\d+)'
    match = re.search(key_pattern, input_str)
    if match:
        return match.group(1)
    
    # If nothing found, provide helpful error message
    raise ValueError(
        f"Could not extract a valid issue key from: '{input_str}'\n"
        f"Expected formats:\n"
        f"  - Direct key: RTDEV-12345\n"  
        f"  - Full URL: https://company.atlassian.net/browse/RTDEV-12345\n"
        f"  - Browse path: /browse/RTDEV-12345"
    )


def validate_issue_key(issue_key: str) -> bool:
    """
    Validate that a string is a properly formatted Jira issue key.
    
    Args:
        issue_key: String to validate
        
    Returns:
        True if the string is a valid issue key format, False otherwise
        
    Examples:
        >>> validate_issue_key('RTDEV-12345')
        True
        >>> validate_issue_key('invalid-key')
        False
    """
    if not issue_key or not isinstance(issue_key, str):
        return False
    
    # Jira issue key pattern: PROJECT-NUMBER
    # Project key: 1+ uppercase letters
    # Number: 1+ digits
    pattern = r'^[A-Z]+-\d+$'
    return bool(re.match(pattern, issue_key.strip()))


def normalize_jira_url(url: str, base_url: str) -> str:
    """
    Normalize a Jira URL to ensure it's properly formatted.
    
    Args:
        url: Input URL (may be partial)
        base_url: Base Jira URL (e.g., 'https://company.atlassian.net')
        
    Returns:
        Fully qualified Jira URL
        
    Examples:
        >>> normalize_jira_url('/browse/RTDEV-123', 'https://company.atlassian.net')
        'https://company.atlassian.net/browse/RTDEV-123'
    """
    if not url:
        return ''
    
    # If already a full URL, return as-is
    if url.startswith(('http://', 'https://')):
        return url
    
    # Remove leading slash if present
    if url.startswith('/'):
        url = url[1:]
    
    # Ensure base URL doesn't end with slash
    base_url = base_url.rstrip('/')
    
    return f"{base_url}/{url}"


def build_jira_url(issue_key: str, base_url: str) -> str:
    """
    Build a Jira browse URL for an issue key.
    
    Args:
        issue_key: Jira issue key (e.g., 'RTDEV-12345')
        base_url: Base Jira URL (e.g., 'https://company.atlassian.net')
        
    Returns:
        Full browse URL for the issue
        
    Examples:
        >>> build_jira_url('RTDEV-12345', 'https://company.atlassian.net')
        'https://company.atlassian.net/browse/RTDEV-12345'
    """
    if not validate_issue_key(issue_key):
        raise ValueError(f"Invalid issue key: {issue_key}")
    
    base_url = base_url.rstrip('/')
    return f"{base_url}/browse/{issue_key}"


def extract_project_key(issue_key: str) -> str:
    """
    Extract the project key portion from an issue key.
    
    Args:
        issue_key: Full issue key (e.g., 'RTDEV-12345')
        
    Returns:
        Project key portion (e.g., 'RTDEV')
        
    Raises:
        ValueError: If issue key is invalid
        
    Examples:
        >>> extract_project_key('RTDEV-12345')
        'RTDEV'
    """
    if not validate_issue_key(issue_key):
        raise ValueError(f"Invalid issue key: {issue_key}")
    
    return issue_key.split('-')[0]


def extract_issue_number(issue_key: str) -> int:
    """
    Extract the issue number portion from an issue key.
    
    Args:
        issue_key: Full issue key (e.g., 'RTDEV-12345')
        
    Returns:
        Issue number as integer (e.g., 12345)
        
    Raises:
        ValueError: If issue key is invalid
        
    Examples:
        >>> extract_issue_number('RTDEV-12345')
        12345
    """
    if not validate_issue_key(issue_key):
        raise ValueError(f"Invalid issue key: {issue_key}")
    
    return int(issue_key.split('-')[1])
