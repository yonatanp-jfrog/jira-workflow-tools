#!/usr/bin/env python3
"""
Create staged files for the file-based workflow.
This bridges the modern template system with the legacy staging workflow.
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add jira_tools to path
sys.path.insert(0, str(Path(__file__).parent))

def create_staged_file(epic_name, template_name="RTDEV-epic-lifecycle", **kwargs):
    """
    Create a staged file compatible with staged_epic_creator.py workflow.
    """
    # Import the staging creator to use its format
    from staged_epic_creator import StagedEpicCreator
    
    # Create staged file directory
    staged_dir = Path("staged-issues")
    staged_dir.mkdir(exist_ok=True)
    
    # Use StagedEpicCreator to generate the file in the correct format
    creator = StagedEpicCreator()
    
    # Map template to project (extract project from template name)
    project = kwargs.get('project', 'RTDEV')
    if 'APP' in template_name.upper():
        project = 'APP'
    elif 'RTDEV' in template_name.upper():
        project = 'RTDEV'
    
    # Map template to team
    team = kwargs.get('team')
    if not team:
        if 'APP' in project:
            team = 'app-core'
        else:
            team = 'dev-artifactory-lifecycle'
    
    # Create the staged epic using the legacy system
    filepath = creator.create_staged_epic(
        project=project,
        epic_name=epic_name,
        description=kwargs.get('description', 'TBD'),
        team=team,
        product_backlog=kwargs.get('product_backlog', 'Q4-25-Backlog'),
        product_manager=kwargs.get('product_manager', 'Yonatan Philip'),
        priority=kwargs.get('priority', '4 - Normal'),
        commitment_level=kwargs.get('commitment_level', 'Soft Commitment'),
        parent=kwargs.get('parent'),
        product_priority=kwargs.get('product_priority'),
        assigned_architect=kwargs.get('assigned_architect'),
        assigned_ux=kwargs.get('assigned_ux', 'Omer Morag'),
        assigned_technical_writer=kwargs.get('assigned_technical_writer', 'Michael Berman'),
        required_doc=kwargs.get('required_doc', 'Yes'),
        release_notes=kwargs.get('release_notes', 'Yes')
    )
    
    return Path(filepath)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 create_staged_file.py 'Epic Name' [template] [--priority=X] [--team=Y]")
        print("\nExamples:")
        print("python3 create_staged_file.py 'My New Epic'")  
        print("python3 create_staged_file.py 'Bug Fix Epic' RTDEV-bug-lifecycle --priority='5 - Low'")
        print("python3 create_staged_file.py 'App Epic' APP-epic-core --team=app-core")
        sys.exit(1)
    
    epic_name = sys.argv[1]
    template = sys.argv[2] if len(sys.argv) > 2 else "RTDEV-epic-lifecycle"
    
    # Parse additional arguments
    kwargs = {}
    for arg in sys.argv[3:]:
        if arg.startswith('--'):
            key, value = arg[2:].split('=', 1)
            kwargs[key.replace('-', '_')] = value
    
    try:
        filepath = create_staged_file(epic_name, template, **kwargs)
        print(f"✅ Staged file created: {filepath}")
        print(f"📝 Edit with: code {filepath}")
        print(f"🚀 Publish with: python3 staged_epic_creator.py submit {filepath}")
    except Exception as e:
        print(f"❌ Error: {e}")
