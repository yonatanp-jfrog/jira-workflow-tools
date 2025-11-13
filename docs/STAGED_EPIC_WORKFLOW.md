# 🎯 Staged Epic Workflow - Two-Phase Epic Creation

**⚠️ NOTE:** This is a **legacy workflow**. For most users, the modern **Cursor AI approach** is recommended:

```
💬 Ask Cursor: "Create an RTDEV epic for platform-team about authentication, but show me what it will create first"
🤖 Cursor will: Run python3 -m jira_tools epic "Authentication" --template RTDEV-epic-lifecycle --dry-run
```

**This staging workflow is useful for:**
- Complex epics requiring extensive collaboration and review
- Teams preferring file-based workflows with version control
- Advanced users who need the two-phase approach

A smart, collaborative workflow for creating Jira epics with review and approval process in jira-workflow-tools.

## 🌟 Why Staged Epics?

The staged epic workflow solves common problems with epic creation:

- ✅ **Review Before Creation** - Collaborate and refine before submitting to Jira
- ✅ **Version Control** - Track changes and iterations in markdown files
- ✅ **Team Collaboration** - Share, comment, and improve epics together
- ✅ **Template-Driven** - Consistent structure with guided sections
- ✅ **Flexible Editing** - Use any text editor or IDE for rich editing experience

## 🔄 Two-Phase Workflow

### Phase 1: 📝 **Staging** 
Create a structured markdown file with epic configuration and detailed planning sections.

### Phase 2: 🚀 **Submission**
Parse the markdown file and create the actual Jira epic with all configurations.

## 🛠️ Setup

1. Ensure dependencies are installed:
   ```bash
   pip3 install pyyaml click requests python-dotenv rich
   ```

2. Make sure your `.env` file contains:
   ```
   JIRA_BASE_URL=https://jfrog-int.atlassian.net
   JIRA_AUTH_TOKEN=your_base64_encoded_token
   ```

## 🎮 Usage

### 🎯 Quick Start (Interactive Mode)

```bash
python3 create_staged_epic.py
```

This guides you through creating a staged epic step-by-step.

### 🔧 Advanced Usage (Command Line)

#### Phase 1: Create Staged Epic

```bash
# Basic staged epic
python3 staged_epic_creator.py stage RTDEV "My New Epic"

# With full configuration
python3 staged_epic_creator.py stage RTDEV "Advanced Epic" \
  --description "Detailed epic description" \
  --team "dev-artifactory-core" \
  --priority "3 - High" \
  --commitment-level "Hard Commitment" \
  --product-priority "P1" \
  --parent "PNEP-123"
```

#### Phase 2: Submit to Jira

```bash
# Dry run (preview what will be created)
python3 staged_epic_creator.py submit RTDEV_20250930_My_Epic.md --dry-run

# Actual submission
python3 staged_epic_creator.py submit RTDEV_20250930_My_Epic.md
```

#### Management Commands

```bash
# List all staged epics
python3 staged_epic_creator.py list

# Get help
python3 staged_epic_creator.py --help
```

## 📁 File Structure

### Staged Epic File Format

Each staged epic is a markdown file with:

```markdown
---
# STAGED EPIC METADATA
---

```yaml
# Epic Configuration
epic_config:
  project: RTDEV
  epic_name: "My Epic"
  team: "dev-artifactory-lifecycle"
  priority: "4 - Normal"
  # ... other config

# Staging Information  
staging_info:
  created_date: "2025-09-30T15:33:10"
  status: "staged"
```

# 🎯 STAGED EPIC: My Epic

## 📋 Epic Configuration
- Configuration summary

## 📝 Epic Description
<!-- Editable description -->

## 🔄 Workflow Instructions
- How to edit and submit

## 📋 Detailed Epic Planning
### 🎯 Goals & Objectives
### 📊 Success Criteria  
### ✅ Acceptance Criteria
### 🔗 Dependencies
### 🚫 Out of Scope
### 📝 Notes & Comments
```

### Directory Structure

```
staged-issues/
├── RTDEV: My Epic.md
├── APP: UI Improvements.md
└── RTDEV: Security Epic.md
```

## 🎯 Workflow Examples

### Example 1: Basic Workflow

```bash
# 1. Create staged epic
python3 create_staged_epic.py
# Follow prompts...

# 2. Edit the generated markdown file
open "staged-issues/RTDEV: My Epic.md"

# 3. Submit when ready
python3 staged_epic_creator.py submit "RTDEV: My Epic.md"
```

### Example 2: Team Collaboration

```bash
# 1. Product Manager creates staged epic
python3 staged_epic_creator.py stage RTDEV "User Authentication Epic" \
  --description "Implement OAuth 2.0 authentication"

# 2. Share file with team for review
# staged-issues/RTDEV: User Authentication Epic.md

# 3. Team members edit and add details:
#    - Technical requirements
#    - Acceptance criteria
#    - Dependencies
#    - Success metrics

# 4. After approval, submit to Jira
python3 staged_epic_creator.py submit "RTDEV: User Authentication Epic.md"
```

### Example 3: Epic Refinement Process

```bash
# 1. Create initial staged epic
python3 staged_epic_creator.py stage APP "Performance Improvements"

# 2. List staged epics to track progress
python3 staged_epic_creator.py list

# 3. Edit and refine over multiple sessions
# (Edit the markdown file with detailed requirements)

# 4. Dry run to preview before submission
python3 staged_epic_creator.py submit "APP: Performance Improvements.md" --dry-run

# 5. Submit when satisfied
python3 staged_epic_creator.py submit "APP: Performance Improvements.md"
```

## 📊 Epic Status Tracking

Staged epics have status tracking:

- 📝 **staged** - Initial creation
- 👀 **reviewed** - Team has reviewed  
- ✅ **approved** - Ready for submission
- 🚀 **submitted** - Created in Jira

Update status by editing the YAML config:

```yaml
staging_info:
  status: "reviewed"  # Change this value
```

## 🎨 Customization & Editing

### Epic Configuration

Edit the YAML block to modify:
- Project settings
- Team assignment  
- Priority and commitment levels
- Parent epic relationships
- Product priorities

### Epic Description

The description section becomes the Jira epic description:

```markdown
## 📝 Epic Description

<!-- Edit below - this becomes the Jira description -->

Your detailed epic description here...
```

### Planning Sections

Use the template sections for comprehensive planning:

- **Goals & Objectives** - High-level business goals
- **Success Criteria** - Measurable outcomes
- **Acceptance Criteria** - Specific, testable requirements
- **Dependencies** - External dependencies
- **Out of Scope** - What's explicitly not included
- **Notes & Comments** - Additional context

## 🔧 Advanced Features

### Custom Templates

You can modify the template in `staged_epic_creator.py` to add:
- Custom sections
- Project-specific fields
- Company-specific requirements

### Integration with Version Control

Since staged epics are markdown files:

```bash
# Track changes with git
git add staged-issues/
git commit -m "Add new authentication epic"

# Collaborate via pull requests
# Review changes via diff tools
# Maintain epic history
```

### Batch Operations

```bash
# Create multiple epics from a script
for epic in "Epic 1" "Epic 2" "Epic 3"; do
  python3 staged_epic_creator.py stage RTDEV "$epic"
done

# Submit multiple approved epics
for file in staged-issues/RTDEV_*_approved_*.md; do
  python3 staged_epic_creator.py submit "$file"
done
```

## 🚨 Troubleshooting

### Common Issues

1. **YAML Parsing Error**
   ```
   Error: Invalid YAML config
   ```
   - Check YAML syntax in the config block
   - Ensure proper indentation
   - Validate quotes around strings

2. **File Not Found**
   ```
   Error: Staged epic file not found
   ```
   - Check file path (use relative path from project root)
   - Ensure file is in `staged-issues/` folder

3. **Jira Submission Failed**
   ```
   Error: Failed to create epic
   ```
   - Verify authentication token
   - Check required fields are present
   - Ensure project permissions

### Validation

```bash
# Validate staged epic before submission
python3 staged_epic_creator.py submit my_epic.md --dry-run
```

## 📈 Best Practices

### 1. **Descriptive Naming**
Use clear, descriptive epic names that indicate the business value.

### 2. **Comprehensive Planning**
Fill out all template sections for better epic quality:
- Clear acceptance criteria
- Defined success metrics
- Identified dependencies

### 3. **Team Review Process**
- Share staged epics for team input
- Use version control for change tracking
- Get approval before submission

### 4. **Status Management**
Update epic status as it progresses through review stages.

### 5. **Regular Cleanup**
Periodically clean up old staged epics:
```bash
# Archive submitted epics
mkdir archived-epics
mv staged-issues/*submitted* archived-epics/
```

## 🔗 Integration

### With Existing Tools

The staged workflow integrates with:
- **Jira Viewer** - View created epics
- **Version Control** - Track epic evolution
- **Text Editors** - Rich editing experience
- **Collaboration Tools** - Share and review

### Workflow Integration

```bash
# Complete workflow example

# Modern approach (recommended):
python3 -m jira_tools epic "My Epic" --template RTDEV-epic-lifecycle --dry-run  # Preview
# ... review output ...
python3 -m jira_tools epic "My Epic" --template RTDEV-epic-lifecycle            # Create
python3 -m jira_tools viewer RTDEV-12345                                        # View result

# Legacy staging approach (may need updates):
python3 create_staged_epic.py          # Create staged file
# ... edit and review ...
python3 staged_epic_creator.py submit  # Submit (may have compatibility issues)
```

## 🎯 Tips & Tricks

1. **Use Templates** - Leverage the structured template for consistency
2. **Collaborate Early** - Share staged epics for early feedback
3. **Version Control** - Track changes and iterations
4. **Dry Run First** - Always preview before submission
5. **Status Updates** - Keep status current for team visibility

---

## 🎉 Benefits

✅ **Better Epic Quality** - Structured planning and review process  
✅ **Team Collaboration** - Easy sharing and feedback  
✅ **Change Tracking** - Version control for epic evolution  
✅ **Flexible Editing** - Use any editor or IDE  
✅ **Reduced Errors** - Validation before Jira submission  
✅ **Consistent Structure** - Template-driven approach  

**Happy Epic Planning! 🚀**
