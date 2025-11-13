#!/usr/bin/env python3
"""
🚨 DEPRECATED SCRIPT 🚨

This script is DEPRECATED and will be removed on 2025-03-01.

👉 USE INSTEAD: python3 -m jira_tools epic
📖 Migration Guide: See MIGRATION_GUIDE.md
🆕 New System: Provides all features + enhancements + security

Epic Creator - A workflow tool for creating Jira epics with smart defaults.

This script allows you to create new Jira epics with customizable parameters
and project-specific defaults.

⚠️ WARNING: This file contains hardcoded JFrog-specific data and is not suitable for team sharing.
"""

import os
import click
import requests
from typing import Dict, Any, Optional
from config import config


class EpicCreator:
    """Creates Jira epics with smart defaults based on project."""
    
    # Project-specific defaults
    PROJECT_DEFAULTS = {
        'RTDEV': {
            'team': 'dev-artifactory-lifecycle',
            'team_id': '10145',
            'project_id': '10129'
        },
        'APP': {
            'team': 'App Core',
            'team_id': '12980',  # App Core team ID
            'project_id': '10246'  # APP project ID
        }
    }
    
    # Field mappings for Jira custom fields
    FIELD_MAPPINGS = {
        'teams': 'customfield_10129',
        'product_backlog': 'customfield_10119',
        'product_manager': 'customfield_10044',
        'commitment_reason': 'customfield_10508',
        'area': 'customfield_10167',
        'commitment_level': 'customfield_10450',
        'product_priority': 'customfield_10327'
    }
    
    # Priority mappings
    PRIORITY_MAPPINGS = {
        '1 - Blocker': '10000',
        '1 - Highest': '10001',
        '2 - Critical': '10001',
        '2 - High': '10002', 
        '3 - High': '10002',
        '4 - Normal': '10003',
        '5 - Minor': '10004',
        '5 - Low': '10004',
        '6 - Trivial': '10005'
    }
    
    # Commitment level mappings
    COMMITMENT_LEVEL_MAPPINGS = {
        'Hard Commitment': '11277',
        'Soft Commitment': '11278',
        'KTLO': '11279'
    }
    
    # Area mappings
    AREA_MAPPINGS = {
        'Features & Innovation': '10312',
        'Enablers & Tech Debt': '10311',
        'KTLO': '10313'
    }
    
    # Commitment reason mappings
    COMMITMENT_REASON_MAPPINGS = {
        'Roadmap': '11490',
        'Customer Commitment': '11491',
        'Security': '11492'
    }
    
    def __init__(self):
        self.base_url = config.jira_base_url
        self.headers = config.auth_headers
        
        # Get current user account ID for default product manager
        self.current_user_account_id = os.getenv('JIRA_USER_ACCOUNT_ID', '')
    
    def create_epic(self, 
                   project: str,
                   epic_name: str,
                   description: str = "TBD",
                   team: Optional[str] = None,
                   product_backlog: str = "Q4-25-Backlog",
                   product_manager: str = "Yonatan Philip",
                   priority: str = "4 - Normal",
                   commitment_level: str = "Soft Commitment",
                   parent: Optional[str] = None,
                   product_priority: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new Jira epic with the specified parameters.
        
        Args:
            project: Project key (e.g., 'RTDEV', 'APP')
            epic_name: Name/summary of the epic
            description: Epic description (default: 'TBD')
            team: Team name (uses project default if not specified)
            product_backlog: Product backlog label (default: 'Q4-25-Backlog')
            product_manager: Product manager name (default: 'Yonatan Philip')
            priority: Priority level (default: '4 - Normal')
            commitment_level: Commitment level (default: 'Soft Commitment')
            parent: Parent issue key (optional)
            product_priority: Product priority (optional)
            
        Returns:
            Dictionary containing the created epic information
        """
        
        # Normalize project key
        project = project.upper()
        
        # Validate project
        if project not in self.PROJECT_DEFAULTS:
            raise ValueError(f"Unsupported project: {project}. Supported projects: {list(self.PROJECT_DEFAULTS.keys())}")
        
        # Get project defaults
        project_defaults = self.PROJECT_DEFAULTS[project]
        
        # Use team default if not specified
        if team is None:
            team = project_defaults['team']
        
        # Build the epic payload
        epic_payload = self._build_epic_payload(
            project=project,
            project_defaults=project_defaults,
            epic_name=epic_name,
            description=description,
            team=team,
            product_backlog=product_backlog,
            product_manager=product_manager,
            priority=priority,
            commitment_level=commitment_level,
            parent=parent,
            product_priority=product_priority
        )
        
        # Create the epic
        response = self._make_jira_request(epic_payload)
        
        return response
    
    def _build_epic_payload(self, **kwargs) -> Dict[str, Any]:
        """Build the Jira API payload for creating an epic."""
        
        project = kwargs['project']
        project_defaults = kwargs['project_defaults']
        
        # Base payload
        payload = {
            "fields": {
                "project": {
                    "id": project_defaults['project_id']
                },
                "summary": kwargs['epic_name'],
                "description": kwargs['description'],
                "issuetype": {
                    "id": "10000"  # Epic issue type
                },
                "priority": {
                    "id": self.PRIORITY_MAPPINGS.get(kwargs['priority'], '10003')  # Default to Normal
                },
                # Required fields
                self.FIELD_MAPPINGS['area']: {
                    "id": self.AREA_MAPPINGS['Features & Innovation']  # Default area
                },
                self.FIELD_MAPPINGS['commitment_reason']: {
                    "id": self.COMMITMENT_REASON_MAPPINGS['Roadmap']  # Default commitment reason
                }
            }
        }
        
        # Add team
        if kwargs['team']:
            # Map team names to IDs based on project
            if project == 'RTDEV' and kwargs['team'] == 'dev-artifactory-lifecycle':
                payload["fields"][self.FIELD_MAPPINGS['teams']] = [{"id": "10145"}]
            elif project == 'APP' and kwargs['team'] == 'App Core':
                payload["fields"][self.FIELD_MAPPINGS['teams']] = [{"id": "12980"}]
            else:
                # Use project default team ID if available
                team_id = project_defaults.get('team_id')
                if team_id:
                    payload["fields"][self.FIELD_MAPPINGS['teams']] = [{"id": team_id}]
        
        # Add product backlog
        if kwargs['product_backlog']:
            payload["fields"][self.FIELD_MAPPINGS['product_backlog']] = [kwargs['product_backlog']]
        
        # Add product manager (using current user as default)
        if kwargs['product_manager']:
            payload["fields"][self.FIELD_MAPPINGS['product_manager']] = {
                "accountId": self.current_user_account_id
            }
        
        # Add commitment level
        if kwargs['commitment_level']:
            commitment_id = self.COMMITMENT_LEVEL_MAPPINGS.get(kwargs['commitment_level'])
            if commitment_id:
                payload["fields"][self.FIELD_MAPPINGS['commitment_level']] = {
                    "id": commitment_id
                }
        
        # Add parent if specified
        if kwargs['parent']:
            payload["fields"]["parent"] = {
                "key": kwargs['parent']
            }
        
        # Add product priority if specified
        if kwargs['product_priority']:
            # Product priority mappings: P0, P1, P2, P3, P4
            priority_mapping = {
                'P0': '11498',
                'P1': '11499', 
                'P2': '11500',
                'P3': '11501',
                'P4': '11502'
            }
            priority_id = priority_mapping.get(kwargs['product_priority'])
            if priority_id:
                payload["fields"][self.FIELD_MAPPINGS['product_priority']] = {
                    "id": priority_id
                }
        
        return payload
    
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
    
    def get_epic_url(self, issue_key: str) -> str:
        """Get the web URL for an epic."""
        return f"{self.base_url}/browse/{issue_key}"


@click.command()
@click.argument('project', required=True)
@click.argument('epic_name', required=True)
@click.option('--description', '-d', default='TBD', help='Epic description (default: TBD)')
@click.option('--team', '-t', help='Team name (uses project default if not specified)')
@click.option('--product-backlog', '-pb', default='Q4-25-Backlog', help='Product backlog (default: Q4-25-Backlog)')
@click.option('--product-manager', '-pm', default='Yonatan Philip', help='Product manager (default: Yonatan Philip)')
@click.option('--priority', '-p', default='4 - Normal', 
              type=click.Choice(['1 - Blocker', '2 - Critical', '3 - High', '4 - Normal', '5 - Minor', '6 - Trivial']),
              help='Priority (default: 4 - Normal)')
@click.option('--commitment-level', '-cl', default='Soft Commitment',
              type=click.Choice(['Hard Commitment', 'Soft Commitment', 'KTLO']),
              help='Commitment level (default: Soft Commitment)')
@click.option('--parent', help='Parent issue key (optional)')
@click.option('--product-priority', '-pp', 
              type=click.Choice(['P0', 'P1', 'P2', 'P3', 'P4']),
              help='Product priority (optional)')
@click.option('--dry-run', is_flag=True, help='Show what would be created without actually creating it')
def main(project: str, epic_name: str, description: str, team: Optional[str], 
         product_backlog: str, product_manager: str, priority: str, 
         commitment_level: str, parent: Optional[str], product_priority: Optional[str],
         dry_run: bool):
    """
    Create a new Jira epic with smart defaults.
    
    PROJECT: Project key (e.g., RTDEV, APP) - case insensitive
    EPIC_NAME: Name/summary of the epic
    
    Examples:
    
    \b
    # Create a basic epic in RTDEV
    python epic_creator.py RTDEV "My New Epic"
    
    \b
    # Create an epic with custom description and team
    python epic_creator.py RTDEV "API Improvements" --description "Improve API performance" --team "dev-artifactory-core"
    
    \b
    # Create an epic in APP project
    python epic_creator.py APP "UI Enhancements" --priority "2 - High"
    
    \b
    # Dry run to see what would be created
    python epic_creator.py RTDEV "Test Epic" --dry-run
    """
    
    # 🚨 DEPRECATION WARNING
    click.echo("🚨 " + "="*70 + " 🚨", err=True)
    click.echo("🚨 DEPRECATION WARNING: This script will be removed on 2025-03-01", err=True)
    click.echo("🚨", err=True)
    click.echo("🚨 👉 USE INSTEAD: python3 -m jira_tools epic", err=True)
    click.echo("🚨 📖 Migration Guide: See MIGRATION_GUIDE.md", err=True)
    click.echo("🚨 🆕 New System: All features + enhancements + security", err=True)
    click.echo("🚨 " + "="*70 + " 🚨", err=True)
    click.echo("")
    
    if not click.confirm("Continue with deprecated script?"):
        click.echo("👍 Great choice! Use the new system: python3 -m jira_tools epic")
        raise click.Abort()
    
    creator = EpicCreator()
    
    try:
        # Show what will be created
        project_upper = project.upper()
        project_defaults = creator.PROJECT_DEFAULTS.get(project_upper, {})
        effective_team = team or project_defaults.get('team', 'Unknown')
        
        click.echo(f"\n🎯 Creating Epic in {project_upper}")
        click.echo(f"📝 Epic Name: {epic_name}")
        click.echo(f"📄 Description: {description}")
        click.echo(f"👥 Team: {effective_team}")
        click.echo(f"📋 Product Backlog: {product_backlog}")
        click.echo(f"👨‍💼 Product Manager: {product_manager}")
        click.echo(f"⚡ Priority: {priority}")
        click.echo(f"🤝 Commitment Level: {commitment_level}")
        if parent:
            click.echo(f"🔗 Parent: {parent}")
        if product_priority:
            click.echo(f"📊 Product Priority: {product_priority}")
        
        if dry_run:
            click.echo("\n🔍 DRY RUN - No epic will be created")
            return
        
        click.echo(f"\n🚀 Creating epic...")
        
        # Create the epic
        result = creator.create_epic(
            project=project,
            epic_name=epic_name,
            description=description,
            team=team,
            product_backlog=product_backlog,
            product_manager=product_manager,
            priority=priority,
            commitment_level=commitment_level,
            parent=parent,
            product_priority=product_priority
        )
        
        # Display results
        issue_key = result.get('key')
        web_url = result.get('web_url')
        
        click.echo(f"\n✅ Epic created successfully!")
        click.echo(f"🎫 Epic Key: {issue_key}")
        click.echo(f"🔗 Web URL: {web_url}")
        
        # Optionally fetch and display the created epic
        if click.confirm("\nWould you like to view the created epic?"):
            import subprocess
            subprocess.run(['python3', 'jira_viewer.py', issue_key])
        
    except Exception as e:
        click.echo(f"\n❌ Error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    main()
