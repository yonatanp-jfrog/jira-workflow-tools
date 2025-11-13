#!/usr/bin/env python3
"""
🚨 DEPRECATED SCRIPT 🚨

This script is DEPRECATED and will be removed on 2025-03-01.

👉 USE INSTEAD: python3 -m jira_tools epic --interactive
📖 Migration Guide: See MIGRATION_GUIDE.md
🆕 New System: Enhanced interactive mode + all features

Simple wrapper for epic_creator.py - makes it even easier to create epics.

This is a simplified interface that asks for the most common parameters interactively.
"""

import click
import subprocess
import sys


@click.command()
def main():
    """
    Interactive epic creator - asks for the most common parameters.
    
    For advanced options, use epic_creator.py directly.
    """
    
    # 🚨 DEPRECATION WARNING
    click.echo("🚨 " + "="*70 + " 🚨", err=True)
    click.echo("🚨 DEPRECATION WARNING: This script will be removed on 2025-03-01", err=True)
    click.echo("🚨", err=True)
    click.echo("🚨 👉 USE INSTEAD: python3 -m jira_tools epic --interactive", err=True)
    click.echo("🚨 📖 Migration Guide: See MIGRATION_GUIDE.md", err=True)
    click.echo("🚨 🆕 New System: Enhanced interactive mode + all features", err=True)
    click.echo("🚨 " + "="*70 + " 🚨", err=True)
    click.echo("")
    
    if not click.confirm("Continue with deprecated script?"):
        click.echo("👍 Great choice! Use the new system: python3 -m jira_tools epic --interactive")
        return
    
    click.echo("🚀 JFrog Epic Creator - Interactive Mode")
    click.echo("=" * 50)
    
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
        'python3', 'epic_creator.py',
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
    click.echo("\n" + "=" * 50)
    click.echo("📋 Epic Summary:")
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
    
    if click.confirm("\n✅ Create this epic?", default=True):
        click.echo("\n🚀 Creating epic...")
        try:
            result = subprocess.run(cmd, check=True, capture_output=False)
            if result.returncode == 0:
                click.echo("\n🎉 Epic created successfully!")
        except subprocess.CalledProcessError as e:
            click.echo(f"\n❌ Error creating epic: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            click.echo("\n⏹️ Cancelled by user")
            sys.exit(1)
    else:
        click.echo("⏹️ Epic creation cancelled")


if __name__ == '__main__':
    main()
