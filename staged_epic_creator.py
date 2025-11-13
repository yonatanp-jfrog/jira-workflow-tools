#!/usr/bin/env python3
"""
Staged Epic Creator - A two-phase workflow for creating Jira epics.

Phase 1: Create staged epic as markdown file for review and editing
Phase 2: Submit approved staged epic to Jira

This allows for collaboration, review, and refinement before actual epic creation.
"""

import click
import os
import json
import yaml
import re
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import requests
from config import config
from jira_tools.core.formatters import jira_formatter

# Rich library for enhanced CLI
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import filesize

console = Console()


class StagedEpicCreator:
    """Creates and manages staged epics with two-phase workflow."""
    
    # Project-specific defaults (same as epic_creator.py)
    PROJECT_DEFAULTS = {
        'RTDEV': {
            'team': 'dev-artifactory-lifecycle',
            'team_id': '10145',
            'project_id': '10129'
        },
        'APP': {
            'team': 'App Core',
            'team_id': '12980',
            'project_id': '10246'
        }
    }
    
    def __init__(self):
        self.staged_folder = Path("staged-issues")
        self.staged_folder.mkdir(exist_ok=True)
        
        # Jira configuration
        self.base_url = config.jira_base_url
        self.headers = config.auth_headers
        self.current_user_account_id = "712020:23cfbba9-878d-4391-8207-d6a32f87cb61"  # Yonatan Philip
    
    def _get_quarter_prefix(self, project: str) -> str:
        """Get the appropriate quarter prefix for the project"""
        # Using Q4 2025 as current quarter - update this as needed
        year = "25"
        quarter = "Q4"
        
        if project == "APP":
            return f"App {year}{quarter} - "
        elif project == "RTDEV":
            return f"RLM {year}{quarter} - "
        else:
            return ""
    
    def create_staged_epic(self, 
                          project: str,
                          epic_name: str,
                          description: str = "TBD",
                          team: Optional[str] = None,
                          product_backlog: str = "Q4-25-Backlog",
                          product_manager: str = "Yonatan Philip",
                          priority: str = "4 - Normal",
                          commitment_level: str = "Soft Commitment",
                          parent: Optional[str] = None,
                          product_priority: Optional[str] = None,
                          assigned_architect: Optional[str] = None,
                          assigned_ux: str = "Omer Morag",
                          assigned_technical_writer: str = "Michael Berman",
                          required_doc: str = "Yes",
                          release_notes: str = "Yes") -> str:
        """
        Create a staged epic as a markdown file.
        
        Returns:
            Path to the created staged epic file
        """
        
        # Normalize project key
        project = project.upper()
        
        # Validate project
        if project not in self.PROJECT_DEFAULTS:
            raise ValueError(f"Unsupported project: {project}. Supported projects: {list(self.PROJECT_DEFAULTS.keys())}")
        
        # Add quarter prefix to epic name
        quarter_prefix = self._get_quarter_prefix(project)
        if not epic_name.startswith(quarter_prefix):
            epic_name = quarter_prefix + epic_name
        
        # Get project defaults
        project_defaults = self.PROJECT_DEFAULTS[project]
        
        # Use team default if not specified
        if team is None:
            team = project_defaults['team']
        
        # Create epic metadata
        epic_metadata = {
            'project': project,
            'epic_name': epic_name,
            'description': description,
            'team': team,
            'product_backlog': product_backlog,
            'product_manager': product_manager,
            'priority': priority,
            'commitment_level': commitment_level,
            'parent': parent,
            'product_priority': product_priority,
            'assigned_architect': assigned_architect,
            'assigned_ux': assigned_ux,
            'assigned_technical_writer': assigned_technical_writer,
            'required_doc': required_doc,
            'release_notes': release_notes,
            'created_date': datetime.now().isoformat(),
            'status': 'staged',
            'project_defaults': project_defaults
        }
        
        # Generate filename - just project and title (no timestamp or numbers)
        safe_name = "".join(c for c in epic_name if c.isalnum() or c in (' ', '-', '_', '&')).strip()
        safe_name = re.sub(r'\s+', ' ', safe_name)  # Normalize whitespace
        filename = f"{project}: {safe_name}.md"
        filepath = self.staged_folder / filename
        
        # Create markdown content
        markdown_content = self._generate_staged_epic_markdown(epic_metadata)
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return str(filepath)
    
    def _generate_staged_epic_markdown(self, metadata: Dict[str, Any]) -> str:
        """Generate markdown content for staged epic."""
        
        md_lines = []
        
        # Header with metadata
        md_lines.append("---")
        md_lines.append("# STAGED EPIC METADATA")
        md_lines.append("# This section contains the epic configuration.")
        md_lines.append("# Edit the values below as needed, then use submit_staged_epic.py to create the Jira epic.")
        md_lines.append("---")
        md_lines.append("")
        
        # YAML metadata block
        md_lines.append("```yaml")
        md_lines.append("# Epic Configuration")
        md_lines.append("epic_config:")
        md_lines.append(f"  project: {metadata['project']}")
        md_lines.append(f"  epic_name: \"{metadata['epic_name']}\"")
        md_lines.append(f"  team: \"{metadata['team']}\"")
        md_lines.append(f"  product_backlog: \"{metadata['product_backlog']}\"")
        md_lines.append(f"  product_manager: \"{metadata['product_manager']}\"")
        md_lines.append(f"  priority: \"{metadata['priority']}\"")
        md_lines.append(f"  commitment_level: \"{metadata['commitment_level']}\"")
        md_lines.append(f"  parent: {metadata['parent'] or 'null'}")
        md_lines.append(f"  product_priority: {metadata['product_priority'] or 'null'}")
        md_lines.append(f"  assigned_architect: {metadata.get('assigned_architect') or 'null'}")
        md_lines.append(f"  assigned_ux: \"{metadata.get('assigned_ux')}\"")
        md_lines.append(f"  assigned_technical_writer: \"{metadata.get('assigned_technical_writer')}\"")
        md_lines.append(f"  required_doc: \"{metadata.get('required_doc')}\"")
        md_lines.append(f"  release_notes: \"{metadata.get('release_notes')}\"")
        md_lines.append("")
        md_lines.append("# Staging Information")
        md_lines.append("staging_info:")
        md_lines.append(f"  created_date: \"{metadata['created_date']}\"")
        md_lines.append(f"  status: \"{metadata['status']}\"")
        md_lines.append("  # Status can be: staged, reviewed, approved, submitted")
        md_lines.append("```")
        md_lines.append("")
        
        # Epic preview
        md_lines.append("---")
        md_lines.append("")
        md_lines.append(f"# 🎯 STAGED EPIC: {metadata['epic_name']}")
        md_lines.append("")
        md_lines.append("## 📋 Epic Configuration")
        md_lines.append("")
        md_lines.append(f"- **🎯 Project:** {metadata['project']}")
        md_lines.append(f"- **📝 Epic Name:** {metadata['epic_name']}")
        md_lines.append(f"- **👥 Team:** {metadata['team']}")
        md_lines.append(f"- **📋 Product Backlog:** {metadata['product_backlog']}")
        md_lines.append(f"- **👨‍💼 Product Manager:** {metadata['product_manager']}")
        md_lines.append(f"- **⚡ Priority:** {metadata['priority']}")
        md_lines.append(f"- **🤝 Commitment Level:** {metadata['commitment_level']}")
        
        if metadata['parent']:
            md_lines.append(f"- **🔗 Parent:** {metadata['parent']}")
        
        if metadata['product_priority']:
            md_lines.append(f"- **📊 Product Priority:** {metadata['product_priority']}")
        
        md_lines.append("")
        md_lines.append("## 📝 Epic Description")
        md_lines.append("")
        md_lines.append("================================================================================")
        md_lines.append("🔸 DESCRIPTION START 🔸")
        md_lines.append("================================================================================")
        md_lines.append("")
        md_lines.append(metadata['description'])
        md_lines.append("")
        md_lines.append("================================================================================")
        md_lines.append("🔸 DESCRIPTION END 🔸")
        md_lines.append("================================================================================")
        md_lines.append("")
        md_lines.append("## 🔗 Hierarchy")
        md_lines.append("")
        md_lines.append("<!-- Optional: Add parent epic or child tasks here if needed -->")
        md_lines.append("")
        
        return "\n".join(md_lines)
    
    def list_staged_epics(self) -> list:
        """List all staged epics with enhanced file information."""
        staged_files = []
        for file_path in self.staged_folder.glob("*.md"):
            try:
                # Get file stats
                stat = file_path.stat()
                file_size = stat.st_size
                modified_time = datetime.fromtimestamp(stat.st_mtime)
                
                metadata = self._parse_staged_epic(file_path)
                staged_files.append({
                    'file': str(file_path),
                    'filename': file_path.name,
                    'project': metadata.get('project', 'Unknown'),
                    'epic_name': metadata.get('epic_name', 'Unknown'),
                    'status': metadata.get('status', 'staged'),
                    'created_date': metadata.get('created_date', 'Unknown'),
                    'file_size': file_size,
                    'modified_time': modified_time,
                    'team': metadata.get('team', 'Unknown'),
                    'priority': metadata.get('priority', 'Unknown')
                })
            except Exception as e:
                # Skip files that can't be parsed
                continue
        
        return sorted(staged_files, key=lambda x: x['modified_time'], reverse=True)
    
    def display_staged_epics_rich(self):
        """Display staged epics using Rich formatting."""
        staged_files = self.list_staged_epics()
        archived_files = self._get_archived_files()
        
        if not staged_files and not archived_files:
            console.print("📭 No staged epics found.")
            console.print("💡 Create one with: python3 staged_epic_creator.py stage RTDEV \"My Epic\"")
            return
        
        # Active staged files
        if staged_files:
            console.print("\n📝 Active Staged Epics", style="bold blue")
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Project", style="cyan", width=8)
            table.add_column("Epic Name", style="green", max_width=30)
            table.add_column("Team", style="yellow", width=15)
            table.add_column("Priority", style="red", width=10)
            table.add_column("Size", style="blue", width=8)
            table.add_column("Modified", style="magenta", width=12)
            
            for epic in staged_files:
                # Format size nicely
                size_str = filesize.decimal(epic['file_size'])
                
                # Format time nicely
                time_str = epic['modified_time'].strftime('%m-%d %H:%M')
                
                # Truncate long epic names
                epic_name = epic['epic_name']
                if len(epic_name) > 27:
                    epic_name = epic_name[:24] + "..."
                
                # Color-code priority
                priority = epic.get('priority', 'Unknown')
                if 'High' in priority or '1' in priority or '2' in priority:
                    priority_style = "bold red"
                elif 'Normal' in priority or '4' in priority:
                    priority_style = "yellow"
                else:
                    priority_style = "green"
                
                table.add_row(
                    epic['project'],
                    epic_name,
                    epic.get('team', 'Unknown')[:12] + ("..." if len(epic.get('team', '')) > 12 else ""),
                    Text(priority, style=priority_style),
                    size_str,
                    time_str
                )
            
            console.print(table)
            console.print(f"📁 Location: {self.staged_folder}")
        
        # Archived files summary
        if archived_files:
            console.print(f"\n📦 Archived Epics: {len(archived_files)} files")
            total_size = sum(f['file_size'] for f in archived_files)
            console.print(f"📊 Total archived size: {filesize.decimal(total_size)}")
            
        return staged_files
    
    def _get_archived_files(self) -> list:
        """Get information about archived files."""
        archived_folder = self.staged_folder / "archived"
        if not archived_folder.exists():
            return []
        
        archived_files = []
        for file_path in archived_folder.glob("*.md"):
            try:
                stat = file_path.stat()
                archived_files.append({
                    'filename': file_path.name,
                    'file_size': stat.st_size,
                    'modified_time': datetime.fromtimestamp(stat.st_mtime)
                })
            except Exception:
                continue
                
        return archived_files
    
    def clean_old_files(self, days_old: int = 30, archived_only: bool = True) -> Dict[str, int]:
        """Clean up old files from staging area."""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days_old)
        removed_counts = {'staged': 0, 'archived': 0}
        
        # Clean archived files (default behavior)
        archived_folder = self.staged_folder / "archived"
        if archived_folder.exists():
            for file_path in archived_folder.glob("*.md"):
                try:
                    if datetime.fromtimestamp(file_path.stat().st_mtime) < cutoff_date:
                        file_path.unlink()
                        removed_counts['archived'] += 1
                except Exception:
                    continue
        
        # Clean staged files only if explicitly requested
        if not archived_only:
            for file_path in self.staged_folder.glob("*.md"):
                try:
                    if datetime.fromtimestamp(file_path.stat().st_mtime) < cutoff_date:
                        file_path.unlink()
                        removed_counts['staged'] += 1
                except Exception:
                    continue
                    
        return removed_counts
    
    def remove_staged_file(self, filename: str) -> bool:
        """Remove a specific staged file."""
        # Try exact match first
        file_path = self.staged_folder / filename
        if file_path.exists():
            file_path.unlink()
            return True
            
        # Try with .md extension
        if not filename.endswith('.md'):
            file_path = self.staged_folder / f"{filename}.md"
            if file_path.exists():
                file_path.unlink()
                return True
                
        return False
    
    def get_staging_status(self) -> Dict[str, Any]:
        """Get comprehensive staging area status."""
        staged_files = self.list_staged_epics()
        archived_files = self._get_archived_files()
        
        # Calculate statistics
        total_staged_size = sum(f['file_size'] for f in staged_files)
        total_archived_size = sum(f['file_size'] for f in archived_files)
        
        # Count by project
        project_counts = {}
        for epic in staged_files:
            project = epic['project']
            project_counts[project] = project_counts.get(project, 0) + 1
        
        # Find oldest file
        oldest_staged = None
        if staged_files:
            oldest_staged = min(staged_files, key=lambda x: x['modified_time'])
            
        return {
            'staged_count': len(staged_files),
            'archived_count': len(archived_files),
            'total_staged_size': total_staged_size,
            'total_archived_size': total_archived_size,
            'project_counts': project_counts,
            'oldest_staged': oldest_staged,
            'staging_dir': str(self.staged_folder),
            'archived_dir': str(self.staged_folder / "archived")
        }
    
    def display_status_rich(self):
        """Display staging status with Rich formatting."""
        status = self.get_staging_status()
        
        # Main status panel
        status_text = f"""📁 Staging Directory: {status['staging_dir']}
📦 Archived Directory: {status['archived_dir']}

📊 File Counts:
   • Active Staged: {status['staged_count']} files
   • Archived: {status['archived_count']} files

💾 Storage Usage:
   • Staged Files: {filesize.decimal(status['total_staged_size'])}
   • Archived Files: {filesize.decimal(status['total_archived_size'])}
   • Total: {filesize.decimal(status['total_staged_size'] + status['total_archived_size'])}"""
        
        if status['project_counts']:
            status_text += "\n\n📋 By Project:\n"
            for project, count in sorted(status['project_counts'].items()):
                status_text += f"   • {project}: {count} epics\n"
                
        if status['oldest_staged']:
            oldest = status['oldest_staged']
            age_days = (datetime.now() - oldest['modified_time']).days
            status_text += f"\n⏰ Oldest Staged: {oldest['filename']} ({age_days} days old)"
        
        panel = Panel(status_text, title="📂 Staging Area Status", border_style="blue")
        console.print(panel)
        
        # Recommendations
        if status['archived_count'] > 10:
            console.print("💡 Consider cleaning old archived files: python3 staged_epic_creator.py clean")
        if status['oldest_staged'] and (datetime.now() - status['oldest_staged']['modified_time']).days > 7:
            console.print("⚠️  You have staged files older than 7 days - consider submitting or removing them")
    
    def _parse_staged_epic(self, file_path: Path) -> Dict[str, Any]:
        """Parse metadata from a staged epic file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract YAML config block
        yaml_start = content.find("```yaml")
        yaml_end = content.find("```", yaml_start + 7)
        
        if yaml_start == -1 or yaml_end == -1:
            raise ValueError("No YAML config block found")
        
        yaml_content = content[yaml_start + 7:yaml_end].strip()
        
        try:
            config_data = yaml.safe_load(yaml_content)
            epic_config = config_data.get('epic_config', {})
            staging_info = config_data.get('staging_info', {})
            
            # Merge the configs
            metadata = {**epic_config, **staging_info}
            return metadata
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML config: {e}")
    
    def submit_staged_epic(self, staged_file_path: str) -> Dict[str, Any]:
        """Submit a staged epic to Jira."""
        file_path = Path(staged_file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Staged epic file not found: {staged_file_path}")
        
        # Parse the staged epic
        metadata = self._parse_staged_epic(file_path)
        
        # Extract ALL content (not just description section) and format for Jira
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove YAML metadata block
        yaml_start = content.find('---')
        yaml_end = content.find('```', content.find('```') + 3) + 3
        if yaml_start != -1 and yaml_end != -1:
            content = content[yaml_end:].strip()
        
        # Remove the title (first line) since Jira has its own title
        lines = content.split('\n')
        if lines[0].startswith('# '):
            content = '\n'.join(lines[1:]).strip()
        
        # Extract content within the description box
        desc_start_marker = '🔸 DESCRIPTION START 🔸'
        desc_end_marker = '🔸 DESCRIPTION END 🔸'
        
        desc_start = content.find(desc_start_marker)
        desc_end = content.find(desc_end_marker)
        
        if desc_start != -1 and desc_end != -1:
            # Move past the start marker and the next line
            desc_start = content.find('\n', desc_start + len(desc_start_marker))
            if desc_start != -1:
                desc_start += 1  # Move past the newline
            
            # Find the line before the end marker (skip the separator line)
            desc_content = content[desc_start:desc_end]
            
            # Remove the separator lines (================) from the beginning and end
            lines = desc_content.split('\n')
            # Remove leading separator lines
            while lines and ('====' in lines[0] or lines[0].strip() == ''):
                lines.pop(0)
            # Remove trailing separator lines  
            while lines and ('====' in lines[-1] or lines[-1].strip() == ''):
                lines.pop()
            
            description_content = '\n'.join(lines).strip()
            
            # Remove redundant title lines that start with "h2. Epic Title:" 
            desc_lines = description_content.split('\n')
            filtered_lines = []
            for line in desc_lines:
                # Skip lines that are redundant epic titles
                if line.strip().startswith('h2. Epic Title:'):
                    continue
                filtered_lines.append(line)
            
            description_content = '\n'.join(filtered_lines).strip()
            metadata['description'] = description_content
        else:
            # Fallback: Format content for Jira markup (legacy support)
            if content:
                formatted_content = jira_formatter.format_content(content)
                metadata['description'] = formatted_content
        
        # Create the epic using the same logic as epic_creator.py
        epic_payload = self._build_jira_payload(metadata)
        
        # Make the API request
        result = self._make_jira_request(epic_payload)
        
        # Update the staged file to mark as submitted
        self._update_staged_epic_status(file_path, 'submitted', result.get('key'))
        
        # Move the staged file to Published Issues folder after successful submission
        issue_key = result.get('key')
        if issue_key:
            self._move_to_issues_folder(file_path, issue_key)
        
        return result
    
    def _build_jira_payload(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Build Jira API payload from staged epic metadata."""
        
        project = metadata['project']
        project_defaults = self.PROJECT_DEFAULTS[project]
        
        # Field mappings (same as epic_creator.py)
        FIELD_MAPPINGS = {
            'teams': 'customfield_10129',
            'product_backlog': 'customfield_10119',
            'product_manager': 'customfield_10044',
            'commitment_reason': 'customfield_10508',
            'area': 'customfield_10167',
            'commitment_level': 'customfield_10450',
            'product_priority': 'customfield_10327',
            'assigned_architect': 'customfield_10112',
            'assigned_ux': 'customfield_10054',
            'assigned_technical_writer': 'customfield_10174',
            'required_doc': 'customfield_10071',
            'release_notes': 'customfield_10090'
        }
        
        PRIORITY_MAPPINGS = {
            'Blocker': '10000',
            '1 - Blocker': '10000',
            'Highest': '10001',
            '1 - Highest': '10001',
            'Critical': '10001',
            '2 - Critical': '10001',
            'High': '10002',           # Fix: Add simple "High" mapping
            '2 - High': '10002', 
            '3 - High': '10002',
            'Normal': '10003',
            '4 - Normal': '10003',
            'Minor': '10004',
            '5 - Minor': '10004',
            '5 - Low': '10004',
            'Trivial': '10005',
            '6 - Trivial': '10005'
        }
        
        COMMITMENT_LEVEL_MAPPINGS = {
            'Hard Commitment': '11277',
            'Soft Commitment': '11278',
            'KTLO': '11279'
        }
        
        AREA_MAPPINGS = {
            'Features & Innovation': '10312',
            'Enablers & Tech Debt': '10311',
            'KTLO': '10313'
        }
        
        COMMITMENT_REASON_MAPPINGS = {
            'Roadmap': '11490',
            'Customer Commitment': '11491',
            'Security': '11492'
        }
        
        # Base payload
        payload = {
            "fields": {
                "project": {
                    "id": project_defaults['project_id']
                },
                "summary": metadata['epic_name'],
                "description": metadata.get('description', 'TBD'),
                "issuetype": {
                    "id": "10000"  # Epic issue type
                },
                "priority": {
                    "id": PRIORITY_MAPPINGS.get(metadata['priority'], '10003')
                },
                # Required fields
                FIELD_MAPPINGS['area']: {
                    "id": AREA_MAPPINGS['Features & Innovation']
                },
                FIELD_MAPPINGS['commitment_reason']: {
                    "id": COMMITMENT_REASON_MAPPINGS['Roadmap']
                }
            }
        }
        
        # Add team
        team = metadata.get('team')
        if team:
            if project == 'RTDEV' and team == 'dev-artifactory-lifecycle':
                payload["fields"][FIELD_MAPPINGS['teams']] = [{"id": "10145"}]
            elif project == 'APP' and team == 'App Core':
                payload["fields"][FIELD_MAPPINGS['teams']] = [{"id": "12980"}]
            else:
                team_id = project_defaults.get('team_id')
                if team_id:
                    payload["fields"][FIELD_MAPPINGS['teams']] = [{"id": team_id}]
        
        # Add other fields
        if metadata.get('product_backlog'):
            payload["fields"][FIELD_MAPPINGS['product_backlog']] = [metadata['product_backlog']]
        
        # Always set product manager (default to Yonatan Philip if not specified)
        product_manager = metadata.get('product_manager', 'Yonatan Philip')
        if product_manager:
            payload["fields"][FIELD_MAPPINGS['product_manager']] = {
                "accountId": self.current_user_account_id
            }
        
        if metadata.get('commitment_level'):
            commitment_id = COMMITMENT_LEVEL_MAPPINGS.get(metadata['commitment_level'])
            if commitment_id:
                payload["fields"][FIELD_MAPPINGS['commitment_level']] = {
                    "id": commitment_id
                }
        
        if metadata.get('parent'):
            payload["fields"]["parent"] = {
                "key": metadata['parent']
            }
        
        if metadata.get('product_priority'):
            priority_mapping = {
                'P0': '11498', 'P1': '11499', 'P2': '11500', 'P3': '11501', 'P4': '11502'
            }
            priority_id = priority_mapping.get(metadata['product_priority'])
            if priority_id:
                payload["fields"][FIELD_MAPPINGS['product_priority']] = {
                    "id": priority_id
                }
        
        
        # Add Epic Owners fields - temporarily commented out to debug
        # if metadata.get('assigned_architect'):
        #     # For user fields, we need to use account ID format  
        #     payload["fields"][FIELD_MAPPINGS['assigned_architect']] = {
        #         "accountId": self._get_user_account_id(metadata['assigned_architect'])
        #     }
        
        # if metadata.get('assigned_ux'):
        #     payload["fields"][FIELD_MAPPINGS['assigned_ux']] = {
        #         "accountId": self._get_user_account_id(metadata['assigned_ux'])
        #     }
        
        # if metadata.get('assigned_technical_writer'):
        #     payload["fields"][FIELD_MAPPINGS['assigned_technical_writer']] = {
        #         "accountId": self._get_user_account_id(metadata['assigned_technical_writer'])
        #     }
        
        # Add Documentation fields - temporarily commented out to debug
        # if metadata.get('required_doc'):
        #     payload["fields"][FIELD_MAPPINGS['required_doc']] = {
        #         "value": metadata['required_doc']
        #     }
        
        # if metadata.get('release_notes'):
        #     payload["fields"][FIELD_MAPPINGS['release_notes']] = {
        #         "value": metadata['release_notes']
        #     }
        return payload
    
    
    def _get_user_account_id(self, user_name: str) -> str:
        """Get user account ID by name. For now, return hardcoded IDs for known users."""
        # TODO: In a full implementation, this should query Jira API to find user by name
        # For now, we'll use hardcoded mappings for the default users
        user_mappings = {
            "Yonatan Philip": "712020:23cfbba9-878d-4391-8207-d6a32f87cb61",
            "Omer Morag": "712020:23cfbba9-878d-4391-8207-d6a32f87cb61",  # TODO: Get actual account ID
            "Michael Berman": "712020:23cfbba9-878d-4391-8207-d6a32f87cb61",  # TODO: Get actual account ID
        }
        
        # Return the account ID if we have it, otherwise default to current user
        return user_mappings.get(user_name, self.current_user_account_id)

    def _make_jira_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make the API request to create the epic."""
        url = f"{self.base_url}/rest/api/2/issue/"
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Add web URL to the result
            issue_key = result.get('key')
            if issue_key:
                result['web_url'] = f"{self.base_url}/browse/{issue_key}"
            
            return result
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to create epic: {e}")
    
    def _update_staged_epic_status(self, file_path: Path, status: str, jira_key: Optional[str] = None):
        """Update the status of a staged epic file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the YAML status
        yaml_start = content.find("```yaml")
        yaml_end = content.find("```", yaml_start + 7)
        
        if yaml_start != -1 and yaml_end != -1:
            yaml_content = content[yaml_start + 7:yaml_end]
            
            # Update status line
            updated_yaml = yaml_content.replace(
                f'status: "staged"',
                f'status: "{status}"'
            ).replace(
                f'status: "reviewed"',
                f'status: "{status}"'
            ).replace(
                f'status: "approved"',
                f'status: "{status}"'
            )
            
            # Add Jira key if provided
            if jira_key and 'jira_key:' not in updated_yaml:
                updated_yaml += f"\n  jira_key: \"{jira_key}\""
                updated_yaml += f"\n  submitted_date: \"{datetime.now().isoformat()}\""
            
            # Replace the YAML block
            updated_content = content[:yaml_start + 7] + updated_yaml + content[yaml_end:]
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
    
    def _move_to_issues_folder(self, staged_file_path: Path, issue_key: str):
        """Move successfully submitted epic from staged-issues to staged-issues/archived/ folder."""
        import shutil
        from datetime import datetime
        
        try:
            # Create archived folder if it doesn't exist
            archived_folder = self.staged_folder / "archived"
            archived_folder.mkdir(exist_ok=True)
            
            # Generate archived filename with issue key and timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            archived_filename = f"{issue_key}-{staged_file_path.stem}-{timestamp}.md"
            archived_path = archived_folder / archived_filename
            
            # Move the staged file to archived folder
            if staged_file_path.exists():
                shutil.move(str(staged_file_path), str(archived_path))
                print(f"✅ Archived staged epic to: staged-issues/archived/{archived_filename}")
                print(f"📁 Find it at: {archived_path}")
            else:
                print(f"⚠️  Staged file not found: {staged_file_path}")
                
        except Exception as e:
            print(f"⚠️  Epic created successfully, but couldn't archive staged file: {e}")
            print(f"📝 Staged file remains at: {staged_file_path}")


# CLI Commands
@click.group()
def cli():
    """Staged Epic Creator - Two-phase epic creation workflow."""
    pass


@cli.command()
@click.argument('project', required=True)
@click.argument('epic_name', required=True)
@click.option('--description', '-d', default='TBD', help='Epic description (default: TBD)')
@click.option('--team', '-t', help='Team name (uses project default if not specified)')
@click.option('--product-backlog', '-pb', default='Q4-25-Backlog', help='Product backlog (default: Q4-25-Backlog)')
@click.option('--product-manager', '-pm', default='Yonatan Philip', help='Product manager (default: Yonatan Philip)')
@click.option('--priority', '-p', default='4 - Normal', 
              type=click.Choice(['Blocker', '1 - Blocker', 'Critical', '2 - Critical', 'High', '3 - High', 'Normal', '4 - Normal', 'Minor', '5 - Minor', 'Trivial', '6 - Trivial']),
              help='Priority (default: 4 - Normal)')
@click.option('--commitment-level', '-cl', default='Soft Commitment',
              type=click.Choice(['Hard Commitment', 'Soft Commitment', 'KTLO']),
              help='Commitment level (default: Soft Commitment)')
@click.option('--parent', help='Parent issue key (optional)')
@click.option('--product-priority', '-pp', 
              type=click.Choice(['P0', 'P1', 'P2', 'P3', 'P4']),
              help='Product priority (optional)')
@click.option('--assigned-architect', '-aa', help='Assigned Architect (optional)')
@click.option('--assigned-ux', '-aux', default='Omer Morag', help='Assigned UX (default: Omer Morag)')
@click.option('--assigned-technical-writer', '-atw', default='Michael Berman', help='Assigned Technical Writer (default: Michael Berman)')
@click.option('--required-doc', '-rd', default='Yes', type=click.Choice(['Yes', 'No']), help='Required Doc (default: Yes)')
@click.option('--release-notes', '-rn', default='Yes', type=click.Choice(['Yes', 'No']), help='Release Notes (default: Yes)')
def stage(project: str, epic_name: str, description: str, team: Optional[str], 
          product_backlog: str, product_manager: str, priority: str, 
          commitment_level: str, parent: Optional[str], product_priority: Optional[str],
          assigned_architect: Optional[str], assigned_ux: str, assigned_technical_writer: str,
          required_doc: str, release_notes: str):
    """
    Create a staged epic for review and editing.
    
    PROJECT: Project key (e.g., RTDEV, APP) - case insensitive
    EPIC_NAME: Name/summary of the epic
    """
    
    creator = StagedEpicCreator()
    
    try:
        click.echo(f"\n🎯 Creating Staged Epic in {project.upper()}")
        click.echo(f"📝 Epic Name: {epic_name}")
        click.echo(f"📄 Description: {description}")
        
        # Create staged epic
        staged_file = creator.create_staged_epic(
            project=project,
            epic_name=epic_name,
            description=description,
            team=team,
            product_backlog=product_backlog,
            product_manager=product_manager,
            priority=priority,
            commitment_level=commitment_level,
            parent=parent,
            product_priority=product_priority,
            assigned_architect=assigned_architect,
            assigned_ux=assigned_ux,
            assigned_technical_writer=assigned_technical_writer,
            required_doc=required_doc,
            release_notes=release_notes
        )
        
        click.echo(f"\n✅ Staged epic created successfully!")
        click.echo(f"📁 File: {staged_file}")
        click.echo(f"\n📝 Next steps:")
        click.echo(f"1. Edit the staged epic file to refine requirements")
        click.echo(f"2. Share with team for review and feedback")
        click.echo(f"3. When ready, submit with: python3 staged_epic_creator.py submit {os.path.basename(staged_file)}")
        
    except Exception as e:
        click.echo(f"\n❌ Error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.argument('staged_file', required=True)
@click.option('--dry-run', is_flag=True, help='Show what would be created without actually creating it')
def submit(staged_file: str, dry_run: bool):
    """
    Submit a staged epic to Jira.
    
    STAGED_FILE: Path to the staged epic markdown file
    """
    
    creator = StagedEpicCreator()
    
    try:
        # Handle relative paths
        if not staged_file.startswith('/') and not staged_file.startswith('staged-issues/'):
            staged_file = f"staged-issues/{staged_file}"
        
        if dry_run:
            click.echo(f"\n🔍 DRY RUN - Parsing staged epic: {staged_file}")
            metadata = creator._parse_staged_epic(Path(staged_file))
            
            click.echo(f"\n📋 Epic Configuration:")
            click.echo(f"🎯 Project: {metadata.get('project')}")
            click.echo(f"📝 Epic Name: {metadata.get('epic_name')}")
            click.echo(f"👥 Team: {metadata.get('team')}")
            click.echo(f"⚡ Priority: {metadata.get('priority')}")
            click.echo(f"🤝 Commitment: {metadata.get('commitment_level')}")
            
            if metadata.get('parent'):
                click.echo(f"🔗 Parent: {metadata.get('parent')}")
            if metadata.get('product_priority'):
                click.echo(f"📊 Product Priority: {metadata.get('product_priority')}")
            
            click.echo(f"\n🔍 DRY RUN - No epic will be created")
            return
        
        click.echo(f"\n🚀 Submitting staged epic: {staged_file}")
        
        result = creator.submit_staged_epic(staged_file)
        
        issue_key = result.get('key')
        web_url = result.get('web_url')
        
        click.echo(f"\n✅ Epic created successfully!")
        click.echo(f"🎫 Epic Key: {issue_key}")
        click.echo(f"🔗 Web URL: {web_url}")
        
        # Optionally view the created epic
        if click.confirm("\nWould you like to view the created epic?"):
            import subprocess
            subprocess.run(['python3', 'jira_viewer.py', issue_key])
        
    except Exception as e:
        click.echo(f"\n❌ Error: {e}", err=True)
        raise click.Abort()


@cli.command()
def list():
    """List all staged epics with enhanced formatting."""
    
    creator = StagedEpicCreator()
    creator.display_staged_epics_rich()


@cli.command()
@click.option('--days', default=30, help='Remove files older than N days (default: 30)')
@click.option('--archived-only/--include-staged', default=True, help='Clean only archived files (default) or include staged files')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def clean(days: int, archived_only: bool, force: bool):
    """Clean up old staged and archived files."""
    
    creator = StagedEpicCreator()
    
    try:
        if not force:
            area = "archived files" if archived_only else "staged and archived files"
            if not click.confirm(f"Remove {area} older than {days} days?"):
                console.print("❌ Cleanup cancelled")
                return
        
        removed_counts = creator.clean_old_files(days, archived_only)
        
        if removed_counts['archived'] > 0 or removed_counts['staged'] > 0:
            console.print("✅ Cleanup completed:")
            if removed_counts['archived'] > 0:
                console.print(f"   📦 Removed {removed_counts['archived']} archived files")
            if removed_counts['staged'] > 0:
                console.print(f"   📝 Removed {removed_counts['staged']} staged files")
        else:
            console.print("💡 No old files found to remove")
            
    except Exception as e:
        console.print(f"❌ Error during cleanup: {e}")
        raise click.Abort()


@cli.command()
@click.argument('filename')
@click.option('--force', is_flag=True, help='Skip confirmation prompt')
def remove(filename: str, force: bool):
    """Remove a specific staged file."""
    
    creator = StagedEpicCreator()
    
    try:
        if not force:
            if not click.confirm(f"Remove staged file '{filename}'?"):
                console.print("❌ Remove cancelled")
                return
        
        success = creator.remove_staged_file(filename)
        
        if success:
            console.print(f"✅ Removed {filename}")
        else:
            console.print(f"❌ File '{filename}' not found")
            console.print("💡 Use 'python3 staged_epic_creator.py list' to see available files")
            
    except Exception as e:
        console.print(f"❌ Error removing file: {e}")
        raise click.Abort()


@cli.command()
def status():
    """Show staging area status and statistics."""
    
    creator = StagedEpicCreator()
    creator.display_status_rich()


if __name__ == '__main__':
    cli()
