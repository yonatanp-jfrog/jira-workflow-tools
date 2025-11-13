#!/usr/bin/env python3
"""
Interactive Staged Epic Creator - Simple interface for the two-phase epic workflow.

This provides a guided interface for creating staged epics that can be reviewed
and refined before submission to Jira.
"""

import click
import subprocess
import sys
from pathlib import Path


@click.command()
def main():
    """
    Interactive staged epic creator - creates epics for review before submission.
    
    This is a two-phase workflow:
    1. Stage: Create markdown file for review and editing
    2. Submit: Create actual Jira epic from approved markdown
    """
    
    click.echo("🎯 JFrog Staged Epic Creator - Interactive Mode")
    click.echo("=" * 60)
    click.echo("📝 Phase 1: Create staged epic for review and collaboration")
    click.echo()
    
    # Get basic required information
    project = click.prompt("Project (RTDEV/APP)", type=click.Choice(['RTDEV', 'APP'], case_sensitive=False))
    epic_name = click.prompt("Epic name")
    
    # Optional parameters with defaults
    description = click.prompt("Description", default="TBD", show_default=True)
    
    # Show project-specific defaults
    if project.upper() == 'RTDEV':
        default_team = 'dev-artifactory-lifecycle'
    else:
        default_team = 'App Core'
    
    team = click.prompt(f"Team", default=default_team, show_default=True)
    
    priority = click.prompt("Priority", 
                          type=click.Choice(['1 - Blocker', '2 - Critical', '3 - High', '4 - Normal', '5 - Minor', '6 - Trivial']),
                          default='4 - Normal', show_default=True)
    
    commitment_level = click.prompt("Commitment Level",
                                  type=click.Choice(['Hard Commitment', 'Soft Commitment', 'KTLO']),
                                  default='Soft Commitment', show_default=True)
    
    # Optional advanced fields
    if click.confirm("Set advanced options? (parent, product priority)", default=False):
        parent = click.prompt("Parent issue key (optional)", default="", show_default=False)
        product_priority = click.prompt("Product priority (P0-P4, optional)", 
                                      type=click.Choice(['', 'P0', 'P1', 'P2', 'P3', 'P4']),
                                      default="", show_default=False)
    else:
        parent = ""
        product_priority = ""
    
    # Build command
    cmd = [
        'python3', 'staged_epic_creator.py', 'stage',
        project,
        epic_name,
        '--description', description,
        '--team', team,
        '--priority', priority,
        '--commitment-level', commitment_level
    ]
    
    if parent:
        cmd.extend(['--parent', parent])
    
    if product_priority:
        cmd.extend(['--product-priority', product_priority])
    
    # Show what will be created
    click.echo("\n" + "=" * 60)
    click.echo("📋 Staged Epic Summary:")
    click.echo(f"🎯 Project: {project}")
    click.echo(f"📝 Name: {epic_name}")
    click.echo(f"📄 Description: {description}")
    click.echo(f"👥 Team: {team}")
    click.echo(f"⚡ Priority: {priority}")
    click.echo(f"🤝 Commitment: {commitment_level}")
    if parent:
        click.echo(f"🔗 Parent: {parent}")
    if product_priority:
        click.echo(f"📊 Product Priority: {product_priority}")
    
    if click.confirm("\n✅ Create staged epic?", default=True):
        click.echo("\n🚀 Creating staged epic...")
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            if result.returncode == 0:
                click.echo(result.stdout)
                
                # Extract filename from output
                lines = result.stdout.split('\n')
                file_line = [line for line in lines if 'File:' in line]
                if file_line:
                    file_path = file_line[0].split('File: ')[1].strip()
                    
                    click.echo("🎉 Staged epic created successfully!")
                    click.echo("\n📝 Next Steps:")
                    click.echo("1. 📖 Review and edit the staged epic file")
                    click.echo("2. 👥 Share with team for feedback")
                    click.echo("3. ✅ When approved, submit to Jira")
                    click.echo("\n🔧 Useful Commands:")
                    click.echo(f"   📝 Edit: open '{file_path}'")
                    click.echo(f"   📋 List: python3 staged_epic_creator.py list")
                    click.echo(f"   🚀 Submit: python3 staged_epic_creator.py submit {Path(file_path).name}")
                    
                    if click.confirm("\nWould you like to open the staged epic file for editing?"):
                        import os
                        os.system(f"open '{file_path}'")
            
        except subprocess.CalledProcessError as e:
            click.echo(f"\n❌ Error creating staged epic: {e}")
            if e.stderr:
                click.echo(f"Details: {e.stderr}")
            sys.exit(1)
        except KeyboardInterrupt:
            click.echo("\n⏹️ Cancelled by user")
            sys.exit(1)
    else:
        click.echo("⏹️ Staged epic creation cancelled")


if __name__ == '__main__':
    main()
