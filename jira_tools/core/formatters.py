"""
Issue formatters for different output types.

This module provides comprehensive formatting capabilities for Jira issues,
supporting console display, markdown export, JSON output, and file operations.
"""

import json
import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown


class JiraFormatter:
    """
    Rich console formatter for Jira issues.
    
    Provides beautiful, readable console output with colors, tables, and panels.
    """
    
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
    
    def format_issue(self, issue_data: Dict[str, Any], issue_key: str = None, issue_url: str = None) -> None:
        """
        Format and display a Jira issue to the console.
        
        Args:
            issue_data: Raw Jira issue data from API
            issue_key: Issue key (e.g., 'RTDEV-12345') 
            issue_url: Web URL to the issue (optional)
        """
        if not issue_data:
            self.console.print("❌ No issue data to display", style="red")
            return
        
        # Extract key if not provided
        if not issue_key:
            issue_key = issue_data.get('key', 'Unknown')
        
        # Extract basic fields
        fields = issue_data.get('fields', {})
        summary = fields.get('summary', 'No Summary')
        description = fields.get('description', 'No Description')
        
        # Status and priority
        status = fields.get('status', {}).get('name', 'Unknown')
        priority = fields.get('priority', {}).get('name', 'Unknown')
        issue_type = fields.get('issuetype', {}).get('name', 'Unknown')
        
        # Assignee and reporter
        assignee = fields.get('assignee')
        reporter = fields.get('reporter')
        assignee_name = assignee.get('displayName', 'Unassigned') if assignee else 'Unassigned'
        reporter_name = reporter.get('displayName', 'Unknown') if reporter else 'Unknown'
        
        # Dates
        created = fields.get('created', '')
        updated = fields.get('updated', '')
        if created:
            created = created.split('T')[0]  # Just the date part
        if updated:
            updated = updated.split('T')[0]  # Just the date part
        
        # Create main panel
        title = f"🎫 [bold cyan]{issue_key}[/bold cyan]: {summary}"
        
        # Create info table
        info_table = Table(show_header=False, box=None, padding=(0, 1))
        info_table.add_column("Field", style="bold magenta", no_wrap=True)
        info_table.add_column("Value", style="green")
        
        info_table.add_row("Status", f"[bold]{status}[/bold]")
        info_table.add_row("Type", issue_type)
        info_table.add_row("Priority", priority)
        info_table.add_row("Assignee", assignee_name)
        info_table.add_row("Reporter", reporter_name)
        
        if created:
            info_table.add_row("Created", created)
        if updated:
            info_table.add_row("Updated", updated)
        if issue_url:
            info_table.add_row("URL", f"[link={issue_url}]{issue_url}[/link]")
        
        # Display main info
        self.console.print(Panel(info_table, title=title, border_style="blue"))
        
        # Display description if available
        if description and description != 'No Description':
            self.console.print("\n📝 [bold]Description:[/bold]")
            
            # Try to render as markdown if it looks like markdown
            if any(marker in description for marker in ['#', '*', '`', '[', ']']):
                try:
                    self.console.print(Markdown(description))
                except Exception:
                    # Fallback to plain text if markdown parsing fails
                    self.console.print(description)
            else:
                self.console.print(description)
        
        # Display custom fields if present
        custom_fields = self._extract_custom_fields(fields)
        if custom_fields:
            self.console.print("\n🔧 [bold]Custom Fields:[/bold]")
            
            custom_table = Table(show_header=True, header_style="bold magenta")
            custom_table.add_column("Field", style="cyan")
            custom_table.add_column("Value", style="green")
            
            for field_name, field_value in custom_fields.items():
                custom_table.add_row(field_name, str(field_value))
            
            self.console.print(custom_table)
    
    def _extract_custom_fields(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """Extract and format custom fields from issue data."""
        custom_fields = {}
        
        # Look for customfield_ entries
        for field_key, field_value in fields.items():
            if field_key.startswith('customfield_') and field_value is not None:
                # Try to get a friendly name, fallback to field key
                field_name = field_key
                
                # Format the value based on type
                if isinstance(field_value, dict):
                    if 'name' in field_value:
                        formatted_value = field_value['name']
                    elif 'displayName' in field_value:
                        formatted_value = field_value['displayName']
                    else:
                        formatted_value = str(field_value)
                elif isinstance(field_value, list):
                    if field_value and isinstance(field_value[0], dict):
                        formatted_value = ', '.join([
                            item.get('name', item.get('displayName', str(item))) 
                            for item in field_value
                        ])
                    else:
                        formatted_value = ', '.join(str(item) for item in field_value)
                else:
                    formatted_value = str(field_value)
                
                custom_fields[field_name] = formatted_value
        
        return custom_fields


class MarkdownFormatter:
    """
    Markdown formatter for Jira issues.
    
    Converts Jira issues to well-formatted markdown suitable for documentation,
    reports, or file export.
    """
    
    def format_issue_to_markdown(self, issue_data: Dict[str, Any], 
                                issue_key: str = None, 
                                issue_url: str = None) -> str:
        """
        Format a Jira issue as markdown.
        
        Args:
            issue_data: Raw Jira issue data from API
            issue_key: Issue key (e.g., 'RTDEV-12345')
            issue_url: Web URL to the issue (optional)
            
        Returns:
            Formatted markdown string
        """
        if not issue_data:
            return "# Error\n\nNo issue data provided."
        
        # Extract key if not provided
        if not issue_key:
            issue_key = issue_data.get('key', 'Unknown')
        
        # Extract basic fields
        fields = issue_data.get('fields', {})
        summary = fields.get('summary', 'No Summary')
        description = fields.get('description', 'No Description')
        
        # Status and priority
        status = fields.get('status', {}).get('name', 'Unknown')
        priority = fields.get('priority', {}).get('name', 'Unknown')
        issue_type = fields.get('issuetype', {}).get('name', 'Unknown')
        
        # Assignee and reporter
        assignee = fields.get('assignee')
        reporter = fields.get('reporter')
        assignee_name = assignee.get('displayName', 'Unassigned') if assignee else 'Unassigned'
        reporter_name = reporter.get('displayName', 'Unknown') if reporter else 'Unknown'
        
        # Dates
        created = fields.get('created', 'Unknown')
        updated = fields.get('updated', 'Unknown')
        
        # Build markdown
        lines = [
            f"# {issue_key}: {summary}",
            "",
            "## Issue Information",
            "",
            f"- **Status:** {status}",
            f"- **Type:** {issue_type}", 
            f"- **Priority:** {priority}",
            f"- **Assignee:** {assignee_name}",
            f"- **Reporter:** {reporter_name}",
            f"- **Created:** {created}",
            f"- **Updated:** {updated}",
        ]
        
        if issue_url:
            lines.extend([
                f"- **URL:** [{issue_key}]({issue_url})",
            ])
        
        # Add description
        if description and description != 'No Description':
            lines.extend([
                "",
                "## Description",
                "",
                description
            ])
        
        # Add custom fields
        custom_fields = self._extract_custom_fields_for_markdown(fields)
        if custom_fields:
            lines.extend([
                "",
                "## Custom Fields",
                ""
            ])
            
            for field_name, field_value in custom_fields.items():
                lines.append(f"- **{field_name}:** {field_value}")
        
        # Add metadata
        lines.extend([
            "",
            "---",
            "",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by Jira Workflow Tools*"
        ])
        
        return "\n".join(lines)
    
    def _extract_custom_fields_for_markdown(self, fields: Dict[str, Any]) -> Dict[str, str]:
        """Extract and format custom fields for markdown output."""
        custom_fields = {}
        
        for field_key, field_value in fields.items():
            if field_key.startswith('customfield_') and field_value is not None:
                # Format the value
                if isinstance(field_value, dict):
                    if 'name' in field_value:
                        formatted_value = field_value['name']
                    elif 'displayName' in field_value:
                        formatted_value = field_value['displayName']
                    else:
                        formatted_value = str(field_value)
                elif isinstance(field_value, list):
                    if field_value and isinstance(field_value[0], dict):
                        formatted_value = ', '.join([
                            item.get('name', item.get('displayName', str(item))) 
                            for item in field_value
                        ])
                    else:
                        formatted_value = ', '.join(str(item) for item in field_value)
                else:
                    formatted_value = str(field_value)
                
                custom_fields[field_key] = formatted_value
        
        return custom_fields


class JSONFormatter:
    """
    JSON formatter for Jira issues.
    
    Provides clean, pretty-printed JSON output for programmatic consumption
    or detailed inspection.
    """
    
    def format_issue_to_json(self, issue_data: Dict[str, Any], indent: int = 2) -> str:
        """
        Format a Jira issue as pretty-printed JSON.
        
        Args:
            issue_data: Raw Jira issue data from API
            indent: JSON indentation level
            
        Returns:
            Pretty-printed JSON string
        """
        if not issue_data:
            return json.dumps({"error": "No issue data provided"}, indent=indent)
        
        return json.dumps(issue_data, indent=indent, ensure_ascii=False, sort_keys=True)


class IssueFileManager:
    """
    Handles file operations for issue output.
    
    Manages output directories, file naming, and file writing operations.
    """
    
    def __init__(self, base_output_dir: str = ".jira-output"):
        self.base_output_dir = Path(base_output_dir)
    
    def save_issue_to_file(self, content: str, issue_key: str, 
                          output_format: str = "md", 
                          custom_path: Optional[str] = None) -> Path:
        """
        Save issue content to a file.
        
        Args:
            content: Formatted issue content
            issue_key: Issue key for filename generation
            output_format: File format extension ('md', 'json', 'txt')
            custom_path: Custom output path (optional)
            
        Returns:
            Path to the saved file
        """
        if custom_path:
            output_path = Path(custom_path)
        else:
            # Ensure output directory exists
            self.base_output_dir.mkdir(exist_ok=True)
            
            # Generate filename
            safe_key = "".join(c for c in issue_key if c.isalnum() or c in ('-', '_'))
            filename = f"{safe_key}.{output_format}"
            output_path = self.base_output_dir / filename
        
        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        output_path.write_text(content, encoding='utf-8')
        
        return output_path
    
    def create_temp_file(self, content: str, suffix: str = ".md") -> Path:
        """
        Create a temporary file with the given content.
        
        Args:
            content: Content to write
            suffix: File suffix/extension
            
        Returns:
            Path to temporary file
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False, encoding='utf-8') as f:
            f.write(content)
            temp_path = Path(f.name)
        
        return temp_path


# Global formatter instances for easy access
jira_formatter = JiraFormatter()
markdown_formatter = MarkdownFormatter() 
json_formatter = JSONFormatter()
file_manager = IssueFileManager()
