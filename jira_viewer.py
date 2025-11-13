#!/usr/bin/env python3
"""
🚨 DEPRECATED SCRIPT 🚨

This script is DEPRECATED and will be removed on 2025-03-01.

👉 USE INSTEAD: python3 -m jira_tools viewer
📖 Migration Guide: See MIGRATION_GUIDE.md
🆕 New System: Enhanced viewer + URL parsing + multiple formats

Jira Ticket Viewer - A command-line tool for viewing Jira tickets in a readable format.

⚠️ WARNING: This file has missing dependencies (formatter module) and may not work correctly.
"""

import click
import re
import tempfile
import os
from rich.console import Console
from jira_client import JiraClient
from formatter import JiraFormatter, MarkdownFormatter


def extract_issue_key(input_str: str) -> str:
    """
    Extract issue key from either a direct key or a full Jira URL.
    
    Args:
        input_str: Either an issue key (e.g., 'RTDEV-55950') or full URL
        
    Returns:
        The extracted issue key
        
    Raises:
        ValueError: If no valid issue key can be extracted
    """
    # If it's already just an issue key, return it
    if re.match(r'^[A-Z]+-\d+$', input_str):
        return input_str
    
    # Try to extract from URL
    url_pattern = r'/browse/([A-Z]+-\d+)'
    match = re.search(url_pattern, input_str)
    if match:
        return match.group(1)
    
    # Try to extract issue key pattern from anywhere in the string
    key_pattern = r'([A-Z]+-\d+)'
    match = re.search(key_pattern, input_str)
    if match:
        return match.group(1)
    
    raise ValueError(f"Could not extract a valid issue key from: {input_str}")


@click.command()
@click.argument('issue_input', required=True)
@click.option('--url', '-u', is_flag=True, help='Also display the web URL for the issue')
@click.option('--raw', '-r', is_flag=True, help='Display raw JSON data instead of formatted output')
@click.option('--output', '-o', help='Output file path (default: creates temp file)')
def main(issue_input: str, url: bool, raw: bool, output: str):
    """
    Fetch and display a Jira ticket in a readable format.
    
    ISSUE_INPUT: The Jira issue key (e.g., RTDEV-55950) or full URL (e.g., https://jfrog-int.atlassian.net/browse/APP-671)
    """
    console = Console()
    
    # 🚨 DEPRECATION WARNING
    console.print("🚨 " + "="*70 + " 🚨", style="red")
    console.print("🚨 DEPRECATION WARNING: This script will be removed on 2025-03-01", style="red")
    console.print("🚨", style="red")
    console.print("🚨 👉 USE INSTEAD: python3 -m jira_tools viewer", style="red")
    console.print("🚨 📖 Migration Guide: See MIGRATION_GUIDE.md", style="red")
    console.print("🚨 🆕 New System: Enhanced viewer + URL parsing + multiple formats", style="red")
    console.print("🚨 " + "="*70 + " 🚨", style="red")
    console.print("")
    
    import click
    if not click.confirm("Continue with deprecated script?"):
        console.print("👍 Great choice! Use the new system: python3 -m jira_tools viewer")
        return
    
    # Extract issue key from input (handles both keys and URLs)
    try:
        issue_key = extract_issue_key(issue_input)
    except ValueError as e:
        console.print(f"❌ {e}", style="red")
        return
    
    # Initialize client and formatter
    client = JiraClient()
    formatter = JiraFormatter()
    
    # Display header
    if issue_input != issue_key:
        console.print(f"🎫 Fetching Jira ticket: {issue_key} (extracted from: {issue_input})", style="bold blue")
    else:
        console.print(f"🎫 Fetching Jira ticket: {issue_key}", style="bold blue")
    console.print()
    
    # Fetch the issue
    issue_data = client.get_issue(issue_key)
    
    if not issue_data:
        console.print("❌ Failed to fetch the issue. Please check the issue key and your credentials.", style="red")
        return
    
    # Display URL if requested
    if url:
        issue_url = client.get_issue_url(issue_key)
        console.print(f"🔗 Web URL: {issue_url}")
        console.print()
    
    # Create output file path
    if output:
        output_file = output
    else:
        # Create temporary markdown file in dedicated output directory
        output_dir = "Published Issues"
        os.makedirs(output_dir, exist_ok=True)
        
        # Get summary for filename
        summary = issue_data.get('fields', {}).get('summary', 'No Summary')
        # Clean summary for filename (remove invalid characters)
        clean_summary = "".join(c for c in summary if c.isalnum() or c in (' ', '-', '_')).strip()
        # Replace multiple spaces with single space and limit length
        clean_summary = ' '.join(clean_summary.split())[:50]
        
        filename = f"{issue_key}: {clean_summary}.md"
        output_file = os.path.join(output_dir, filename)
    
    # Display the issue and write to file
    if raw:
        console.print_json(data=issue_data)
        # Write raw JSON to file
        with open(output_file, 'w', encoding='utf-8') as f:
            import json
            json.dump(issue_data, f, indent=2, ensure_ascii=False)
    else:
        # Create markdown formatter and write to file
        md_formatter = MarkdownFormatter()
        markdown_content = md_formatter.format_issue_to_markdown(
            issue_data, 
            issue_key=issue_key,
            issue_url=client.get_issue_url(issue_key) if url else None
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Display to console
        formatter.format_issue(issue_data)
    
    console.print(f"📄 Output written to: {output_file}", style="cyan")
    console.print("✅ Done!", style="green")


if __name__ == '__main__':
    main()
