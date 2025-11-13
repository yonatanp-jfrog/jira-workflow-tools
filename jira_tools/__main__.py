"""
Main entry point for Jira Workflow Tools.

This module allows the package to be run as:
    python -m jira_tools [command] [args]

Examples:
    python -m jira_tools setup --private
    python -m jira_tools epic create "My Epic"
    python -m jira_tools viewer PROJ-123
    python -m jira_tools --help
"""

import sys
from pathlib import Path

# Add the parent directory to sys.path for development
# This allows importing from the legacy modules during transition
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

try:
    from .cli import main
except ImportError:
    # Fallback during development - create a basic CLI
    import click
    from rich.console import Console
    
    console = Console()


    def _interactive_epic_creation():
        """Interactive epic creation with step-by-step prompts."""
        from jira_tools.core.field_mappings import jira_fields
        from rich.panel import Panel
        from rich.table import Table
        
        console.print(Panel(
            "[bold green]🚀 Interactive Epic Creator[/bold green]\n\n"
            "This wizard will guide you through creating a Jira epic with all available options.",
            title="Epic Creation Wizard"
        ))
        
        # Get basic information
        epic_name = click.prompt("Epic name")
        project = click.prompt("Project", type=click.Choice(['RTDEV', 'APP']), default='RTDEV')
        
        # Get project defaults  
        project_defaults = jira_fields.get_project_defaults(project)
        
        description = click.prompt("Description", default="TBD", show_default=True)
        priority = click.prompt("Priority", 
                               type=click.Choice(jira_fields.get_available_choices()['priorities']),
                               default='4 - Normal', show_default=True)
        
        # Advanced fields with defaults
        commitment_level = None
        area = None
        product_priority = None
        parent = None
        commitment_reason = None
        
        if click.confirm("Set advanced fields? (commitment level, area, priorities, etc.)", default=False):
            commitment_level = click.prompt("Commitment Level",
                                          type=click.Choice(jira_fields.get_available_choices()['commitment_levels']),
                                          default='Soft Commitment', show_default=True)
            area = click.prompt("Area",
                              type=click.Choice(jira_fields.get_available_choices()['areas']),
                              default='Features & Innovation', show_default=True)
            commitment_reason = click.prompt("Commitment Reason",
                                           type=click.Choice(jira_fields.get_available_choices()['commitment_reasons']),
                                           default='Roadmap', show_default=True)
            
            if click.confirm("Set product priority and parent epic?", default=False):
                product_priority = click.prompt("Product Priority (optional)",
                                              type=click.Choice([''] + jira_fields.get_available_choices()['product_priorities']),
                                              default='', show_default=False)
                product_priority = product_priority if product_priority else None
                
                parent = click.prompt("Parent issue key (optional, e.g. RTDEV-12345)", default='', show_default=False)
                parent = parent if parent else None
        
        # Team and product manager
        team = click.prompt("Team", default=project_defaults['team'], show_default=True)
        product_backlog = click.prompt("Product Backlog", default='Q4-25-Backlog', show_default=True)
        
        # Show summary
        console.print("\n📋 Epic Summary:")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Epic Name", epic_name)
        table.add_row("Project", project)
        table.add_row("Description", description or "TBD")
        table.add_row("Priority", priority)
        table.add_row("Team", team)
        table.add_row("Product Backlog", product_backlog)
        
        if commitment_level:
            table.add_row("Commitment Level", commitment_level)
        if area:
            table.add_row("Area", area)
        if commitment_reason:
            table.add_row("Commitment Reason", commitment_reason)
        if product_priority:
            table.add_row("Product Priority", product_priority)
        if parent:
            table.add_row("Parent Epic", parent)
        
        console.print(table)
        
        if click.confirm("\nCreate this epic?", default=True):
            # Call the epic function directly with the collected parameters
            epic(
                epic_name=epic_name,
                project=project,
                template=None,
                description=description,
                priority=priority,
                commitment_level=commitment_level,
                area=area,
                product_manager=None,
                product_backlog=product_backlog,
                parent=parent,
                product_priority=product_priority,
                team=team,
                commitment_reason=commitment_reason,
                interactive=False,
                dry_run=False
            )
        else:
            console.print("Epic creation cancelled.")


    @click.group()
    @click.version_option(version="2.0.0-team")
    def main():
        """
        🎯 Jira Workflow Tools - Internal Team Version
        
        Secure, team-focused toolkit for Jira epic creation and ticket management.
        """
        pass
    
    @main.command()
    @click.option('--private', is_flag=True, help='Set up private mode')
    def setup(private):
        """Set up Jira Workflow Tools configuration."""
        if private:
            console.print("🔒 Private mode setup will be implemented in Phase 4")
            console.print("For now, please use environment variables:")
            console.print("1. Copy env.template to .env")
            console.print("2. Fill in your Jira credentials")
            console.print("3. Run: python -m jira_tools test-config")
        else:
            console.print("📋 Basic setup:")
            console.print("1. Copy env.template to .env")
            console.print("2. Edit .env with your Jira configuration")
            console.print("3. Test: python -m jira_tools test-config")
    
    @main.command()
    def test_config():
        """Test Jira configuration and connection."""
        try:
            from jira_tools.core.config import ConfigManager
            from jira_tools.core.client import JiraClient
            
            console.print("🧪 Testing Jira configuration...")
            
            config = ConfigManager()
            console.print(f"📡 Configuration source: {config.config_source}")
            
            if not config.validate_config():
                console.print("❌ Configuration invalid. Please check your .env file.")
                return
            
            console.print("✅ Configuration valid")
            console.print(f"🌐 Jira URL: {config.jira_base_url}")
            
            # Test connection
            with JiraClient(config) as client:
                if client.test_connection():
                    user_info = client.get_user_info()
                    if user_info:
                        console.print(f"✅ Connection successful!")
                        console.print(f"👤 Logged in as: {user_info.get('displayName', 'Unknown')}")
                    else:
                        console.print("✅ Connection successful!")
                else:
                    console.print("❌ Connection failed. Please check your credentials.")
                    
        except Exception as e:
            console.print(f"❌ Error: {e}")
    
    @main.command()
    @click.argument('issue_input')
    @click.option('--raw', is_flag=True, help='Display raw JSON data instead of formatted output')
    @click.option('--output', '-o', help='Output file path (saves to file instead of console)')
    @click.option('--format', 'output_format', 
                  type=click.Choice(['console', 'markdown', 'json']), 
                  default='console', help='Output format')
    @click.option('--url', is_flag=True, help='Also display the web URL for the issue')
    def viewer(issue_input, raw, output, output_format, url):
        """
        View a Jira issue in various formats.
        
        ISSUE_INPUT can be:
        - Direct issue key: RTDEV-12345
        - Full Jira URL: https://company.atlassian.net/browse/RTDEV-12345
        - Browse path: /browse/RTDEV-12345
        """
        try:
            from jira_tools.core.client import JiraClient
            from jira_tools.core.formatters import (
                jira_formatter, markdown_formatter, json_formatter, file_manager
            )
            from jira_tools.utils.url_parser import extract_issue_key
            from jira_tools.core.config import ConfigManager
            
            # Extract issue key from input (handles both keys and URLs)
            try:
                issue_key = extract_issue_key(issue_input)
            except ValueError as e:
                console.print(f"❌ {e}", style="red")
                return
            
            # Show what we're fetching
            if issue_input != issue_key:
                console.print(f"🔍 Fetching issue: [bold cyan]{issue_key}[/bold cyan] (extracted from: {issue_input})")
            else:
                console.print(f"🔍 Fetching issue: [bold cyan]{issue_key}[/bold cyan]")
            
            # Get configuration for URL building
            config = ConfigManager()
            
            # Fetch the issue
            client = JiraClient()
            issue_data = client.get_issue(issue_key)
            
            if not issue_data:
                console.print(f"❌ Issue {issue_key} not found or access denied", style="red")
                return
            
            # Build issue URL
            issue_url = client.get_issue_url(issue_key) if url or output_format != 'console' else None
            
            # Handle raw JSON output (legacy compatibility)
            if raw:
                output_format = 'json'
            
            # Generate output based on format
            if output_format == 'console':
                if output:
                    console.print("⚠️  Console format with --output flag will save formatted text", style="yellow")
                    # Generate plain text version for file output
                    content = f"Issue: {issue_key}\n"
                    content += f"Summary: {issue_data['fields']['summary']}\n"
                    content += f"Status: {issue_data['fields']['status']['name']}\n"
                    content += f"Priority: {issue_data['fields']['priority']['name']}\n"
                    content += f"Type: {issue_data['fields']['issuetype']['name']}\n"
                    if issue_url:
                        content += f"URL: {issue_url}\n"
                    
                    # Save to file
                    output_path = file_manager.save_issue_to_file(
                        content, issue_key, "txt", output
                    )
                    console.print(f"📄 Output saved to: [cyan]{output_path}[/cyan]")
                else:
                    # Display to console with rich formatting
                    jira_formatter.format_issue(issue_data, issue_key, issue_url)
                    
            elif output_format == 'markdown':
                content = markdown_formatter.format_issue_to_markdown(
                    issue_data, issue_key, issue_url
                )
                
                if output:
                    output_path = file_manager.save_issue_to_file(
                        content, issue_key, "md", output
                    )
                    console.print(f"📄 Markdown saved to: [cyan]{output_path}[/cyan]")
                else:
                    console.print(content)
                    
            elif output_format == 'json':
                content = json_formatter.format_issue_to_json(issue_data)
                
                if output:
                    output_path = file_manager.save_issue_to_file(
                        content, issue_key, "json", output
                    )
                    console.print(f"📄 JSON saved to: [cyan]{output_path}[/cyan]")
                else:
                    console.print_json(data=issue_data)
            
            # Show URL if requested and not already included
            if url and output_format == 'console' and not output:
                console.print(f"\n🔗 Web URL: [link={issue_url}]{issue_url}[/link]")
            
            if not output:
                console.print("✅ Done!", style="green")
                
        except Exception as e:
            console.print(f"❌ Error: {e}", style="red")

    @main.group()
    def templates():
        """Manage Jira issue templates."""
        pass
    
    @templates.command()
    @click.option('--issue-type', help='Filter by issue type (epic, story, task, bug)')
    def list(issue_type):
        """List available templates."""
        try:
            from jira_tools.core.templates import template_manager
            from rich.table import Table
            
            console.print("🎨 Available Jira Templates")
            
            templates_list = template_manager.list_templates(issue_type)
            
            if not templates_list:
                console.print("No templates found.")
                return
            
            table = Table(title="Templates")
            table.add_column("Template Name", style="green")
            table.add_column("Project", style="cyan")
            table.add_column("Issue Type", style="magenta") 
            table.add_column("Team", style="blue")
            table.add_column("Description", style="yellow")
            
            for template in templates_list:
                template_name = template['name']
                project = template['project']
                issue_type = template['issue_type']
                team = template.get('team') or 'optional'
                description = template['description']
                
                # Truncate long descriptions
                if len(description) > 50:
                    description = description[:47] + "..."
                
                table.add_row(
                    template_name,
                    project,
                    issue_type,
                    team,
                    description
                )
            
            console.print(table)
            
        except Exception as e:
            console.print(f"❌ Error: {e}")
    
    @templates.command()
    @click.argument('template_path')
    def validate(template_path):
        """Validate a template file."""
        try:
            from jira_tools.core.templates import template_manager
            
            console.print(f"🧪 Validating template: {template_path}")
            
            result = template_manager.validate_template(template_path)
            
            if result['valid']:
                console.print("✅ Template is valid!")
                if result['metadata']:
                    meta = result['metadata']
                    console.print(f"📋 Type: {meta['issue_type']}")
                    console.print(f"📄 Name: {meta['name']}")
                    console.print(f"📝 Description: {meta['description']}")
            else:
                console.print("❌ Template validation failed:")
                for error in result['errors']:
                    console.print(f"  • {error}")
            
            if result['warnings']:
                console.print("⚠️  Warnings:")
                for warning in result['warnings']:
                    console.print(f"  • {warning}")
                    
        except Exception as e:
            console.print(f"❌ Error: {e}")
    
    @templates.command()
    @click.argument('template_name')
    @click.option('--type', 'issue_type', help='Filter by issue type (epic, story, task, bug)')
    def describe(template_name, issue_type):
        """Get detailed, user-friendly description of what a template does."""
        try:
            from jira_tools.core.templates import template_manager
            from rich.panel import Panel
            from rich.table import Table
            from rich.columns import Columns
            from rich.text import Text
            
            console.print(f"🔍 Analyzing template: [bold cyan]{template_name}[/bold cyan]")
            
            # Get detailed template description
            description = template_manager.describe_template(template_name, issue_type)
            
            if 'error' in description:
                console.print(f"❌ Error: {description['error']}", style="red")
                return
            
            # Display template header
            header_table = Table.grid(padding=1)
            header_table.add_column("Field", style="bold cyan")
            header_table.add_column("Value", style="white")
            
            header_table.add_row("📛 Name:", description['name'])
            header_table.add_row("📂 Type:", description['type'] or 'generic')
            header_table.add_row("📄 Source:", description['source'])
            header_table.add_row("📁 Path:", description['path'])
            
            console.print(Panel(header_table, title="📋 Template Information", border_style="blue"))
            
            # Display summary
            console.print("\n📝 What This Template Does:")
            console.print(Panel(description['summary'], border_style="green"))
            
            # Display fields analysis
            fields = description.get('fields', {})
            
            if fields.get('always_set'):
                console.print("\n✅ Fields Always Set:")
                always_table = Table(show_header=True, header_style="bold green")
                always_table.add_column("Field", style="cyan")
                always_table.add_column("Value", style="white")
                always_table.add_column("Description", style="dim")
                
                for field in fields['always_set']:
                    always_table.add_row(field['field'], field['value'], field['description'])
                console.print(always_table)
            
            if fields.get('defaults_used'):
                console.print("\n🎯 Smart Defaults Provided:")
                defaults_table = Table(show_header=True, header_style="bold yellow")
                defaults_table.add_column("Field", style="cyan")
                defaults_table.add_column("Default Value", style="white")
                defaults_table.add_column("Description", style="dim")
                
                for field in fields['defaults_used']:
                    defaults_table.add_row(field['field'], field['value'], field['description'])
                console.print(defaults_table)
            
            if fields.get('user_provided'):
                console.print("\n👤 Your Input Used For:")
                user_table = Table(show_header=True, header_style="bold magenta")
                user_table.add_column("Field", style="cyan")
                user_table.add_column("Source", style="white")
                user_table.add_column("Description", style="dim")
                
                for field in fields['user_provided']:
                    user_table.add_row(field['field'], field['value'], field['description'])
                console.print(user_table)
            
            if fields.get('conditional'):
                console.print("\n🔄 Optional Advanced Fields:")
                cond_table = Table(show_header=True, header_style="bold blue")
                cond_table.add_column("Field", style="cyan")
                cond_table.add_column("When Set", style="white")
                cond_table.add_column("Description", style="dim")
                
                for field in fields['conditional']:
                    cond_table.add_row(field['field'], field['value'], field['description'])
                console.print(cond_table)
            
            # Display usage examples
            examples = description.get('usage_examples', [])
            if examples:
                console.print("\n🚀 Usage Examples:")
                for i, example in enumerate(examples, 1):
                    console.print(f"[dim]{i}.[/dim] [green]{example}[/green]")
            
            console.print(f"\n✅ Template analysis complete for [bold cyan]{template_name}[/bold cyan]!")
            
        except Exception as e:
            console.print(f"❌ Error describing template: {e}", style="red")

    @templates.command()
    @click.argument('issue_type', type=click.Choice(['epic', 'story', 'task', 'bug']))
    @click.argument('template_name')
    @click.option('--description', help='Template description')
    def create(issue_type, template_name, description):
        """Create a new template (interactive)."""
        try:
            from jira_tools.core.templates import template_manager
            
            console.print(f"🎨 Creating new {issue_type} template: {template_name}")
            
            # Get template content from user
            console.print("Enter template content (JSON format). Press Ctrl+D when done:")
            console.print("Example:")
            console.print('{"fields": {"project": {"id": "{{ project.id }}"}, "summary": "{{ epic.name }}"}}')
            console.print("")
            
            import sys
            content_lines = []
            try:
                for line in sys.stdin:
                    content_lines.append(line)
            except KeyboardInterrupt:
                console.print("\n❌ Template creation cancelled")
                return
            
            content = ''.join(content_lines)
            
            if not content.strip():
                console.print("❌ No content provided")
                return
            
            # Create template
            template_file = template_manager.create_template(
                issue_type, template_name, content, description
            )
            
            console.print(f"✅ Template created: {template_file}")
            
            # Validate the new template
            result = template_manager.validate_template(template_file)
            if result['valid']:
                console.print("✅ Template validation passed")
            else:
                console.print("⚠️  Template created but has validation issues:")
                for error in result['errors']:
                    console.print(f"  • {error}")
                    
        except Exception as e:
            console.print(f"❌ Error: {e}")
    
    @main.command()
    @click.argument('epic_name')
    @click.option('--project', default='RTDEV', type=click.Choice(['RTDEV', 'APP']), help='Project key')
    @click.option('--template', help='Template name to use')
    @click.option('--description', help='Epic description')
    @click.option('--priority', default='4 - Normal', 
                  type=click.Choice(['1 - Blocker', '1 - Highest', '2 - Critical', '2 - High', '3 - High', '4 - Normal', '5 - Minor', '5 - Low', '6 - Trivial']), 
                  help='Priority level')
    @click.option('--commitment-level', 
                  type=click.Choice(['Hard Commitment', 'Soft Commitment', 'KTLO']), 
                  help='Commitment level (Hard/Soft/KTLO)')
    @click.option('--area', 
                  type=click.Choice(['Features & Innovation', 'Enablers & Tech Debt', 'KTLO']), 
                  help='Work area classification')
    @click.option('--product-manager', help='Product manager (defaults to current user if not specified)')
    @click.option('--product-backlog', default='Q4-25-Backlog', help='Product backlog classification')
    @click.option('--parent', help='Parent issue key (e.g., RTDEV-12345)')
    @click.option('--product-priority', 
                  type=click.Choice(['P0', 'P1', 'P2', 'P3', 'P4']), 
                  help='Product priority ranking')
    @click.option('--team', help='Team name (uses project default if not specified)')
    @click.option('--commitment-reason', 
                  type=click.Choice(['Roadmap', 'Customer Commitment', 'Security']), 
                  help='Reason for commitment')
    @click.option('--technical-writer', help='Technical writer account ID or username')
    @click.option('--ux-designer', help='UX designer account ID or username')
    @click.option('--architect', help='Architect account ID or username')
    @click.option('--interactive', is_flag=True, help='Interactive mode with step-by-step prompts')
    @click.option('--dry-run', is_flag=True, help='Show rendered template without creating')
    @click.option('--explain', is_flag=True, help='Show what the template will do in human-readable format')
    @click.option('--attach', help='Comma-separated list of files to attach (e.g., screenshot.png,design.pdf)')
    def epic(epic_name, project, template, description, priority, commitment_level, area, 
             product_manager, product_backlog, parent, product_priority, team, 
             commitment_reason, technical_writer, ux_designer, architect, interactive, dry_run, explain, attach):
        """Create a Jira epic using templates."""
        try:
            from jira_tools.core.templates import template_manager, TemplateContext
            from jira_tools.core.client import JiraClient
            from jira_tools.core.config import ConfigManager
            from jira_tools.core.field_mappings import jira_fields
            
            # Handle interactive mode
            if interactive:
                return _interactive_epic_creation()
            
            console.print(f"🎯 Creating epic: {epic_name}")
            
            # Get configuration and project defaults
            config = ConfigManager()
            project_defaults = jira_fields.get_project_defaults(project)
            
            # Use project default team if not specified
            if not team:
                team = project_defaults['team']
            
            # Default template selection based on provided fields
            if not template:
                # Use advanced template if any advanced fields are provided
                has_advanced_fields = any([
                    commitment_level, area, product_manager, parent, 
                    product_priority, commitment_reason
                ])
                template = 'advanced' if has_advanced_fields else 'base'
            
            # Build comprehensive template context
            context = TemplateContext.build_epic_context(
                epic_name=epic_name,
                project_key=project,
                description=description,
                priority=priority,
                commitment_level=commitment_level,
                area=area,
                product_manager=product_manager or config.user_account_id,
                product_backlog=product_backlog,
                parent=parent,
                product_priority=product_priority,
                team_name=team,
                commitment_reason=commitment_reason,
                project_id=project_defaults['project_id'],
                team_id=project_defaults['team_id'],
                user_account_id=config.user_account_id,
                technical_writer=technical_writer,
                ux_designer=ux_designer,
                architect=architect
            )
            
            # Select and render template
            template_obj = template_manager.select_template(
                issue_type='epic',
                project_key=project,
                template_name=template
            )
            
            rendered = template_manager.render_template(template_obj, context)
            
            if explain:
                # Show user-friendly explanation of what the template will do
                console.print(f"🔍 Explaining what template '[cyan]{template}[/cyan]' will do:")
                
                try:
                    description = template_manager.describe_template(template, 'epic')
                    
                    # Show a condensed explanation
                    console.print(f"\n📝 {description['summary']}")
                    
                    fields = description.get('fields', {})
                    
                    if fields.get('always_set'):
                        console.print(f"\n✅ Will automatically set {len(fields['always_set'])} required fields:")
                        for field in fields['always_set'][:3]:  # Show first 3
                            console.print(f"   • {field['field']}: {field['value']}")
                        if len(fields['always_set']) > 3:
                            console.print(f"   • ... and {len(fields['always_set']) - 3} more")
                    
                    if fields.get('defaults_used'):
                        console.print(f"\n🎯 Will use {len(fields['defaults_used'])} smart defaults:")
                        for field in fields['defaults_used'][:3]:  # Show first 3
                            console.print(f"   • {field['field']}: {field['value']}")
                        if len(fields['defaults_used']) > 3:
                            console.print(f"   • ... and {len(fields['defaults_used']) - 3} more")
                    
                    if fields.get('conditional'):
                        console.print(f"\n🔄 Supports {len(fields['conditional'])} optional advanced fields:")
                        for field in fields['conditional'][:3]:  # Show first 3
                            console.print(f"   • {field['field']}: {field['description']}")
                        if len(fields['conditional']) > 3:
                            console.print(f"   • ... and {len(fields['conditional']) - 3} more")
                    
                    console.print(f"\n💡 For full details: [green]python3 -m jira_tools templates describe {template}[/green]")
                    
                except Exception as e:
                    console.print(f"⚠️  Could not explain template: {e}")
                    console.print("Use --dry-run instead to see the raw JSON output")
                
                return
            
            if dry_run:
                console.print("🔍 Rendered template (dry run):")
                console.print(rendered)
                return
            
            # Create the epic
            with JiraClient(config) as client:
                import json
                issue_data = json.loads(rendered)
                result = client.create_issue(issue_data)
                
                if result:
                    console.print("✅ Epic created successfully!")
                    console.print(f"🎫 Epic Key: {result['key']}")
                    console.print(f"🔗 URL: {result.get('web_url', 'N/A')}")
                    
                    # Handle file attachments if provided
                    if attach:
                        try:
                            # Parse attachment file paths
                            file_paths = [path.strip() for path in attach.split(',') if path.strip()]
                            
                            if file_paths:
                                console.print(f"📎 Attaching {len(file_paths)} file(s)...")
                                
                                # Attach files to the created issue
                                attachments = client.attach_files_to_issue(result['key'], file_paths)
                                
                                console.print("✅ Files attached successfully!")
                                for attachment in attachments:
                                    size_mb = attachment.get('size', 0) / (1024 * 1024)
                                    console.print(f"   📎 {attachment.get('filename', 'Unknown')} ({size_mb:.1f}MB)")
                                
                                # Update issue description with attachment references
                                attachment_list = []
                                for attachment in attachments:
                                    filename = attachment.get('filename', 'Unknown')
                                    attachment_list.append(f"- 📎 [{filename}]({attachment.get('content', '#')})")
                                
                                if attachment_list:
                                    console.print("💡 Tip: Attachments are now visible in the Jira issue")
                        
                        except ValueError as e:
                            console.print(f"⚠️  Attachment error: {e}", style="yellow")
                        except Exception as e:
                            console.print(f"⚠️  Failed to attach files: {e}", style="yellow")
                            console.print("💡 Epic was created successfully, but file attachment failed")
                else:
                    console.print("❌ Failed to create epic")
                    
        except Exception as e:
            console.print(f"❌ Error: {e}")

    @main.group()
    def private():
        """Manage private mode (encrypted local storage)."""
        pass
    
    @private.command()
    def setup():
        """Set up private mode with interactive wizard."""
        try:
            from jira_tools.private_mode import private_mode_manager
            
            success = private_mode_manager.setup_interactive()
            if success:
                console.print("🎉 Private mode setup complete!")
                console.print("You can now use all commands with encrypted local storage.")
            else:
                console.print("❌ Private mode setup failed")
                
        except Exception as e:
            console.print(f"❌ Error setting up private mode: {e}")
    
    @private.command()
    def status():
        """Show private mode status and configuration."""
        try:
            from jira_tools.private_mode import private_mode_manager
            from rich.table import Table
            
            console.print("🔒 Private Mode Status")
            
            # Basic status
            is_configured = private_mode_manager.is_configured()
            status_color = "green" if is_configured else "red"
            status_text = "✅ Configured" if is_configured else "❌ Not Configured"
            
            console.print(f"Status: [{status_color}]{status_text}[/{status_color}]")
            console.print(f"Config Directory: {private_mode_manager.config_dir}")
            
            if is_configured:
                # Load configuration details
                config_data = private_mode_manager.get_jira_config()
                
                table = Table(title="Configuration Details")
                table.add_column("Setting", style="cyan")
                table.add_column("Value", style="yellow")
                
                table.add_row("Jira URL", config_data.get('jira_base_url', 'N/A'))
                table.add_row("User Account ID", config_data.get('user_account_id', 'N/A'))
                table.add_row("Email", config_data.get('email', 'N/A'))
                table.add_row("Setup Date", config_data.get('setup_date', 'N/A'))
                
                console.print(table)
                
                # Template directory info
                template_count = len(list(private_mode_manager.templates_dir.rglob("*.j2"))) if private_mode_manager.templates_dir.exists() else 0
                console.print(f"📝 Local Templates: {template_count}")
                
                # Backup info
                backups = private_mode_manager.list_backups()
                console.print(f"💾 Backups: {len(backups)}")
                
            else:
                console.print("\n💡 To set up private mode:")
                console.print("   python -m jira_tools private setup")
                
        except Exception as e:
            console.print(f"❌ Error checking private mode status: {e}")
    
    @private.command()
    @click.argument('backup_name', required=False)
    def backup(backup_name):
        """Create encrypted backup of private mode configuration."""
        try:
            from jira_tools.private_mode import private_mode_manager
            
            if not private_mode_manager.is_configured():
                console.print("❌ Private mode not configured")
                return
                
            backup_file = private_mode_manager.create_backup(backup_name)
            console.print(f"✅ Backup created: {backup_file.name}")
            
        except Exception as e:
            console.print(f"❌ Error creating backup: {e}")
    
    @private.command()
    def list_backups():
        """List available encrypted backups."""
        try:
            from jira_tools.private_mode import private_mode_manager
            from rich.table import Table
            
            backups = private_mode_manager.list_backups()
            
            if not backups:
                console.print("No backups found")
                return
            
            table = Table(title="Available Backups")
            table.add_column("Name", style="cyan")
            table.add_column("Created", style="yellow")
            table.add_column("Size", style="green")
            
            for backup in backups:
                size_mb = backup['size'] / 1024 / 1024
                table.add_row(
                    backup['name'],
                    backup['created'].strftime('%Y-%m-%d %H:%M:%S'),
                    f"{size_mb:.2f} MB"
                )
            
            console.print(table)
            
        except Exception as e:
            console.print(f"❌ Error listing backups: {e}")
    
    @private.command()
    @click.argument('backup_name')
    def restore(backup_name):
        """Restore from encrypted backup."""
        try:
            from jira_tools.private_mode import private_mode_manager
            from rich.prompt import Confirm
            
            console.print(f"⚠️  This will overwrite current private mode configuration!")
            if not Confirm.ask(f"Restore from backup '{backup_name}'?"):
                console.print("Restore cancelled")
                return
            
            success = private_mode_manager.restore_backup(backup_name)
            if success:
                console.print("✅ Restore completed successfully")
            else:
                console.print("❌ Restore failed")
                
        except Exception as e:
            console.print(f"❌ Error restoring backup: {e}")
    
    @private.command()
    def audit():
        """Perform security audit of private mode setup."""
        try:
            from jira_tools.private_mode import private_mode_manager
            from rich.panel import Panel
            
            if not private_mode_manager.is_configured():
                console.print("❌ Private mode not configured")
                return
            
            audit_results = private_mode_manager.audit()
            
            # Display results
            status_color = {
                'secure': 'green',
                'warning': 'yellow', 
                'error': 'red'
            }.get(audit_results['overall_status'], 'white')
            
            status_icon = {
                'secure': '🔒',
                'warning': '⚠️',
                'error': '🚨'
            }.get(audit_results['overall_status'], '❓')
            
            console.print(Panel(
                f"[{status_color}]{status_icon} Overall Status: {audit_results['overall_status'].upper()}[/{status_color}]",
                title="Security Audit Results"
            ))
            
            if audit_results['warnings']:
                console.print("\n⚠️  Warnings:")
                for warning in audit_results['warnings']:
                    console.print(f"  • {warning}")
            
            if audit_results['errors']:
                console.print("\n🚨 Errors:")
                for error in audit_results['errors']:
                    console.print(f"  • {error}")
            
            if audit_results['recommendations']:
                console.print("\n💡 Recommendations:")
                for rec in audit_results['recommendations']:
                    console.print(f"  • {rec}")
            
            if audit_results['overall_status'] == 'secure':
                console.print("\n✅ Private mode setup is secure!")
                
        except Exception as e:
            console.print(f"❌ Error performing audit: {e}")
    
    @private.command()
    def reset():
        """Reset private mode (delete all data)."""
        try:
            from jira_tools.private_mode import private_mode_manager
            
            private_mode_manager.reset()
            
        except Exception as e:
            console.print(f"❌ Error resetting private mode: {e}")

if __name__ == '__main__':
    main()
