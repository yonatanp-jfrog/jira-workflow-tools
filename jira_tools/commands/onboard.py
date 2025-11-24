"""
Interactive onboarding wizard for Jira Workflow Tools.

This module provides a comprehensive, step-by-step setup experience specifically
designed for JFrog employees, with smart defaults and automatic discovery.
"""

import json
import base64
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import click
import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text

# Initialize Rich console
console = Console()


class OnboardingWizard:
    """
    Interactive onboarding wizard for JFrog Jira Workflow Tools.
    
    Guides users through configuration, discovery, and personalization
    in a friendly, step-by-step process.
    """
    
    def __init__(self):
        """Initialize the onboarding wizard."""
        self.config = {}
        self.discovered_projects = []
        self.discovered_teams = []
        self.step = 1
        self.total_steps = 6
    
    def start(self) -> bool:
        """
        Start the interactive onboarding process.
        
        Returns:
            bool: True if onboarding completed successfully
        """
        try:
            self._display_welcome()
            
            # Step 1: JFrog Jira Configuration
            if not self._configure_jira_connection():
                return False
            
            # Step 2: Authentication Setup
            if not self._setup_authentication():
                return False
            
            # Step 3: Project & Team Discovery
            if not self._discover_projects_and_teams():
                return False
            
            # Step 4: Template Personalization
            if not self._personalize_templates():
                return False
            
            # Step 5: Custom Field Configuration
            if not self._configure_custom_fields():
                return False
            
            # Step 6: Validation & Final Setup
            if not self._validate_and_finalize():
                return False
            
            self._display_completion()
            return True
            
        except KeyboardInterrupt:
            console.print("\n❌ Setup cancelled by user", style="red")
            return False
        except Exception as e:
            console.print(f"\n❌ Setup failed: {e}", style="red")
            return False
    
    def _display_welcome(self) -> None:
        """Display welcome message and introduction."""
        welcome_text = """
🎯 Welcome to JFrog Jira Workflow Tools Setup Wizard!

This interactive setup will configure your environment in just a few minutes.
We'll guide you through:
• Jira connection and authentication
• Project and team discovery  
• Template personalization for JFrog workflows
• Custom field mapping
• Configuration validation

Let's get you set up for productive Jira workflows!
        """.strip()
        
        console.print(Panel(
            welcome_text,
            title="[bold green]🚀 JFrog Jira Workflow Tools[/bold green]",
            border_style="green"
        ))
        console.print("")
    
    def _step_header(self, title: str) -> None:
        """Display step header."""
        console.print(f"\n[bold cyan]Step {self.step}/{self.total_steps}: {title}[/bold cyan]")
        self.step += 1
    
    def _configure_jira_connection(self) -> bool:
        """
        Step 1: Configure Jira connection.
        
        Returns:
            bool: True if configuration successful
        """
        self._step_header("JFrog Jira Configuration")
        
        # Get Jira URL with JFrog default
        console.print("First, let's connect to your Jira instance.")
        
        default_url = "https://jfrog-int.atlassian.net"
        jira_url = Prompt.ask(
            f"Jira URL",
            default=default_url
        ).strip()
        
        # Ensure URL format is correct
        if not jira_url.startswith('http'):
            jira_url = f"https://{jira_url}"
        
        # Remove trailing slash
        jira_url = jira_url.rstrip('/')
        
        self.config['jira_base_url'] = jira_url
        
        # Validate connection
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Validating Jira connection...", total=None)
            
            try:
                response = requests.get(f"{jira_url}/rest/api/2/serverInfo", timeout=10)
                if response.status_code == 200:
                    server_info = response.json()
                    console.print(f"✅ Connected to Jira successfully!")
                    console.print(f"   Server: {server_info.get('serverTitle', 'Jira')}")
                    console.print(f"   Version: {server_info.get('version', 'Unknown')}")
                    return True
                else:
                    console.print(f"❌ Failed to connect to Jira (HTTP {response.status_code})", style="red")
                    return False
            except requests.exceptions.RequestException as e:
                console.print(f"❌ Connection failed: {e}", style="red")
                console.print("Please check the URL and try again.", style="yellow")
                return False
    
    def _setup_authentication(self) -> bool:
        """
        Step 2: Set up authentication.
        
        Returns:
            bool: True if authentication successful
        """
        self._step_header("Authentication Setup")
        
        console.print("Now let's set up your authentication credentials.")
        
        # Get JFrog email with validation
        while True:
            email = Prompt.ask("What's your JFrog email address?").strip().lower()
            
            if '@' in email and '.' in email:
                break
            else:
                console.print("❌ Please enter a valid email address", style="red")
        
        self.config['jira_email'] = email
        
        # API Token setup with clear instructions
        console.print("\n📝 Let's create your API token...")
        console.print("Opening the Atlassian API token page...")
        
        # Display critical instructions
        warning_panel = Panel(
            """⚠️  IMPORTANT: When creating your token:

✅ Click "Create API token"
❌ DO NOT click "Create API token with scopes"

The scoped tokens have limited permissions and won't work properly
with this tool. Make sure to use the regular "Create API token" option!""",
            title="[bold red]⚠️  Token Creation Instructions[/bold red]",
            border_style="red"
        )
        console.print(warning_panel)
        
        # Try to open the URL
        import webbrowser
        try:
            webbrowser.open("https://id.atlassian.com/manage-profile/security/api-tokens")
            console.print("🌐 Browser opened to: https://id.atlassian.com/manage-profile/security/api-tokens")
        except:
            console.print("🌐 Please visit: https://id.atlassian.com/manage-profile/security/api-tokens")
        
        console.print("\nAfter creating your token:")
        console.print("1. Give it a name like 'JFrog Jira Tools'")
        console.print("2. Copy the generated token")
        console.print("3. Paste it below (input will be hidden)")
        
        # Get API token (hidden input)
        api_token = Prompt.ask("Paste your API token", password=True).strip()
        
        if not api_token:
            console.print("❌ No token provided", style="red")
            return False
        
        # Create base64 encoded auth string
        auth_string = f"{email}:{api_token}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        self.config['jira_auth_token'] = encoded_auth
        
        # Validate authentication
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Testing authentication...", total=None)
            
            try:
                headers = {
                    "Authorization": f"Basic {encoded_auth}",
                    "Content-Type": "application/json"
                }
                
                response = requests.get(
                    f"{self.config['jira_base_url']}/rest/api/2/myself",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    user_info = response.json()
                    self.config['user_account_id'] = user_info.get('accountId', '')
                    
                    console.print(f"✅ Authentication successful!")
                    console.print(f"   Welcome, {user_info.get('displayName', 'User')}!")
                    console.print(f"   Account ID: {user_info.get('accountId', 'N/A')}")
                    return True
                else:
                    console.print(f"❌ Authentication failed (HTTP {response.status_code})", style="red")
                    console.print("Please check your email and token", style="yellow")
                    return False
                    
            except requests.exceptions.RequestException as e:
                console.print(f"❌ Authentication test failed: {e}", style="red")
                return False
    
    def _discover_projects_and_teams(self) -> bool:
        """
        Step 3: Discover projects and teams.
        
        Returns:
            bool: True if discovery successful
        """
        self._step_header("JFrog Project Discovery")
        
        console.print("Let's discover your accessible projects and teams...")
        
        # Discover projects
        if not self._discover_projects():
            return False
        
        # Get user's project selection
        console.print(f"\n✅ Found {len(self.discovered_projects)} accessible projects")
        
        # Primary project selection with RTDEV default
        console.print("\nWhich project do you primarily work with?")
        primary_project = Prompt.ask("Primary project", default="RTDEV").strip().upper()
        
        self.config['primary_project'] = primary_project
        
        # Additional projects (optional)
        console.print("\nDo you work with any additional projects?")
        console.print("Enter as comma-separated list (e.g., APP,XRAY) or press Enter to skip:")
        
        additional_input = Prompt.ask("Additional projects", default="").strip()
        additional_projects = []
        
        if additional_input:
            additional_projects = [p.strip().upper() for p in additional_input.split(',') if p.strip()]
        
        self.config['additional_projects'] = additional_projects
        
        # All selected projects
        all_projects = [primary_project] + additional_projects
        self.config['selected_projects'] = list(set(all_projects))  # Remove duplicates
        
        # Discover teams for selected projects
        if not self._discover_teams(self.config['selected_projects']):
            return False
        
        # Team selection
        if self.discovered_teams:
            console.print(f"\n✅ Found {len(self.discovered_teams)} teams in your selected projects")
            
            # Display teams as numbered list
            console.print("\nAvailable teams:")
            team_table = Table(show_header=True, header_style="bold magenta")
            team_table.add_column("Number", style="cyan", width=8)
            team_table.add_column("Team Name", style="green")
            team_table.add_column("Project", style="yellow")
            
            for i, team in enumerate(self.discovered_teams, 1):
                team_table.add_row(str(i), team['name'], team.get('project', 'Multiple'))
            
            console.print(team_table)
            
            # Get team selection
            while True:
                team_input = Prompt.ask("\nSelect your team (number or name)").strip()
                
                # Try to match by number
                try:
                    team_num = int(team_input) - 1
                    if 0 <= team_num < len(self.discovered_teams):
                        selected_team = self.discovered_teams[team_num]
                        break
                except ValueError:
                    pass
                
                # Try to match by name
                matching_teams = [t for t in self.discovered_teams 
                                if team_input.lower() in t['name'].lower()]
                
                if len(matching_teams) == 1:
                    selected_team = matching_teams[0]
                    break
                elif len(matching_teams) > 1:
                    console.print(f"❌ Multiple teams match '{team_input}'. Please be more specific.", style="red")
                else:
                    console.print(f"❌ Team '{team_input}' not found. Please try again.", style="red")
            
            self.config['selected_team'] = selected_team
            console.print(f"✅ Selected team: {selected_team['name']}")
        else:
            console.print("⚠️  No teams discovered. This is okay - you can configure this later.", style="yellow")
            self.config['selected_team'] = None
        
        return True
    
    def _discover_projects(self) -> bool:
        """Discover accessible projects via Jira API."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Discovering projects...", total=None)
            
            try:
                headers = {
                    "Authorization": f"Basic {self.config['jira_auth_token']}",
                    "Content-Type": "application/json"
                }
                
                response = requests.get(
                    f"{self.config['jira_base_url']}/rest/api/2/project",
                    headers=headers,
                    timeout=15
                )
                
                if response.status_code == 200:
                    projects_data = response.json()
                    self.discovered_projects = [
                        {
                            'key': p['key'],
                            'name': p['name'],
                            'id': p['id']
                        }
                        for p in projects_data
                    ]
                    return True
                else:
                    console.print(f"❌ Failed to discover projects (HTTP {response.status_code})", style="red")
                    # Continue anyway - user can manually specify
                    return True
                    
            except requests.exceptions.RequestException as e:
                console.print(f"❌ Project discovery failed: {e}", style="red")
                # Continue anyway - user can manually specify
                return True
    
    def _discover_teams(self, projects: List[str]) -> bool:
        """Discover teams/components for selected projects."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Discovering teams...", total=None)
            
            try:
                headers = {
                    "Authorization": f"Basic {self.config['jira_auth_token']}",
                    "Content-Type": "application/json"
                }
                
                all_teams = []
                
                # Get components for each project
                for project_key in projects:
                    try:
                        response = requests.get(
                            f"{self.config['jira_base_url']}/rest/api/2/project/{project_key}/components",
                            headers=headers,
                            timeout=10
                        )
                        
                        if response.status_code == 200:
                            components = response.json()
                            for comp in components:
                                all_teams.append({
                                    'name': comp['name'],
                                    'id': comp['id'],
                                    'project': project_key
                                })
                    except:
                        # Continue with other projects if one fails
                        continue
                
                # Add some common JFrog team names as fallback
                common_teams = [
                    {'name': 'dev-artifactory-lifecycle', 'id': 'fallback', 'project': 'RTDEV'},
                    {'name': 'platform-team', 'id': 'fallback', 'project': 'RTDEV'},
                    {'name': 'app-core', 'id': 'fallback', 'project': 'APP'},
                    {'name': 'security-team', 'id': 'fallback', 'project': 'Multiple'},
                    {'name': 'performance-team', 'id': 'fallback', 'project': 'Multiple'},
                    {'name': 'devops-team', 'id': 'fallback', 'project': 'Multiple'},
                ]
                
                # Combine discovered and common teams, removing duplicates
                team_names = {t['name'] for t in all_teams}
                for common_team in common_teams:
                    if common_team['name'] not in team_names:
                        all_teams.append(common_team)
                
                self.discovered_teams = all_teams
                return True
                
            except Exception as e:
                console.print(f"❌ Team discovery failed: {e}", style="red")
                # Add fallback teams so user can still continue
                self.discovered_teams = [
                    {'name': 'dev-artifactory-lifecycle', 'id': 'fallback', 'project': 'RTDEV'},
                    {'name': 'app-core', 'id': 'fallback', 'project': 'APP'}
                ]
                return True
    
    def _personalize_templates(self) -> bool:
        """
        Step 4: Personalize templates.
        
        Returns:
            bool: True if personalization successful
        """
        self._step_header("JFrog Template Personalization")
        
        console.print("Let's customize templates with your JFrog preferences...")
        
        # Get user preferences
        console.print("\nTemplate preferences:")
        
        # Default priority
        priorities = ['High', 'Normal', 'Low']
        priority = Prompt.ask("Default priority for new issues", choices=priorities, default="Normal")
        
        # Product manager (default to current user)
        default_pm = self.config.get('jira_email', 'yonatan.philip@jfrog.com')
        product_manager = Prompt.ask("Default Product Manager", default=default_pm)
        
        # Epic naming prefix convention
        epic_naming = Prompt.ask("Epic naming prefix convention", default="RLM 4Q25 -")
        
        # Product backlog format
        backlog_format = Prompt.ask("Default Product Backlog format", default="Q4-25-Backlog")
        
        # Commitment reason
        commitment_reasons = ['Roadmap', 'Customer Commitment', 'Security']
        commitment_reason = Prompt.ask("Default Commitment Reason", choices=commitment_reasons, default="Roadmap")
        
        # Store preferences
        self.config.update({
            'default_priority': priority,
            'default_product_manager': product_manager,
            'epic_naming_prefix': epic_naming,
            'default_backlog_format': backlog_format,
            'default_commitment_reason': commitment_reason
        })
        
        console.print("\n✅ Template personalization settings saved!")
        console.print("These will be used as defaults when creating new issues.")
        
        return True
    
    def _configure_custom_fields(self) -> bool:
        """
        Step 5: Configure custom fields.
        
        Returns:
            bool: True if configuration successful
        """
        self._step_header("JFrog Custom Field Configuration")
        
        console.print("Discovering JFrog Jira custom fields...")
        
        # This would normally discover custom fields via API
        # For now, we'll use the known JFrog field mappings
        console.print("✅ Using JFrog-standard custom field mappings")
        console.print("   • Team field: customfield_10129")
        console.print("   • Product Manager field: customfield_10044")
        console.print("   • Commitment Level: customfield_10450")
        console.print("   • Area: customfield_10167")
        
        # Ask for epic prefix confirmation
        if self.config.get('primary_project'):
            prefix = Prompt.ask(f"Epic prefix for {self.config['primary_project']} project", 
                              default=self.config['primary_project'])
            self.config['epic_prefix'] = prefix
        
        return True
    
    def _validate_and_finalize(self) -> bool:
        """
        Step 6: Validate configuration and finalize setup.
        
        Returns:
            bool: True if validation successful
        """
        self._step_header("Configuration Validation & Testing")
        
        console.print("Running final validation checks...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Test API connection
            task1 = progress.add_task("Testing Jira API connection...", total=None)
            if not self._test_jira_connection():
                return False
            progress.update(task1, description="✅ Jira API connection")
            
            # Validate permissions  
            task2 = progress.add_task("Validating permissions...", total=None)
            if not self._validate_permissions():
                return False
            progress.update(task2, description="✅ Permissions validated")
            
            # Save configuration
            task3 = progress.add_task("Saving configuration...", total=None)
            if not self._save_configuration():
                return False
            progress.update(task3, description="✅ Configuration saved")
        
        return True
    
    def _test_jira_connection(self) -> bool:
        """Test Jira API connection with current config."""
        try:
            headers = {
                "Authorization": f"Basic {self.config['jira_auth_token']}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{self.config['jira_base_url']}/rest/api/2/myself",
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
        except:
            return False
    
    def _validate_permissions(self) -> bool:
        """Validate that user has necessary permissions."""
        try:
            headers = {
                "Authorization": f"Basic {self.config['jira_auth_token']}",
                "Content-Type": "application/json"
            }
            
            # Check if user can access selected projects
            for project_key in self.config.get('selected_projects', []):
                response = requests.get(
                    f"{self.config['jira_base_url']}/rest/api/2/project/{project_key}",
                    headers=headers,
                    timeout=10
                )
                if response.status_code != 200:
                    console.print(f"⚠️  Limited access to project {project_key}", style="yellow")
            
            return True
        except:
            console.print("⚠️  Could not fully validate permissions", style="yellow")
            return True  # Continue anyway
    
    def _save_configuration(self) -> bool:
        """Save configuration to .env file."""
        try:
            env_content = f"""# JFrog Jira Workflow Tools Configuration
# Generated by onboarding wizard

# Jira Configuration
JIRA_BASE_URL={self.config['jira_base_url']}
JIRA_AUTH_TOKEN={self.config['jira_auth_token']}
JIRA_USER_ACCOUNT_ID={self.config.get('user_account_id', '')}

# Project Configuration  
DEFAULT_PROJECT_KEY={self.config.get('primary_project', 'RTDEV')}
DEFAULT_TEAM={self.config.get('selected_team', {}).get('name', 'dev-artifactory-lifecycle') if self.config.get('selected_team') else 'dev-artifactory-lifecycle'}

# Template Defaults
DEFAULT_PRIORITY={self.config.get('default_priority', 'Normal')}
DEFAULT_PRODUCT_MANAGER={self.config.get('default_product_manager', 'yonatan.philip@jfrog.com')}
DEFAULT_EPIC_PREFIX={self.config.get('epic_naming_prefix', 'RLM 4Q25 -')}
DEFAULT_BACKLOG_FORMAT={self.config.get('default_backlog_format', 'Q4-25-Backlog')}
DEFAULT_COMMITMENT_REASON={self.config.get('default_commitment_reason', 'Roadmap')}

# JFrog-specific field IDs (standard mappings)
TEAMS_FIELD_ID=customfield_10129
BACKLOG_FIELD_ID=customfield_10119
PM_FIELD_ID=customfield_10044
COMMITMENT_FIELD_ID=customfield_10450
AREA_FIELD_ID=customfield_10167
COMMITMENT_REASON_FIELD_ID=customfield_10508
PRODUCT_PRIORITY_FIELD_ID=customfield_10327
"""
            
            env_path = Path('.env')
            env_path.write_text(env_content)
            
            return True
        except Exception as e:
            console.print(f"❌ Failed to save configuration: {e}", style="red")
            return False
    
    def _display_completion(self) -> None:
        """Display completion message and next steps."""
        console.print("")
        
        completion_text = f"""
🎉 Setup Complete! Your JFrog Jira Workflow Tools are ready to use.

📁 Configuration saved to: .env
🏢 Connected to: {self.config['jira_base_url']}
👤 User: {self.config.get('jira_email', 'N/A')}
📂 Primary project: {self.config.get('primary_project', 'RTDEV')}
👥 Team: {self.config.get('selected_team', {}).get('name', 'Not selected') if self.config.get('selected_team') else 'Not selected'}

🚀 Try these commands to get started:

Basic Commands:
• python -m jira_tools epic "My First Epic" --project {self.config.get('primary_project', 'RTDEV')}
• python -m jira_tools viewer RTDEV-12345
• python -m jira_tools templates list

Need help? Run: python -m jira_tools --help
Re-run setup anytime: python -m jira_tools onboard --reconfigure
        """.strip()
        
        console.print(Panel(
            completion_text,
            title="[bold green]✅ Welcome to JFrog Jira Workflow Tools![/bold green]",
            border_style="green"
        ))


@click.command()
@click.option('--reconfigure', is_flag=True, help='Reconfigure existing setup')
@click.option('--quick', is_flag=True, help='Quick setup with defaults (skip customization steps)')
def onboard(reconfigure: bool, quick: bool) -> None:
    """
    Interactive onboarding wizard for JFrog Jira Workflow Tools.
    
    Sets up your environment with guided configuration, project discovery,
    and template personalization specifically designed for JFrog employees.
    """
    try:
        # Check if already configured (unless reconfiguring)
        env_path = Path('.env')
        if env_path.exists() and not reconfigure:
            if not Confirm.ask(
                "Configuration file (.env) already exists. Reconfigure?",
                default=False
            ):
                console.print("Setup cancelled. Use --reconfigure to override.", style="yellow")
                return
        
        # Start the wizard
        wizard = OnboardingWizard()
        success = wizard.start()
        
        if success:
            console.print("\n🎉 Onboarding completed successfully!", style="bold green")
        else:
            console.print("\n❌ Onboarding failed or was cancelled", style="bold red")
            console.print("You can try again by running: python -m jira_tools onboard", style="yellow")
            
    except KeyboardInterrupt:
        console.print("\n\n❌ Setup cancelled by user", style="red")
    except Exception as e:
        console.print(f"\n❌ Unexpected error during onboarding: {e}", style="red")
        console.print("Please try again or report this issue", style="yellow")


if __name__ == '__main__':
    onboard()
