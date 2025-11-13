# 🔄 **Workflows & Troubleshooting Guide**

**Advanced workflows, staging process, and comprehensive troubleshooting for jira-workflow-tools.**

*Updated for the newly renamed project structure.*

---

## 📋 **Common Workflows**

### 🎯 **Daily Issue Analysis**
```bash
# Quick issue research
python3 -m jira_tools viewer RTDEV-12345
python3 -m jira_tools viewer RTDEV-12345 --url  # Include web link

# Save for documentation
python3 -m jira_tools viewer RTDEV-12345 --format markdown --output reports/
python3 -m jira_tools viewer RTDEV-12345 --raw --output data.json

# Parse URLs from any format
python3 -m jira_tools viewer "Check issue RTDEV-12345 for details"
python3 -m jira_tools viewer "https://company.atlassian.net/browse/RTDEV-12345"
```

### 🚀 **Epic Creation Patterns**

#### **Interactive Epic Creation (Recommended)**
```bash
# Guided step-by-step process
python3 -m jira_tools epic --interactive

# The wizard will prompt for:
# - Epic name and project
# - Description and priority  
# - Advanced fields (commitment level, area, etc.)
# - Team and product settings
```

#### **Template-Based Creation**
```bash
# Use built-in templates
python3 -m jira_tools epic "Feature Epic" --template RTDEV-epic-lifecycle --project RTDEV
python3 -m jira_tools epic "Bug Fix Epic" --template APP-bug-core --project APP

# Advanced epic with all fields including role assignments
python3 -m jira_tools epic "Complex Epic" --project RTDEV \
  --template RTDEV-epic-lifecycle \
  --commitment-level "Hard Commitment" \
  --area "Features & Innovation" \
  --product-priority P1 \
  --parent RTDEV-12345 \
  --technical-writer "michael.berman" \
  --ux-designer "sarah.jones"
```

#### **Always Test First**
```bash
# Dry run to preview
python3 -m jira_tools epic "Test Epic" --template RTDEV-epic-lifecycle --project RTDEV --dry-run

# Understand what a template does
python3 -m jira_tools templates describe RTDEV-epic-lifecycle
```

---

## 📝 **Two-Phase Staging Workflow**

**For collaborative epic planning and review before Jira submission.**

### **Phase 1: Create Staged Epic**
```bash
# Interactive staging creation
python3 create_staged_epic.py

# Or command-line staging
python3 staged_epic_creator.py stage --project RTDEV --epic-name "My Epic"
```

**This creates:** `staged-issues/RTDEV_YYYYMMDD_My_Epic.md`

### **Phase 2: Review and Submit**
```bash
# Edit the staged file with your preferred editor
code staged-issues/RTDEV_20241112_My_Epic.md

# Review staged content
python3 staged_epic_creator.py review staged-issues/RTDEV_20241112_My_Epic.md

# Submit when ready
python3 staged_epic_creator.py submit staged-issues/RTDEV_20241112_My_Epic.md
```

### **Staging Workflow Benefits**
- ✅ **Collaborate** on epic content before submission
- ✅ **Version control** track changes and iterations  
- ✅ **Review process** ensure quality before Jira creation
- ✅ **Template consistency** structured epic planning

---

## 🔄 **Epic Refresh Workflow**

**Keep local epic files synchronized with current Jira data.**

### **Refresh Single Epic** 
```bash
# Refresh specific epic file
python3 epic_refresher.py --file "Published Issues/RTDEV-12345 Epic Name.md"

# Refresh by issue key
python3 epic_refresher.py --issue RTDEV-12345
```

### **Batch Refresh**
```bash
# Refresh all epic files
python3 epic_refresher.py --refresh-all

# Refresh specific project
python3 epic_refresher.py --project RTDEV
```

### **Refresh Features**
- ✅ **Update content** with latest Jira data
- ✅ **Rename files** if epic name changed
- ✅ **Remove files** if epic was deleted
- ✅ **Batch processing** for multiple epics

---

## 🎨 **Template Management**

### **Working with Templates**
```bash
# List all available templates
python3 -m jira_tools templates list

# Validate template syntax
python3 -m jira_tools templates validate templates/my-template.j2

# Create new template
python3 -m jira_tools templates create epic my-custom-template
```

### **Template Locations**
- **All templates:** `templates/` directory (human-readable format)
- **Field mappings:** `templates/FIELD_MAPPINGS.md` (reference guide)
- **Current templates:**
  - `APP-epic-core.j2` - APP project epics
  - `APP-bug-core.j2` - APP project bugs
  - `RTDEV-epic-lifecycle.j2` - RTDEV project epics  
  - `RTDEV-bug-lifecycle.j2` - RTDEV project bugs
  - `RTDEV-task-lifecycle.j2` - RTDEV project tasks

### **Template Development**
```bash
# Test template rendering
python3 -m jira_tools epic "Test" --template APP-epic-core --dry-run

# Understand template behavior
python3 -m jira_tools templates describe APP-epic-core

# Templates use human-readable format:
# "project": "RTDEV" (not {"id": "10129"})
# "team": "dev-artifactory-lifecycle" (not {"id": "10145"})
# See templates/FIELD_MAPPINGS.md for all mappings
```

---

## 🔒 **Private Mode Management**

### **Setup and Configuration**
```bash
# Initial setup
python3 -m jira_tools private setup

# Check status
python3 -m jira_tools private status

# Create backup
python3 -m jira_tools private backup
```

### **Private Mode Benefits**
- 🔐 **Encrypted storage** using OS keyring + Fernet
- 🏠 **Local-only** no external dependencies
- 🔄 **Backup/restore** for configuration management
- 🔍 **Security audit** validate encryption

---

## 🚨 **Troubleshooting Guide**

### **Quick Diagnosis**
```bash
# Test basic functionality
python3 --version                      # Should be 3.9+
python3 -m jira_tools --help          # Should show help
python3 -m jira_tools test-config     # Should show valid config

# Test Jira connectivity
curl -I https://your-org.atlassian.net
```

### **Authentication Issues**

#### **Problem: "Authentication failed"**
```bash
# Check credentials
cat .env  # Verify JIRA_BASE_URL and JIRA_AUTH_TOKEN

# Test API token
curl -X GET -H "Authorization: Basic $(echo -n email:token | base64)" \
  https://your-org.atlassian.net/rest/api/2/myself

# Regenerate token if needed (Jira profile → Security → API tokens)
```

#### **Problem: "Access denied"**
```bash
# Check permissions for specific issue
python3 -m jira_tools viewer RTDEV-12345

# Verify account has access to project
# Contact Jira admin if needed
```

### **Configuration Issues**

#### **Problem: "Configuration missing"**
```bash
# Check if .env exists
ls -la .env

# Copy template if missing
cp env.template .env

# Edit with your credentials
```

#### **Problem: "Private mode error"**
```bash
# Reset private mode
python3 -m jira_tools private reset

# Setup again
python3 -m jira_tools private setup
```

### **Template Issues**

#### **Problem: "Template not found"**
```bash
# List available templates
python3 -m jira_tools templates list

# Check template paths
ls -la templates/
ls -la jira_tools/core/builtin_templates/
```

#### **Problem: "Template syntax error"**
```bash
# Validate template
python3 -m jira_tools templates validate path/to/template.j2

# Common issues:
# - Missing {{ }} around variables
# - Incorrect Jinja2 syntax
# - Invalid JSON structure
```

### **Epic Creation Issues**

#### **Problem: "Field validation error"**
```bash
# Use dry-run to test
python3 -m jira_tools epic "Test" --project RTDEV --dry-run

# Check field mappings and current templates
python3 -m jira_tools templates list

# See human-readable field mappings  
cat templates/FIELD_MAPPINGS.md
```

#### **Problem: "Project not found"**
```bash
# Supported projects: RTDEV, APP
python3 -m jira_tools epic "Test" --project RTDEV  # Not rtdev or Rtdev
```

### **Staging Workflow Issues**

#### **Problem: "Staged file not found"**
```bash
# Check staged files
ls -la staged-issues/

# Use full path or filename only
python3 staged_epic_creator.py submit staged-issues/RTDEV_20241112_Epic.md
```

#### **Problem: "YAML parsing error"**
```bash
# Validate YAML frontmatter
python3 -c "import yaml; yaml.safe_load(open('staged-issues/file.md').read())"

# Common issues:
# - Missing --- delimiters
# - Incorrect YAML indentation
# - Special characters in values
```

### **Performance Issues**

#### **Problem: "Slow responses"**
```bash
# Test network connectivity
curl -w "@curl-format.txt" -s -o /dev/null https://your-org.atlassian.net

# Check if VPN is required
# Try different network connection
```

#### **Problem: "Timeout errors"**
```bash
# Increase timeout (not configurable currently)
# Try during off-peak hours
# Contact network admin if persistent
```

---

## 📚 **Command Reference**

### **Main Commands**
```bash
python3 -m jira_tools --help           # Main help
python3 -m jira_tools test-config      # Validate setup
```

### **Epic Management**
```bash
python3 -m jira_tools epic --help                    # Epic help
python3 -m jira_tools epic --interactive             # Interactive creation
python3 -m jira_tools epic "Name" --project RTDEV    # Direct creation
python3 -m jira_tools epic "Name" --dry-run          # Test only
```

### **Issue Viewing**
```bash
python3 -m jira_tools viewer --help                  # Viewer help
python3 -m jira_tools viewer ISSUE-123               # View issue
python3 -m jira_tools viewer ISSUE-123 --raw         # Raw JSON
python3 -m jira_tools viewer ISSUE-123 --format md   # Markdown format
```

### **Template Management**
```bash
python3 -m jira_tools templates --help       # Template help
python3 -m jira_tools templates list         # List templates
python3 -m jira_tools templates validate     # Validate template
```

### **Private Mode**
```bash
python3 -m jira_tools private --help         # Private mode help
python3 -m jira_tools private setup          # Setup encryption
python3 -m jira_tools private status         # Check status
python3 -m jira_tools private backup         # Create backup
```

### **Staging Workflow**
```bash
# Modern approach (recommended):
python3 -m jira_tools epic "My Epic" --dry-run  # Preview before creation
python3 -m jira_tools epic --interactive        # Interactive creation

# Legacy staging (may need compatibility updates):
python3 create_staged_epic.py               # Interactive staging (works)
python3 staged_epic_creator.py --help       # Staging help (may have issues)
python3 staged_epic_creator.py stage        # Create staged epic (may have issues)
python3 staged_epic_creator.py submit       # Submit to Jira (may have issues)
```

### **Epic Refresh**
```bash
python3 epic_refresher.py --help            # Refresh help
python3 epic_refresher.py --refresh-all     # Refresh all epics
python3 epic_refresher.py --issue KEY       # Refresh specific epic
```

---

## 💡 **Frequently Asked Questions**

### **Q: Which system should I use - modern or legacy?**
**A:** Use the modern system (`python3 -m jira_tools`). Legacy scripts are deprecated and will be removed in 2025.

### **Q: Can I create epics without templates?**
**A:** Yes, use direct creation: `python3 -m jira_tools epic "Name" --project RTDEV`

### **Q: How do I add custom fields?**
**A:** Use the advanced template or add fields via CLI options. See `python3 -m jira_tools epic --help`

### **Q: Can I work offline?**
**A:** Partially. You can create staged epics and templates offline, but submitting to Jira requires connectivity.

### **Q: How do I backup my configuration?**
**A:** For private mode: `python3 -m jira_tools private backup`. For .env files: copy them manually.

### **Q: What if I need features not in the modern system?**
**A:** Create a GitHub issue with your request. We prioritize missing functionality from legacy scripts.

---

## 🆘 **Getting Help**

### **Self-Help Resources**
1. **Command help:** `python3 -m jira_tools COMMAND --help`
2. **Configuration test:** `python3 -m jira_tools test-config`
3. **Template validation:** `python3 -m jira_tools templates validate`

### **Common Solutions**
- **Authentication:** Regenerate API token, check .env file
- **Templates:** Validate syntax, check available templates
- **Staging:** Verify YAML frontmatter, check file paths
- **Performance:** Check network, try off-peak hours

### **Still Need Help?**
Create a GitHub issue with:
- Command that failed
- Full error message  
- Your environment (Python version, OS)
- What you were trying to accomplish

---

**Happy workflow management!** 🎯

*For initial setup, see the main `README.md`*  
*For staging workflows, see `STAGED_EPIC_WORKFLOW.md`*
