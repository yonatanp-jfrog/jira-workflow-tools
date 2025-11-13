# 🎯 Jira Workflow Tools - AI-Powered Team Edition

**Modern, secure, and AI-integrated toolkit for seamless Jira workflow management.**

*Designed for AI assistants, perfect for humans.*

---

## 🤖 **AI-First Workflow** (Primary Usage)

This tool is designed to work seamlessly with **Cursor**, **GitHub Copilot**, and other agentic AI systems. Instead of remembering complex commands, simply describe what you want to do in natural language.

### **✨ How It Works with AI**

1. **Describe your intent** in natural language to your AI assistant
2. **AI translates** your request into the appropriate tool commands  
3. **Tool executes** the Jira operations securely and efficiently
4. **Results delivered** in your preferred format

### **🎯 Common AI Interactions**

```
👤 "Create an epic for the RTDEV platform-team for a new user authentication feature"
🤖 Uses: python3 -m jira_tools epic "User Authentication Platform" --template RTDEV-epic-lifecycle --project RTDEV

👤 "Show me the details of ticket RTDEV-12345 in markdown format"  
🤖 Uses: python3 -m jira_tools viewer RTDEV-12345 --format markdown

👤 "What templates are available for APP project core-team work?"
🤖 Uses: python3 -m jira_tools templates list
        (Then filters/explains APP templates for core team)

👤 "Create a high-priority bug for the APP core-team and assign UX designer"
🤖 Uses: python3 -m jira_tools epic "Critical User Flow Bug" --project APP \
      --template APP-bug-core --priority "2 - High" --ux-designer "sarah.jones"

👤 "Create an RTDEV lifecycle epic for dev-artifactory-lifecycle team with technical writer"
🤖 Uses: python3 -m jira_tools epic "Artifactory Lifecycle Enhancement" --project RTDEV \
      --template RTDEV-epic-lifecycle --team "dev-artifactory-lifecycle" \
      --technical-writer "mike.chen" --commitment-level "Hard Commitment"
```

### **💡 How to Get Better AI Results**

**Include these details in your requests for optimal AI assistance:**

- **Project**: `RTDEV` or `APP`
- **Team**: `platform-team`, `core-team`, `dev-artifactory-lifecycle`, `mobile-team`, etc.
- **Type**: `epic` (large initiatives), `bug` (defects), `task` (work items), `story` (features)
- **Priority**: `high`, `critical`, `normal`, `low`
- **Roles**: Mention if you need `technical-writer`, `ux-designer`, or `architect` assignments

**Examples of well-structured requests:**
```
✅ "Create a high-priority bug for APP core-team with UX designer assigned"
✅ "Make an RTDEV lifecycle epic for platform-team with technical writer" 
✅ "Create an APP epic for core-team focused on user authentication features"
✅ "Show RTDEV-12345 details formatted for our team documentation"
✅ "List all templates available for APP project work"
```

### **🚀 Benefits of AI Integration**

- **Natural Language Interface** - No need to memorize command syntax
- **Context Awareness** - AI can suggest appropriate templates and projects  
- **Smart Defaults** - AI applies best practices automatically
- **Error Prevention** - AI validates inputs before execution
- **Rich Formatting** - AI can format outputs for your specific needs
- **Workflow Integration** - Seamlessly fits into your existing development process

---

## ⚡ **Quick Setup (5 minutes)**

### **Prerequisites**
- **Python 3.9+** - `python3 --version`
- **Your team's Jira access** - Organization Jira instance
- **API token** - From your Jira profile settings

### **Setup Steps**

1. **Clone and Install**
```bash
git clone https://github.com/yonatanp-jfrog/jira-workflow-tools.git
cd jira-workflow-tools
pip3 install -r requirements.txt
```

2. **Configure Credentials**
```bash
cp env.template .env
# Edit .env with your credentials:
# JIRA_BASE_URL=https://your-org.atlassian.net
# JIRA_AUTH_TOKEN=your_api_token_here
```

3. **Test Configuration**
```bash
python3 -m jira_tools test-config
# Should show: ✅ Configuration valid, ✅ Connection successful!
```

### **Getting Your API Token**
1. Go to your Jira profile → **Security** → **API tokens**
2. Click **Create API token**
3. Give it a name (e.g., "AI Jira Tools")
4. Copy the token and paste into `.env` file

---

## 🔒 **Security & Team Features**

### **✅ Production Ready**
- **No hardcoded secrets** - Environment variables or encrypted private mode
- **Safe for team sharing** - No organizational data embedded in code
- **Comprehensive security** - Input validation, secure defaults, audit trail
- **Role-based assignments** - Technical writers, UX designers, architects
- **Private mode available** - Encrypted credential storage with OS keyring

### **👥 Team Collaboration**
- **Consistent AI experience** - Same interface for all team members
- **Template system** - Human-readable, shareable, customizable
- **Rich output formats** - Console, markdown, JSON with proper formatting
- **Professional documentation** - GitHub integration with issue templates

---

## 🎨 **Available Templates & Projects**

### **Current Templates**
```bash
# List all available templates
python3 -m jira_tools templates list

# Understand what a template does  
python3 -m jira_tools templates describe APP-epic-core
python3 -m jira_tools templates describe RTDEV-epic-lifecycle
```

### **Built-in Templates**
- **APP-epic-core** - Customer-facing features and core application epics
- **APP-bug-core** - Critical application bugs and customer issues
- **RTDEV-epic-lifecycle** - Platform features and Artifactory lifecycle work  
- **RTDEV-bug-lifecycle** - Platform bugs and infrastructure issues
- **RTDEV-task-lifecycle** - Operational tasks and development work

---

## 📚 **Advanced Documentation**

### **Team Resources**
- **[Team Setup Guide](TEAM_SETUP.md)** - Complete onboarding for new team members
- **[Workflows & Troubleshooting](docs/WORKFLOWS_AND_TROUBLESHOOTING.md)** - Advanced workflows and problem solving
- **[Staged Epic Workflow](docs/STAGED_EPIC_WORKFLOW.md)** - Collaborative epic creation process
- **[Template Field Mappings](templates/FIELD_MAPPINGS.md)** - Field reference for custom templates

### **Support & Contributing**
- **🐛 Bug Reports:** [Create Issue](../../issues/new?template=bug-report.yml)
- **💡 Feature Requests:** [Create Issue](../../issues/new?template=feature-request.yml)  
- **❓ Team Support:** [Create Issue](../../issues/new?template=team-support.yml)

---

## 🛠️ **Manual Usage** (Backup/Advanced Users)

*For direct command-line usage without AI assistance*

### **Core Commands**
```bash
# Configuration and testing
python3 -m jira_tools --help           # Main help system
python3 -m jira_tools test-config      # Test your setup

# Epic creation
python3 -m jira_tools epic --interactive                    # Interactive wizard
python3 -m jira_tools epic "Epic Name" --project RTDEV      # Direct creation
python3 -m jira_tools epic "Complex Epic" --project RTDEV \
  --template RTDEV-epic-lifecycle --commitment-level "Hard Commitment" \
  --area "Features & Innovation" --technical-writer "sarah.jones"

# Issue viewing  
python3 -m jira_tools viewer RTDEV-12345                    # View issue
python3 -m jira_tools viewer "https://company.atlassian.net/browse/RTDEV-12345" --format markdown
python3 -m jira_tools viewer RTDEV-12345 --raw --output report.json

# Template management
python3 -m jira_tools templates list                        # List templates
python3 -m jira_tools templates describe APP-epic-core      # Understand template
```

### **Advanced Configuration**
```bash
# Private mode (encrypted storage)
python3 -m jira_tools private setup    # Set up encrypted storage
python3 -m jira_tools private status   # Check private mode status
python3 -m jira_tools private backup   # Backup configuration

# Template validation
python3 -m jira_tools templates validate path/to/template.j2
```

### **Manual Troubleshooting**
```bash
# Common diagnostic commands
python3 --version                       # Check Python version (need 3.9+)
python3 -m jira_tools test-config      # Verify credentials and connectivity
python3 -m jira_tools templates list   # Check available templates
pip3 install -r requirements.txt       # Reinstall dependencies if needed
```

---

## 🧪 **Testing & Validation**

```bash
# Test the tool without making changes
python3 -m jira_tools epic "Test Epic" --project RTDEV --dry-run

# Run comprehensive test suite
python3 tests/test_runner.py

# Validate templates
python3 -m jira_tools templates validate templates/APP-epic-core.j2
```

---

## 🚨 **Legacy System Migration**

> **IMPORTANT:** Legacy scripts (`epic_creator.py`, `create_epic.py`, `jira_viewer.py`) are **DEPRECATED** and will be removed on **2025-03-01**. 

**Migration is simple:** All legacy functionality is available in the modern system with enhanced features and security.

---

## 🎯 **System Status**

| Component | Status | Security | AI Integration | Team Ready |
|-----------|--------|----------|----------------|------------|
| **Core System** | ✅ Production | ✅ Secure | ✅ Optimized | ✅ Yes |
| **Templates** | ✅ Active | ✅ Validated | ✅ AI-Friendly | ✅ Yes |
| **Documentation** | ✅ Complete | ✅ Reviewed | ✅ AI-Ready | ✅ Yes |

---

**🎉 Ready to streamline your Jira workflow with AI-powered automation!**

*Have questions? Ask your AI assistant to help you use this tool - that's what it's designed for!*