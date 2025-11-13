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
    Create a staged file using modern templates but legacy workflow format.
    """
    # Import modern system
    from jira_tools.core.templates import TemplateManager, TemplateContext
    
    # Initialize template manager
    template_manager = TemplateManager()
    
    # Build context like the modern system
    context = TemplateContext.build_epic_context(
        epic_name=epic_name,
        project_key=kwargs.get('project', 'RTDEV'),
        **kwargs
    )
    
    # Render template to get Jira API payload
    template_filename = f"{template_name}.j2"
    template = template_manager.env.get_template(template_filename)
    rendered_json = template_manager.render_template(template, context)
    jira_payload = json.loads(rendered_json)
    
    # Create staged file directory
    staged_dir = Path("staged-issues")
    staged_dir.mkdir(exist_ok=True)
    
    # Create filename
    safe_name = epic_name.replace(" ", "-").replace("/", "-").replace(":", "")
    filename = f"STAGED-{safe_name}.md"
    filepath = staged_dir / filename
    
    # Extract key info from payload
    fields = jira_payload['fields']
    project_name = "RTDEV" if fields.get('project', {}).get('id') == "10129" else "APP"
    issue_type = "Epic" if fields.get('issuetype', {}).get('id') == "10000" else "Bug"
    
    # Generate staged file content
    content = f"""# [STAGED: {epic_name}] - Ready for Review

**🎯 STAGING STATUS:** Ready for Review  
**🔄 WORKFLOW:** staged-issues/ → (review/edit) → publish → archived-published-issues/

## Basic Information

- **Type:** {issue_type}
- **Status:** STAGED (Not yet published to Jira)
- **Priority:** {kwargs.get('priority', '4 - Normal')}
- **Project:** {project_name}
- **Template:** {template_name}
- **Teams:** {kwargs.get('team', 'dev-artifactory-lifecycle')}
- **Product Backlog:** {kwargs.get('product_backlog', 'Q4-25-Backlog')}
- **Commitment Level:** {kwargs.get('commitment_level', 'Soft Commitment')}
- **Created:** {datetime.now().isoformat()}

## 📝 Description

================================================================================
🔸 DESCRIPTION START 🔸
================================================================================

{kwargs.get('description', '''**Description**

**Problem:** [Describe the problem this epic solves]

**Solution:** [High-level approach to solve the problem]

**Requirements**
- [ ] [Requirement 1]
- [ ] [Requirement 2]

**Scope**
**In Scope:**
- [What will be delivered]

**Out of Scope:**
- [What will not be delivered in this epic]

**Definition of Done (DoD)**
- [ ] All requirements implemented and tested
- [ ] Code reviewed and approved
- [ ] Documentation updated''')}

================================================================================
🔸 DESCRIPTION END 🔸
================================================================================

## 🎮 Jira API Payload (Generated from Template)

```json
{json.dumps(jira_payload, indent=2)}
```

## 📋 Next Steps

1. **Edit this file** in your IDE/text editor
2. **Review with team** (share via version control if needed)  
3. **Publish when ready** using: `python3 staged_epic_creator.py submit {filepath}`
4. **File will move** from `staged-issues/` to `.jira-staging/archived-published-issues/`

## 🎯 Commands for This Workflow

```bash
# Edit this file
code {filepath}

# View all staged files
ls -la staged-issues/

# Publish when ready (moves to archived)
python3 staged_epic_creator.py submit {filepath}

# View published files  
ls -la .jira-staging/archived-published-issues/
```"""

    # Write the staged file
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath

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
