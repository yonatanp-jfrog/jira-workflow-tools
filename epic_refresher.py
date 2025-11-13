#!/usr/bin/env python3
"""
Epic Refresher - Keep local epic markdown files in sync with Jira.

This tool refreshes existing epic markdown files by:
- Fetching current data from Jira
- Updating file content with latest information
- Renaming files if epic name or project changed
- Removing files if epic was deleted
- Batch refresh all epics in Issues/ folder
"""

import click
import os
import re
import glob
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import requests
from config import config
from jira_client import JiraClient
from formatter import JiraFormatter, MarkdownFormatter


class EpicRefresher:
    """Refreshes epic markdown files to match current Jira state."""
    
    def __init__(self):
        self.issues_folder = Path("Published Issues")
        self.issues_folder.mkdir(exist_ok=True)
        
        # Jira configuration
        self.base_url = config.jira_base_url
        self.headers = config.auth_headers
        self.jira_client = JiraClient()
        self.formatter = JiraFormatter()
        self.markdown_formatter = MarkdownFormatter()
    
    def extract_epic_key_from_filename(self, filename: str) -> Optional[str]:
        """Extract epic key from markdown filename."""
        # Pattern: RTDEV-12345: Epic Name.md or APP-678: Epic Name.md
        match = re.match(r'^([A-Z]+-\d+):', filename)
        return match.group(1) if match else None
    
    def get_all_epic_files(self) -> List[Tuple[str, str]]:
        """Get all epic markdown files and their keys."""
        epic_files = []
        
        for file_path in self.issues_folder.glob("*.md"):
            epic_key = self.extract_epic_key_from_filename(file_path.name)
            if epic_key:
                epic_files.append((str(file_path), epic_key))
        
        return epic_files
    
    def check_epic_exists(self, epic_key: str) -> bool:
        """Check if epic still exists in Jira."""
        try:
            url = f"{self.base_url}/rest/api/2/issue/{epic_key}"
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False
    
    def get_epic_info(self, epic_key: str) -> Optional[Dict]:
        """Get current epic information from Jira."""
        try:
            url = f"{self.base_url}/rest/api/2/issue/{epic_key}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            click.echo(f"❌ Failed to fetch {epic_key}: {e}")
            return None
    
    def generate_expected_filename(self, epic_data: Dict) -> str:
        """Generate expected filename based on current epic data."""
        key = epic_data['key']
        summary = epic_data['fields']['summary']
        
        # Clean summary for filename
        safe_summary = "".join(c for c in summary if c.isalnum() or c in (' ', '-', '_', '&')).strip()
        safe_summary = re.sub(r'\s+', ' ', safe_summary)  # Normalize whitespace
        
        return f"{key}: {safe_summary}.md"
    
    def refresh_epic(self, epic_key: str, current_file_path: Optional[str] = None) -> Dict[str, str]:
        """
        Refresh a single epic.
        
        Returns:
            Dict with 'status', 'message', 'old_file', 'new_file'
        """
        
        # Check if epic exists
        if not self.check_epic_exists(epic_key):
            if current_file_path and os.path.exists(current_file_path):
                os.remove(current_file_path)
                return {
                    'status': 'deleted',
                    'message': f'Epic {epic_key} no longer exists - removed file',
                    'old_file': current_file_path,
                    'new_file': None
                }
            else:
                return {
                    'status': 'not_found',
                    'message': f'Epic {epic_key} not found in Jira',
                    'old_file': current_file_path,
                    'new_file': None
                }
        
        # Get current epic data
        epic_data = self.get_epic_info(epic_key)
        if not epic_data:
            return {
                'status': 'error',
                'message': f'Failed to fetch data for {epic_key}',
                'old_file': current_file_path,
                'new_file': None
            }
        
        # Generate new content using jira_client and formatter
        try:
            # Generate the markdown content directly
            markdown_content = self.markdown_formatter.format_issue_to_markdown(epic_data, issue_key=epic_key)
            
            # Determine the filename
            expected_filename = self.generate_expected_filename(epic_data)
            new_file_path = self.issues_folder / expected_filename
            
            # Write the updated content
            with open(new_file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Handle file renaming if needed
            if current_file_path and os.path.exists(current_file_path):
                current_filename = os.path.basename(current_file_path)
                if current_filename != expected_filename:
                    # Rename the file
                    if new_file_path.exists():
                        # If target exists, remove old file
                        os.remove(current_file_path)
                    else:
                        # Rename to new name
                        os.rename(current_file_path, new_file_path)
                    
                    return {
                        'status': 'renamed',
                        'message': f'Epic {epic_key} renamed: {current_filename} → {expected_filename}',
                        'old_file': current_file_path,
                        'new_file': str(new_file_path)
                    }
            
            return {
                'status': 'updated',
                'message': f'Epic {epic_key} refreshed successfully',
                'old_file': current_file_path,
                'new_file': str(new_file_path)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Failed to refresh {epic_key}: {e}',
                'old_file': current_file_path,
                'new_file': None
            }
    
    def refresh_all_epics(self) -> Dict[str, List[Dict]]:
        """
        Refresh all epic files in the Issues folder.
        
        Returns:
            Dict with lists of results by status
        """
        
        results = {
            'updated': [],
            'renamed': [],
            'deleted': [],
            'error': [],
            'not_found': []
        }
        
        epic_files = self.get_all_epic_files()
        
        if not epic_files:
            click.echo("📭 No epic files found in Issues/ folder")
            return results
        
        click.echo(f"🔄 Refreshing {len(epic_files)} epic files...")
        
        for file_path, epic_key in epic_files:
            click.echo(f"🔍 Checking {epic_key}...", nl=False)
            
            result = self.refresh_epic(epic_key, file_path)
            results[result['status']].append(result)
            
            # Status indicator
            status_emoji = {
                'updated': '✅',
                'renamed': '📝',
                'deleted': '🗑️',
                'error': '❌',
                'not_found': '❓'
            }
            
            click.echo(f" {status_emoji.get(result['status'], '❓')}")
        
        return results
    
    def print_refresh_summary(self, results: Dict[str, List[Dict]]):
        """Print a summary of refresh results."""
        
        total = sum(len(results[status]) for status in results)
        
        click.echo(f"\n📊 Refresh Summary ({total} files processed):")
        click.echo("=" * 50)
        
        if results['updated']:
            click.echo(f"✅ Updated: {len(results['updated'])} files")
            for result in results['updated']:
                epic_key = self.extract_epic_key_from_filename(os.path.basename(result['new_file']))
                click.echo(f"   📄 {epic_key}")
        
        if results['renamed']:
            click.echo(f"📝 Renamed: {len(results['renamed'])} files")
            for result in results['renamed']:
                old_name = os.path.basename(result['old_file'])
                new_name = os.path.basename(result['new_file'])
                click.echo(f"   📝 {old_name} → {new_name}")
        
        if results['deleted']:
            click.echo(f"🗑️  Deleted: {len(results['deleted'])} files")
            for result in results['deleted']:
                epic_key = self.extract_epic_key_from_filename(os.path.basename(result['old_file']))
                click.echo(f"   🗑️  {epic_key} (epic no longer exists)")
        
        if results['error']:
            click.echo(f"❌ Errors: {len(results['error'])} files")
            for result in results['error']:
                epic_key = self.extract_epic_key_from_filename(os.path.basename(result['old_file'] or ''))
                click.echo(f"   ❌ {epic_key}: {result['message']}")
        
        if results['not_found']:
            click.echo(f"❓ Not Found: {len(results['not_found'])} files")
            for result in results['not_found']:
                click.echo(f"   ❓ {result['message']}")
        
        # Summary stats
        success_count = len(results['updated']) + len(results['renamed'])
        if success_count > 0:
            click.echo(f"\n🎉 Successfully refreshed {success_count} epics!")
        
        if results['deleted']:
            click.echo(f"🧹 Cleaned up {len(results['deleted'])} deleted epics")


# CLI Commands
@click.group()
def cli():
    """Epic Refresher - Keep local epic files in sync with Jira."""
    pass


@cli.command()
@click.argument('epic_key', required=True)
def refresh(epic_key: str):
    """
    Refresh a single epic markdown file.
    
    EPIC_KEY: The Jira epic key (e.g., RTDEV-12345)
    """
    
    refresher = EpicRefresher()
    
    # Find existing file for this epic
    epic_files = refresher.get_all_epic_files()
    current_file = None
    
    for file_path, key in epic_files:
        if key.upper() == epic_key.upper():
            current_file = file_path
            break
    
    click.echo(f"🔄 Refreshing epic: {epic_key}")
    
    result = refresher.refresh_epic(epic_key, current_file)
    
    # Display result
    status_emoji = {
        'updated': '✅',
        'renamed': '📝',
        'deleted': '🗑️',
        'error': '❌',
        'not_found': '❓'
    }
    
    emoji = status_emoji.get(result['status'], '❓')
    click.echo(f"{emoji} {result['message']}")
    
    if result['status'] == 'renamed':
        click.echo(f"📁 Old file: {result['old_file']}")
        click.echo(f"📁 New file: {result['new_file']}")
    elif result['status'] in ['updated', 'renamed'] and result['new_file']:
        click.echo(f"📁 File: {result['new_file']}")


@cli.command()
@click.option('--dry-run', is_flag=True, help='Show what would be refreshed without making changes')
def refresh_all(dry_run: bool):
    """
    Refresh all epic markdown files in the Issues folder.
    """
    
    refresher = EpicRefresher()
    
    if dry_run:
        click.echo("🔍 DRY RUN - Checking all epic files...")
        epic_files = refresher.get_all_epic_files()
        
        if not epic_files:
            click.echo("📭 No epic files found in Issues/ folder")
            return
        
        click.echo(f"📋 Found {len(epic_files)} epic files:")
        
        for file_path, epic_key in epic_files:
            exists = refresher.check_epic_exists(epic_key)
            status = "✅ Exists" if exists else "❌ Deleted"
            click.echo(f"   {epic_key}: {status}")
            
            if exists:
                epic_data = refresher.get_epic_info(epic_key)
                if epic_data:
                    expected_filename = refresher.generate_expected_filename(epic_data)
                    current_filename = os.path.basename(file_path)
                    if current_filename != expected_filename:
                        click.echo(f"      📝 Would rename: {current_filename} → {expected_filename}")
        
        click.echo(f"\n🔍 DRY RUN complete. Use 'refresh-all' without --dry-run to apply changes.")
        return
    
    # Actual refresh
    results = refresher.refresh_all_epics()
    refresher.print_refresh_summary(results)


@cli.command()
def status():
    """
    Show status of all epic files without refreshing.
    """
    
    refresher = EpicRefresher()
    epic_files = refresher.get_all_epic_files()
    
    if not epic_files:
        click.echo("📭 No epic files found in Issues/ folder")
        return
    
    click.echo(f"📋 Epic Files Status ({len(epic_files)} files):")
    click.echo("=" * 50)
    
    stats = {'exists': 0, 'deleted': 0, 'needs_rename': 0, 'error': 0}
    
    for file_path, epic_key in epic_files:
        click.echo(f"🎫 {epic_key}: ", nl=False)
        
        if not refresher.check_epic_exists(epic_key):
            click.echo("❌ Deleted in Jira")
            stats['deleted'] += 1
            continue
        
        epic_data = refresher.get_epic_info(epic_key)
        if not epic_data:
            click.echo("❌ Error fetching data")
            stats['error'] += 1
            continue
        
        expected_filename = refresher.generate_expected_filename(epic_data)
        current_filename = os.path.basename(file_path)
        
        if current_filename != expected_filename:
            click.echo(f"📝 Needs rename: {current_filename} → {expected_filename}")
            stats['needs_rename'] += 1
        else:
            click.echo("✅ Up to date")
            stats['exists'] += 1
    
    # Summary
    click.echo(f"\n📊 Summary:")
    click.echo(f"✅ Up to date: {stats['exists']}")
    click.echo(f"📝 Need rename: {stats['needs_rename']}")
    click.echo(f"❌ Deleted: {stats['deleted']}")
    click.echo(f"❌ Errors: {stats['error']}")
    
    if stats['needs_rename'] > 0 or stats['deleted'] > 0:
        click.echo(f"\n💡 Run 'python3 epic_refresher.py refresh-all' to sync all files")


if __name__ == '__main__':
    cli()
